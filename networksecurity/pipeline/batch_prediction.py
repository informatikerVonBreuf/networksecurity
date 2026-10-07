"""Prédire depuis un CSV avec le même modèle que l’API."""

import argparse
from pathlib import Path

import pandas as pd

from networksecurity.utils.main_utils.utils import load_object


def predict_csv(input_path, output_path, model_path="final_model/model.pkl"):
    """Ajouter les prédictions au CSV et enregistrer le résultat sans index."""
    frame = pd.read_csv(input_path)
    frame["prediction"] = load_object(model_path).predict(frame)
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    frame.to_csv(output_path, index=False)
    return frame


def main():
    """Lire les chemins du CSV d’entrée et du fichier de sortie."""
    parser = argparse.ArgumentParser(
        description="Prédire les classes depuis un CSV sans colonne cible."
    )
    parser.add_argument("input")
    parser.add_argument("output")
    args = parser.parse_args()
    predict_csv(args.input, args.output)


if __name__ == "__main__":
    main()
