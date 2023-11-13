from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware

from middleware.middleware import ProcessTimeMiddleware #, DBSessionMiddleware

from routes import users, trigger_router

origins = [
    "http://localhost:8000",
    "http://localhost:8080",
    "http://localhost:3000",
]

app = FastAPI(debug=True)
app.add_middleware(GZipMiddleware, minimum_size=1000)
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# app.add_middleware(DBSessionMiddleware)
app.add_middleware(ProcessTimeMiddleware)

app.include_router(users.router, prefix="/api/v1/users")
app.include_router(trigger_router.trigger)

