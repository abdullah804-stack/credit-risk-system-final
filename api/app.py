from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi import Request

from pydantic import BaseModel

from src.pipelines.predict_pipeline import predict

app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Static files
app.mount("/static", StaticFiles(directory="api/static"), name="static")

# Templates
templates = Jinja2Templates(directory="api/templates")


# Home Route
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html"
    )


# Input Schema
class LoanData(BaseModel):
    loan_amnt: float
    term: str
    int_rate: float
    installment: float
    annual_inc: float
    dti: float
    open_acc: float
    pub_rec: float
    revol_bal: float
    revol_util: float
    total_acc: float
    mort_acc: float
    pub_rec_bankruptcies: float


# Prediction Route
@app.post("/predict")
def get_prediction(data: LoanData):

    sample = data.dict()

    prediction, probability = predict(sample)

    return {
        "prediction": int(prediction),
        "probability": float(probability)
    }