"""CSV inference API; training remains an explicit CLI operation."""

from pathlib import Path

import pandas as pd
from fastapi import FastAPI, File, HTTPException, Request, UploadFile
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

from networksecurity.utils.main_utils.utils import load_object

app = FastAPI(
    title="Network Security", description="Phishing feature classification demo", version="0.1.0"
)
templates = Jinja2Templates(directory="templates")
MODEL_PATH = Path("final_model/model.pkl")


@app.get("/", include_in_schema=False)
def index():
    """Open the interactive API documentation."""
    return RedirectResponse("/docs")


@app.get("/health")
def health():
    """Report service liveness and whether a trained artifact is available."""
    return {"status": "ok", "model_available": MODEL_PATH.is_file()}


@app.post("/predict")
def predict_route(request: Request, file: UploadFile = File(...)):
    """Validate a feature CSV and return escaped HTML with encoded predictions."""
    if not MODEL_PATH.is_file():
        raise HTTPException(503, "Train a model first using main.py.")
    try:
        frame = pd.read_csv(file.file)
        model = load_object(MODEL_PATH)
        frame["prediction"] = model.predict(frame)
    except (ValueError, pd.errors.ParserError) as exc:
        raise HTTPException(422, str(exc)) from exc
    # Escape cells before marking the generated table HTML safe in the template.
    return templates.TemplateResponse(
        request=request,
        name="table.html",
        context={"table": frame.to_html(index=False, escape=True)},
    )
