"""API de prédiction à partir d’un CSV. L’entraînement se lance depuis main.py."""

from pathlib import Path

import pandas as pd
from fastapi import FastAPI, File, HTTPException, Request, UploadFile
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

from networksecurity.utils.main_utils.utils import load_object

app = FastAPI(
    title="Network Security",
    description="Classification de sites web à partir de caractéristiques numériques.",
    version="0.1.0",
)
templates = Jinja2Templates(directory="templates")
MODEL_PATH = Path("final_model/model.pkl")


@app.get("/", include_in_schema=False)
def index():
    """Ouvrir la documentation interactive."""
    return RedirectResponse("/docs")


@app.get("/health")
def health():
    """Indiquer si le service répond et si un modèle est disponible."""
    return {"status": "ok", "model_available": MODEL_PATH.is_file()}


@app.post("/predict")
def predict_route(request: Request, file: UploadFile = File(...)):
    """Vérifier le CSV et afficher les prédictions dans un tableau HTML."""
    if not MODEL_PATH.is_file():
        raise HTTPException(503, "Aucun modèle disponible. Lancez un entraînement avec main.py.")
    try:
        frame = pd.read_csv(file.file)
        model = load_object(MODEL_PATH)
        frame["prediction"] = model.predict(frame)
    except (ValueError, pd.errors.ParserError) as exc:
        raise HTTPException(422, str(exc)) from exc
    # Échapper les cellules avant d’insérer le tableau dans le modèle HTML.
    return templates.TemplateResponse(
        request=request,
        name="table.html",
        context={
            "table": frame.to_html(index=False, escape=True, border=0),
            "row_count": len(frame),
            "feature_count": len(frame.columns) - 1,
        },
    )
