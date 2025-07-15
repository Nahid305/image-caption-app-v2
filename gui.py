import customtkinter as ctk
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
from auth import login, signup
from model import generate_caption
from tts import speak
from history import save_caption, load_captions
from voice_input import listen_for_command
from webcam import capture_image
from customtkinter import CTkImage, CTkFont
from googletrans import Translator
import os
import time
from datetime import datetime

# Set appearance and theme
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")  # Modern blue theme

translator = Translator()

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("VisionSpeak Pro - AI Image Caption Generator")
        self.geometry("1100x800")
        self.minsize(1000, 700)
        
        # Custom fonts
        self.title_font = CTkFont(family="Roboto", size=26, weight="bold")
        self.subtitle_font = CTkFont(family="Roboto", size=16)
        self.button_font = CTkFont(family="Roboto", size=14, weight="bold")
        self.caption_font = CTkFont(family="Roboto", size=14)
        self.history_font = CTkFont(family="Roboto", size=13)

        self.user_logged_in = False
        self.image_path = None
        self.language_code = "en"
        self.current_theme = "dark"

        # Configure grid layout
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.create_login_screen()

    def create_login_screen(self):
        # Main login container with gradient background
        self.login_frame = ctk.CTkFrame(
            self, 
            corner_radius=20,
            border_width=2,
            border_color="#3A7EBF"
        )
        self.login_frame.pack(expand=True, padx=50, pady=50, fill="both")
        
        # Header section with logo
        header_frame = ctk.CTkFrame(self.login_frame, fg_color="transparent")
        header_frame.pack(pady=(40, 20))
        
        # App logo and title
        logo_label = ctk.CTkLabel(
            header_frame, 
            text="👁️🗨️", 
            font=CTkFont(size=50),
            text_color="#3A7EBF"
        )
        logo_label.pack()
        
        ctk.CTkLabel(
            header_frame, 
            text="VisionSpeak Pro", 
            font=self.title_font
        ).pack(pady=(10, 0))
        
        ctk.CTkLabel(
            header_frame, 
            text="AI-Powered Image Understanding", 
            font=self.subtitle_font,
            text_color="gray70"
        ).pack()

        # Login form
        form_frame = ctk.CTkFrame(self.login_frame, fg_color="transparent")
        form_frame.pack(pady=30, padx=50, fill="x")
        
        # Username field with icon
        username_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        username_frame.pack(pady=10, fill="x")
        
        ctk.CTkLabel(
            username_frame,
            text="👤",
            font=CTkFont(size=16)
        ).pack(side="left", padx=(0, 10))
        
        self.username = ctk.CTkEntry(
            username_frame, 
            placeholder_text="Username",
            height=45,
            corner_radius=10,
            font=self.subtitle_font,
            border_color="#3A7EBF"
        )
        self.username.pack(side="left", expand=True, fill="x")
        
        # Password field with icon
        password_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        password_frame.pack(pady=10, fill="x")
        
        ctk.CTkLabel(
            password_frame,
            text="🔒",
            font=CTkFont(size=16)
        ).pack(side="left", padx=(0, 10))
        
        self.password = ctk.CTkEntry(
            password_frame, 
            placeholder_text="Password", 
            show="*",
            height=45,
            corner_radius=10,
            font=self.subtitle_font,
            border_color="#3A7EBF"
        )
        self.password.pack(side="left", expand=True, fill="x")
        
        # Action buttons
        button_frame = ctk.CTkFrame(self.login_frame, fg_color="transparent")
        button_frame.pack(pady=20)
        
        login_button = ctk.CTkButton(
            button_frame,
            text="Login",
            command=self.try_login,
            height=45,
            width=150,
            font=self.button_font,
            corner_radius=10,
            fg_color="#3A7EBF",
            hover_color="#2D5F8B"
        )
        login_button.pack(pady=10, ipadx=10)
        
        signup_button = ctk.CTkButton(
            button_frame,
            text="Create Account",
            command=self.try_signup,
            height=45,
            width=150,
            font=self.button_font,
            corner_radius=10,
            fg_color="transparent",
            border_width=2,
            border_color="#3A7EBF",
            hover_color="#2E2E2E",
            text_color="#3A7EBF"
        )
        signup_button.pack(pady=(0, 20), ipadx=10)
        
        # Footer note
        ctk.CTkLabel(
            self.login_frame,
            text="© 2023 VisionSpeak Pro | AI Image Caption Generator",
            font=CTkFont(size=12),
            text_color="gray60"
        ).pack(side="bottom", pady=10)

    def try_login(self):
        user = self.username.get()
        pwd = self.password.get()
        
        # Show loading indicator
        loading = ctk.CTkLabel(
            self.login_frame, 
            text="🔐 Authenticating...", 
            font=self.subtitle_font
        )
        loading.pack(pady=10)
        self.update()
        
        if login(user, pwd):
            loading.destroy()
            self.login_frame.pack_forget()
            self.user_logged_in = True
            self.create_main_app()
        else:
            loading.destroy()
            messagebox.showerror("Login Failed", "Invalid username or password")

    def try_signup(self):
        user = self.username.get()
        pwd = self.password.get()
        
        if signup(user, pwd):
            messagebox.showinfo("Account Created", "Your account has been successfully created!")
        else:
            messagebox.showerror("Signup Failed", "Username already exists or invalid credentials")

    def create_main_app(self):
        # Main container with shadow effect
        self.main_container = ctk.CTkFrame(
            self, 
            corner_radius=20,
            border_width=2,
            border_color="#3A7EBF"
        )
        self.main_container.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Create header with user info
        self.create_app_header()
        
        # Create tabview with custom styling
        self.tabs = ctk.CTkTabview(
            self.main_container,
            segmented_button_fg_color="#2E2E2E",
            segmented_button_selected_color="#3A7EBF",
            segmented_button_selected_hover_color="#2D5F8B",
            corner_radius=10,
            height=600
        )
        self.tabs.pack(fill="both", expand=True, padx=5, pady=(0, 5))
        
        # Create application tabs
        self.create_home_tab()
        self.create_voice_tab()
        self.create_webcam_tab()
        self.create_history_tab()
        self.create_settings_tab()

    def create_app_header(self):
        header_frame = ctk.CTkFrame(
            self.main_container, 
            fg_color="transparent",
            height=60
        )
        header_frame.pack(fill="x", padx=10, pady=10)
        
        # App title
        ctk.CTkLabel(
            header_frame,
            text="👁️🗨️ VisionSpeak Pro",
            font=self.title_font,
            text_color="#3A7EBF"
        ).pack(side="left", padx=10)
        
        # User info and logout button
        user_frame = ctk.CTkFrame(header_frame, fg_color="transparent")
        user_frame.pack(side="right", padx=10)
        
        ctk.CTkLabel(
            user_frame,
            text=f"👤 {self.username.get()}",
            font=self.subtitle_font
        ).pack(side="left", padx=(0, 10))
        
        logout_btn = ctk.CTkButton(
            user_frame,
            text="Logout",
            command=self.logout,
            width=80,
            height=30,
            font=self.subtitle_font,
            fg_color="transparent",
            border_width=1,
            border_color="#FF6B6B",
            hover_color="#2E2E2E",
            text_color="#FF6B6B"
        )
        logout_btn.pack(side="left")

    def create_home_tab(self):
        self.tab_home = self.tabs.add(" 🏠 Home ")
        
        # Configure grid layout
        self.tab_home.grid_columnconfigure(0, weight=1)
        self.tab_home.grid_rowconfigure(1, weight=1)
        
        # Header
        header_frame = ctk.CTkFrame(self.tab_home, fg_color="transparent")
        header_frame.grid(row=0, column=0, pady=(10, 20), sticky="ew")
        
        ctk.CTkLabel(
            header_frame,
            text="Image Caption Generator",
            font=self.title_font
        ).pack(side="left", padx=10)
        
        # Main content
        content_frame = ctk.CTkFrame(self.tab_home, fg_color="transparent")
        content_frame.grid(row=1, column=0, sticky="nsew", padx=20, pady=10)
        content_frame.grid_columnconfigure(0, weight=1)
        
        # Upload button with modern styling
        self.upload_button = ctk.CTkButton(
            content_frame,
            text="📁 Upload Image",
            command=self.upload_image,
            height=50,
            font=self.button_font,
            fg_color="#3A7EBF",
            hover_color="#2D5F8B",
            corner_radius=10,
            border_width=2,
            border_color="#3A7EBF"
        )
        self.upload_button.grid(row=0, column=0, pady=20, sticky="ew")
        
        # Image display area with modern styling
        self.image_container = ctk.CTkFrame(
            content_frame,
            corner_radius=15,
            border_width=2,
            border_color="gray30",
            fg_color="gray20"
        )
        self.image_container.grid(row=1, column=0, pady=10, sticky="nsew")
        
        self.image_label = ctk.CTkLabel(
            self.image_container,
            text="No image selected",
            font=self.subtitle_font,
            text_color="gray60"
        )
        self.image_label.pack(expand=True, padx=20, pady=20)
        
        # Caption area with modern styling
        caption_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        caption_frame.grid(row=2, column=0, sticky="ew", pady=(20, 10))
        
        ctk.CTkLabel(
            caption_frame,
            text="AI-Generated Caption:",
            font=self.subtitle_font
        ).pack(anchor="w", pady=(0, 5))
        
        self.caption_textbox = ctk.CTkTextbox(
            caption_frame,
            height=120,
            font=self.caption_font,
            wrap="word",
            corner_radius=10,
            border_width=2,
            border_color="gray30",
            fg_color="gray20"
        )
        self.caption_textbox.pack(fill="x", pady=(0, 10))
        self.caption_textbox.insert("0.0", "Your image caption will appear here...")
        
        # Action buttons with modern styling
        button_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        button_frame.grid(row=3, column=0, sticky="ew", pady=(0, 20))
        button_frame.grid_columnconfigure(0, weight=1)
        button_frame.grid_columnconfigure(1, weight=1)
        
        self.speak_button = ctk.CTkButton(
            button_frame,
            text="🔊 Speak Caption",
            command=self.speak_caption,
            height=45,
            font=self.button_font,
            fg_color="#3A7EBF",
            hover_color="#2D5F8B",
            corner_radius=10
        )
        self.speak_button.grid(row=0, column=0, padx=5, sticky="ew")
        
        self.copy_button = ctk.CTkButton(
            button_frame,
            text="⎘ Copy Caption",
            command=self.copy_caption,
            height=45,
            font=self.button_font,
            fg_color="transparent",
            border_width=2,
            border_color="#3A7EBF",
            hover_color="#2E2E2E",
            corner_radius=10
        )
        self.copy_button.grid(row=0, column=1, padx=5, sticky="ew")

    def create_voice_tab(self):
        self.tab_voice = self.tabs.add(" 🎤 Voice ")
        
        content_frame = ctk.CTkFrame(self.tab_voice, fg_color="transparent")
        content_frame.pack(expand=True, fill="both", padx=20, pady=20)
        
        # Header
        ctk.CTkLabel(
            content_frame,
            text="Voice Command Upload",
            font=self.title_font
        ).pack(pady=(10, 20))
        
        # Description
        ctk.CTkLabel(
            content_frame,
            text="Use your voice to select an image for captioning:",
            font=self.subtitle_font,
            text_color="gray70"
        ).pack(pady=(0, 30))
        
        # Voice command button with animation
        self.voice_button = ctk.CTkButton(
            content_frame,
            text="🎤  Start Listening",
            command=self.voice_upload,
            height=70,
            width=350,
            font=self.button_font,
            fg_color="#FF6B6B",
            hover_color="#E05555",
            corner_radius=15,
            border_width=2,
            border_color="#FF6B6B"
        )
        self.voice_button.pack(pady=30)
        
        # Instructions panel
        instructions_frame = ctk.CTkFrame(
            content_frame,
            corner_radius=15,
            border_width=2,
            border_color="gray30"
        )
        instructions_frame.pack(fill="x", pady=20)
        
        ctk.CTkLabel(
            instructions_frame,
            text="How to use voice commands:",
            font=self.subtitle_font,
            text_color="#3A7EBF"
        ).pack(anchor="w", padx=20, pady=(15, 5))
        
        instructions_text = ctk.CTkTextbox(
            instructions_frame,
            height=120,
            font=self.subtitle_font,
            wrap="word",
            fg_color="transparent",
            border_width=0
        )
        instructions_text.pack(fill="x", padx=10, pady=(0, 15))
        instructions_text.insert("0.0", "1. Click the microphone button\n2. Clearly say the name of an image file in this directory\n3. Example: 'beach sunset.jpg'\n\nNote: The file must be in the current working directory")
        instructions_text.configure(state="disabled")

    def create_webcam_tab(self):
        self.tab_webcam = self.tabs.add(" 📷 Webcam ")
        
        content_frame = ctk.CTkFrame(self.tab_webcam, fg_color="transparent")
        content_frame.pack(expand=True, fill="both", padx=20, pady=20)
        
        # Header
        ctk.CTkLabel(
            content_frame,
            text="Webcam Capture",
            font=self.title_font
        ).pack(pady=(10, 20))
        
        # Description
        ctk.CTkLabel(
            content_frame,
            text="Capture an image directly from your webcam:",
            font=self.subtitle_font,
            text_color="gray70"
        ).pack(pady=(0, 30))
        
        # Webcam button with modern styling
        self.webcam_button = ctk.CTkButton(
            content_frame,
            text="📷  Capture Image",
            command=self.capture_from_webcam,
            height=70,
            width=350,
            font=self.button_font,
            fg_color="#6B66FF",
            hover_color="#554FE0",
            corner_radius=15,
            border_width=2,
            border_color="#6B66FF"
        )
        self.webcam_button.pack(pady=20)
        
        # Preview frame with modern styling
        self.webcam_preview = ctk.CTkLabel(
            content_frame,
            text="Captured image will appear here",
            font=self.subtitle_font,
            text_color="gray60",
            corner_radius=15,
            fg_color="gray20",
            width=400,
            height=300
        )
        self.webcam_preview.pack(pady=20)

    def create_history_tab(self):
        self.tab_history = self.tabs.add(" 📜 History ")
        
        # Header with title and refresh button
        header_frame = ctk.CTkFrame(self.tab_history, fg_color="transparent")
        header_frame.pack(fill="x", padx=20, pady=10)
        
        ctk.CTkLabel(
            header_frame,
            text="Caption History",
            font=self.title_font
        ).pack(side="left")
        
        # Refresh button with modern styling
        refresh_button = ctk.CTkButton(
            header_frame,
            text="🔄 Refresh",
            command=self.load_history,
            width=100,
            height=30,
            font=self.subtitle_font,
            fg_color="transparent",
            border_width=1,
            border_color="gray50",
            hover_color="#2E2E2E"
        )
        refresh_button.pack(side="right")
        
        # History content in scrollable frame
        self.history_scroll = ctk.CTkScrollableFrame(
            self.tab_history,
            fg_color="transparent"
        )
        self.history_scroll.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        # History text widget with custom styling
        self.history_content = ctk.CTkTextbox(
            self.history_scroll,
            wrap="word",
            font=self.history_font,
            fg_color="transparent",
            height=500
        )
        self.history_content.pack(fill="both", expand=True)
        
        # Initial load of history
        self.load_history()

    def create_settings_tab(self):
        self.tab_settings = self.tabs.add(" ⚙️ Settings ")
        
        content_frame = ctk.CTkFrame(self.tab_settings, fg_color="transparent")
        content_frame.pack(expand=True, fill="both", padx=20, pady=20)
        
        # Header
        ctk.CTkLabel(
            content_frame,
            text="Application Settings",
            font=self.title_font
        ).pack(pady=(10, 30))
        
        # Language settings section
        lang_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        lang_frame.pack(fill="x", pady=10)
        
        ctk.CTkLabel(
            lang_frame,
            text="Caption Language:",
            font=self.subtitle_font
        ).pack(anchor="w", pady=5)
        
        self.lang_dropdown = ctk.CTkOptionMenu(
            lang_frame,
            values=["English (en)", "Hindi (hi)", "French (fr)", "German (de)", "Spanish (es)"],
            command=self.set_language,
            font=self.subtitle_font,
            dropdown_font=self.subtitle_font,
            fg_color="#2E2E2E",
            button_color="#3A7EBF",
            button_hover_color="#2D5F8B",
            corner_radius=8,
            width=200
        )
        self.lang_dropdown.set("English (en)")
        self.lang_dropdown.pack(fill="x", pady=5)
        
        # Theme settings section
        theme_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        theme_frame.pack(fill="x", pady=20)
        
        ctk.CTkLabel(
            theme_frame,
            text="Appearance:",
            font=self.subtitle_font
        ).pack(anchor="w", pady=5)
        
        theme_button_frame = ctk.CTkFrame(theme_frame, fg_color="transparent")
        theme_button_frame.pack(fill="x", pady=10)
        
        # Theme buttons with modern styling
        ctk.CTkButton(
            theme_button_frame,
            text="🌞 Light Mode",
            command=lambda: self.change_theme("light"),
            height=45,
            font=self.button_font,
            fg_color="#FFD166",
            hover_color="#EEBC51",
            corner_radius=10
        ).pack(side="left", expand=True, padx=5)
        
        ctk.CTkButton(
            theme_button_frame,
            text="🌙 Dark Mode",
            command=lambda: self.change_theme("dark"),
            height=45,
            font=self.button_font,
            fg_color="#3A7EBF",
            hover_color="#2D5F8B",
            corner_radius=10
        ).pack(side="left", expand=True, padx=5)
        
        ctk.CTkButton(
            theme_button_frame,
            text="🌓 System Default",
            command=lambda: self.change_theme("system"),
            height=45,
            font=self.button_font,
            fg_color="transparent",
            border_width=2,
            border_color="#3A7EBF",
            hover_color="#2E2E2E",
            corner_radius=10
        ).pack(side="left", expand=True, padx=5)
        
        # About section
        about_frame = ctk.CTkFrame(
            content_frame,
            fg_color="transparent",
            corner_radius=15,
            border_width=2,
            border_color="gray30"
        )
        about_frame.pack(fill="x", pady=30)
        
        ctk.CTkLabel(
            about_frame,
            text="About VisionSpeak Pro",
            font=self.subtitle_font,
            text_color="#3A7EBF"
        ).pack(anchor="w", padx=20, pady=(15, 5))
        
        about_text = ctk.CTkTextbox(
            about_frame,
            height=100,
            font=self.subtitle_font,
            wrap="word",
            fg_color="transparent",
            border_width=0
        )
        about_text.pack(fill="x", padx=10, pady=(0, 15))
        about_text.insert("0.0", "Version 1.0.0\nDeveloped with Python, CustomTkinter, and AI technologies\n© 2023 VisionSpeak Pro - All rights reserved")
        about_text.configure(state="disabled")

    def upload_image(self, file_path=None):
        if not file_path:
            file_path = filedialog.askopenfilename(
                filetypes=[("Image Files", "*.jpg *.jpeg *.png *.bmp *.gif")]
            )
            if not file_path:
                return
        
        # Show loading state
        self.image_label.configure(text="🔄 Loading image...", text_color="gray70")
        self.caption_textbox.delete("0.0", "end")
        self.caption_textbox.insert("0.0", "Generating caption... Please wait.")
        self.update()
        
        try:
            self.image_path = file_path
            img = Image.open(file_path)
            img = img.resize((400, 300), Image.LANCZOS)
            img_ctk = CTkImage(light_image=img, size=(400, 300))
            
            # Update image display
            self.image_label.configure(image=img_ctk, text="")
            self.image_label.image = img_ctk
            
            # Generate caption
            caption = generate_caption(file_path)
            if self.language_code != "en":
                caption = translator.translate(caption, dest=self.language_code).text
            
            # Update caption with typing animation
            self.caption_textbox.delete("0.0", "end")
            self.typewriter_effect(self.caption_textbox, caption)
            
            # Save to history
            save_caption(file_path, caption)
            self.load_history()
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to process image: {str(e)}")
            self.image_label.configure(text="❌ Error loading image", text_color="#FF6B6B")

    def speak_caption(self):
        caption = self.caption_textbox.get("0.0", "end").strip()
        if caption and caption != "Your image caption will appear here...":
            # Show speaking indicator
            original_text = self.speak_button.cget("text")
            self.speak_button.configure(text="🔊 Speaking...", state="disabled")
            self.update()
            
            speak(caption, lang=self.language_code)
            
            # Restore button state
            self.speak_button.configure(text=original_text, state="normal")

    def copy_caption(self):
        caption = self.caption_textbox.get("0.0", "end").strip()
        if caption and caption != "Your image caption will appear here...":
            self.clipboard_clear()
            self.clipboard_append(caption)
            
            # Show copied notification
            original_text = self.copy_button.cget("text")
            self.copy_button.configure(text="✓ Copied!", fg_color="#4BB543")
            self.after(2000, lambda: self.copy_button.configure(
                text=original_text, 
                fg_color="transparent"
            ))

    def load_history(self):
        entries = load_captions()
        self.history_content.delete("0.0", "end")
        
        if not entries:
            self.history_content.insert("end", "No history entries yet.")
            return
        
        for row in entries:
            timestamp = datetime.strptime(row[0], "%Y-%m-%d %H:%M:%S").strftime("%b %d, %Y %I:%M %p")
            image_path = os.path.basename(row[1])
            caption = row[2]
            
            # Format history entry with colors
            self.history_content.insert("end", f"⏱️ {timestamp}\n", "timestamp")
            self.history_content.insert("end", f"📷 {image_path}\n", "path")
            self.history_content.insert("end", f"💬 {caption}\n\n", "caption")
            
        # Configure text colors
        self.history_content.tag_config("timestamp", foreground="#3A7EBF")
        self.history_content.tag_config("path", foreground="#FFD166")
        self.history_content.tag_config("caption", foreground="gray80")

    def voice_upload(self):
        # Show listening state
        original_text = self.voice_button.cget("text")
        self.voice_button.configure(
            text="🎤 Listening... Speak now",
            fg_color="#E05555",
            state="disabled"
        )
        self.update()
        
        file_name = listen_for_command().lower().strip()
        
        # Restore button state
        self.voice_button.configure(
            text=original_text,
            fg_color="#FF6B6B",
            state="normal"
        )
        self.update()
        
        if os.path.exists(file_name):
            self.upload_image(file_name)
        else:
            messagebox.showerror("File Not Found", f"'{file_name}' was not found in this folder.")

    def capture_from_webcam(self):
        # Show capturing state
        original_text = self.webcam_button.cget("text")
        self.webcam_button.configure(
            text="📷 Capturing...",
            fg_color="#554FE0",
            state="disabled"
        )
        self.webcam_preview.configure(text="", fg_color="gray20")
        self.update()
        
        file_path = capture_image()
        
        # Restore button state
        self.webcam_button.configure(
            text=original_text,
            fg_color="#6B66FF",
            state="normal"
        )
        
        if file_path:
            # Display preview
            img = Image.open(file_path)
            img = img.resize((400, 300), Image.LANCZOS)
            img_ctk = CTkImage(light_image=img, size=(400, 300))
            self.webcam_preview.configure(image=img_ctk)
            self.webcam_preview.image = img_ctk
            
            self.upload_image(file_path)

    def set_language(self, lang_option):
        # Extract language code from the option (e.g., "English (en)" -> "en")
        self.language_code = lang_option[-3:-1]
        
        # Show notification
        self.show_notification(f"Language set to {lang_option}")

    def change_theme(self, mode):
        ctk.set_appearance_mode(mode)
        self.current_theme = mode
        
        # Update UI elements that need theme-specific colors
        border_color = "gray70" if mode == "light" else "gray30"
        self.caption_textbox.configure(border_color=border_color)
        self.image_container.configure(border_color=border_color)
        
        self.show_notification(f"Theme changed to {mode.capitalize()} Mode")

    def typewriter_effect(self, widget, text, delay=30):
        widget.delete("0.0", "end")
        for i in range(len(text) + 1):
            widget.delete("0.0", "end")
            widget.insert("0.0", text[:i])
            self.update()
            time.sleep(delay/1000)

    def show_notification(self, message):
        # Create a temporary top-level window for notification
        notification = ctk.CTkToplevel(self)
        notification.geometry("300x80+{}+{}".format(
            self.winfo_x() + (self.winfo_width() // 2) - 150,
            self.winfo_y() + (self.winfo_height() // 2) - 40
        ))
        notification.overrideredirect(True)
        notification.attributes("-alpha", 0)
        notification.lift()
        
        # Notification frame
        frame = ctk.CTkFrame(
            notification,
            corner_radius=10,
            border_width=2,
            border_color="#3A7EBF"
        )
        frame.pack(fill="both", expand=True)
        
        ctk.CTkLabel(
            frame,
            text=message,
            font=self.subtitle_font
        ).pack(expand=True)
        
        # Fade in animation
        for i in range(0, 101, 5):
            notification.attributes("-alpha", i/100)
            notification.update()
            time.sleep(0.02)
        
        # Wait and fade out
        self.after(2000, lambda: self.fade_out(notification))

    def fade_out(self, window):
        for i in range(100, -1, -5):
            window.attributes("-alpha", i/100)
            window.update()
            time.sleep(0.02)
        window.destroy()

    def logout(self):
        self.main_container.pack_forget()
        self.user_logged_in = False
        self.create_login_screen()

if __name__ == "__main__":
    app = App()
    app.mainloop()