import os
import asyncio
from langchain_openai import ChatOpenAI
from tqdm.asyncio import tqdm
from typing import Optional
from pydantic import BaseModel, Field, create_model
from langchain_core.prompts import ChatPromptTemplate
from langchain_text_splitters import RecursiveCharacterTextSplitter

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=400,
    chunk_overlap=20,
    length_function=len,
    is_separator_regex=False,
)

def create_model_name(phenomenon_of_interest: str) -> str:
    return ''.join(word.capitalize() for word in phenomenon_of_interest.split())

def create_llm_analysis_model(phenomenon_of_interest: str) -> BaseModel:
    """
    This model goes to the LLM. The difference here is that the original_sentence field is not present
    as it would be a waste of resources to let the LLM do that.
    """
    model_name = create_model_name(phenomenon_of_interest)
    return create_model(
        f"{model_name}InText",
        explanation=(str, Field(description=f"Explain whether the sentence contains information about {phenomenon_of_interest}")),
        judgement=(bool, Field(description=f"Whether the sentence contains information about {phenomenon_of_interest}"))
    )


def create_full_analysis_model(phenomenon_of_interest: str) -> BaseModel:
    """
    This model is the same as the llm_analysis_model but with the original sentence field added.
    """
    model_name = create_model_name(phenomenon_of_interest)
    return create_model(
        f"{model_name}InText",
        explanation=(str, Field(description=f"Explain whether the sentence contains information about {phenomenon_of_interest}")),
        judgement=(bool, Field(description=f"Whether the sentence contains information about {phenomenon_of_interest}")),
        original_sentence=(str, Field(description="The original sentence from the document"))
    )

def get_system_prompt(phenomenon_of_interest: str) -> str:
    return f"""I am a Cultural Historian and Literary Scholar interested in  {phenomenon_of_interest}. Your task is to read sentences in Early Modern Dutch and indicate whether, 
    given my research interest, the sentence is relevant to my research. You should provide a clear explanation, a boolean judgement, and details about
    {phenomenon_of_interest} if present."""

async def analyze_sentence(sentence: str, structured_llm, FullAnalysisModel):
    try:
        llm_result = await structured_llm.ainvoke(sentence)
        
        full_result = FullAnalysisModel(
            explanation = llm_result.explanation,
            judgement = llm_result.judgement,
            original_sentence = sentence
        )
        return full_result
    except Exception as e:
        print(f"Error analyzing sentence: {e}")
        print(f"Problematic sentence: {sentence}")
        return None

async def analyze_document(input_file: str, phenomenon_of_interest: str, text_splitter=text_splitter,
                         model="gpt-4-turbo-mini-2024-07-18"):
    
    with open(input_file, 'r', encoding='utf-8') as f:
        original_text = f.read()

    sentences = text_splitter.split_text(original_text)
    
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("API key not found. Install python-dotenv, make .env file and save the API key there as: OPENAI_API_KEY=your-api-key-here")
    
    # Initialize cost tracker
    cost_tracker = TokenCostTracker(model)
    
    llm = ChatOpenAI(
        model=model,
        callbacks=[{
            "on_llm_start": lambda x: cost_tracker.update_usage(
                cost_tracker.count_tokens(str(x.prompts)),
                0
            ),
            "on_llm_end": lambda x: cost_tracker.update_usage(
                0,
                cost_tracker.count_tokens(str(x.response))
            )
        }]
    )
    
    LLMAnalysisModel = create_llm_analysis_model(phenomenon_of_interest)
    FullAnalysisModel = create_full_analysis_model(phenomenon_of_interest)

    llm_structured_output = llm.with_structured_output(LLMAnalysisModel)

    system_prompt = get_system_prompt(phenomenon_of_interest)
    prompt = ChatPromptTemplate.from_messages([("system", system_prompt), ("human", "{input}")])
    structured_llm = prompt | llm_structured_output
    
    tasks = [analyze_sentence(sentence, structured_llm, FullAnalysisModel) for sentence in sentences]
    
    results = await tqdm.gather(*tasks)
    
    # Get final usage report
    usage_report = cost_tracker.get_usage_report()
    print("\nToken Usage and Cost Report:")
    print(f"Model: {usage_report['model']}")
    print(f"Prompt Tokens: {usage_report['prompt_tokens']}")
    print(f"Completion Tokens: {usage_report['completion_tokens']}")
    print(f"Total Tokens: {usage_report['total_tokens']}")
    print(f"Estimated Cost: ${usage_report['estimated_cost_usd']:.4f}")
    
    return results, usage_report