import argparse
import sys
import subprocess
from src.utils.logger import logger

def main():
    parser = argparse.ArgumentParser(description="Order Fulfillment & Margin Mart Orchestrator")
    parser.add_argument("--generate-data", action="store_true", help="Generate synthetic raw e-commerce supply chain dataset")
    parser.add_argument("--build-mart", action="store_true", help="Execute DuckDB Kimball ELT transformations")
    parser.add_argument("--run-tests", action="store_true", help="Run automated data validation test suite")
    parser.add_argument("--dashboard", action="store_true", help="Launch Streamlit interactive analytics UI")
    parser.add_argument("--full-pipeline", action="store_true", help="Execute end-to-end data pipeline & test verification")

    args = parser.parse_args()

    if not any(vars(args).values()):
        parser.print_help()
        sys.exit(1)

    if args.generate_data or args.full_pipeline:
        logger.info("=== STEP 1: Generating Raw Supply Chain Dataset ===")
        from src.pipeline.generate_raw_data import main as gen_main
        gen_main()

    if args.build_mart or args.full_pipeline:
        logger.info("=== STEP 2: Executing Kimball Mart Transformations ===")
        from src.pipeline.transform_mart import run_transformations
        run_transformations()

    if args.run_tests or args.full_pipeline:
        logger.info("=== STEP 3: Running Data Quality & Mart Integrity Tests ===")
        res = subprocess.run([sys.executable, "-m", "pytest", "tests/", "-v"])
        if res.returncode != 0:
            logger.error("Data pipeline tests failed!")
            sys.exit(res.returncode)
        logger.info("All data quality tests passed successfully!")

    if args.dashboard:
        logger.info("=== Launching Streamlit Interactive Dashboard ===")
        subprocess.run([sys.executable, "-m", "streamlit", "run", "app.py"])

if __name__ == "__main__":
    main()
