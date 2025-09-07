# bot_core.py
import praw
import random
from datetime import datetime

class RedditBot:
    def __init__(self):
        self.reddit = None
        self.authenticated = False
    
    def authenticate(self, client_id, client_secret, username, password):
        """Authenticate with Reddit API"""
        try:
            # Validate inputs
            if not all([client_id, client_secret, username, password]):
                raise Exception("All credentials must be provided")
            
            self.reddit = praw.Reddit(
                client_id=client_id,
                client_secret=client_secret,
                username=username,
                password=password,
                user_agent=f"RedditBot/1.0 by {username}"
            )
            
            # Test authentication
            user = self.reddit.user.me()
            if user is None:
                raise Exception("Authentication failed - unable to retrieve user info")
                
            self.authenticated = True
            return True
        
        except Exception as e:
            self.authenticated = False
            # Provide more specific error messages for common issues
            error_msg = str(e)
            if "401" in error_msg or "invalid_grant" in error_msg:
                raise Exception("Authentication failed: Invalid username/password or incorrect app credentials")
            elif "403" in error_msg:
                raise Exception("Authentication failed: Access forbidden - check your app permissions")
            elif "invalid_client" in error_msg:
                raise Exception("Authentication failed: Invalid Client ID or Client Secret")
            else:
                raise Exception(f"Authentication failed: {error_msg}")
    
    def get_username(self):
        """Get authenticated username"""
        if self.authenticated:
            return self.reddit.user.me().name
        return None
    
    def post_images(self, subreddit_name, title, image_paths):
        """Post images to a subreddit"""
        if not self.authenticated:
            raise Exception("Not authenticated")
        
        try:
            subreddit = self.reddit.subreddit(subreddit_name)
            
            if len(image_paths) == 1:
                # Single image post
                submission = subreddit.submit_image(title=title, image_path=image_paths[0])
            else:
                # Multiple images post (gallery)
                images = [{"image_path": path} for path in image_paths]
                submission = subreddit.submit_gallery(title=title, images=images)
            
            return f"https://reddit.com{submission.permalink}"
        
        except Exception as e:
            print(f"Error posting to r/{subreddit_name}: {e}")
            return None
