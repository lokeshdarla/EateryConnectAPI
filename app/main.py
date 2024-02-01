from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .api.routers import customer
origins = [
    "*",
]

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {"message": "Welcome to EateryConnectAPI"}


app.include_router(customer.router)
