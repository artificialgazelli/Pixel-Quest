"""
Korean module for the Pixel Quest application.
Handles Korean language skill tracking and logging.
"""

import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from src.utils import update_streak, check_level_up, create_pixel_progress_bar

class KoreanModule:
    """
    Manages the Korean module functionality.
    """
    
    def __init__(self, app, data_manager, theme):
        """
        Initialize the Korean module.
        
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
        Show the Korean module interface.
        
        Args:
            parent_frame: Parent frame to place module content
        """
        # Title
        title_label = tk.Label(
            parent_frame,
            text="KOREAN QUEST",
            font=self.theme.heading_font,
            bg=self.theme.bg_color,
            fg=self.theme.korean_color,
        )
        title_label.pack(pady=20)

        # Stats frame
        stats_frame = tk.Frame(parent_frame, bg=self.theme.bg_color, relief=tk.RIDGE, bd=3)
        stats_frame.pack(pady=10, fill=tk.X, padx=20)

        level_label = tk.Label(
            stats_frame,
            text=f"Level: {self.data['korean']['level']}",
            font=self.theme.pixel_font,
            bg=self.theme.bg_color,
            fg=self.theme.text_color,
        )
        level_label.grid(row=0, column=0, padx=20, pady=10)

        points_label = tk.Label(
            stats_frame,
            text=f"Points: {self.data['korean']['points']}",
            font=self.theme.pixel_font,
            bg=self.theme.bg_color,
            fg=self.theme.text_color,
        )
        points_label.grid(row=0, column=1, padx=20, pady=10)

        streak_label = tk.Label(
            stats_frame,
            text=f"Streak: {self.data['korean']['streak']} days",
            font=self.theme.pixel_font,
            bg=self.theme.bg_color,
            fg="#FF5722",
        )
        streak_label.grid(row=0, column=2, padx=20, pady=10)

        # Projects frame
        projects_frame = tk.Frame(parent_frame, bg=self.theme.bg_color)
        projects_frame.pack(pady=20, fill=tk.BOTH, expand=True, padx=20)

        # Show Korean projects
        self.show_korean_projects(projects_frame)

        # Back button
        back_button = self.theme.create_pixel_button(
            parent_frame,
            "Back to Main Menu",
            self.app.show_main_menu,
            color="#9E9E9E",
        )
        back_button.pack(pady=20)
        
    def show_korean_projects(self, parent_frame):
        """
        Show Korean module projects with pixel art styling.
        
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

        projects = ["Korean Fundamentals", "Korean Immersion", "Korean Application"]
        self.selected_korean_project = tk.StringVar(value=projects[0])

        project_dropdown = ttk.Combobox(
            project_select_frame,
            textvariable=self.selected_korean_project,
            values=projects,
            state="readonly",
            width=30,
            font=self.theme.pixel_font,
        )
        project_dropdown.pack(side=tk.LEFT, padx=5)
        project_dropdown.bind(
            "<<ComboboxSelected>>",
            lambda e: self.update_korean_project_view(parent_frame),
        )

        # Create a container frame for project content
        self.korean_project_container = tk.Frame(parent_frame, bg=self.theme.bg_color)
        self.korean_project_container.pack(pady=10, fill=tk.BOTH, expand=True)

        # Show the first project by default
        self.show_korean_fundamentals(self.korean_project_container)
        
    def update_korean_project_view(self, parent_frame):
        """
        Update the displayed project based on dropdown selection.
        
        Args:
            parent_frame: Parent frame containing the projects
        """
        # Clear the container
        for widget in self.korean_project_container.winfo_children():
            widget.destroy()

        # Show the selected project
        project = self.selected_korean_project.get()
        if project == "Korean Fundamentals":
            self.show_korean_fundamentals(self.korean_project_container)
        elif project == "Korean Immersion":
            self.show_korean_immersion(self.korean_project_container)
        elif project == "Korean Application":
            self.show_korean_application(self.korean_project_container)
            
    def show_korean_fundamentals(self, parent_frame):
        """
        Show Korean fundamentals project details with pixel art styling.
        
        Args:
            parent_frame: Parent frame to place the fundamentals content
        """
        # Project 1: Korean Fundamentals
        project_frame = tk.LabelFrame(
            parent_frame,
            text="Project 1: Korean Fundamentals",
            font=self.theme.pixel_font,
            bg=self.theme.bg_color,
            fg=self.theme.text_color,
            relief=tk.RIDGE,
            bd=3,
        )
        project_frame.pack(pady=10, fill=tk.BOTH, expand=True, padx=10)

        description = """Complete structured Korean lessons (Hangul, vocabulary, grammar)
    Each completed lesson earns 2 points
    Practice 3-4 days per week for 20-30 minutes"""

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

        total_lessons = len(self.data["korean"]["exercises"]["fundamentals"])
        progress_percent = (
            (self.data["korean"]["fundamentals_completed"] / total_lessons) * 100
            if total_lessons > 0
            else 0
        )

        tk.Label(
            progress_frame,
            text=f"Progress: {self.data['korean']['fundamentals_completed']}/{total_lessons} lessons",
            bg=self.theme.bg_color,
            fg=self.theme.text_color,
            font=self.theme.small_font,
        ).pack(side=tk.LEFT, padx=5)

        # Create pixel art progress bar
        create_pixel_progress_bar(
            progress_frame, 
            progress_percent, 
            self.theme.korean_color, 
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

        # Lesson selection
        selection_frame = tk.LabelFrame(
            project_frame,
            text="Select Lesson",
            font=self.theme.pixel_font,
            bg=self.theme.bg_color,
            fg=self.theme.text_color,
            relief=tk.RIDGE,
            bd=3,
        )
        selection_frame.pack(pady=10, fill=tk.BOTH, expand=True, padx=10)

        # Create scrollable frame for lessons
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

        # Lesson dropdown
        tk.Label(
            scrollable_frame,
            text="Select a specific lesson:",
            bg=self.theme.bg_color,
            fg=self.theme.text_color,
            font=self.theme.small_font,
        ).grid(row=0, column=0, sticky="w", pady=5, padx=5)

        self.selected_korean_lesson = tk.StringVar()
        lesson_dropdown = ttk.Combobox(
            scrollable_frame,
            textvariable=self.selected_korean_lesson,
            values=self.data["korean"]["exercises"]["fundamentals"],
            width=40,
            font=self.theme.small_font,
        )
        lesson_dropdown.grid(row=0, column=1, pady=5, padx=5)

        # Lesson list with checkmarks for completed lessons
        completed_label = tk.Label(
            scrollable_frame,
            text="Completed Lessons:",
            font=self.theme.pixel_font,
            bg=self.theme.bg_color,
            fg=self.theme.text_color,
        )
        completed_label.grid(row=1, column=0, columnspan=2, sticky="w", pady=10, padx=5)

        # Lesson list (for demonstration, we're not tracking individual lessons yet)
        for i, lesson in enumerate(self.data["korean"]["exercises"]["fundamentals"]):
            completed = (
                "☑" if i < self.data["korean"]["fundamentals_completed"] else "☐"
            )
            tk.Label(
                scrollable_frame,
                text=f"{completed} {lesson}",
                bg=self.theme.bg_color,
                fg=self.theme.text_color,
                font=self.theme.small_font,
            ).grid(row=i + 2, column=0, columnspan=2, sticky="w", pady=2, padx=5)

        # Add lesson button
        add_lesson_button = self.theme.create_pixel_button(
            scrollable_frame,
            "Add New Lesson",
            lambda: self.add_custom_exercise("korean", "fundamentals"),
            color="#673AB7",
        )
        add_lesson_button.grid(
            row=len(self.data["korean"]["exercises"]["fundamentals"]) + 2,
            column=0,
            columnspan=2,
            pady=10,
        )

        # Button to log progress
        button_frame = tk.Frame(project_frame, bg=self.theme.bg_color)
        button_frame.pack(pady=10, fill=tk.X, padx=10)

        log_button = self.theme.create_pixel_button(
            button_frame,
            "Log Completed Lesson",
            lambda: self.log_korean_lesson(self.selected_korean_lesson.get()),
            color=self.theme.korean_color,
        )
        log_button.pack(pady=10)
        
    def show_korean_immersion(self, parent_frame):
        """
        Show Korean immersion project details with pixel art styling.
        
        Args:
            parent_frame: Parent frame to place the immersion content
        """
        # Project 2: Korean Immersion
        project_frame = tk.LabelFrame(
            parent_frame,
            text="Project 2: Korean Immersion",
            font=self.theme.pixel_font,
            bg=self.theme.bg_color,
            fg=self.theme.text_color,
            relief=tk.RIDGE,
            bd=3,
        )
        project_frame.pack(pady=10, fill=tk.BOTH, expand=True, padx=10)

        description = """Consume Korean content (K-dramas, K-pop, webtoons)
    Each 30-minute immersion session earns 5 points
    Practice 2-3 times per week"""

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

        # Display total immersion hours
        tk.Label(
            progress_frame,
            text=f"Total immersion: {self.data['korean']['immersion_hours']} hours",
            bg=self.theme.bg_color,
            fg=self.theme.text_color,
            font=self.theme.pixel_font,
        ).pack(pady=5)

        # Progress display for monthly goal (5 hours)
        monthly_goal = 5.0
        monthly_progress = min(
            (self.data["korean"]["immersion_hours"] % monthly_goal)
            / monthly_goal
            * 100,
            100,
        )

        progress_frame2 = tk.Frame(project_frame, bg=self.theme.bg_color)
        progress_frame2.pack(pady=5, fill=tk.X, padx=10)

        tk.Label(
            progress_frame2,
            text=f"Monthly goal: {self.data['korean']['immersion_hours'] % monthly_goal:.1f}/{monthly_goal} hours",
            bg=self.theme.bg_color,
            fg=self.theme.text_color,
            font=self.theme.small_font,
        ).pack(side=tk.LEFT, padx=5)

        # Create pixel art progress bar
        create_pixel_progress_bar(
            progress_frame2, 
            monthly_progress, 
            self.theme.korean_color, 
            self.theme.bg_color, 
            self.theme.text_color,
            self.theme.darken_color
        )

        tk.Label(
            progress_frame2,
            text=f"{monthly_progress:.1f}%",
            bg=self.theme.bg_color,
            fg=self.theme.text_color,
            font=self.theme.small_font,
        ).pack(side=tk.LEFT, padx=5)

        # Content type selection
        selection_frame = tk.LabelFrame(
            project_frame,
            text="Immersion Activity",
            font=self.theme.pixel_font,
            bg=self.theme.bg_color,
            fg=self.theme.text_color,
            relief=tk.RIDGE,
            bd=3,
        )
        selection_frame.pack(pady=10, fill=tk.BOTH, expand=True, padx=10)

        tk.Label(
            selection_frame,
            text="Select immersion type:",
            bg=self.theme.bg_color,
            fg=self.theme.text_color,
            font=self.theme.small_font,
        ).pack(pady=5, padx=5, anchor="w")

        self.selected_immersion_type = tk.StringVar()
        immersion_dropdown = ttk.Combobox(
            selection_frame,
            textvariable=self.selected_immersion_type,
            values=self.data["korean"]["exercises"]["immersion"],
            width=40,
            font=self.theme.small_font,
        )
        immersion_dropdown.pack(pady=5, padx=5)

        # Custom immersion type
        custom_frame = tk.Frame(selection_frame, bg=self.theme.bg_color)
        custom_frame.pack(pady=10, fill=tk.X)

        tk.Label(
            custom_frame,
            text="Or enter custom immersion activity:",
            bg=self.theme.bg_color,
            fg=self.theme.text_color,
            font=self.theme.small_font,
        ).pack(side=tk.LEFT, padx=5)

        self.custom_immersion_entry = tk.Entry(
            custom_frame,
            width=30,
            font=self.theme.small_font,
            bg=self.theme.primary_color,
            fg=self.theme.text_color,
        )
        self.custom_immersion_entry.pack(side=tk.LEFT, padx=5)

        # Add immersion type button
        add_type_button = self.theme.create_pixel_button(
            selection_frame,
            "Add New Immersion Type",
            lambda: self.add_custom_exercise("korean", "immersion"),
            color="#673AB7",
        )
        add_type_button.pack(pady=10)

        # Content details
        details_frame = tk.LabelFrame(
            project_frame,
            text="Content Details",
            font=self.theme.pixel_font,
            bg=self.theme.bg_color,
            fg=self.theme.text_color,
            relief=tk.RIDGE,
            bd=3,
        )
        details_frame.pack(pady=10, fill=tk.X, padx=10)

        tk.Label(
            details_frame,
            text="Title (optional):",
            bg=self.theme.bg_color,
            fg=self.theme.text_color,
            font=self.theme.small_font,
        ).pack(anchor="w", padx=10, pady=5)

        self.immersion_title_entry = tk.Entry(
            details_frame,
            width=50,
            font=self.theme.small_font,
            bg=self.theme.primary_color,
            fg=self.theme.text_color,
        )
        self.immersion_title_entry.pack(padx=10, pady=5, fill=tk.X)

        # Duration selection
        duration_frame = tk.Frame(details_frame, bg=self.theme.bg_color)
        duration_frame.pack(pady=10, fill=tk.X, padx=10)

        tk.Label(
            duration_frame,
            text="Duration:",
            bg=self.theme.bg_color,
            fg=self.theme.text_color,
            font=self.theme.small_font,
        ).pack(side=tk.LEFT, padx=5)

        self.selected_duration = tk.StringVar(value="30 minutes")
        durations = [
            "15 minutes",
            "30 minutes",
            "45 minutes",
            "1 hour",
            "1.5 hours",
            "2 hours",
        ]

        duration_dropdown = ttk.Combobox(
            duration_frame,
            textvariable=self.selected_duration,
            values=durations,
            width=15,
            font=self.theme.small_font,
        )
        duration_dropdown.pack(side=tk.LEFT, padx=5)

        # Button to log progress
        button_frame = tk.Frame(project_frame, bg=self.theme.bg_color)
        button_frame.pack(pady=10, fill=tk.X, padx=10)

        log_button = self.theme.create_pixel_button(
            button_frame,
            "Log Immersion Session",
            self.log_korean_immersion_with_details,
            color=self.theme.korean_color,
        )
        log_button.pack(pady=10)
        
    def show_korean_application(self, parent_frame):
        """
        Show Korean application project details with pixel art styling.
        
        Args:
            parent_frame: Parent frame to place the application content
        """
        # Project 3: Korean Application
        project_frame = tk.LabelFrame(
            parent_frame,
            text="Project 3: Korean Application",
            font=self.theme.pixel_font,
            bg=self.theme.bg_color,
            fg=self.theme.text_color,
            relief=tk.RIDGE,
            bd=3,
        )
        project_frame.pack(pady=10, fill=tk.BOTH, expand=True, padx=10)

        description = """Use Korean practically (writing journal entries, speaking practice)
    Each application session earns 10 points
    Practice weekly for 15-30 minutes"""

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
            text=f"Application sessions: {self.data['korean']['application_sessions']}",
            bg=self.theme.bg_color,
            fg=self.theme.text_color,
            font=self.theme.pixel_font,
        ).pack(pady=5)

        # Progress display for monthly goal (4 sessions)
        monthly_goal = 4
        monthly_progress = min(
            (self.data["korean"]["application_sessions"] % monthly_goal)
            / monthly_goal
            * 100,
            100,
        )

        progress_frame2 = tk.Frame(project_frame, bg=self.theme.bg_color)
        progress_frame2.pack(pady=5, fill=tk.X, padx=10)

        tk.Label(
            progress_frame2,
            text=f"Monthly goal: {self.data['korean']['application_sessions'] % monthly_goal}/{monthly_goal} sessions",
            bg=self.theme.bg_color,
            fg=self.theme.text_color,
            font=self.theme.small_font,
        ).pack(side=tk.LEFT, padx=5)

        # Create pixel art progress bar
        create_pixel_progress_bar(
            progress_frame2, 
            monthly_progress, 
            self.theme.korean_color, 
            self.theme.bg_color, 
            self.theme.text_color,
            self.theme.darken_color
        )

        tk.Label(
            progress_frame2,
            text=f"{monthly_progress:.1f}%",
            bg=self.theme.bg_color,
            fg=self.theme.text_color,
            font=self.theme.small_font,
        ).pack(side=tk.LEFT, padx=5)

        # Application type selection
        selection_frame = tk.LabelFrame(
            project_frame,
            text="Application Activity",
            font=self.theme.pixel_font,
            bg=self.theme.bg_color,
            fg=self.theme.text_color,
            relief=tk.RIDGE,
            bd=3,
        )
        selection_frame.pack(pady=10, fill=tk.BOTH, expand=True, padx=10)

        tk.Label(
            selection_frame,
            text="Select application type:",
            bg=self.theme.bg_color,
            fg=self.theme.text_color,
            font=self.theme.small_font,
        ).pack(pady=5, padx=5, anchor="w")

        self.selected_application_type = tk.StringVar()
        application_dropdown = ttk.Combobox(
            selection_frame,
            textvariable=self.selected_application_type,
            values=self.data["korean"]["exercises"]["application"],
            width=40,
            font=self.theme.small_font,
        )
        application_dropdown.pack(pady=5, padx=5)

        # Add application type button
        add_type_button = self.theme.create_pixel_button(
            selection_frame,
            "Add New Application Activity",
            lambda: self.add_custom_exercise("korean", "application"),
            color="#673AB7",
        )
        add_type_button.pack(pady=10)

        # Application notes
        notes_frame = tk.LabelFrame(
            project_frame,
            text="Session Notes",
            font=self.theme.pixel_font,
            bg=self.theme.bg_color,
            fg=self.theme.text_color,
            relief=tk.RIDGE,
            bd=3,
        )
        notes_frame.pack(pady=10, fill=tk.X, padx=10)

        self.application_notes = tk.Text(
            notes_frame,
            height=4,
            width=50,
            font=self.theme.small_font,
            bg=self.theme.primary_color,
            fg=self.theme.text_color,
        )
        self.application_notes.pack(padx=10, pady=10, fill=tk.X)

        # Button to log progress
        button_frame = tk.Frame(project_frame, bg=self.theme.bg_color)
        button_frame.pack(pady=10, fill=tk.X, padx=10)

        log_button = self.theme.create_pixel_button(
            button_frame,
            "Log Application Session",
            self.log_korean_application_with_details,
            color=self.theme.korean_color,
        )
        log_button.pack(pady=10)
        
    def add_custom_exercise(self, module, project_type):
        """
        Add a custom exercise to a project.
        
        Args:
            module: Module name ('art', 'korean', or 'french')
            project_type: Project type ('fundamentals', 'immersion', 'application', etc.)
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
            project_type: Project type ('fundamentals', 'immersion', 'application', etc.)
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
            self.update_korean_project_view(self.app.main_frame)
        else:
            messagebox.showwarning(
                "Empty Input", "Please enter an exercise description."
            )
            
    def log_korean_lesson(self, lesson=None):
        """
        Log completion of a Korean lesson.
        
        Args:
            lesson: The specific lesson completed (optional)
        """
        if not self.data["health_status"]:
            messagebox.showinfo(
                "Health Check Required",
                "Please complete your daily health check before logging progress.",
            )
            return

        # If no specific lesson is selected
        if not lesson or lesson == "":
            # Show a warning
            if not messagebox.askyesno(
                "No Lesson Selected",
                "No specific lesson selected. Log a generic Korean lesson?",
            ):
                return

        # Add points
        self.data["korean"]["points"] += 2
        self.data["korean"]["fundamentals_completed"] += 1

        # Track completed lesson
        if "completed_lessons" not in self.data["korean"]:
            self.data["korean"]["completed_lessons"] = []

        if lesson and lesson != "":
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
            self.data["korean"]["completed_lessons"].append(
                {
                    "lesson": lesson,
                    "type": "fundamentals",
                    "timestamp": timestamp,
                    "points": 2,
                }
            )

        # Update streak
        update_streak(self.data, "korean")

        # Save data
        self.data_manager.save_data()

        if lesson and lesson != "":
            messagebox.showinfo(
                "Progress Logged", f"You completed the '{lesson}' lesson! +2 points"
            )
        else:
            messagebox.showinfo(
                "Progress Logged", "You completed a Korean lesson! +2 points"
            )

        # Check if level up is needed
        new_level, level_increased, streak_bonus = check_level_up(self.data, "korean")
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
        
    def log_korean_immersion_with_details(self):
        """Log a Korean immersion session with details."""
        if not self.data["health_status"]:
            messagebox.showinfo(
                "Health Check Required",
                "Please complete your daily health check before logging progress.",
            )
            return

        # Get immersion details
        immersion_type = self.selected_immersion_type.get()
        custom_type = self.custom_immersion_entry.get().strip()
        title = self.immersion_title_entry.get().strip()
        duration = self.selected_duration.get()

        # Convert duration to hours
        duration_map = {
            "15 minutes": 0.25,
            "30 minutes": 0.5,
            "45 minutes": 0.75,
            "1 hour": 1.0,
            "1.5 hours": 1.5,
            "2 hours": 2.0,
        }

        hours = duration_map.get(duration, 0.5)  # Default to 0.5 if not found

        # Calculate points (5 points per 30 minutes)
        points = int(5 * (hours / 0.5))

        if custom_type:
            immersion_type = custom_type

            # Add custom immersion type to the list if it's not already there
            if custom_type not in self.data["korean"]["exercises"]["immersion"]:
                self.data["korean"]["exercises"]["immersion"].append(custom_type)

        # Validate inputs
        if not immersion_type:
            messagebox.showwarning(
                "Missing Information", "Please select or enter an immersion type."
            )
            return

        # Add points and hours
        self.data["korean"]["points"] += points
        self.data["korean"]["immersion_hours"] += hours

        # Track immersion details
        if "immersion_log" not in self.data["korean"]:
            self.data["korean"]["immersion_log"] = []

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
        self.data["korean"]["immersion_log"].append(
            {
                "type": immersion_type,
                "title": title,
                "duration": duration,
                "hours": hours,
                "timestamp": timestamp,
                "points": points,
            }
        )

        # Update streak
        update_streak(self.data, "korean")

        # Save data
        self.data_manager.save_data()

        messagebox.showinfo(
            "Progress Logged",
            f"You completed {duration} of Korean immersion ({immersion_type})! +{points} points",
        )

        # Clear form fields
        self.selected_immersion_type.set("")
        self.custom_immersion_entry.delete(0, tk.END)
        self.immersion_title_entry.delete(0, tk.END)
        self.selected_duration.set("30 minutes")

        # Check if level up is needed
        new_level, level_increased, streak_bonus = check_level_up(self.data, "korean")
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
        
    def log_korean_application_with_details(self):
        """Log a Korean application session with details."""
        if not self.data["health_status"]:
            messagebox.showinfo(
                "Health Check Required",
                "Please complete your daily health check before logging progress.",
            )
            return

        # Get application details
        application_type = self.selected_application_type.get()
        notes = self.application_notes.get("1.0", tk.END).strip()

        # Validate inputs
        if not application_type:
            messagebox.showwarning(
                "Missing Information", "Please select an application type."
            )
            return

        # Add points
        self.data["korean"]["points"] += 10
        self.data["korean"]["application_sessions"] += 1

        # Track application details
        if "application_log" not in self.data["korean"]:
            self.data["korean"]["application_log"] = []

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
        self.data["korean"]["application_log"].append(
            {
                "type": application_type,
                "notes": notes,
                "timestamp": timestamp,
                "points": 10,
            }
        )

        # Update streak
        update_streak(self.data, "korean")

        # Save data
        self.data_manager.save_data()

        messagebox.showinfo(
            "Progress Logged",
            f"You applied your Korean skills with {application_type}! +10 points",
        )

        # Clear form fields
        self.selected_application_type.set("")
        self.application_notes.delete("1.0", tk.END)

        # Check if level up is needed
        new_level, level_increased, streak_bonus = check_level_up(self.data, "korean")
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
