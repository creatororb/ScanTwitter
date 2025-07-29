from fastapi import FastAPI, Query # type: ignore
from pydantic import BaseModel # type: ignore
import snscrape.modules.twitter as sntwitter # type: ignore
from typing import List

app = FastAPI()

class Tweet(BaseModel):
    date: str
    username: str
    content: str

@app.get("/search_tweets", response_model=List[Tweet])
async def search_tweets(
    query: str = Query(..., description="Search query (keyword or hashtag)"),
    max_tweets: int = Query(100, description="Max number of tweets to fetch")
):
    tweets = []
    for i, tweet in enumerate(sntwitter.TwitterSearchScraper(query).get_items()):
        if i >= max_tweets:
            break
        tweets.append(Tweet(
            date=str(tweet.date),
            username=tweet.user.username,
            content=tweet.content
        ))
    return tweets