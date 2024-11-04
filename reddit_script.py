import praw
import pandas as pd
from datetime import datetime

reddit = praw.Reddit(
    client_id='WsclGJjb_JCK0fewwULu5A',  # Your client ID
    client_secret='lB_YxjhBfFdAH88SKvw9nrCgQEbzDw',  # Your client secret
    user_agent='Model Ranking by Difficult-Check-1934',  # Custom user agent
)

def fetch_subreddit_data(subreddit, post_limit=100):
    posts = []
    comments = []

    # Fetch posts
    for submission in reddit.subreddit(subreddit).new(limit=post_limit):
        posts.append({
            'id': submission.id,
            'title': submission.title,
            'selftext': submission.selftext,
            'created_utc': datetime.fromtimestamp(submission.created_utc),
            'score': submission.score,
            'url': submission.url
        })

        # Fetch comments for each post
        submission.comments.replace_more(limit=None)  # Load all comments
        for comment in submission.comments.list():
            comments.append({
                'id': comment.id,
                'post_id': submission.id,
                'body': comment.body,
                'created_utc': datetime.fromtimestamp(comment.created_utc),
                'score': comment.score
            })

    # Convert to DataFrames
    posts_df = pd.DataFrame(posts)
    comments_df = pd.DataFrame(comments)

    return posts_df, comments_df

# Example usage
subreddit_name = 'LocalLLaMA'
posts_df, comments_df = fetch_subreddit_data(subreddit_name)
print(posts_df.head())
print(comments_df.head())

# Save to CSV for incremental updates
posts_df.to_csv('localllama_posts.csv', mode='a', header=False, index=False)
comments_df.to_csv('localllama_comments.csv', mode='a', header=False, index=False)