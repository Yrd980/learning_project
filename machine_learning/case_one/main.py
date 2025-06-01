import argparse

def parse_args():
    parser = argparse.ArgumentParser(description="Run the machine learning case one.")

    parser.add_argument(
        "--config", type=str, default="config.yaml", help="config path"
    )
