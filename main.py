# main.py
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, filedialog
import threading
import time
import random
import os
from datetime import datetime
from bot_core import RedditBot
from logger import BotLogger
from PIL import Image, ImageTk

class RedditBotDashboard:
    def __init__(self, root):
        self.root = root
        self.root.title("Reddit Multi-Post Bot Dashboard")
        self.root.geometry("1400x900")
        self.root.minsize(1200, 800)
        
        # Configure modern styling
        self.configure_styles()
        
        self.bot = RedditBot()
        self.logger = BotLogger()
        
        self.is_posting = False
        self.posting_thread = None
        self.image_gallery = []
        self.subreddit_entries = []
        self.title_entries = []
        self.image_thumbnails = []
        
        self.create_dashboard()
        self.update_status("Ready - Configure your settings and start posting")
        
        # Bind window resize event to update canvas scroll regions
        self.root.bind('<Configure>', self.on_window_resize)
    
    def configure_styles(self):
        """Configure modern styling for the application"""
        style = ttk.Style()
        
        # Configure modern colors and styles
        style.configure('Title.TLabel', font=('Arial', 16, 'bold'), foreground='#2c3e50')
        style.configure('Heading.TLabel', font=('Arial', 12, 'bold'), foreground='#34495e')
        style.configure('Modern.TLabelframe', relief='flat', borderwidth=2)
        style.configure('Modern.TLabelframe.Label', font=('Arial', 11, 'bold'), foreground='#2980b9')
        
        # Button styles
        style.configure('Success.TButton', font=('Arial', 10, 'bold'))
        style.configure('Danger.TButton', font=('Arial', 10, 'bold'))
        style.configure('Primary.TButton', font=('Arial', 10, 'bold'))
        
        # Configure the root background
        self.root.configure(bg='#ecf0f1')
    
    def on_window_resize(self, event):
        """Handle window resize events"""
        if hasattr(self, 'left_canvas') and hasattr(self, 'right_canvas'):
            # Update canvas scroll regions when window is resized
            self.root.after_idle(lambda: self.left_canvas.configure(scrollregion=self.left_canvas.bbox("all")))
            self.root.after_idle(lambda: self.right_canvas.configure(scrollregion=self.right_canvas.bbox("all")))
    
    def create_dashboard(self):
        """Create the main dashboard"""
        # Main container
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Left panel - Configuration with scrollable area
        left_scroll_frame = ttk.Frame(main_frame)
        left_scroll_frame.pack(side="left", fill="both", expand=True, padx=5)
        
        # Create scrollable canvas for left panel
        left_canvas = tk.Canvas(left_scroll_frame)
        left_scrollbar = ttk.Scrollbar(left_scroll_frame, orient="vertical", command=left_canvas.yview)
        left_scrollable_frame = ttk.Frame(left_canvas)
        
        left_scrollable_frame.bind(
            "<Configure>",
            lambda e: left_canvas.configure(scrollregion=left_canvas.bbox("all"))
        )
        
        left_canvas.create_window((0, 0), window=left_scrollable_frame, anchor="nw")
        left_canvas.configure(yscrollcommand=left_scrollbar.set)
        
        left_canvas.pack(side="left", fill="both", expand=True)
        left_scrollbar.pack(side="right", fill="y")
        
        # Right panel - Status and logs with scrollable area
        right_scroll_frame = ttk.Frame(main_frame)
        right_scroll_frame.pack(side="right", fill="both", expand=True, padx=5)
        
        # Create scrollable canvas for right panel
        right_canvas = tk.Canvas(right_scroll_frame)
        right_scrollbar = ttk.Scrollbar(right_scroll_frame, orient="vertical", command=right_canvas.yview)
        right_scrollable_frame = ttk.Frame(right_canvas)
        
        right_scrollable_frame.bind(
            "<Configure>",
            lambda e: right_canvas.configure(scrollregion=right_canvas.bbox("all"))
        )
        
        right_canvas.create_window((0, 0), window=right_scrollable_frame, anchor="nw")
        right_canvas.configure(yscrollcommand=right_scrollbar.set)
        
        right_canvas.pack(side="left", fill="both", expand=True)
        right_scrollbar.pack(side="right", fill="y")
        
        # Store canvas references for mouse wheel binding
        self.left_canvas = left_canvas
        self.right_canvas = right_canvas
        
        # Bind mouse wheel events
        self.bind_mousewheel(left_canvas)
        self.bind_mousewheel(right_canvas)
        
        self.create_config_section(left_scrollable_frame)
        self.create_status_section(right_scrollable_frame)
    
    def create_config_section(self, parent):
        """Create configuration section"""
        # Reddit API Config
        api_frame = ttk.LabelFrame(parent, text="🔐 Reddit API Configuration", padding="15", style='Modern.TLabelframe')
        api_frame.pack(fill="x", pady=(0, 10))
        
        # Credentials in a grid
        ttk.Label(api_frame, text="Client ID:", style='Heading.TLabel').grid(row=0, column=0, sticky="w", pady=5)
        self.client_id_var = tk.StringVar()
        client_id_entry = ttk.Entry(api_frame, textvariable=self.client_id_var, width=45, font=('Arial', 10))
        client_id_entry.grid(row=0, column=1, padx=15, pady=5, sticky="ew")
        
        ttk.Label(api_frame, text="Client Secret:", style='Heading.TLabel').grid(row=1, column=0, sticky="w", pady=5)
        self.client_secret_var = tk.StringVar()
        client_secret_entry = ttk.Entry(api_frame, textvariable=self.client_secret_var, width=45, font=('Arial', 10))
        client_secret_entry.grid(row=1, column=1, padx=15, pady=5, sticky="ew")
        
        ttk.Label(api_frame, text="Username:", style='Heading.TLabel').grid(row=2, column=0, sticky="w", pady=5)
        self.username_var = tk.StringVar()
        username_entry = ttk.Entry(api_frame, textvariable=self.username_var, width=45, font=('Arial', 10))
        username_entry.grid(row=2, column=1, padx=15, pady=5, sticky="ew")
        
        ttk.Label(api_frame, text="Password:", style='Heading.TLabel').grid(row=3, column=0, sticky="w", pady=5)
        self.password_var = tk.StringVar()
        password_entry = ttk.Entry(api_frame, textvariable=self.password_var, width=45, font=('Arial', 10))
        password_entry.grid(row=3, column=1, padx=15, pady=5, sticky="ew")
        
        # Configure grid weights for responsive design
        api_frame.columnconfigure(1, weight=1)
        
        ttk.Button(api_frame, text="🔌 Test Connection", command=self.test_connection, 
                  style='Primary.TButton').grid(row=4, column=1, pady=15, sticky="w")
        
        # Subreddits with dynamic entry system
        sub_frame = ttk.LabelFrame(parent, text="📍 Target Subreddits", padding="15", style='Modern.TLabelframe')
        sub_frame.pack(fill="x", pady=(0, 10))
        
        sub_controls = ttk.Frame(sub_frame)
        sub_controls.pack(fill="x", pady=(0, 10))
        
        ttk.Button(sub_controls, text="➕ Add Subreddit", command=self.add_subreddit_entry,
                  style='Primary.TButton').pack(side="left", padx=(0, 10))
        ttk.Button(sub_controls, text="🗑 Clear All", command=self.clear_subreddits,
                  style='Danger.TButton').pack(side="left")
        
        self.subreddits_frame = ttk.Frame(sub_frame)
        self.subreddits_frame.pack(fill="x")
        
        # Add initial subreddit entries
        self.add_subreddit_entry("test")
        self.add_subreddit_entry("testingground4bots")
        
        # Add some buttons for quick subreddit management
        sub_quick_frame = ttk.Frame(sub_frame)
        sub_quick_frame.pack(fill="x", pady=(5, 0))
        
        ttk.Label(sub_quick_frame, text="Quick add:", font=('Arial', 9)).pack(side="left", padx=(0, 5))
        ttk.Button(sub_quick_frame, text="+ pics", 
                  command=lambda: self.add_subreddit_entry("pics")).pack(side="left", padx=2)
        ttk.Button(sub_quick_frame, text="+ funny", 
                  command=lambda: self.add_subreddit_entry("funny")).pack(side="left", padx=2)
        ttk.Button(sub_quick_frame, text="+ mildlyinteresting", 
                  command=lambda: self.add_subreddit_entry("mildlyinteresting")).pack(side="left", padx=2)
        
        # Titles with dynamic entry system
        titles_frame = ttk.LabelFrame(parent, text="📝 Post Titles", padding="15", style='Modern.TLabelframe')
        titles_frame.pack(fill="x", pady=(0, 10))
        
        title_controls = ttk.Frame(titles_frame)
        title_controls.pack(fill="x", pady=(0, 10))
        
        ttk.Button(title_controls, text="➕ Add Title", command=self.add_title_entry,
                  style='Primary.TButton').pack(side="left", padx=(0, 10))
        ttk.Button(title_controls, text="🗑 Clear All", command=self.clear_titles,
                  style='Danger.TButton').pack(side="left")
        
        self.titles_frame = ttk.Frame(titles_frame)
        self.titles_frame.pack(fill="x")
        
        # Add initial title entries
        self.add_title_entry("Amazing Photo Collection")
        self.add_title_entry("Check out these awesome pics")
        
        # Add some buttons for quick title management
        title_quick_frame = ttk.Frame(titles_frame)
        title_quick_frame.pack(fill="x", pady=(5, 0))
        
        ttk.Label(title_quick_frame, text="Templates:", font=('Arial', 9)).pack(side="left", padx=(0, 5))
        ttk.Button(title_quick_frame, text="+ Photo Collection", 
                  command=lambda: self.add_title_entry("Amazing Photo Collection")).pack(side="left", padx=2)
        ttk.Button(title_quick_frame, text="+ Check this out", 
                  command=lambda: self.add_title_entry("Check out these awesome pics")).pack(side="left", padx=2)
        ttk.Button(title_quick_frame, text="+ Daily dump", 
                  command=lambda: self.add_title_entry("Daily photo dump")).pack(side="left", padx=2)
        
        # Image Gallery with thumbnails
        gallery_frame = ttk.LabelFrame(parent, text="🖼 Image Gallery", padding="15", style='Modern.TLabelframe')
        gallery_frame.pack(fill="x", pady=(0, 10))
        
        gallery_controls = ttk.Frame(gallery_frame)
        gallery_controls.pack(fill="x", pady=(0, 10))
        
        ttk.Button(gallery_controls, text="📁 Select Folder", 
                  command=self.select_image_folder, style='Primary.TButton').pack(side="left", padx=(0, 10))
        ttk.Button(gallery_controls, text="🖼 Add Images", 
                  command=self.add_images, style='Primary.TButton').pack(side="left", padx=(0, 10))
        ttk.Button(gallery_controls, text="🗑 Clear Gallery", 
                  command=self.clear_gallery, style='Danger.TButton').pack(side="left")
        
        self.gallery_display_frame = ttk.Frame(gallery_frame)
        self.gallery_display_frame.pack(fill="both", expand=True, pady=(10, 0))
        
        # Create scrollable canvas for thumbnails
        self.gallery_canvas = tk.Canvas(self.gallery_display_frame, height=120, bg='white')
        gallery_scrollbar = ttk.Scrollbar(self.gallery_display_frame, orient="horizontal", command=self.gallery_canvas.xview)
        self.gallery_scrollable_frame = ttk.Frame(self.gallery_canvas)
        
        self.gallery_scrollable_frame.bind(
            "<Configure>",
            lambda e: self.gallery_canvas.configure(scrollregion=self.gallery_canvas.bbox("all"))
        )
        
        self.gallery_canvas.create_window((0, 0), window=self.gallery_scrollable_frame, anchor="nw")
        self.gallery_canvas.configure(xscrollcommand=gallery_scrollbar.set)
        
        self.gallery_canvas.pack(side="top", fill="both", expand=True)
        gallery_scrollbar.pack(side="bottom", fill="x")
        
        self.gallery_status_label = ttk.Label(gallery_frame, text="No images in gallery", 
                                            style='Heading.TLabel', foreground='gray')
        self.gallery_status_label.pack(pady=(10, 0))
        
        # Posting Settings
        settings_frame = ttk.LabelFrame(parent, text="⚙️ Posting Settings", padding="15", style='Modern.TLabelframe')
        settings_frame.pack(fill="x", pady=(0, 10))
        
        settings_grid = ttk.Frame(settings_frame)
        settings_grid.pack()
        
        # Base pause time
        ttk.Label(settings_grid, text="Base pause time (seconds):", style='Heading.TLabel').grid(row=0, column=0, sticky="w", pady=8)
        self.pause_var = tk.StringVar(value="60")
        ttk.Spinbox(settings_grid, from_=10, to=600, textvariable=self.pause_var, width=12, font=('Arial', 10)).grid(row=0, column=1, padx=15)
        
        # Random variance
        ttk.Label(settings_grid, text="Random variance (±seconds):", style='Heading.TLabel').grid(row=1, column=0, sticky="w", pady=8)
        self.random_variance_var = tk.StringVar(value="15")
        ttk.Spinbox(settings_grid, from_=0, to=120, textvariable=self.random_variance_var, width=12, font=('Arial', 10)).grid(row=1, column=1, padx=15)
        
        # Enable human-like delays
        self.human_like_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(settings_grid, text="🧠 Enable human-like delays", variable=self.human_like_var,
                       style='Heading.TCheckbutton').grid(row=2, column=0, columnspan=2, sticky="w", pady=8)
        
        # Pause range display
        self.pause_range_label = ttk.Label(settings_grid, text="", foreground="#7f8c8d", font=("Arial", 9))
        self.pause_range_label.grid(row=3, column=0, columnspan=2, pady=5)
        
        # Update pause range when values change
        self.pause_var.trace('w', self.update_pause_range)
        self.random_variance_var.trace('w', self.update_pause_range)
        
        # Images per post
        ttk.Label(settings_grid, text="Images per post:", style='Heading.TLabel').grid(row=4, column=0, sticky="w", pady=8)
        self.images_per_post_var = tk.StringVar(value="2")
        ttk.Spinbox(settings_grid, from_=1, to=10, textvariable=self.images_per_post_var, width=12, font=('Arial', 10)).grid(row=4, column=1, padx=15)
        
        # Random image count
        self.random_images_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(settings_grid, text="🎲 Randomize images per post", variable=self.random_images_var,
                       style='Heading.TCheckbutton').grid(row=5, column=0, columnspan=2, sticky="w", pady=8)
        
        # Initialize pause range display
        self.update_pause_range()
        
        # Control Buttons
        control_frame = ttk.LabelFrame(parent, text="🎮 Controls", padding="15", style='Modern.TLabelframe')
        control_frame.pack(fill="x", pady=(0, 10))
        
        buttons_frame = ttk.Frame(control_frame)
        buttons_frame.pack()
        
        self.start_btn = ttk.Button(buttons_frame, text="🚀 Start Posting", 
                                   command=self.start_posting, style="Success.TButton")
        self.start_btn.pack(side="left", padx=(0, 15))
        
        self.stop_btn = ttk.Button(buttons_frame, text="⏹ Stop Posting", 
                                  command=self.stop_posting, state="disabled", style="Danger.TButton")
        self.stop_btn.pack(side="left", padx=(0, 15))
        
        self.preview_btn = ttk.Button(buttons_frame, text="👁 Preview Posts", 
                                     command=self.preview_posts, style="Primary.TButton")
        self.preview_btn.pack(side="left")
    
    def create_status_section(self, parent):
        """Create status and logging section"""
        # Status
        status_frame = ttk.LabelFrame(parent, text="📊 Status", padding="15", style='Modern.TLabelframe')
        status_frame.pack(fill="x", pady=(0, 10))
        
        self.status_label = ttk.Label(status_frame, text="Ready", font=("Arial", 12, "bold"), 
                                    foreground='#27ae60')
        self.status_label.pack(pady=(0, 10))
        
        self.progress = ttk.Progressbar(status_frame, mode='determinate', length=400)
        self.progress.pack(fill="x", pady=(0, 10))
        
        self.current_action_label = ttk.Label(status_frame, text="", foreground="#3498db", 
                                            font=("Arial", 10))
        self.current_action_label.pack()
        
        # Statistics
        stats_frame = ttk.LabelFrame(parent, text="📈 Session Statistics", padding="15", style='Modern.TLabelframe')
        stats_frame.pack(fill="x", pady=(0, 10))
        
        self.stats_text = tk.Text(stats_frame, height=6, state="disabled", font=("Consolas", 10),
                                 bg='#f8f9fa', relief='flat', borderwidth=0)
        self.stats_text.pack(fill="x", padx=5, pady=5)
        
        # Live Log
        log_frame = ttk.LabelFrame(parent, text="📝 Activity Log", padding="15", style='Modern.TLabelframe')
        log_frame.pack(fill="both", expand=True)
        
        log_controls = ttk.Frame(log_frame)
        log_controls.pack(fill="x", pady=(0, 10))
        
        ttk.Button(log_controls, text="🗑 Clear Log", command=self.clear_log,
                  style='Danger.TButton').pack(side="right")
        
        self.log_text = scrolledtext.ScrolledText(log_frame, height=15, font=("Consolas", 9),
                                                 bg='#f8f9fa', relief='flat', borderwidth=0)
        self.log_text.pack(fill="both", expand=True)
    
    def select_image_folder(self):
        """Select folder containing images"""
        folder = filedialog.askdirectory(title="Select Image Folder")
        if folder:
            image_extensions = ('.png', '.jpg', '.jpeg', '.gif', '.bmp', '.webp')
            images = []
            
            for file in os.listdir(folder):
                if file.lower().endswith(image_extensions):
                    images.append(os.path.join(folder, file))
            
            self.image_gallery.extend(images)
            self.update_gallery_display()
            self.log(f"📁 Added {len(images)} images from folder")
    
    def add_images(self):
        """Add individual images"""
        files = filedialog.askopenfilenames(
            title="Select Images",
            filetypes=[
                ("Image files", "*.png *.jpg *.jpeg *.gif *.bmp *.webp"),
                ("All files", "*.*")
            ]
        )
        if files:
            self.image_gallery.extend(files)
            self.update_gallery_display()
            self.log(f"🖼 Added {len(files)} images to gallery")
    
    def clear_gallery(self):
        """Clear image gallery"""
        self.image_gallery.clear()
        self.update_gallery_display()
        self.log("🗑 Gallery cleared")
    
    def test_connection(self):
        """Test Reddit API connection"""
        try:
            # Get and validate credentials
            client_id = self.client_id_var.get().strip()
            client_secret = self.client_secret_var.get().strip()
            username = self.username_var.get().strip()
            password = self.password_var.get().strip()
            
            # Check for empty fields
            if not client_id:
                messagebox.showerror("Error", "Client ID is required")
                return
            if not client_secret:
                messagebox.showerror("Error", "Client Secret is required")
                return
            if not username:
                messagebox.showerror("Error", "Username is required")
                return
            if not password:
                messagebox.showerror("Error", "Password is required")
                return
            
            if self.bot.authenticate(client_id, client_secret, username, password):
                messagebox.showinfo("Success", f"Connected successfully as {self.bot.get_username()}")
                self.log("✅ Reddit API connection successful")
            else:
                messagebox.showerror("Error", "Failed to authenticate with Reddit API")
                self.log("❌ Reddit API authentication failed")
        except Exception as e:
            messagebox.showerror("Error", f"Connection failed: {str(e)}")
            self.log(f"❌ Connection error: {str(e)}")
    
    def preview_posts(self):
        """Preview what posts will be made with visual thumbnails"""
        subreddits = self.get_subreddits()
        titles = self.get_titles()
        
        if not subreddits or not titles:
            messagebox.showwarning("Warning", "Please add subreddits and titles first")
            return
        
        if not self.image_gallery:
            messagebox.showwarning("Warning", "Please add images to the gallery first")
            return
        
        # Create preview window
        preview_window = tk.Toplevel(self.root)
        preview_window.title("📋 Post Preview")
        preview_window.geometry("900x700")
        preview_window.configure(bg='#ecf0f1')
        
        # Create scrollable frame
        canvas = tk.Canvas(preview_window, bg='#ecf0f1')
        scrollbar = ttk.Scrollbar(preview_window, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Title
        title_label = ttk.Label(scrollable_frame, text="🚀 POST PREVIEW", 
                               font=('Arial', 18, 'bold'), foreground='#2c3e50')
        title_label.pack(pady=(20, 10))
        
        # Settings summary
        settings_frame = ttk.LabelFrame(scrollable_frame, text="⚙️ Settings Summary", 
                                      padding="15", style='Modern.TLabelframe')
        settings_frame.pack(fill="x", padx=20, pady=(0, 20))
        
        base_pause = int(self.pause_var.get())
        variance = int(self.random_variance_var.get())
        min_pause = max(5, base_pause - variance)
        max_pause = base_pause + variance
        
        images_text = f"{self.images_per_post_var.get()}"
        if self.random_images_var.get():
            images_text += f" (randomized 1-{self.images_per_post_var.get()})"
        
        settings_text = f"""⏱ Pause time: {min_pause}-{max_pause} seconds (base: {base_pause}±{variance})
🧠 Human-like delays: {'Enabled' if self.human_like_var.get() else 'Disabled'}
🖼 Images per post: {images_text}
📊 Total posts planned: {min(len(subreddits), len(titles))}"""
        
        settings_label = ttk.Label(settings_frame, text=settings_text, font=('Arial', 10))
        settings_label.pack(anchor="w")
        
        # Preview each post
        max_posts = min(len(subreddits), len(titles))
        for i in range(min(max_posts, 10)):  # Limit to 10 previews for performance
            # Post frame
            post_frame = ttk.LabelFrame(scrollable_frame, text=f"📝 Post {i+1}", 
                                      padding="15", style='Modern.TLabelframe')
            post_frame.pack(fill="x", padx=20, pady=(0, 15))
            
            # Subreddit and title
            post_info = ttk.Frame(post_frame)
            post_info.pack(fill="x", pady=(0, 10))
            
            ttk.Label(post_info, text=f"📍 Subreddit: r/{subreddits[i]}", 
                     font=('Arial', 11, 'bold'), foreground='#e74c3c').pack(anchor="w")
            ttk.Label(post_info, text=f"📋 Title: {titles[i]}", 
                     font=('Arial', 11, 'bold'), foreground='#2980b9').pack(anchor="w", pady=(5, 0))
            
            # Image preview
            images_per_post = self.get_images_per_post()
            selected_images = random.sample(self.image_gallery, min(images_per_post, len(self.image_gallery)))
            
            if selected_images:
                images_label = ttk.Label(post_info, text=f"🖼 Images ({len(selected_images)}):", 
                                       font=('Arial', 10, 'bold'), foreground='#27ae60')
                images_label.pack(anchor="w", pady=(10, 5))
                
                # Thumbnail frame
                thumb_frame = ttk.Frame(post_frame)
                thumb_frame.pack(fill="x")
                
                for j, img_path in enumerate(selected_images[:5]):  # Show max 5 thumbnails
                    thumb = self.create_thumbnail(img_path, (60, 60))
                    if thumb:
                        img_frame = ttk.Frame(thumb_frame, relief='solid', borderwidth=1)
                        img_frame.pack(side="left", padx=5)
                        
                        img_label = tk.Label(img_frame, image=thumb, bg='white')
                        img_label.pack(padx=2, pady=2)
                        img_label.image = thumb  # Keep reference
                        
                        # Filename
                        filename = os.path.basename(img_path)
                        if len(filename) > 10:
                            filename = filename[:7] + "..."
                        name_label = ttk.Label(img_frame, text=filename, font=('Arial', 8))
                        name_label.pack()
                
                if len(selected_images) > 5:
                    more_label = ttk.Label(thumb_frame, text=f"... and {len(selected_images)-5} more", 
                                         font=('Arial', 9), foreground='#7f8c8d')
                    more_label.pack(side="left", padx=10, anchor="center")
            
            # Pause info (except for last post)
            if i < max_posts - 1:
                pause_label = ttk.Label(post_frame, text=f"⏳ Then pause: {min_pause}-{max_pause} seconds", 
                                      font=('Arial', 9), foreground='#7f8c8d')
                pause_label.pack(anchor="w", pady=(10, 0))
        
        if max_posts > 10:
            more_label = ttk.Label(scrollable_frame, text=f"... and {max_posts-10} more posts", 
                                 font=('Arial', 12), foreground='#7f8c8d')
            more_label.pack(pady=20)
        
        # Bind mousewheel to canvas
        def on_mousewheel(event):
            canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
        
        canvas.bind("<MouseWheel>", on_mousewheel)
        preview_window.bind("<MouseWheel>", on_mousewheel)
    
    def get_subreddits(self):
        """Get list of subreddits from entry fields"""
        subreddits = []
        for entry_var in self.subreddit_entries:
            value = entry_var.get().strip()
            if value:
                # Remove 'r/' prefix if user added it
                if value.startswith('r/'):
                    value = value[2:]
                subreddits.append(value)
        return subreddits
    
    def get_titles(self):
        """Get list of titles from entry fields"""
        titles = []
        for entry_var in self.title_entries:
            value = entry_var.get().strip()
            if value:
                titles.append(value)
        return titles
    
    def start_posting(self):
        """Start the posting process"""
        # Validate inputs
        if not self.validate_inputs():
            return
        
        # Clear the activity log for a fresh start
        if hasattr(self, 'log_text'):
            self.log_text.delete("1.0", tk.END)
        
        self.is_posting = True
        self.start_btn.config(state="disabled")
        self.stop_btn.config(state="normal")
        
        self.log("🚀 Starting posting process...")
        
        # Start posting thread
        self.posting_thread = threading.Thread(target=self.posting_worker, daemon=True)
        self.posting_thread.start()
    
    def stop_posting(self):
        """Stop the posting process"""
        self.is_posting = False
        self.start_btn.config(state="normal")
        self.stop_btn.config(state="disabled")
        self.update_status("Stopping... (will finish current post)")
    def bind_mousewheel(self, canvas):
        """Bind mouse wheel events to canvas for scrolling"""
        def on_mousewheel(event):
            # Determine which canvas the mouse is over
            widget = event.widget
            # Find the canvas that contains this widget
            while widget and not isinstance(widget, tk.Canvas):
                widget = widget.master
            
            if widget:
                widget.yview_scroll(int(-1 * (event.delta / 120)), "units")
        
        def bind_to_mousewheel(event):
            canvas.bind_all("<MouseWheel>", on_mousewheel)
            canvas.bind_all("<Button-4>", lambda e: canvas.yview_scroll(-1, "units"))
            canvas.bind_all("<Button-5>", lambda e: canvas.yview_scroll(1, "units"))
        
        def unbind_from_mousewheel(event):
            canvas.unbind_all("<MouseWheel>")
            canvas.unbind_all("<Button-4>")
            canvas.unbind_all("<Button-5>")
        
        canvas.bind('<Enter>', bind_to_mousewheel)
        canvas.bind('<Leave>', unbind_from_mousewheel)
    
    def validate_inputs(self):
        """Validate all inputs"""
        if not all([self.client_id_var.get(), self.client_secret_var.get(), 
                   self.username_var.get(), self.password_var.get()]):
            messagebox.showerror("Error", "Please fill in all Reddit API credentials")
            return False
        
        if not self.get_subreddits():
            messagebox.showerror("Error", "Please add at least one subreddit")
            return False
        
        if not self.get_titles():
            messagebox.showerror("Error", "Please add at least one title")
            return False
        
        if not self.image_gallery:
            messagebox.showerror("Error", "Please add images to the gallery")
            return False
        
        # Validate numeric inputs
        try:
            pause_time = int(self.pause_var.get())
            variance = int(self.random_variance_var.get())
            images_per_post = int(self.images_per_post_var.get())
            
            if pause_time < 5:
                messagebox.showerror("Error", "Base pause time must be at least 5 seconds")
                return False
            
            if variance < 0:
                messagebox.showerror("Error", "Random variance cannot be negative")
                return False
                
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numbers for pause time and variance")
            return False
        
        images_needed = int(self.images_per_post_var.get())
        if len(self.image_gallery) < images_needed:
            messagebox.showerror("Error", f"Need at least {images_needed} images in gallery")
            return False
        
        return True
    
    def posting_worker(self):
        """Main posting worker thread"""
        try:
            # Authenticate
            if not self.bot.authenticate(
                self.client_id_var.get(),
                self.client_secret_var.get(),
                self.username_var.get(),
                self.password_var.get()
            ):
                self.log("❌ Authentication failed")
                return
            
            subreddits = self.get_subreddits()
            titles = self.get_titles()
            
            max_posts = min(len(subreddits), len(titles))
            
            # Initialize progress
            self.root.after(0, lambda: self.progress.config(maximum=max_posts))
            
            successful_posts = 0
            failed_posts = 0
            
            for i in range(max_posts):
                if not self.is_posting:
                    break
                
                subreddit = subreddits[i]
                title = titles[i]
                
                # Select random images
                images_per_post = self.get_images_per_post()
                selected_images = random.sample(self.image_gallery, min(images_per_post, len(self.image_gallery)))
                
                self.root.after(0, lambda i=i, sub=subreddit: self.current_action_label.config(
                    text=f"Posting to r/{sub} ({i+1}/{max_posts})"))
                
                try:
                    # Post to Reddit
                    post_url = self.bot.post_images(subreddit, title, selected_images)
                    
                    if post_url:
                        successful_posts += 1
                        self.log(f"✅ Posted to r/{subreddit}: {title}")
                        self.log(f"   URL: {post_url}")
                        self.log(f"   Images: {[os.path.basename(img) for img in selected_images]}")
                    else:
                        failed_posts += 1
                        self.log(f"❌ Failed to post to r/{subreddit}")
                
                except Exception as e:
                    failed_posts += 1
                    self.log(f"❌ Error posting to r/{subreddit}: {str(e)}")
                
                # Update progress
                self.root.after(0, lambda: self.progress.config(value=i+1))
                self.root.after(0, lambda: self.update_stats(successful_posts, failed_posts, i+1, max_posts))
                
                # Pause before next post (except for last post)
                if i < max_posts - 1 and self.is_posting:
                    pause_time = self.calculate_pause_time()
                    self.log(f"⏳ Pausing for {pause_time} seconds...")
                    for remaining in range(pause_time, 0, -1):
                        if not self.is_posting:
                            break
                        self.root.after(0, lambda r=remaining: self.current_action_label.config(
                            text=f"Pausing... {r} seconds remaining"))
                        time.sleep(1)
            
            # Final status
            if self.is_posting:
                self.log("🎉 All posts completed!")
                self.root.after(0, lambda: self.update_status("Completed successfully"))
            else:
                self.log("⏹ Posting stopped by user")
                self.root.after(0, lambda: self.update_status("Stopped by user"))
        
        except Exception as e:
            self.log(f"💥 Unexpected error: {str(e)}")
        
        finally:
            self.root.after(0, lambda: self.current_action_label.config(text=""))
            self.root.after(0, lambda: self.start_btn.config(state="normal"))
            self.root.after(0, lambda: self.stop_btn.config(state="disabled"))
            self.is_posting = False
    
    def update_status(self, message):
        """Update status label with appropriate color"""
        self.status_label.config(text=message)
        
        # Set color based on message content
        if "success" in message.lower() or "completed" in message.lower():
            self.status_label.config(foreground='#27ae60')  # Green
        elif "error" in message.lower() or "failed" in message.lower():
            self.status_label.config(foreground='#e74c3c')  # Red
        elif "posting" in message.lower() or "running" in message.lower():
            self.status_label.config(foreground='#f39c12')  # Orange
        elif "stopped" in message.lower() or "stopping" in message.lower():
            self.status_label.config(foreground='#8e44ad')  # Purple
        else:
            self.status_label.config(foreground='#2980b9')  # Blue
    
    def update_stats(self, successful, failed, completed, total):
        """Update statistics display"""
        success_rate = (successful/(successful+failed)*100) if (successful+failed) > 0 else 0
        
        stats = f"""📊 Posts Completed: {completed}/{total}
✅ Successful: {successful}
❌ Failed: {failed}
📈 Success Rate: {success_rate:.1f}%
⏰ Current Time: {datetime.now().strftime('%H:%M:%S')}"""
        
        self.stats_text.config(state="normal")
        self.stats_text.delete("1.0", tk.END)
        self.stats_text.insert("1.0", stats)
        self.stats_text.config(state="disabled")
    
    def log(self, message):
        """Add message to log"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        log_entry = f"[{timestamp}] {message}\\n"
        
        self.root.after(0, lambda: self.log_text.insert(tk.END, log_entry))
        self.root.after(0, lambda: self.log_text.see(tk.END))
    
    def update_pause_range(self, *args):
        """Update the pause range display"""
        try:
            base_pause = int(self.pause_var.get())
            variance = int(self.random_variance_var.get())
            min_pause = max(5, base_pause - variance)  # Minimum 5 seconds
            max_pause = base_pause + variance
            self.pause_range_label.config(text=f"Actual pause will be: {min_pause}-{max_pause} seconds")
        except ValueError:
            self.pause_range_label.config(text="Invalid values entered")
    
    def calculate_pause_time(self):
        """Calculate randomized pause time with human-like behavior"""
        try:
            base_pause = int(self.pause_var.get())
            variance = int(self.random_variance_var.get())
            
            if self.human_like_var.get():
                # Human-like randomization with weighted distribution
                # More likely to be close to base time
                random_factor = random.triangular(-variance, variance, 0)
                pause_time = base_pause + random_factor
            else:
                # Simple uniform distribution
                pause_time = random.randint(max(5, base_pause - variance), base_pause + variance)
            
            return max(5, int(pause_time))  # Minimum 5 seconds
        except ValueError:
            return 60  # Default fallback
    
    def get_images_per_post(self):
        """Get number of images per post with optional randomization"""
        base_count = int(self.images_per_post_var.get())
        
        if self.random_images_var.get():
            # Randomize between 1 and the set maximum
            return random.randint(1, base_count)
        
        return base_count
    
    def add_subreddit_entry(self, initial_value=""):
        """Add a new subreddit entry field"""
        entry_frame = ttk.Frame(self.subreddits_frame)
        entry_frame.pack(fill="x", pady=2)
        
        # r/ prefix label
        ttk.Label(entry_frame, text="r/", font=('Arial', 10, 'bold'), 
                 foreground='#e74c3c').pack(side="left", padx=(0, 5))
        
        # Entry field
        entry_var = tk.StringVar(value=initial_value)
        entry = ttk.Entry(entry_frame, textvariable=entry_var, font=('Arial', 10))
        entry.pack(side="left", fill="x", expand=True, padx=(0, 10))
        
        # Remove button
        remove_btn = ttk.Button(entry_frame, text="❌", width=3,
                               command=lambda: self.remove_subreddit_entry(entry_frame, entry_var))
        remove_btn.pack(side="right")
        
        self.subreddit_entries.append(entry_var)
        
        # Focus on the new entry if it's empty
        if not initial_value:
            entry.focus()
    
    def remove_subreddit_entry(self, frame, entry_var):
        """Remove a subreddit entry"""
        if len(self.subreddit_entries) > 1:  # Keep at least one entry
            self.subreddit_entries.remove(entry_var)
            frame.destroy()
        else:
            messagebox.showwarning("Warning", "At least one subreddit entry must remain")
    
    def clear_subreddits(self):
        """Clear all subreddit entries and add one empty entry"""
        for widget in self.subreddits_frame.winfo_children():
            widget.destroy()
        self.subreddit_entries.clear()
        self.add_subreddit_entry()
    
    def add_title_entry(self, initial_value=""):
        """Add a new title entry field"""
        entry_frame = ttk.Frame(self.titles_frame)
        entry_frame.pack(fill="x", pady=2)
        
        # Entry field
        entry_var = tk.StringVar(value=initial_value)
        entry = ttk.Entry(entry_frame, textvariable=entry_var, font=('Arial', 10))
        entry.pack(side="left", fill="x", expand=True, padx=(0, 10))
        
        # Remove button
        remove_btn = ttk.Button(entry_frame, text="❌", width=3,
                               command=lambda: self.remove_title_entry(entry_frame, entry_var))
        remove_btn.pack(side="right")
        
        self.title_entries.append(entry_var)
        
        # Focus on the new entry if it's empty
        if not initial_value:
            entry.focus()
    
    def remove_title_entry(self, frame, entry_var):
        """Remove a title entry"""
        if len(self.title_entries) > 1:  # Keep at least one entry
            self.title_entries.remove(entry_var)
            frame.destroy()
        else:
            messagebox.showwarning("Warning", "At least one title entry must remain")
    
    def clear_titles(self):
        """Clear all title entries and add one empty entry"""
        for widget in self.titles_frame.winfo_children():
            widget.destroy()
        self.title_entries.clear()
        self.add_title_entry()
    
    def create_thumbnail(self, image_path, size=(100, 100)):
        """Create a thumbnail for an image"""
        try:
            with Image.open(image_path) as img:
                # Convert to RGB if necessary (for PNG with transparency)
                if img.mode in ('RGBA', 'LA', 'P'):
                    background = Image.new('RGB', img.size, (255, 255, 255))
                    if img.mode == 'P':
                        img = img.convert('RGBA')
                    background.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
                    img = background
                
                # Calculate aspect ratio and resize
                img.thumbnail(size, Image.Resampling.LANCZOS)
                
                # Create a white background and center the image
                background = Image.new('RGB', size, (255, 255, 255))
                x = (size[0] - img.size[0]) // 2
                y = (size[1] - img.size[1]) // 2
                background.paste(img, (x, y))
                
                return ImageTk.PhotoImage(background)
        except Exception as e:
            print(f"Error creating thumbnail for {image_path}: {e}")
            return None
    
    def update_gallery_display(self):
        """Update gallery display with thumbnails"""
        # Clear existing thumbnails
        for widget in self.gallery_scrollable_frame.winfo_children():
            widget.destroy()
        self.image_thumbnails.clear()
        
        count = len(self.image_gallery)
        if count == 0:
            self.gallery_status_label.config(text="No images in gallery", foreground='#7f8c8d')
            return
        
        self.gallery_status_label.config(text=f"📸 {count} images in gallery", foreground='#27ae60')
        
        # Create thumbnails in a grid
        for i, image_path in enumerate(self.image_gallery):
            # Create frame for each thumbnail
            thumb_frame = ttk.Frame(self.gallery_scrollable_frame, relief='solid', borderwidth=1)
            thumb_frame.pack(side="left", padx=5, pady=5)
            
            # Create thumbnail
            thumbnail = self.create_thumbnail(image_path, (80, 80))
            if thumbnail:
                self.image_thumbnails.append(thumbnail) # Keep reference
                
                # Image label
                img_label = tk.Label(thumb_frame, image=thumbnail, bg='white')
                img_label.pack(padx=2, pady=2)
                
                # Filename label (truncated)
                filename = os.path.basename(image_path)
                if len(filename) > 12:
                    filename = filename[:9] + "..."
                
                name_label = ttk.Label(thumb_frame, text=filename, font=('Arial', 8))
                name_label.pack()
                
                # Remove button
                remove_btn = ttk.Button(thumb_frame, text="❌", width=3,
                                      command=lambda path=image_path: self.remove_image(path))
                remove_btn.pack(pady=(2, 2))
        
        # Update canvas scroll region
        self.gallery_canvas.update_idletasks()
        self.gallery_canvas.configure(scrollregion=self.gallery_canvas.bbox("all"))
    
    def remove_image(self, image_path):
        """Remove an image from the gallery"""
        if image_path in self.image_gallery:
            self.image_gallery.remove(image_path)
            self.update_gallery_display()
            self.log(f"Removed image: {os.path.basename(image_path)}")
    
    def clear_log(self):
        """Clear the activity log"""
        self.log_text.delete("1.0", tk.END)
        self.log("🧹 Log cleared")


# Run the application
if __name__ == "__main__":
    root = tk.Tk()
    app = RedditBotDashboard(root)
    root.mainloop()