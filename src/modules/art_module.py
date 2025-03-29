"""
Art module for the Pixel Quest application.
Handles art skill tracking and logging.
"""

import tkinter as tk
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
        stats_frame = tk.Frame(parent_frame, bg=self.theme.bg_color, relief=tk.RIDGE, bd=3)
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

        description = """Complete art fundamental exercises for your current level
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
            self.theme.darken_color
        )

        tk.Label(
            progress_frame,
            text=f"{progress_percent:.1f}%",
            bg=self.theme.bg_color,
            fg=self.theme.text_color,
            font=self.theme.small_font,
        ).pack(side=tk.LEFT, padx=5)

        # Exercise selection
        selection_frame = tk.LabelFrame(
            project_frame,
            text="Select Exercise",
            font=self.theme.pixel_font,
            bg=self.theme.bg_color,
            fg=self.theme.text_color,
            relief=tk.RIDGE,
            bd=3,
        )
        selection_frame.pack(pady=10, fill=tk.BOTH, expand=True, padx=10)

        # Create scrollable frame for exercises
        canvas = tk.Canvas(selection_frame, bg=self.theme.bg_color, highlightthickness=0)
        scrollbar = ttk.Scrollbar(
            selection_frame, orient="vertical", command=canvas.yview
        )
        scrollable_frame = tk.Frame(canvas, bg=self.theme.bg_color)

        scrollable_frame.bind(
            "<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Exercise dropdown
        tk.Label(
            scrollable_frame,
            text="Select a specific exercise:",
            bg=self.theme.bg_color,
            fg=self.theme.text_color,
            font=self.theme.small_font,
        ).grid(row=0, column=0, sticky="w", pady=5, padx=5)

        self.selected_art_exercise = tk.StringVar()
        exercise_dropdown = ttk.Combobox(
            scrollable_frame,
            textvariable=self.selected_art_exercise,
            values=self.data["art"]["exercises"]["fundamentals"],
            width=40,
            font=self.theme.small_font,
        )
        exercise_dropdown.grid(row=0, column=1, pady=5, padx=5)

        # Exercise list with checkmarks for completed exercises
        completed_label = tk.Label(
            scrollable_frame,
            text="Completed Exercises:",
            font=self.theme.pixel_font,
            bg=self.theme.bg_color,
            fg=self.theme.text_color,
        )
        completed_label.grid(row=1, column=0, columnspan=2, sticky="w", pady=10, padx=5)

        # Exercise list (for demonstration, we're not tracking individual exercises yet)
        for i, exercise in enumerate(self.data["art"]["exercises"]["fundamentals"]):
            completed = "☑" if i < self.data["art"]["fundamentals_completed"] else "☐"
            tk.Label(
                scrollable_frame,
                text=f"{completed} {exercise}",
                bg=self.theme.bg_color,
                fg=self.theme.text_color,
                font=self.theme.small_font,
            ).grid(row=i + 2, column=0, columnspan=2, sticky="w", pady=2, padx=5)

        # Add exercise button
        add_exercise_button = self.theme.create_pixel_button(
            scrollable_frame,
            "Add New Exercise",
            lambda: self.add_custom_exercise("art", "fundamentals"),
            color="#673AB7",
        )
        add_exercise_button.grid(
            row=len(self.data["art"]["exercises"]["fundamentals"]) + 2,
            column=0,
            columnspan=2,
            pady=10,
        )

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

        description = """Fill a sketchbook with drawings for enjoyment
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
            self.theme.darken_color
        )

        tk.Label(
            progress_frame,
            text=f"{sketchbook_progress:.1f}%",
            bg=self.theme.bg_color,
            fg=self.theme.text_color,
            font=self.theme.small_font,
        ).pack(side=tk.LEFT, padx=5)

        # Drawing type selection
        selection_frame = tk.LabelFrame(
            project_frame,
            text="Select Drawing Type",
            font=self.theme.pixel_font,
            bg=self.theme.bg_color,
            fg=self.theme.text_color,
            relief=tk.RIDGE,
            bd=3,
        )
        selection_frame.pack(pady=10, fill=tk.BOTH, expand=True, padx=10)

        tk.Label(
            selection_frame,
            text="Select drawing type:",
            bg=self.theme.bg_color,
            fg=self.theme.text_color,
            font=self.theme.small_font,
        ).pack(pady=5, padx=5, anchor="w")

        self.selected_drawing_type = tk.StringVar()
        drawing_dropdown = ttk.Combobox(
            selection_frame,
            textvariable=self.selected_drawing_type,
            values=self.data["art"]["exercises"]["sketchbook"],
            width=40,
            font=self.theme.small_font,
        )
        drawing_dropdown.pack(pady=5, padx=5)

        # Custom drawing type
        custom_frame = tk.Frame(selection_frame, bg=self.theme.bg_color)
        custom_frame.pack(pady=10, fill=tk.X)

        tk.Label(
            custom_frame,
            text="Or enter custom drawing type:",
            bg=self.theme.bg_color,
            fg=self.theme.text_color,
            font=self.theme.small_font,
        ).pack(side=tk.LEFT, padx=5)

        self.custom_drawing_entry = tk.Entry(
            custom_frame,
            width=30,
            font=self.theme.small_font,
            bg=self.theme.primary_color,
            fg=self.theme.text_color,
        )
        self.custom_drawing_entry.pack(side=tk.LEFT, padx=5)

        # Add drawing type button
        add_type_button = self.theme.create_pixel_button(
            selection_frame,
            "Add New Drawing Type",
            lambda: self.add_custom_exercise("art", "sketchbook"),
            color="#673AB7",
        )
        add_type_button.pack(pady=10)

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

        description = """Document your art progress and create content about your process
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

        # Post type selection
        selection_frame = tk.LabelFrame(
            project_frame,
            text="Post Type",
            font=self.theme.pixel_font,
            bg=self.theme.bg_color,
            fg=self.theme.text_color,
            relief=tk.RIDGE,
            bd=3,
        )
        selection_frame.pack(pady=10, fill=tk.BOTH, expand=True, padx=10)

        tk.Label(
            selection_frame,
            text="Select post type:",
            bg=self.theme.bg_color,
            fg=self.theme.text_color,
            font=self.theme.small_font,
        ).pack(pady=5, padx=5, anchor="w")

        self.selected_post_type = tk.StringVar()
        post_dropdown = ttk.Combobox(
            selection_frame,
            textvariable=self.selected_post_type,
            values=self.data["art"]["exercises"]["accountability"],
            width=40,
            font=self.theme.small_font,
        )
        post_dropdown.pack(pady=5, padx=5)

        # Add post type button
        add_type_button = self.theme.create_pixel_button(
            selection_frame,
            "Add New Post Type",
            lambda: self.add_custom_exercise("art", "accountability"),
            color="#673AB7",
        )
        add_type_button.pack(pady=10)

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
    
    def add_custom_exercise(self, module, project_type):
        """
        Add a custom exercise to a project.
        
        Args:
            module: Module name ('art', 'korean', or 'french')
            project_type: Project type ('fundamentals', 'sketchbook', 'accountability', etc.)
        """
        # Create a dialog window
        dialog = tk.Toplevel(self.app.root)
        dialog.title(f"Add Custom {project_type.capitalize()} Exercise")
        dialog.geometry("500x150")
        dialog.configure(bg=self.theme.bg_color)
        dialog.transient(self.app.root)
        dialog.grab_set()

        # Label and entry for new exercise
        tk.Label(
            dialog,
            text=f"Enter new {project_type} exercise or activity:",
            font=self.theme.pixel_font,
            bg=self.theme.bg_color,
            fg=self.theme.text_color,
        ).pack(pady=10)

        entry = tk.Entry(
            dialog,
            width=50,
            font=self.theme.small_font,
            bg=self.theme.primary_color,
            fg=self.theme.text_color,
        )
        entry.pack(pady=10, padx=20)
        entry.focus_set()

        # Button frame
        button_frame = tk.Frame(dialog, bg=self.theme.bg_color)
        button_frame.pack(pady=10)

        # Add button
        add_button = self.theme.create_pixel_button(
            button_frame,
            "Add Exercise",
            lambda: self.process_add_exercise(
                dialog, module, project_type, entry.get()
            ),
            color="#4CAF50",
        )
        add_button.pack(side=tk.LEFT, padx=10)

        # Cancel button
        cancel_button = self.theme.create_pixel_button(
            button_frame, "Cancel", dialog.destroy, color="#9E9E9E"
        )
        cancel_button.pack(side=tk.LEFT, padx=10)
        
    def process_add_exercise(self, dialog, module, project_type, exercise_text):
        """
        Process adding the new exercise.
        
        Args:
            dialog: The dialog window to close after processing
            module: Module name ('art', 'korean', or 'french')
            project_type: Project type ('fundamentals', 'sketchbook', 'accountability', etc.)
            exercise_text: The text of the new exercise
        """
        if exercise_text.strip():
            # Add to data if it doesn't already exist
            if exercise_text not in self.data[module]["exercises"][project_type]:
                self.data[module]["exercises"][project_type].append(exercise_text)
                self.data_manager.save_data()
                messagebox.showinfo(
                    "Exercise Added",
                    f"Added new {project_type} exercise: {exercise_text}",
                )
            else:
                messagebox.showinfo(
                    "Already Exists",
                    f"This {project_type} exercise already exists in your list.",
                )

            # Close dialog
            dialog.destroy()

            # Refresh the view
            if module == "art":
                self.update_art_project_view(self.app.main_frame)
        else:
            messagebox.showwarning(
                "Empty Input", "Please enter an exercise description."
            )
    
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
