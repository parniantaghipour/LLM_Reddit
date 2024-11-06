import pandas as pd
from textblob import TextBlob

# Load the comments CSV file
comments_df = pd.read_csv('localllama_all_comments_overnight.csv', names=['id', 'post_id', 'body', 'created_utc', 'score'])

# Define a list of model names to track (adjust as needed)
models_to_track = [
    "GPT-4o", "Grok-2", "Claude 3.5", "Gemini", "Llama 3.1",
    "Yi-Large", "GLM-4", "Molmo", "Mixtral of Experts", "GPT-4-Turbo",
    "Jamba 1.5", "Gemma 2", "Claude", "DeepSeek Coder v2", "Nemotron-4 340B",
    "Llama 3", "Athene-70B", "Qwen Max", "GPT-3.5", "Phi-3",
    "Reka Core", "Reka Flash", "Command-R-Plus", "Command R",
    "Qwen 1.5", "InternLM", "InternVL 2"
]
# Function to identify model mentions and calculate sentiment
def analyze_model_sentiment(comments_df, models):
    model_mentions = {model: {'count': 0, 'total_sentiment': 0} for model in models}

    for _, row in comments_df.iterrows():
        comment_body = row['body']
        comment_sentiment = TextBlob(comment_body).sentiment.polarity  # Sentiment score

        # Check if any model is mentioned in the comment
        for model in models:
            if model.lower() in comment_body.lower():
                model_mentions[model]['count'] += 1
                model_mentions[model]['total_sentiment'] += comment_sentiment

    # Calculate average sentiment per model
    for model, data in model_mentions.items():
        if data['count'] > 0:
            data['average_sentiment'] = data['total_sentiment'] / data['count']
        else:
            data['average_sentiment'] = None  # No mentions, so no average sentiment

    # Convert to DataFrame for easier analysis
    model_sentiment_df = pd.DataFrame([
        {'Model': model, 'Mentions': data['count'], 'Average Sentiment': data['average_sentiment']}
        for model, data in model_mentions.items()
    ])

    return model_sentiment_df

# Perform the sentiment analysis and model ranking
model_sentiment_df = analyze_model_sentiment(comments_df, models_to_track)

# Sort models by average sentiment, highest first
model_sentiment_df = model_sentiment_df.sort_values(by='Average Sentiment', ascending=False)
print(model_sentiment_df)

# Optionally, save the model sentiment ranking to a CSV file
model_sentiment_df.to_csv('model_sentiment_ranking.csv', index=False)
print("Model sentiment ranking saved to 'model_sentiment_ranking.csv'")
