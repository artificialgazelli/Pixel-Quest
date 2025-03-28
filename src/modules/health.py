"""
Health check module for the Pixel Quest application.
Handles daily health check functionality.
"""

import tkinter as tk
from tkinter import messagebox
from datetime import datetime

class HealthCheckModule:
    """
    Manages the health check functionality.
    """
    
    def __init__(self, app, data_manager, theme):
        """
        Initialize the health check module.
        
        Args:
            app: Main application instance
            data_manager: Data manager instance
            theme: Theme manager instance
        """
        self.app = app
        self.data_manager = data_manager
        self.data = data_manager.data
        self.theme = theme
        
    def do_health_check(self):
        """Daily health check dialog with pixel art styling."""
        health_window = tk.Toplevel(self.app.root)
        health_window.title("Daily Health Check")
        health_window.geometry("400x300")
        health_window.configure(bg=self.theme.bg_color)

        # Center the window
        health_window.transient(self.app.root)
        health_window.grab_set()

        tk.Label(
            health_window,
            text="Daily Health Check",
            font=self.theme.pixel_font,
            bg=self.theme.bg_color,
            fg=self.theme.text_color,
        ).pack(pady=10)

        # Health questions frame with pixel styling
        questions_frame = tk.Frame(
            health_window, bg=self.theme.bg_color, relief=tk.RIDGE, bd=3
        )
        questions_frame.pack(pady=10, fill=tk.X, padx=20)

        # Variables to store responses
        self.eating_well = tk.BooleanVar(value=True)
        self.exercised = tk.BooleanVar(value=True)
        self.mental_health = tk.BooleanVar(value=True)

        # Questions with pixel styling
        tk.Checkbutton(
            questions_frame,
            text="I ate well today",
            variable=self.eating_well,
            bg=self.theme.bg_color,
            fg=self.theme.text_color,
            font=self.theme.small_font,
            selectcolor=self.theme.secondary_color,
        ).grid(row=0, column=0, sticky="w", pady=5)

        tk.Checkbutton(
            questions_frame,
            text="I exercised or moved my body today",
            variable=self.exercised,
            bg=self.theme.bg_color,
            fg=self.theme.text_color,
            font=self.theme.small_font,
            selectcolor=self.theme.secondary_color,
        ).grid(row=1, column=0, sticky="w", pady=5)

        tk.Checkbutton(
            questions_frame,
            text="I took care of my mental health today",
            variable=self.mental_health,
            bg=self.theme.bg_color,
            fg=self.theme.text_color,
            font=self.theme.small_font,
            selectcolor=self.theme.secondary_color,
        ).grid(row=2, column=0, sticky="w", pady=5)

        # Submit button with pixel styling
        submit_button = self.theme.create_pixel_button(
            health_window,
            "Submit",
            lambda: self.submit_health_check(health_window),
            color="#673AB7",
        )
        submit_button.pack(pady=20)
        
    def submit_health_check(self, window):
        """
        Process health check submission.
        
        Args:
            window: The health check window to close after submission
        """
        # Health status is True if all checks are True
        health_status = (
            self.eating_well.get() and self.exercised.get() and self.mental_health.get()
        )

        # Update health status in data
        self.data["health_status"] = health_status
        self.data["last_health_check"] = datetime.now().strftime("%Y-%m-%d")

        # Display result
        if health_status:
            messagebox.showinfo(
                "Health Check",
                "Great job taking care of yourself today! You can earn points in your quests.",
            )
        else:
            messagebox.showinfo(
                "Health Check",
                "Remember that health is important for your journey. No points can be earned until you complete your health checks.",
            )

        # Save data and refresh
        self.data_manager.save_data()
        window.destroy()
        self.app.show_main_menu()
