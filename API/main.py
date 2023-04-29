from typing import Optional

from fastapi import FastAPI

from joblib import load

from pydantic import BaseModel

import pandas as pd

class Review(BaseModel):
   id: float
   review_text: str

   def columns(self):
        return ["review_text"]

class Label(BaseModel):
   label: int

app = FastAPI()

@app.get("/")
def read_root():
   return {"Hello": "World"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: Optional[str] = None):
   return {"item_id": item_id, "q": q}

@app.post("/predictNB")
def make_predictions(review: Review):
   df = pd.DataFrame(review.dict(), columns=review.dict().keys(), index=[0])
   model = load("pipelineNB.pkl")
   result = model.predict(df)
   label: Label = {"label": result[0].item()}
   return label

@app.post("/predictSVC")
def make_predictions(review: Review):
   df = pd.DataFrame(review.dict(), columns=review.dict().keys(), index=[0])
   model = load("pipelineSVC.pkl")
   result = model.predict(df)
   label: Label = {"label": result[0].item()}
   return label

@app.post("/predictForest")
def make_predictions(review: Review):
   df = pd.DataFrame(review.dict(), columns=review.dict().keys(), index=[0])
   model = load("pipelineForest.pkl")
   result = model.predict(df)
   label: Label = {"label": result[0].item()}
   return label