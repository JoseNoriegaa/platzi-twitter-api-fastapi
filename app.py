# FastAPI
from fastapi import FastAPI

# Routers
from routes.auth import router as auth_router
from routes.user import router as user_router
from routes.tweet import router as tweet_router

# Database
from config.db import meta
from config.db import engine

# Initialize database
meta.create_all(engine)

# Initialize the app
app = FastAPI()

app.include_router(auth_router, prefix='/auth')
app.include_router(user_router, prefix='/users')
app.include_router(tweet_router, prefix='/tweets')
