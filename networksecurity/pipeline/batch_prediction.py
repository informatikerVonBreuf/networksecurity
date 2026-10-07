"""Batch CSV prediction using the same inference bundle as the API."""

import argparse
from pathlib import Path

import pandas as pd

from networksecurity.utils.main_utils.utils import load_object


def predict_csv(input_path, output_path, model_path="final_model/model.pkl"):
    """Validate inputs, add predictions and write a CSV without an index column."""
    frame = pd.read_csv(input_path)
    frame["prediction"] = load_object(model_path).predict(frame)
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    frame.to_csv(output_path, index=False)
    return frame


def main():
    """Expose batch inference as python -m networksecurity.pipeline.batch_prediction."""
    parser = argparse.ArgumentParser(description="Predict classes from a feature-only CSV.")
    parser.add_argument("input")
    parser.add_argument("output")
    args = parser.parse_args()
    predict_csv(args.input, args.output)


if __name__ == "__main__":
    main()
