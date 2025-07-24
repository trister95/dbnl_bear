import os
import asyncio
from . import ai_read

async def _process_file(path: str, phenomenon: str, output_dir: str):
    result, _ = await ai_read.analyze_document(path, phenomenon)
    relevant = [r.original_sentence for r in result if r.judgement]
    if relevant:
        out_path = os.path.join(output_dir, os.path.basename(path) + "_relevant.txt")
        with open(out_path, "w", encoding="utf-8") as f:
            for passage in relevant:
                f.write(f"{passage}\n")
    else:
        print(f"No relevant passages found in file {os.path.basename(path)}")

async def _run(paths, phenomenon: str, output_dir: str, max_tasks: int):
    os.makedirs(output_dir, exist_ok=True)
    semaphore = asyncio.Semaphore(max_tasks)

    async def sem_task(p):
        async with semaphore:
            await _process_file(p, phenomenon, output_dir)

    await asyncio.gather(*(sem_task(p) for p in paths))


def run_processing(phenomenon_of_interest: str, input_dir: str, output_dir: str,
                   batch_size: int = 1, max_document_tasks: int = 1,
                   max_fragment_tasks: int = 10):
    """Analyze all text files in ``input_dir`` and save relevant passages."""
    paths = [os.path.join(input_dir, f) for f in os.listdir(input_dir) if f.endswith('.txt')]
    if not paths:
        raise ValueError(f"No .txt files found in {input_dir}")
    asyncio.run(_run(paths, phenomenon_of_interest, output_dir, max_document_tasks))

