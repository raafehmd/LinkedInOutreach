# ai_messaging.py
import os
import openai
import logging
from dotenv import load_dotenv
from transformers import pipeline

load_dotenv()
openai.api_key = os.getenv('OPENAI_API_KEY')

# Initialize sentiment analysis pipeline
sentiment_pipeline = pipeline("sentiment-analysis")

def get_ai_response(user_message):
    # Analyze sentiment
    sentiment = sentiment_pipeline(user_message)[0]
    logging.info("Sentiment analysis result: %s", sentiment)
    if sentiment['label'] == "NEGATIVE" and sentiment['score'] > 0.9:
        # Escalate messages with strongly negative sentiment
        return "Your message indicates concern. A human representative will assist you shortly."
    
    # Use GPT for generating a response
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": user_message}]
    )
    return response['choices'][0]['message']['content']
