from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routes.analyze import router as analyze_router
from routes.audit import router as audit_router
from routes.regulations import router as regulations_router


app = FastAPI(title="RegWatch Backend", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(regulations_router, prefix="/api")
app.include_router(analyze_router, prefix="/api")
app.include_router(audit_router, prefix="/api")


@app.get("/")
def root() -> dict:
    return {"message": "RegWatch backend running"}
