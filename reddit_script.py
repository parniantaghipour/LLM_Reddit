import praw
import pandas as pd
from datetime import datetime
import time

# Configure Reddit API credentials
reddit = praw.Reddit(
    client_id='WsclGJjb_JCK0fewwULu5A',          # Your client ID
    client_secret='lB_YxjhBfFdAH88SKvw9nrCgQEbzDw',  # Your client secret
    user_agent='Model Ranking by Difficult-Check-1934'  # Custom user agent
)

def fetch_all_subreddit_data(subreddit, max_posts=None):
    posts = []
    comments = []
    post_count = 0

    # Fetch posts using pagination with .new() method
    for submission in reddit.subreddit(subreddit).new(limit=None):
        # Stop if max_posts limit is reached (if specified)
        if max_posts and post_count >= max_posts:
            break

        posts.append({
            'id': submission.id,
            'title': submission.title,
            'selftext': submission.selftext,
            'created_utc': datetime.fromtimestamp(submission.created_utc),
            'score': submission.score,
            'url': submission.url
        })
        post_count += 1

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

        # Print progress and avoid rate limits
        print(f"Fetched post {post_count}: {submission.title}")
        time.sleep(0.5)  # Pause to respect Reddit API rate limits

    # Convert lists to DataFrames
    posts_df = pd.DataFrame(posts)
    comments_df = pd.DataFrame(comments)

    return posts_df, comments_df, post_count, len(comments)

# Example usage
subreddit_name = 'LocalLLaMA'
posts_df, comments_df, total_posts, total_comments = fetch_all_subreddit_data(subreddit_name)

# Save to CSV for future use
posts_df.to_csv('localllama_all_posts_overnight.csv', index=False)
comments_df.to_csv('localllama_all_comments_overnight.csv', index=False)

# Print totals
print(f"\nTotal posts saved: {total_posts}")
print(f"Total comments saved: {total_comments}")
print("Data saved to 'localllama_all_posts.csv' and 'localllama_all_comments.csv'")