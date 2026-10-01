import subprocess
import sys


def run_step(command):
    print(f"\nRunning: {' '.join(command)}")
    subprocess.run(command, check=True)


def main():
    python = sys.executable

    run_step([
        python,
        "python/ingestion/load_to_postgres.py"
    ])

    run_step([
        python,
        "python/ingestion/run_transformations.py"
    ])

    print("\n===================================")
    print("MAGIC ROAST PIPELINE COMPLETED")
    print("===================================")


if __name__ == "__main__":
    main()