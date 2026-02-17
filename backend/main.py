from fastapi import FastAPI
from app.routes import auth, balance, expense, group, participant

app = FastAPI()

app.include_router(auth.router)
app.include_router(balance.router)
app.include_router(expense.router)
app.include_router(group.router)
app.include_router(participant.router)
