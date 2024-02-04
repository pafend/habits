from fastapi import FastAPI

from app.routes import routes
from app.database import engine, Base, SessionLocal

app = FastAPI()

# Include the habits router with a prefix
app.include_router(routes.router, prefix="/api")

# Create tables in the database on startup
@app.on_event("startup")
async def startup_db():
    Base.metadata.create_all(bind=engine)

# Shutdown event to close database connections
@app.on_event("shutdown")
async def shutdown_db():
    SessionLocal().close()

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000, reload=True, lifespan="on")
