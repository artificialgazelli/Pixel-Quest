"""
Art module for the Pixel Quest application.
Handles art skill tracking and logging.
"""

import tkinter as tk
import random
from tkinter import ttk, messagebox
from datetime import datetime
from src.utils import update_streak, check_level_up, create_pixel_progress_bar


class ArtModule:
    """
    Manages the art module functionality.
    """

    def __init__(self, app, data_manager, theme):
        """
        Initialize the art module.

        Args:
            app: Main application instance
            data_manager: Data manager instance
            theme: Theme manager instance
        """
        self.app = app
        self.data_manager = data_manager
        self.data = data_manager.data
        self.theme = theme

    def show_module(self, parent_frame):
        """
        Show the art module interface.

        Args:
            parent_frame: Parent frame to place module content
        """
        # Title
        title_label = tk.Label(
            parent_frame,
            text="ART QUEST",
            font=self.theme.heading_font,
            bg=self.theme.bg_color,
            fg=self.theme.art_color,
        )
        title_label.pack(pady=20)

        # Stats frame
        stats_frame = tk.Frame(
            parent_frame, bg=self.theme.bg_color, relief=tk.RIDGE, bd=3
        )
        stats_frame.pack(pady=10, fill=tk.X, padx=20)

        level_label = tk.Label(
            stats_frame,
            text=f"Level: {self.data['art']['level']}",
            font=self.theme.pixel_font,
            bg=self.theme.bg_color,
            fg=self.theme.text_color,
        )
        level_label.grid(row=0, column=0, padx=20, pady=10)

        points_label = tk.Label(
            stats_frame,
            text=f"Points: {self.data['art']['points']}",
            font=self.theme.pixel_font,
            bg=self.theme.bg_color,
            fg=self.theme.text_color,
        )
        points_label.grid(row=0, column=1, padx=20, pady=10)

        streak_label = tk.Label(
            stats_frame,
            text=f"Streak: {self.data['art']['streak']} days",
            font=self.theme.pixel_font,
            bg=self.theme.bg_color,
            fg="#FF5722",
        )
        streak_label.grid(row=0, column=2, padx=20, pady=10)

        # Projects frame
        projects_frame = tk.Frame(parent_frame, bg=self.theme.bg_color)
        projects_frame.pack(pady=20, fill=tk.BOTH, expand=True, padx=20)

        # Show art projects
        self.show_art_projects(projects_frame)

        # Back button
        back_button = self.theme.create_pixel_button(
            parent_frame,
            "Back to Main Menu",
            self.app.show_main_menu,
            color="#9E9E9E",
        )
        back_button.pack(pady=20)

    def show_art_projects(self, parent_frame):
        """
        Show art module projects with pixel art styling.

        Args:
            parent_frame: Parent frame to place the projects
        """
        # Project selection frame
        project_select_frame = tk.Frame(parent_frame, bg=self.theme.bg_color)
        project_select_frame.pack(pady=10, fill=tk.X, padx=10)

        tk.Label(
            project_select_frame,
            text="Select Project:",
            font=self.theme.pixel_font,
            bg=self.theme.bg_color,
            fg=self.theme.text_color,
        ).pack(side=tk.LEFT, padx=5)

        projects = ["Art Fundamentals", "Fun Drawing Practice", "Accountability"]
        self.selected_art_project = tk.StringVar(value=projects[0])

        project_dropdown = ttk.Combobox(
            project_select_frame,
            textvariable=self.selected_art_project,
            values=projects,
            state="readonly",
            width=30,
            font=self.theme.pixel_font,
        )
        project_dropdown.pack(side=tk.LEFT, padx=5)
        project_dropdown.bind(
            "<<ComboboxSelected>>", lambda e: self.update_art_project_view(parent_frame)
        )

        # Create a container frame for project content
        self.art_project_container = tk.Frame(parent_frame, bg=self.theme.bg_color)
        self.art_project_container.pack(pady=10, fill=tk.BOTH, expand=True)

        # Show the first project by default
        self.show_art_fundamentals(self.art_project_container)

    def update_art_project_view(self, parent_frame):
        """
        Update the displayed project based on dropdown selection.

        Args:
            parent_frame: Parent frame containing the projects
        """
        # Clear the container
        for widget in self.art_project_container.winfo_children():
            widget.destroy()

        # Show the selected project
        project = self.selected_art_project.get()
        if project == "Art Fundamentals":
            self.show_art_fundamentals(self.art_project_container)
        elif project == "Fun Drawing Practice":
            self.show_art_sketchbook(self.art_project_container)
        elif project == "Accountability":
            self.show_art_accountability(self.art_project_container)

    def show_art_fundamentals(self, parent_frame):
        """
        Show art fundamentals project details with pixel art styling.

        Args:
            parent_frame: Parent frame to place the fundamentals content
        """
        # Project 1: Art Fundamentals
        project_frame = tk.LabelFrame(
            parent_frame,
            text="Project 1: Art Fundamentals",
            font=self.theme.pixel_font,
            bg=self.theme.bg_color,
            fg=self.theme.text_color,
            relief=tk.RIDGE,
            bd=3,
        )
        project_frame.pack(pady=10, fill=tk.BOTH, expand=True, padx=10)

        description = """
Complete art fundamental exercises for your current level
Each completed exercise page earns 2 points
Must complete all exercises for current level before advancing"""

        tk.Label(
            project_frame,
            text=description,
            justify=tk.LEFT,
            bg=self.theme.bg_color,
            fg=self.theme.text_color,
            font=self.theme.small_font,
        ).pack(pady=10, padx=10, anchor="w")

        # Progress bar
        progress_frame = tk.Frame(project_frame, bg=self.theme.bg_color)
        progress_frame.pack(pady=10, fill=tk.X, padx=10)

        total_exercises = len(self.data["art"]["exercises"]["fundamentals"])
        progress_percent = (
            (self.data["art"]["fundamentals_completed"] / total_exercises) * 100
            if total_exercises > 0
            else 0
        )

        tk.Label(
            progress_frame,
            text=f"Progress: {self.data['art']['fundamentals_completed']}/{total_exercises} exercises",
            bg=self.theme.bg_color,
            fg=self.theme.text_color,
            font=self.theme.small_font,
        ).pack(side=tk.LEFT, padx=5)

        # Create pixel art progress bar
        create_pixel_progress_bar(
            progress_frame,
            progress_percent,
            self.theme.art_color,
            self.theme.bg_color,
            self.theme.text_color,
            self.theme.darken_color,
        )

        tk.Label(
            progress_frame,
            text=f"{progress_percent:.1f}%",
            bg=self.theme.bg_color,
            fg=self.theme.text_color,
            font=self.theme.small_font,
        ).pack(side=tk.LEFT, padx=5)

        # Random Exercise Selection
        selection_frame = tk.LabelFrame(
            project_frame,
            text="Random Exercise",
            font=self.theme.pixel_font,
            bg=self.theme.bg_color,
            fg=self.theme.text_color,
            relief=tk.RIDGE,
            bd=3,
        )
        selection_frame.pack(pady=10, fill=tk.BOTH, expand=True, padx=10)

        # Random exercise display
        exercise_display_frame = tk.Frame(selection_frame, bg=self.theme.bg_color)
        exercise_display_frame.pack(pady=10, fill=tk.X, padx=5)

        self.exercise_display = tk.Label(
            exercise_display_frame,
            text="",
            bg=self.theme.primary_color,
            fg=self.theme.text_color,
            font=self.theme.pixel_font,
            wraplength=400,
            justify=tk.LEFT,
            relief=tk.SUNKEN,
            padx=10,
            pady=10,
        )
        self.exercise_display.pack(fill=tk.X, pady=5, padx=5)

        self.exercise_tip_text = tk.Label(
            exercise_display_frame,
            text="",
            bg=self.theme.bg_color,
            fg=self.theme.text_color,
            font=self.theme.small_font,
            wraplength=400,
            justify=tk.LEFT,
        )
        self.exercise_tip_text.pack(fill=tk.X, pady=5, padx=5)

        # Store the selected exercise
        self.selected_art_exercise = tk.StringVar()

        # Random generator button
        random_button = self.theme.create_pixel_button(
            exercise_display_frame,
            "Get Random Exercise",
            self.generate_random_art_exercise,
            color="#FF9800",
        )
        random_button.pack(pady=10)

        # Generate initial random exercise
        self.generate_random_art_exercise()

        # Button to log progress
        button_frame = tk.Frame(project_frame, bg=self.theme.bg_color)
        button_frame.pack(pady=10, fill=tk.X, padx=10)

        log_button = self.theme.create_pixel_button(
            button_frame,
            "Log Completed Exercise",
            lambda: self.log_art_fundamental(self.selected_art_exercise.get()),
            color=self.theme.art_color,
        )
        log_button.pack(pady=10)

    def show_art_sketchbook(self, parent_frame):
        """
        Show art sketchbook project details with pixel art styling.

        Args:
            parent_frame: Parent frame to place sketchbook content
        """
        # Project 2: Fun Drawing Practice
        project_frame = tk.LabelFrame(
            parent_frame,
            text="Project 2: Fun Drawing Practice",
            font=self.theme.pixel_font,
            bg=self.theme.bg_color,
            fg=self.theme.text_color,
            relief=tk.RIDGE,
            bd=3,
        )
        project_frame.pack(pady=10, fill=tk.BOTH, expand=True, padx=10)

        description = """
Fill a sketchbook with drawings for enjoyment 
Each filled sketchbook page earns 5 points 
Complete when at least 1/3 of the sketchbook is filled (80 pages)"""

        tk.Label(
            project_frame,
            text=description,
            justify=tk.LEFT,
            bg=self.theme.bg_color,
            fg=self.theme.text_color,
            font=self.theme.small_font,
        ).pack(pady=10, padx=10, anchor="w")

        # Progress bar
        progress_frame = tk.Frame(project_frame, bg=self.theme.bg_color)
        progress_frame.pack(pady=10, fill=tk.X, padx=10)

        sketchbook_progress = (
            self.data["art"]["sketchbook_pages"] / 80
        ) * 100  # 80 pages is 1/3

        tk.Label(
            progress_frame,
            text=f"Sketchbook pages: {self.data['art']['sketchbook_pages']}/80 minimum",
            bg=self.theme.bg_color,
            fg=self.theme.text_color,
            font=self.theme.small_font,
        ).pack(side=tk.LEFT, padx=5)

        # Create pixel art progress bar
        create_pixel_progress_bar(
            progress_frame,
            min(sketchbook_progress, 100),
            self.theme.art_color,
            self.theme.bg_color,
            self.theme.text_color,
            self.theme.darken_color,
        )

        tk.Label(
            progress_frame,
            text=f"{sketchbook_progress:.1f}%",
            bg=self.theme.bg_color,
            fg=self.theme.text_color,
            font=self.theme.small_font,
        ).pack(side=tk.LEFT, padx=5)

        # Random Drawing Type Selection
        selection_frame = tk.LabelFrame(
            project_frame,
            text="Random Drawing Type",
            font=self.theme.pixel_font,
            bg=self.theme.bg_color,
            fg=self.theme.text_color,
            relief=tk.RIDGE,
            bd=3,
        )
        selection_frame.pack(pady=10, fill=tk.BOTH, expand=True, padx=10)

        # Random drawing display
        drawing_display_frame = tk.Frame(selection_frame, bg=self.theme.bg_color)
        drawing_display_frame.pack(pady=10, fill=tk.X, padx=5)

        self.drawing_display = tk.Label(
            drawing_display_frame,
            text="",
            bg=self.theme.primary_color,
            fg=self.theme.text_color,
            font=self.theme.pixel_font,
            wraplength=400,
            justify=tk.LEFT,
            relief=tk.SUNKEN,
            padx=10,
            pady=10,
        )
        self.drawing_display.pack(fill=tk.X, pady=5, padx=5)

        self.drawing_tip_text = tk.Label(
            drawing_display_frame,
            text="",
            bg=self.theme.bg_color,
            fg=self.theme.text_color,
            font=self.theme.small_font,
            wraplength=400,
            justify=tk.LEFT,
        )
        self.drawing_tip_text.pack(fill=tk.X, pady=5, padx=5)

        # Store the selected drawing type
        self.selected_drawing_type = tk.StringVar()

        # Random generator button
        random_button = self.theme.create_pixel_button(
            drawing_display_frame,
            "Get Random Drawing Type",
            self.generate_random_drawing_type,
            color="#FF9800",
        )
        random_button.pack(pady=10)

        # Add drawing type button

        # Notes field
        notes_frame = tk.LabelFrame(
            project_frame,
            text="Drawing Notes (Optional)",
            font=self.theme.pixel_font,
            bg=self.theme.bg_color,
            fg=self.theme.text_color,
            relief=tk.RIDGE,
            bd=3,
        )
        notes_frame.pack(pady=10, fill=tk.X, padx=10)

        self.drawing_notes = tk.Text(
            notes_frame,
            height=4,
            width=40,
            font=self.theme.small_font,
            bg=self.theme.primary_color,
            fg=self.theme.text_color,
        )
        self.drawing_notes.pack(pady=10, padx=10, fill=tk.X)

        # Button to log progress
        button_frame = tk.Frame(project_frame, bg=self.theme.bg_color)
        button_frame.pack(pady=10, fill=tk.X, padx=10)

        log_button = self.theme.create_pixel_button(
            button_frame,
            "Log Sketchbook Page",
            self.log_sketchbook_page_with_details,
            color=self.theme.art_color,
        )
        log_button.pack(pady=10)

        # Generate initial random drawing type
        self.generate_random_drawing_type()

    def show_art_accountability(self, parent_frame):
        """
        Show art accountability project details with pixel art styling.

        Args:
            parent_frame: Parent frame to place accountability content
        """
        # Project 3: Accountability
        project_frame = tk.LabelFrame(
            parent_frame,
            text="Project 3: Accountability",
            font=self.theme.pixel_font,
            bg=self.theme.bg_color,
            fg=self.theme.text_color,
            relief=tk.RIDGE,
            bd=3,
        )
        project_frame.pack(pady=10, fill=tk.BOTH, expand=True, padx=10)

        description = """
Document your art progress and create content about your process
Share your journey to build accountability and get feedback
Each accountability post earns 3 points"""

        tk.Label(
            project_frame,
            text=description,
            justify=tk.LEFT,
            bg=self.theme.bg_color,
            fg=self.theme.text_color,
            font=self.theme.small_font,
        ).pack(pady=10, padx=10, anchor="w")

        # Progress display
        progress_frame = tk.Frame(project_frame, bg=self.theme.bg_color)
        progress_frame.pack(pady=10, fill=tk.X, padx=10)

        tk.Label(
            progress_frame,
            text=f"Accountability posts: {self.data['art']['accountability_posts']}",
            bg=self.theme.bg_color,
            fg=self.theme.text_color,
            font=self.theme.pixel_font,
        ).pack(pady=5)

        # Random Post Type Selection
        selection_frame = tk.LabelFrame(
            project_frame,
            text="Random Post Type",
            font=self.theme.pixel_font,
            bg=self.theme.bg_color,
            fg=self.theme.text_color,
            relief=tk.RIDGE,
            bd=3,
        )
        selection_frame.pack(pady=10, fill=tk.BOTH, expand=True, padx=10)

        # Random post display
        post_display_frame = tk.Frame(selection_frame, bg=self.theme.bg_color)
        post_display_frame.pack(pady=10, fill=tk.X, padx=5)

        self.post_display = tk.Label(
            post_display_frame,
            text="",
            bg=self.theme.primary_color,
            fg=self.theme.text_color,
            font=self.theme.pixel_font,
            wraplength=400,
            justify=tk.LEFT,
            relief=tk.SUNKEN,
            padx=10,
            pady=10,
        )
        self.post_display.pack(fill=tk.X, pady=5, padx=5)

        self.post_tip_text = tk.Label(
            post_display_frame,
            text="",
            bg=self.theme.bg_color,
            fg=self.theme.text_color,
            font=self.theme.small_font,
            wraplength=400,
            justify=tk.LEFT,
        )
        self.post_tip_text.pack(fill=tk.X, pady=5, padx=5)

        # Store the selected post type
        self.selected_post_type = tk.StringVar()

        # Random generator button
        random_button = self.theme.create_pixel_button(
            post_display_frame,
            "Get Random Post Type",
            self.generate_random_post_type,
            color="#FF9800",
        )
        random_button.pack(pady=10)

        # Post details
        details_frame = tk.LabelFrame(
            project_frame,
            text="Post Details",
            font=self.theme.pixel_font,
            bg=self.theme.bg_color,
            fg=self.theme.text_color,
            relief=tk.RIDGE,
            bd=3,
        )
        details_frame.pack(pady=10, fill=tk.X, padx=10)

        tk.Label(
            details_frame,
            text="Title:",
            bg=self.theme.bg_color,
            fg=self.theme.text_color,
            font=self.theme.small_font,
        ).pack(anchor="w", padx=10, pady=5)

        self.post_title_entry = tk.Entry(
            details_frame,
            width=50,
            font=self.theme.small_font,
            bg=self.theme.primary_color,
            fg=self.theme.text_color,
        )
        self.post_title_entry.pack(padx=10, pady=5, fill=tk.X)

        tk.Label(
            details_frame,
            text="Description:",
            bg=self.theme.bg_color,
            fg=self.theme.text_color,
            font=self.theme.small_font,
        ).pack(anchor="w", padx=10, pady=5)

        self.post_description = tk.Text(
            details_frame,
            height=4,
            width=50,
            font=self.theme.small_font,
            bg=self.theme.primary_color,
            fg=self.theme.text_color,
        )
        self.post_description.pack(padx=10, pady=5, fill=tk.X)

        # Platform selection
        platform_frame = tk.Frame(details_frame, bg=self.theme.bg_color)
        platform_frame.pack(pady=10, fill=tk.X, padx=10)

        tk.Label(
            platform_frame,
            text="Platform:",
            bg=self.theme.bg_color,
            fg=self.theme.text_color,
            font=self.theme.small_font,
        ).pack(side=tk.LEFT, padx=5)

        self.selected_platform = tk.StringVar(value="Personal Journal")
        platforms = [
            "Personal Journal",
            "Blog",
            "Instagram",
            "YouTube",
            "Twitter/X",
            "TikTok",
            "Discord",
            "Other",
        ]

        platform_dropdown = ttk.Combobox(
            platform_frame,
            textvariable=self.selected_platform,
            values=platforms,
            width=20,
            font=self.theme.small_font,
        )
        platform_dropdown.pack(side=tk.LEFT, padx=5)

        # Button to log progress
        button_frame = tk.Frame(project_frame, bg=self.theme.bg_color)
        button_frame.pack(pady=10, fill=tk.X, padx=10)

        log_button = self.theme.create_pixel_button(
            button_frame,
            "Log Accountability Post",
            self.log_accountability_with_details,
            color=self.theme.art_color,
        )
        log_button.pack(pady=10)

        # Generate initial random post type
        self.generate_random_post_type()

    def log_art_fundamental(self, exercise=None):
        """
        Log completion of an art fundamental exercise.

        Args:
            exercise: The specific exercise completed (optional)
        """
        if not self.data["health_status"]:
            messagebox.showinfo(
                "Health Check Required",
                "Please complete your daily health check before logging progress.",
            )
            return

        # If no specific exercise is selected
        if not exercise or exercise == "":
            # Show a warning
            if not messagebox.askyesno(
                "No Exercise Selected",
                "No specific exercise selected. Log a generic art fundamental exercise?",
            ):
                return

        # Add points
        self.data["art"]["points"] += 2
        self.data["art"]["fundamentals_completed"] += 1

        # Track completed exercise (in a future update we could store which specific exercises are completed)
        if "completed_exercises" not in self.data["art"]:
            self.data["art"]["completed_exercises"] = []

        if exercise and exercise != "":
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
            self.data["art"]["completed_exercises"].append(
                {
                    "exercise": exercise,
                    "type": "fundamentals",
                    "timestamp": timestamp,
                    "points": 2,
                }
            )

        # Update streak
        update_streak(self.data, "art")

        # Save data
        self.data_manager.save_data()

        if exercise and exercise != "":
            messagebox.showinfo(
                "Progress Logged", f"You completed '{exercise}'! +2 points"
            )
        else:
            messagebox.showinfo(
                "Progress Logged",
                "You completed an art fundamental exercise! +2 points",
            )

        # Check if level up is needed
        new_level, level_increased, streak_bonus = check_level_up(self.data, "art")
        if level_increased:
            if streak_bonus > 0:
                messagebox.showinfo(
                    "Level Up!",
                    f"Congratulations! You advanced to Level {new_level}!\n\nStreak Bonus: +{streak_bonus} points",
                )
            else:
                messagebox.showinfo(
                    "Level Up!", f"Congratulations! You advanced to Level {new_level}!"
                )

        # Refresh display
        self.show_module(self.app.main_frame)

    def log_sketchbook_page_with_details(self):
        """Log completion of a sketchbook page with details."""
        if not self.data["health_status"]:
            messagebox.showinfo(
                "Health Check Required",
                "Please complete your daily health check before logging progress.",
            )
            return

        # Get drawing type
        drawing_type = self.selected_drawing_type.get()
        custom_type = self.custom_drawing_entry.get().strip()

        if custom_type:
            drawing_type = custom_type

            # Add custom drawing type to the list if it's not already there
            if custom_type not in self.data["art"]["exercises"]["sketchbook"]:
                self.data["art"]["exercises"]["sketchbook"].append(custom_type)

        # Get notes
        notes = self.drawing_notes.get("1.0", tk.END).strip()

        # Add points
        self.data["art"]["points"] += 5
        self.data["art"]["sketchbook_pages"] += 1

        # Track drawing details
        if "drawing_log" not in self.data["art"]:
            self.data["art"]["drawing_log"] = []

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
        self.data["art"]["drawing_log"].append(
            {"type": drawing_type, "notes": notes, "timestamp": timestamp, "points": 5}
        )

        # Update streak
        update_streak(self.data, "art")

        # Save data
        self.data_manager.save_data()

        if drawing_type:
            messagebox.showinfo(
                "Progress Logged", f"You completed a {drawing_type} drawing! +5 points"
            )
        else:
            messagebox.showinfo(
                "Progress Logged", "You completed a sketchbook page! +5 points"
            )

        # Clear form fields
        self.selected_drawing_type.set("")
        self.custom_drawing_entry.delete(0, tk.END)
        self.drawing_notes.delete("1.0", tk.END)

        # Check if level up is needed
        new_level, level_increased, streak_bonus = check_level_up(self.data, "art")
        if level_increased:
            if streak_bonus > 0:
                messagebox.showinfo(
                    "Level Up!",
                    f"Congratulations! You advanced to Level {new_level}!\n\nStreak Bonus: +{streak_bonus} points",
                )
            else:
                messagebox.showinfo(
                    "Level Up!", f"Congratulations! You advanced to Level {new_level}!"
                )

        # Refresh display
        self.show_module(self.app.main_frame)

    def log_accountability_with_details(self):
        """Log an accountability post with details."""
        if not self.data["health_status"]:
            messagebox.showinfo(
                "Health Check Required",
                "Please complete your daily health check before logging progress.",
            )
            return

        # Get post details
        post_type = self.selected_post_type.get()
        title = self.post_title_entry.get().strip()
        description = self.post_description.get("1.0", tk.END).strip()
        platform = self.selected_platform.get()

        # Validate inputs
        if not post_type:
            messagebox.showwarning("Missing Information", "Please select a post type.")
            return

        if not title:
            messagebox.showwarning(
                "Missing Information", "Please enter a title for your post."
            )
            return

        # Add points (3 points per accountability post)
        self.data["art"]["points"] += 3
        self.data["art"]["accountability_posts"] += 1

        # Track post details
        if "accountability_log" not in self.data["art"]:
            self.data["art"]["accountability_log"] = []

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
        self.data["art"]["accountability_log"].append(
            {
                "type": post_type,
                "title": title,
                "description": description,
                "platform": platform,
                "timestamp": timestamp,
                "points": 3,
            }
        )

        # Update streak
        update_streak(self.data, "art")

        # Save data
        self.data_manager.save_data()

        messagebox.showinfo(
            "Progress Logged",
            f"You shared your progress with a {post_type} post! +3 points",
        )

        # Clear form fields
        self.selected_post_type.set("")
        self.post_title_entry.delete(0, tk.END)
        self.post_description.delete("1.0", tk.END)
        self.selected_platform.set("Personal Journal")

        # Check if level up is needed
        new_level, level_increased, streak_bonus = check_level_up(self.data, "art")
        if level_increased:
            if streak_bonus > 0:
                messagebox.showinfo(
                    "Level Up!",
                    f"Congratulations! You advanced to Level {new_level}!\n\nStreak Bonus: +{streak_bonus} points",
                )
            else:
                messagebox.showinfo(
                    "Level Up!", f"Congratulations! You advanced to Level {new_level}!"
                )

        # Refresh display
        self.show_module(self.app.main_frame)

    def toggle_description(self):
        """Toggle the visibility of the description text."""
        if self.description_visible.get():
            self.description_text.pack_forget()
            self.description_visible.set(False)
        else:
            self.description_text.pack(pady=5, padx=5, fill=tk.X, expand=True)
            self.description_visible.set(True)

    def generate_random_art_exercise(self):
        """Generate a random art exercise."""
        import random

        exercises = self.data["art"]["exercises"]["fundamentals"]
        if exercises:
            selected = random.choice(exercises)
            self.selected_art_exercise.set(selected)
            self.exercise_display.config(text=selected)

            # Optional: display a tip for the exercise
            exercise_tips = {
                "Basic Mark Making - Line control exercises": "Draw parallel straight lines with consistent spacing or practice drawing smooth curves and circles.",
                "Shape Accuracy - Drawing basic geometric forms": "Draw squares, circles, and triangles with precise proportions. Try to make them look balanced and clean.",
                "Proportion & Measurement techniques": "Draw a still life while using your pencil to measure relative sizes of objects.",
                "Contour Drawing - Blind contour exercises": "Draw the outline of an object without looking at your paper, focusing only on the object.",
                "Value Scales - Creating value ranges": "Create a gradient from white to black with at least 10 distinct shades in between.",
                "Basic Lighting - Core shadow, cast shadow": "Draw a simple object like a sphere and practice showing light, midtone, core shadow, reflected light, and cast shadow.",
                "Rendering Techniques - Hatching methods": "Practice different hatching patterns (parallel, cross-hatching, contour hatching) to create various tones and textures.",
                "Rendering Techniques - Blending methods": "Practice smooth shading transitions using techniques like stumping, circular motions, or layering.",
                "Color Wheel - Primary and secondary colors": "Create a color wheel showing primary, secondary, and tertiary colors with correct placement.",
                "Color Mixing - Creating specific colors": "Mix colors to match specific objects or create a harmonious color palette for a composition.",
                "Compositional Structures - Rule of thirds": "Draw a landscape using the rule of thirds to place key elements at intersection points.",
                "Visual Flow - Leading the eye through artwork": "Create a composition with elements that guide the viewer's eye in a deliberate path.",
                "Gesture Drawing - Capturing essence of pose": "Do quick 30-second sketches of people or animals to capture the energy and movement.",
                "Structural Anatomy - Basic figure proportions": "Draw a simplified human figure using basic proportions (head is 1/8 of body height, etc.).",
                "Master Studies - Copying works by artists": "Choose a drawing by a master artist and make a detailed copy to understand their techniques.",
                "Linear Perspective - One-point perspective": "Draw a simple interior scene with a single vanishing point.",
                "Linear Perspective - Two-point perspective": "Draw a building or box with two vanishing points on the horizon line.",
                "Foreshortening - Drawing objects in space": "Draw an arm or leg extending toward the viewer, showing how form appears compressed.",
                "Texture Development - Various drawing techniques": "Draw different textures like wood grain, fabric folds, or rough stone using appropriate mark-making.",
                "Negative Space Drawing": "Draw the shapes between and around objects instead of the objects themselves to improve spatial awareness and composition.",
                "Dynamic Poses - Action lines": "Sketch figures in motion using quick, flowing action lines to capture energy and movement before adding details.",
                "Animal Anatomy Studies": "Draw different animal skeletal and muscle structures to understand how their bodies are constructed and move.",
                "Environmental Sketching": "Practice creating atmospheric perspective by showing how objects fade and lose detail as they recede into the distance.",
                "Mixed Media Experimentation": "Combine different art materials (pencil, ink, watercolor, etc.) in one piece to explore how they interact and create textures.",  # Add more tips as needed
            }

            tip = exercise_tips.get(
                selected,
                "Focus on this fundamental skill to improve your art foundation.",
            )
            self.exercise_tip_text.config(text=f"{tip}")
        else:
            self.exercise_tip_text.config(
                text="No Exercises: No exercises available in the database."
            )

    def generate_random_drawing_type(self):
        """Generate a random drawing type."""
        import random

        drawing_types = self.data["art"]["exercises"]["sketchbook"]
        if drawing_types:
            selected = random.choice(drawing_types)
            self.selected_drawing_type.set(selected)
            self.drawing_display.config(text=selected)

            # Tips for different drawing types
            drawing_tips = {
                "Free drawing": "Draw whatever comes to mind without planning - let your imagination flow freely.",
                "Still life": "Arrange a small collection of objects and draw them from observation.",
                "Landscape sketch": "Draw a scene from nature or an urban landscape from reference or imagination.",
                "Character design": "Create a fictional character with distinct personality traits shown through design.",
                "Animal sketches": "Practice drawing different animals focusing on their unique shapes and features.",
                "Object studies": "Choose everyday objects and draw them from different angles.",
                "Urban sketching": "Draw buildings, streets, or cityscapes with attention to perspective.",
                "Nature elements": "Focus on plants, trees, rocks, or water and their textures.",
                "Fantasy creatures": "Invent and design creatures that don't exist in our world.",
                "Portrait practice": "Draw faces focusing on proportions and expressions.",
                "Comic strip creation": "Tell a short story in 3-4 sequential panels with simple characters and dialogue.",
                "Mood board illustration": "Create a collection of small sketches around a theme, color scheme, or emotion.",
                "Hand lettering practice": "Combine decorative text and illustrations to create an artistic quote or phrase.",
                "Dream journal sketch": "Illustrate a scene from a recent dream, focusing on the surreal or emotional elements.",
                "Food illustration": "Draw appetizing depictions of your favorite foods or an entire meal.",
                "Book cover redesign": "Reimagine the cover art for your favorite book with your own artistic interpretation.",
                "Fashion design sketch": "Create clothing designs, focusing on fabric textures, draping, and silhouettes.",
                "Mechanical objects": "Draw machines, vehicles, or gadgets, focusing on how their parts connect and function.",
                "Map creation": "Design a fictional map of an imaginary place with landmarks, terrain features, and a legend.",
                "Mythological scene": "Illustrate a scene from mythology or folklore, focusing on dramatic composition.",
            }

            tip = drawing_tips.get(
                selected, "Draw in your own style and focus on enjoying the process."
            )
            self.drawing_tip_text.config(text=f"{tip}")
        else:
            self.drawing_tip_text.config(
                text="No drawing types available in the database."
            )

    def generate_random_post_type(self):
        """Generate a random accountability post type."""
        import random

        post_types = self.data["art"]["exercises"]["accountability"]
        if post_types:
            selected = random.choice(post_types)
            self.selected_post_type.set(selected)
            self.post_display.config(text=selected)

            # Tips for different post types
            post_tips = {
                "Progress photo documentation": "Take photos of your artwork at different stages to show your process.",
                "Create process video": "Record a time-lapse or narrated video of your drawing/painting process.",
                "Write about learning experience": "Write about what you learned, challenges you faced, and how you overcame them.",
                "Post progress on social media": "Share your work with a supportive community for feedback and encouragement.",
                "Share before/after comparison": "Show your skills improvement by comparing early works with recent ones.",
                "Weekly art challenge participation": "Join a community art challenge and commit to completing and sharing your entry.",
                "Art critique exchange": "Pair up with another artist to exchange constructive feedback on each other's work.",
                "Skill-focused journal entry": "Document your focused practice on a specific skill and what you observed about your progress.",
                "Study group participation": "Share your work with a small group of artists for focused feedback and discussion.",
                "Portfolio review update": "Assess your body of work, select pieces for your portfolio, and document why they represent your skills.",
                "Technical breakdown post": "Create a detailed explanation of techniques you used in a specific artwork.",
                "Artist statement writing": "Develop or update your artist statement explaining your approach and artistic vision.",
                "Reference collection sharing": "Share your organized reference materials and explain how they inform your art practice.",
                "Goal-setting and tracking post": "Document your short and long-term art goals and track your progress toward them.",
                "Resource recommendation": "Share helpful resources you've discovered (books, courses, videos) with your thoughts on their value.",
            }

            tip = post_tips.get(
                selected,
                "Document your art journey in a way that feels comfortable and authentic to you.",
            )
            self.post_tip_text.config(text=f"{tip}")
        else:
            self.post_tip_text.config(text="No post types available in the database.")
