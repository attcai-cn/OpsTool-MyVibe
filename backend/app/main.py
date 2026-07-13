from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import get_settings
from app.database import engine, Base
from app.routers import auth, notes, cheatsheet, calculator, cron, todo

settings = get_settings()

# Create tables (for dev convenience; Alembic should be used in production)
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description=settings.DESCRIPTION,
    docs_url="/docs",
    redoc_url="/redoc",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/api/v1")
app.include_router(notes.router, prefix="/api/v1")
app.include_router(cheatsheet.router, prefix="/api/v1")
app.include_router(calculator.router, prefix="/api/v1")
app.include_router(cron.router, prefix="/api/v1")
app.include_router(todo.router, prefix="/api/v1")


@app.get("/health")
def health_check():
    return {"status": "ok"}
