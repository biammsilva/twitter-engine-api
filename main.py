import os
from fastapi import FastAPI
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware

from src.service import TwitterService


app = FastAPI(
    docs_url="/",
    title="Tweet search api",
    description="That project was designed to provide the 100 tweets with\
                 a specific term and the top 10 hashtags in it"
)
origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET"],
    allow_headers=["*"],
)
load_dotenv()


@app.get("/search/{term}")
def search(term: str, language: str = '') -> dict:
    if not os.environ.get('TWITTER_BEARER_TOKEN'):
        raise ValueError(
            'You need to set the environment variable: "TWITTER_BEARER_TOKEN"'
        )
    return TwitterService.get_100_tweets(term, language)
