from fastapi import FastAPI
import uvicorn

import requests
from pydantic import BaseModel, HttpUrl
from bs4 import BeautifulSoup


app = FastAPI()


class URL(BaseModel):
    url: HttpUrl


@app.get('/')
def index():
    return {'message': "Hello world"}


@app.post('/scrap_tags')
async def scrape_tags(url: URL):

    page = requests.get(str(url.url))

    soup = BeautifulSoup(page.text, 'html.parser')

    def get_keywords():
        keywords = soup.head.find('meta', attrs={'name': 'keywords'}).get(
            'content') if soup.head.find('meta', attrs={'name': 'keywords'}) else None
        return keywords

    def get_title():
        return soup.head.find('title').text if soup.head.find('title') else None

    def get_description():
        main_description = soup.head.find('meta', attrs={'name': 'description'}).get(
            'content') if soup.head.find('meta', attrs={'name': 'description'}) else None

        og_description = soup.find(
            'meta', property="og:description").get('content') if soup.find(
            'meta', property="og:description") else None

        return main_description or og_description or None

    def get_image():
        return soup.find(
            'meta', property="og:image").get('content') if soup.find(
            'meta', property="og:image") else None

    return {
        "title": get_title(),
        "description": get_description(),
        "keywords": get_keywords(),
        "image": get_image(),
    }
