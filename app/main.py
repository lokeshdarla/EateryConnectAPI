from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import customer,auth,restaurant,cuisine,menu_item,driver

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

app.include_router(customer.router)
app.include_router(auth.router)
app.include_router(restaurant.router)
app.include_router(cuisine.router)
app.include_router(menu_item.router)
app.include_router(driver.router)
