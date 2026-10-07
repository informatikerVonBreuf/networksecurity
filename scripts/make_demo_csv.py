"""Créer un CSV d’exemple sans la colonne cible."""

from pathlib import Path

import pandas as pd


def main():
    """Enregistrer cinq lignes pour essayer la prédiction."""
    output = Path("prediction_output/demo.csv")
    output.parent.mkdir(exist_ok=True)
    pd.read_csv("Network_Data/phisingData.csv").drop(columns="Result").head(5).to_csv(
        output, index=False
    )
    print(output)


if __name__ == "__main__":
    main()
