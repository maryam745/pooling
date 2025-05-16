from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from items_route import create_router as item_router

from database import DatabasePool
from fastapi.staticfiles import StaticFiles

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins (change this for production security)
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods (GET, POST, PUT, DELETE, etc.)
    allow_headers=["*"],  # Allow all headers
)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Initialize database pool globally
database_pool = DatabasePool()

@app.on_event("startup")
async def startup():
    await database_pool.initialize()

@app.on_event("shutdown")
async def shutdown():
    if database_pool.pool:
        await database_pool.close()

# Include Routers
app.include_router(item_router(database_pool), prefix="/items", tags=["Items"])

@app.get("/")
async def root():
    return {"message": "Welcome to the API"}
