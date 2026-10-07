"""Generate feature-only demo inputs from the bundled labeled dataset."""

from pathlib import Path

import pandas as pd


def main():
    """Save five examples; this is an API demo, not an independent model evaluation."""
    output = Path("prediction_output/demo.csv")
    output.parent.mkdir(exist_ok=True)
    pd.read_csv("Network_Data/phisingData.csv").drop(columns="Result").head(5).to_csv(
        output, index=False
    )
    print(output)


if __name__ == "__main__":
    main()
