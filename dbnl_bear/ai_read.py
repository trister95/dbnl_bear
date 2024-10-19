import os
import asyncio
from dotenv import load_dotenv
from langchain_core import prompts
from langchain_openai import ChatOpenAI
from tqdm.asyncio import tqdm
from typing import Optional, Dict, Any, List
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

def create_analysis_model(phenomenon_of_interest: str) -> BaseModel:
    model_name = create_model_name(phenomenon_of_interest)
    return create_model(
        f"{model_name}InText",
        explanation=(str, Field(description=f"Explain whether the sentence contains information about {phenomenon_of_interest}")),
        judgement=(bool, Field(description=f"Whether the sentence contains information about {phenomenon_of_interest}")),
        details=(Optional[str], Field(description=f"Details about the {phenomenon_of_interest} mentioned in the sentence"))
    )

def get_system_prompt(phenomenon_of_interest: str) -> str:
    return f"""I am a Cultural Historian and Literary Scholar interested in  {phenomenon_of_interest}. Your task is to read sentences in Early Modern Dutch and indicate whether, 
    given my research interest, the sentence is relevant to my research. You should provide a clear explanation, a boolean judgement, and details about
    {phenomenon_of_interest} if present."""

async def analyze_sentence(sentence: str, structured_llm):
    try:
        result = await structured_llm.ainvoke(sentence)
        return result
    except Exception as e:
        print(f"Error analyzing sentence: {e}")
        print(f"Problematic sentence: {sentence}")
        return None


async def analyze_document(input_file: str, phenomenon_of_interest: str, text_splitter = text_splitter,
                           model = "gpt-4o-mini-2024-07-18"):

    with open(input_file, 'r', encoding='utf-8') as f:
        original_text = f.read()

    sentences = text_splitter.split_text(original_text)

    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("API key not found. Install python-dotenv, make .env style and save the API key there as: OPENAI_API_KEY=your-api-key-here")                           
    llm = ChatOpenAI(model=model)
    AnalysisModel = create_analysis_model(phenomenon_of_interest)
    llm_structured_output = llm.with_structured_output(AnalysisModel)

    system_prompt = get_system_prompt(phenomenon_of_interest)
    prompt = ChatPromptTemplate.from_messages([("system", system_prompt), ("human", "{input}")])
    structured_llm = prompt | llm_structured_output

    tasks = [analyze_sentence(sentence, structured_llm) for sentence in sentences]    
    results = await tqdm.gather(*tasks, total=len(tasks))

    final_results = []
    for sentence, result in zip(sentences, results):
        if result:
            result.original_sentence = sentence
            final_results.append(result)

    return final_results
