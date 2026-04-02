from fastapi import FastAPI
from app.api.routes import router
from app.models.database import engine, Base
from app.models.case import Case
from app.models.user import User
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Autonomous Risk & Decision Intelligence System")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # fine for demo; tighten later
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
Base.metadata.create_all(bind=engine)

app.include_router(router)


@app.get("/")
def root():
    return {"message": "Autonomous Risk & Decision Intelligence System API is running"}


