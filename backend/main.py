from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes import auth, group, participant, expense, balance

app = FastAPI(title="HisabKitab API")

# CORS (equivalent to Express CORS middleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Health check (like GET / in Express)
@app.get("/")
def root():
    return {"message": "HisabKitab server is running!"}

# Routes (equivalent to app.use("/api", router))
app.include_router(auth.router, prefix="/api")
app.include_router(group.router, prefix="/api")
app.include_router(participant.router, prefix="/api")
app.include_router(expense.router, prefix="/api")
app.include_router(balance.router, prefix="/api")

@app.on_event("startup")
def startup_event():
    print("🚀 Server started successfully")
