import openai
import os
from dotenv import find_dotenv, load_dotenv
import time
import logging
from datetime import datetime
import requests
import json

load_dotenv()
# openai.api_key = os.environ.get("OPENAI_API_KEY")
# defaults to getting the key using os.environ.get("OPENAI_API_KEY")
# if you saved the key under a different environment variable name, you can do something like:
# client = OpenAI(
#   api_key=os.environ.get("CUSTOM_ENV_NAME"),
# )

# news api
news_api_key = os.environ.get("NEWS_API_KEY")

client = openai.OpenAI()
model = 'gpt-3.5-turbo-1106'



def get_news(topic):
    url = (
        f"https://newsapi.org/v2/everything?q={topic}&apiKey={news_api_key}&pageSize=5"
    )

    try:
        response = requests.get(url)
        if response.status_code == 200:
            news = json.dumps(response.json(), indent=4)
            news_json = json.loads(news)

            data = news_json

            # Access all the fields (via APIs structure)
            status = data["status"]
            total_results = data["totalResults"]
            articles = data["articles"]
            final_news = [] 

            # Loop through articles
            for article in articles:
                source_name = article["source"]["name"]
                author = article["author"]
                title = article["title"]
                description = article["description"]
                url = article["url"]
                content = article["content"]
                title_description = f"""
                    Title: {title},
                    Author: {author},
                    Source: {source_name},
                    Description: {description},
                    URL: {url}
                    """
                final_news.append(title_description) #add to the final_news[]

                return final_news
            else:
                return []
        
    except requests.exceptions.RequestException as e:
        print("Error occurred during API Request", e)



def main():
    news = get_news("bitcoin")
    print(news)

if __name__ == "__main__":
    main()