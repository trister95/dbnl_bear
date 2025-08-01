import argparse
from dbnl_bear.processing import run_processing

def main():
    parser = argparse.ArgumentParser(description="Process documents for relevant passages.")
    parser.add_argument("phenomenon_of_interest", type=str, help="The phenomenon to analyze.")
    parser.add_argument("--input_dir", type=str, required=True, help="Directory of input files.")
    parser.add_argument("--output_dir", type=str, required=True, help="Directory for output files.")
    parser.add_argument("--max_document_tasks", type=int, default=1, help="Max concurrent document tasks.")
    args = parser.parse_args()

    run_processing(
        phenomenon_of_interest=args.phenomenon_of_interest,
        input_dir=args.input_dir,
        output_dir=args.output_dir,
        max_document_tasks=args.max_document_tasks
    )

if __name__ == "__main__":
    main()

