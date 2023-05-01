from typing import Optional

from fastapi import FastAPI

from joblib import load

from pydantic import BaseModel

import pandas as pd

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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

@app.options("/{somepath}")
def cors():
   return 

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