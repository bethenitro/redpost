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
            # Convert to strings and strip whitespace
            client_id = str(client_id).strip() if client_id else ""
            client_secret = str(client_secret).strip() if client_secret else ""
            username = str(username).strip() if username else ""
            password = str(password).strip() if password else ""
            
            # Validate inputs after processing
            if not client_id:
                raise Exception("Client ID is required and cannot be empty")
            if not client_secret:
                raise Exception("Client Secret is required and cannot be empty")
            if not username:
                raise Exception("Username is required and cannot be empty")
            if not password:
                raise Exception("Password is required and cannot be empty")
            
            print(f"Attempting authentication for user: {username}")
            print(f"Client ID length: {len(client_id)}")
            print(f"Client Secret length: {len(client_secret)}")
            
            self.reddit = praw.Reddit(
                client_id=client_id,
                client_secret=client_secret,
                username=username,
                password=password,
                user_agent=f"RedditBot/1.0 by {username}"
            )
            
            # Test authentication by getting user info
            print("Testing authentication...")
            user = self.reddit.user.me()
            print(f"Authentication successful for user: {user.name}")
                
            self.authenticated = True
            return True
        
        except Exception as e:
            self.authenticated = False
            error_msg = str(e)
            print(f"Authentication error: {error_msg}")
            
            # Provide more specific error messages for common issues
            if "Client ID is required" in error_msg or "Client Secret is required" in error_msg or "Username is required" in error_msg or "Password is required" in error_msg:
                raise Exception(error_msg)  # Pass through our validation errors
            elif "401" in error_msg or "invalid_grant" in error_msg:
                raise Exception("Authentication failed: Invalid username/password combination")
            elif "403" in error_msg:
                raise Exception("Authentication failed: Access forbidden - check your app permissions")
            elif "invalid_client" in error_msg:
                raise Exception("Authentication failed: Invalid Client ID or Client Secret")
            elif "429" in error_msg:
                raise Exception("Authentication failed: Too many requests - please wait and try again")
            elif "prawcore.exceptions.ResponseException" in error_msg:
                raise Exception("Authentication failed: Reddit API error - check your credentials")
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
