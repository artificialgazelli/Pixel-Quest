"""
French module for the Pixel Quest application.
Handles French language skill tracking and logging.
"""

import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from src.utils import update_streak, check_level_up, create_pixel_progress_bar


class FrenchModule:
    """
    Manages the French module functionality.
    """

    def __init__(self, app, data_manager, theme):
        """
        Initialize the French module.

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
        Show the French module interface.

        Args:
            parent_frame: Parent frame to place module content
        """
        # Title
        title_label = tk.Label(
            parent_frame,
            text="FRENCH QUEST",
            font=self.theme.heading_font,
            bg=self.theme.bg_color,
            fg=self.theme.french_color,
        )
        title_label.pack(pady=20)

        # Stats frame
        stats_frame = tk.Frame(
            parent_frame, bg=self.theme.bg_color, relief=tk.RIDGE, bd=3
        )
        stats_frame.pack(pady=10, fill=tk.X, padx=20)

        level_label = tk.Label(
            stats_frame,
            text=f"Level: {self.data['french']['level']}",
            font=self.theme.pixel_font,
            bg=self.theme.bg_color,
            fg=self.theme.text_color,
        )
        level_label.grid(row=0, column=0, padx=20, pady=10)

        points_label = tk.Label(
            stats_frame,
            text=f"Points: {self.data['french']['points']}",
            font=self.theme.pixel_font,
            bg=self.theme.bg_color,
            fg=self.theme.text_color,
        )
        points_label.grid(row=0, column=1, padx=20, pady=10)

        streak_label = tk.Label(
            stats_frame,
            text=f"Streak: {self.data['french']['streak']} days",
            font=self.theme.pixel_font,
            bg=self.theme.bg_color,
            fg="#FF5722",
        )
        streak_label.grid(row=0, column=2, padx=20, pady=10)

        # Projects frame
        projects_frame = tk.Frame(parent_frame, bg=self.theme.bg_color)
        projects_frame.pack(pady=20, fill=tk.BOTH, expand=True, padx=20)

        # Show French projects
        self.show_french_projects(projects_frame)

        # Back button
        back_button = self.theme.create_pixel_button(
            parent_frame,
            "Back to Main Menu",
            self.app.show_main_menu,
            color="#9E9E9E",
        )
        back_button.pack(pady=20)

    def show_french_projects(self, parent_frame):
        """
        Show French module projects with pixel art styling.

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

        projects = ["French Fundamentals", "French Immersion", "French Application"]
        self.selected_french_project = tk.StringVar(value=projects[0])

        project_dropdown = ttk.Combobox(
            project_select_frame,
            textvariable=self.selected_french_project,
            values=projects,
            state="readonly",
            width=30,
            font=self.theme.pixel_font,
        )
        project_dropdown.pack(side=tk.LEFT, padx=5)
        project_dropdown.bind(
            "<<ComboboxSelected>>",
            lambda e: self.update_french_project_view(parent_frame),
        )

        # Create a container frame for project content
        self.french_project_container = tk.Frame(parent_frame, bg=self.theme.bg_color)
        self.french_project_container.pack(pady=10, fill=tk.BOTH, expand=True)

        # Show the first project by default
        self.show_french_fundamentals(self.french_project_container)

    def update_french_project_view(self, parent_frame):
        """
        Update the displayed project based on dropdown selection.

        Args:
            parent_frame: Parent frame containing the projects
        """
        # Clear the container
        for widget in self.french_project_container.winfo_children():
            widget.destroy()

        # Show the selected project
        project = self.selected_french_project.get()
        if project == "French Fundamentals":
            self.show_french_fundamentals(self.french_project_container)
        elif project == "French Immersion":
            self.show_french_immersion(self.french_project_container)
        elif project == "French Application":
            self.show_french_application(self.french_project_container)

    def show_french_fundamentals(self, parent_frame):
        """
        Show French fundamentals project details with pixel art styling.

        Args:
            parent_frame: Parent frame to place the fundamentals content
        """
        # Project 1: French Fundamentals
        project_frame = tk.LabelFrame(
            parent_frame,
            text="Project 1: French Fundamentals",
            font=self.theme.pixel_font,
            bg=self.theme.bg_color,
            fg=self.theme.text_color,
            relief=tk.RIDGE,
            bd=3,
        )
        project_frame.pack(pady=10, fill=tk.BOTH, expand=True, padx=10)

        description = """
Complete structured French lessons (grammar, vocabulary, pronunciation)
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

        total_lessons = len(self.data["french"]["exercises"]["fundamentals"])
        progress_percent = (
            (self.data["french"]["fundamentals_completed"] / total_lessons) * 100
            if total_lessons > 0
            else 0
        )

        tk.Label(
            progress_frame,
            text=f"Progress: {self.data['french']['fundamentals_completed']}/{total_lessons} lessons",
            bg=self.theme.bg_color,
            fg=self.theme.text_color,
            font=self.theme.small_font,
        ).pack(side=tk.LEFT, padx=5)

        # Create pixel art progress bar
        create_pixel_progress_bar(
            progress_frame,
            progress_percent,
            self.theme.french_color,
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
        self.selected_french_lesson = tk.StringVar()

        # Random generator button
        random_button = self.theme.create_pixel_button(
            exercise_display_frame,
            "Get Random Exercise",
            self.generate_random_french_exercise,
            color="#FF9800",
        )
        random_button.pack(pady=10)

        # Generate initial random exercise
        self.generate_random_french_exercise()

        # Button to log progress
        button_frame = tk.Frame(project_frame, bg=self.theme.bg_color)
        button_frame.pack(pady=10, fill=tk.X, padx=10)

        log_button = self.theme.create_pixel_button(
            button_frame,
            "Log Completed Lesson",
            lambda: self.log_french_lesson(self.selected_french_lesson.get()),
            color=self.theme.french_color,
        )
        log_button.pack(pady=10)

    def show_french_immersion(self, parent_frame):
        """
        Show French immersion project details with pixel art styling.

        Args:
            parent_frame: Parent frame to place the immersion content
        """
        # Project 2: French Immersion
        project_frame = tk.LabelFrame(
            parent_frame,
            text="Project 2: French Immersion",
            font=self.theme.pixel_font,
            bg=self.theme.bg_color,
            fg=self.theme.text_color,
            relief=tk.RIDGE,
            bd=3,
        )
        project_frame.pack(pady=10, fill=tk.BOTH, expand=True, padx=10)

        description = """
Consume French content (films, music, books, podcasts)
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
            text=f"Total immersion: {self.data['french']['immersion_hours']} hours",
            bg=self.theme.bg_color,
            fg=self.theme.text_color,
            font=self.theme.pixel_font,
        ).pack(pady=5)

        # Progress display for monthly goal (5 hours)
        monthly_goal = 5.0
        monthly_progress = min(
            (self.data["french"]["immersion_hours"] % monthly_goal)
            / monthly_goal
            * 100,
            100,
        )

        progress_frame2 = tk.Frame(project_frame, bg=self.theme.bg_color)
        progress_frame2.pack(pady=5, fill=tk.X, padx=10)

        tk.Label(
            progress_frame2,
            text=f"Monthly goal: {self.data['french']['immersion_hours'] % monthly_goal:.1f}/{monthly_goal} hours",
            bg=self.theme.bg_color,
            fg=self.theme.text_color,
            font=self.theme.small_font,
        ).pack(side=tk.LEFT, padx=5)

        # Create pixel art progress bar
        create_pixel_progress_bar(
            progress_frame2,
            monthly_progress,
            self.theme.french_color,
            self.theme.bg_color,
            self.theme.text_color,
            self.theme.darken_color,
        )

        tk.Label(
            progress_frame2,
            text=f"{monthly_progress:.1f}%",
            bg=self.theme.bg_color,
            fg=self.theme.text_color,
            font=self.theme.small_font,
        ).pack(side=tk.LEFT, padx=5)

        # Random Immersion Selection
        selection_frame = tk.LabelFrame(
            project_frame,
            text="Random Immersion Activity",
            font=self.theme.pixel_font,
            bg=self.theme.bg_color,
            fg=self.theme.text_color,
            relief=tk.RIDGE,
            bd=3,
        )
        selection_frame.pack(pady=10, fill=tk.BOTH, expand=True, padx=10)

        # Random immersion display
        immersion_display_frame = tk.Frame(selection_frame, bg=self.theme.bg_color)
        immersion_display_frame.pack(pady=10, fill=tk.X, padx=5)

        self.immersion_display = tk.Label(
            immersion_display_frame,
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
        self.immersion_display.pack(fill=tk.X, pady=5, padx=5)

        self.immersion_tip_text = tk.Label(
            immersion_display_frame,
            text="",
            bg=self.theme.bg_color,
            fg=self.theme.text_color,
            font=self.theme.small_font,
            wraplength=400,
            justify=tk.LEFT,
        )
        self.immersion_tip_text.pack(fill=tk.X, pady=5, padx=5)

        # Store the selected immersion activity
        self.selected_french_immersion_type = tk.StringVar()

        # Random generator button
        random_button = self.theme.create_pixel_button(
            immersion_display_frame,
            "Get Random Immersion",
            self.generate_random_french_immersion,
            color="#FF9800",
        )
        random_button.pack(pady=10)

        # Generate initial random immersion activity
        self.generate_random_french_immersion()

        # Duration selection
        duration_frame = tk.Frame(project_frame, bg=self.theme.bg_color)
        duration_frame.pack(pady=10, fill=tk.X, padx=10)

        tk.Label(
            duration_frame,
            text="Duration:",
            bg=self.theme.bg_color,
            fg=self.theme.text_color,
            font=self.theme.pixel_font,
        ).pack(side=tk.LEFT, padx=5)

        self.selected_french_duration = tk.StringVar(value="30 minutes")
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
            textvariable=self.selected_french_duration,
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
            self.log_french_immersion_session,
            color=self.theme.french_color,
        )
        log_button.pack(pady=10)

    def show_french_application(self, parent_frame):
        """
        Show French application project details with pixel art styling.

        Args:
            parent_frame: Parent frame to place the application content
        """
        # Project 3: French Application
        project_frame = tk.LabelFrame(
            parent_frame,
            text="Project 3: French Application",
            font=self.theme.pixel_font,
            bg=self.theme.bg_color,
            fg=self.theme.text_color,
            relief=tk.RIDGE,
            bd=3,
        )
        project_frame.pack(pady=10, fill=tk.BOTH, expand=True, padx=10)

        description = """
Use French practically (writing, conversation practice)
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
            text=f"Application sessions: {self.data['french']['application_sessions']}",
            bg=self.theme.bg_color,
            fg=self.theme.text_color,
            font=self.theme.pixel_font,
        ).pack(pady=5)

        # Progress display for monthly goal (4 sessions)
        monthly_goal = 4
        monthly_progress = min(
            (self.data["french"]["application_sessions"] % monthly_goal)
            / monthly_goal
            * 100,
            100,
        )

        progress_frame2 = tk.Frame(project_frame, bg=self.theme.bg_color)
        progress_frame2.pack(pady=5, fill=tk.X, padx=10)

        tk.Label(
            progress_frame2,
            text=f"Monthly goal: {self.data['french']['application_sessions'] % monthly_goal}/{monthly_goal} sessions",
            bg=self.theme.bg_color,
            fg=self.theme.text_color,
            font=self.theme.small_font,
        ).pack(side=tk.LEFT, padx=5)

        # Create pixel art progress bar
        create_pixel_progress_bar(
            progress_frame2,
            monthly_progress,
            self.theme.french_color,
            self.theme.bg_color,
            self.theme.text_color,
            self.theme.darken_color,
        )

        tk.Label(
            progress_frame2,
            text=f"{monthly_progress:.1f}%",
            bg=self.theme.bg_color,
            fg=self.theme.text_color,
            font=self.theme.small_font,
        ).pack(side=tk.LEFT, padx=5)

        # Random Application Selection
        selection_frame = tk.LabelFrame(
            project_frame,
            text="Random Application Activity",
            font=self.theme.pixel_font,
            bg=self.theme.bg_color,
            fg=self.theme.text_color,
            relief=tk.RIDGE,
            bd=3,
        )
        selection_frame.pack(pady=10, fill=tk.BOTH, expand=True, padx=10)

        # Random application display
        application_display_frame = tk.Frame(selection_frame, bg=self.theme.bg_color)
        application_display_frame.pack(pady=10, fill=tk.X, padx=5)

        self.application_display = tk.Label(
            application_display_frame,
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
        self.application_display.pack(fill=tk.X, pady=5, padx=5)

        self.application_tip_text = tk.Label(
            application_display_frame,
            text="",
            bg=self.theme.bg_color,
            fg=self.theme.text_color,
            font=self.theme.small_font,
            wraplength=400,
            justify=tk.LEFT,
        )
        self.application_tip_text.pack(fill=tk.X, pady=5, padx=5)

        # Store the selected application activity
        self.selected_french_application_type = tk.StringVar()

        # Random generator button
        random_button = self.theme.create_pixel_button(
            application_display_frame,
            "Get Random Activity",
            self.generate_random_french_application,
            color="#FF9800",
        )
        random_button.pack(pady=10)

        # Generate initial random application activity
        self.generate_random_french_application()

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

        self.french_application_notes = tk.Text(
            notes_frame,
            height=4,
            width=50,
            font=self.theme.small_font,
            bg=self.theme.primary_color,
            fg=self.theme.text_color,
        )
        self.french_application_notes.pack(padx=10, pady=10, fill=tk.X)

        # Button to log progress
        button_frame = tk.Frame(project_frame, bg=self.theme.bg_color)
        button_frame.pack(pady=10, fill=tk.X, padx=10)

        log_button = self.theme.create_pixel_button(
            button_frame,
            "Log Application Session",
            self.log_french_application_session,
            color=self.theme.french_color,
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
            self.update_french_project_view(self.app.main_frame)
        else:
            messagebox.showwarning(
                "Empty Input", "Please enter an exercise description."
            )

    def log_french_lesson(self, lesson=None):
        """
        Log completion of a French lesson.

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
                "No specific lesson selected. Log a generic French lesson?",
            ):
                return

        # Add points
        self.data["french"]["points"] += 2
        self.data["french"]["fundamentals_completed"] += 1

        # Track completed lesson
        if "completed_lessons" not in self.data["french"]:
            self.data["french"]["completed_lessons"] = []

        if lesson and lesson != "":
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
            self.data["french"]["completed_lessons"].append(
                {
                    "lesson": lesson,
                    "type": "fundamentals",
                    "timestamp": timestamp,
                    "points": 2,
                }
            )

        # Update streak
        update_streak(self.data, "french")

        # Save data
        self.data_manager.save_data()

        if lesson and lesson != "":
            messagebox.showinfo(
                "Progress Logged", f"You completed the '{lesson}' lesson! +2 points"
            )
        else:
            messagebox.showinfo(
                "Progress Logged", "You completed a French lesson! +2 points"
            )

        # Check if level up is needed
        new_level, level_increased, streak_bonus = check_level_up(self.data, "french")
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

    def log_french_immersion_session(self):
        """Log a French immersion session."""
        if not self.data["health_status"]:
            messagebox.showinfo(
                "Health Check Required",
                "Please complete your daily health check before logging progress.",
            )
            return

        # Get immersion details
        immersion_type = self.selected_french_immersion_type.get()
        duration = self.selected_french_duration.get()

        # Validate inputs
        if not immersion_type:
            messagebox.showwarning(
                "Missing Information", "Please select an immersion type."
            )
            return

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

        # Add points and hours
        self.data["french"]["points"] += points
        self.data["french"]["immersion_hours"] += hours

        # Track immersion details
        if "immersion_log" not in self.data["french"]:
            self.data["french"]["immersion_log"] = []

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
        self.data["french"]["immersion_log"].append(
            {
                "type": immersion_type,
                "duration": duration,
                "hours": hours,
                "timestamp": timestamp,
                "points": points,
            }
        )

        # Update streak
        update_streak(self.data, "french")

        # Save data
        self.data_manager.save_data()

        messagebox.showinfo(
            "Progress Logged",
            f"You completed {duration} of French immersion ({immersion_type})! +{points} points",
        )

        # Check if level up is needed
        new_level, level_increased, streak_bonus = check_level_up(self.data, "french")
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

        # Generate a new random immersion activity
        self.generate_random_french_immersion()

        # Update the current project view
        self.update_french_project_view(self.app.main_frame)

    def log_french_application_session(self):
        """Log a French application session."""
        if not self.data["health_status"]:
            messagebox.showinfo(
                "Health Check Required",
                "Please complete your daily health check before logging progress.",
            )
            return

        # Get application details
        application_type = self.selected_french_application_type.get()
        notes = self.french_application_notes.get("1.0", tk.END).strip()

        # Validate inputs
        if not application_type:
            messagebox.showwarning(
                "Missing Information", "Please select an application type."
            )
            return

        # Add points
        self.data["french"]["points"] += 10
        self.data["french"]["application_sessions"] += 1

        # Track application details
        if "application_log" not in self.data["french"]:
            self.data["french"]["application_log"] = []

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
        self.data["french"]["application_log"].append(
            {
                "type": application_type,
                "notes": notes,
                "timestamp": timestamp,
                "points": 10,
            }
        )

        # Update streak
        update_streak(self.data, "french")

        # Save data
        self.data_manager.save_data()

        messagebox.showinfo(
            "Progress Logged",
            f"You applied your French skills with {application_type}! +10 points",
        )

        # Clear form fields
        self.french_application_notes.delete("1.0", tk.END)

        # Check if level up is needed
        new_level, level_increased, streak_bonus = check_level_up(self.data, "french")
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

        # Generate a new random application activity
        self.generate_random_french_application()

        # Update the current project view instead of refreshing the entire module
        # This helps prevent UI duplication issues
        self.update_french_project_view(self.app.main_frame)

    def generate_random_french_exercise(self):
        """Generate a random French exercise."""
        import random

        exercises = self.data["french"]["exercises"]["fundamentals"]
        if exercises:
            selected = random.choice(exercises)
            self.selected_french_lesson.set(selected)
            self.exercise_display.config(text=selected)

            # Optional: display a tip for the exercise
            exercise_tips = {
                "French Alphabet & Pronunciation": "Practice pronouncing each letter aloud, focusing on vowel sounds that differ from English.",
                "Basic Greetings & Introductions": "Practice introducing yourself with proper formal and informal expressions.",
                "Numbers 1-100 in French": "Count objects around you, saying the numbers aloud in French.",
                "Basic Sentence Structure": "Create simple sentences following subject-verb-object word order.",
                "Present Tense Regular Verbs": "Practice conjugating -er, -ir, and -re verbs with different subjects.",
                "Common Irregular Verbs (être, avoir, aller)": "Create sentences using these essential irregular verbs.",
                "Question Formation": "Transform statements into questions using inversion and est-ce que forms.",
                "Family Vocabulary": "Learn terms for immediate and extended family members.",
                "Food & Restaurant Vocabulary": "Practice ordering food and describing flavors in French.",
                "Time Expressions & Telling Time": "Practice telling the time and making schedule-related sentences.",
                "Basic Adjectives & Agreement": "Practice making adjectives agree with nouns in gender and number.",
                "Location & Directions": "Practice giving and understanding simple directions in French.",
                "Transportation Vocabulary": "Learn vocabulary for different modes of transportation.",
                "Weather & Seasons": "Construct sentences about weather conditions and seasonal activities.",
                "Basic Prepositions": "Learn prepositions of place, time, and movement.",
                "Past Tense - Passé Composé": "Convert present tense sentences to passé composé.",
                "Past Tense - Imparfait": "Practice when to use imparfait vs. passé composé.",
                "Future Tense": "Create sentences about plans and future activities.",
                "Direct & Indirect Object Pronouns": "Replace nouns with appropriate pronouns in sentences.",
                "Reflexive Verbs": "Practice daily routine descriptions using reflexive verbs.",
                "Negation Patterns": "Convert positive sentences to negative using ne...pas and other negative expressions.",
                "Imperative Forms": "Practice giving instructions or commands in French.",
                "Shopping & Money Expressions": "Role-play purchasing items and asking about prices.",
                "Expressing Opinions": "Learn phrases for agreeing, disagreeing, and stating preferences.",
                "Cultural Etiquette & Expressions": "Study appropriate expressions for different social situations.",
            }

            tip = exercise_tips.get(
                selected,
                "Focus on this fundamental skill to improve your French language foundation.",
            )
            self.exercise_tip_text.config(text=f"{tip}")
        else:
            self.exercise_tip_text.config(
                text="No Exercises: No exercises available in the database."
            )

    def generate_random_french_immersion(self):
        """Generate a random French immersion activity."""
        import random

        activities = self.data["french"]["exercises"]["immersion"]
        if activities:
            selected = random.choice(activities)
            self.selected_french_immersion_type.set(selected)
            self.immersion_display.config(text=selected)

            # Optional: display a tip for the immersion activity
            immersion_tips = {
                "French films with subtitles": "Start with French subtitles if you're intermediate, or English if you're a beginner.",
                "French music listening": "Look up lyrics and try to sing along. Pay attention to pronunciation and rhythm.",
                "French news reading": "Start with simpler news sites like 1jour1actu or TV5Monde. Read headlines first, then full articles.",
                "French podcast listening": "Choose podcasts meant for French learners first before moving to native content.",
                "French YouTube channels": "Try channels that teach French in French or simple vlog content with clear speech.",
                "Reading comic books in French": "French comics (BD) like Astérix or Tintin have visual context that helps with comprehension.",
                "French TV shows": "Series like 'Call My Agent!' or 'Lupin' are popular and available with subtitles on streaming platforms.",
                "French radio programs": "Radio France Internationale (RFI) offers programs specifically for language learners.",
                "French language exchange apps": "Try HelloTalk or Tandem to chat with native speakers and learn natural expressions.",
                "French social media browsing": "Follow French celebrities, brands, or news accounts on Instagram, Twitter, or other platforms.",
                "Listening to French audiobooks": "Start with children's stories or graded readers designed for language learners.",
                "Reading French magazines": "Fashion, sports, or special interest magazines offer vocabulary related to your interests.",
                "French cooking videos": "Food preparation videos often use repetitive, practical vocabulary with visual context.",
                "French animation/cartoons": "Children's content often uses simpler language and clear pronunciation.",
                "French documentaries": "Nature or historical documentaries often have clear narration and interesting content.",
            }

            tip = immersion_tips.get(
                selected,
                "Immerse yourself in authentic French content to develop natural language feel and cultural understanding.",
            )
            self.immersion_tip_text.config(text=f"{tip}")
        else:
            self.immersion_tip_text.config(
                text="No Activities: No immersion activities available in the database."
            )

    def generate_random_french_application(self):
        """Generate a random French application activity."""
        import random

        activities = self.data["french"]["exercises"]["application"]
        if activities:
            selected = random.choice(activities)
            self.selected_french_application_type.set(selected)
            self.application_display.config(text=selected)

            # Optional: display a tip for the application activity
            application_tips = {
                "Journal writing in French": "Even 3-5 sentences about your day can be effective practice. Use a dictionary for new words.",
                "Conversation practice with language partner": "Prepare 2-3 topics in advance so you're not stuck for things to talk about.",
                "Describing pictures in French": "Start with simple descriptions of what you see, then add more details and opinions.",
                "Translation exercises": "Try translating song lyrics or short paragraphs from English to French.",
                "Recording yourself speaking French": "Record yourself reading a dialogue, then listen back to identify pronunciation issues.",
                "Role-playing common scenarios": "Practice ordering food, asking directions, or making appointments.",
                "Writing letters/emails in French": "Try writing a thank-you note or formal request to practice different styles.",
                "Creating flashcards with new vocabulary": "Add sample sentences that show how the word is used in context.",
                "Summarizing a French article/video": "Watch or read something in French, then write or speak a summary in your own words.",
                "Retelling a story in French": "Take a familiar story and try to tell it in simple French.",
                "Making a presentation in French": "Choose a topic you're passionate about and prepare a short 2-3 minute presentation.",
                "Teaching someone else basic French": "Explaining concepts to others is a great way to solidify your own understanding.",
                "Language shadowing": "Listen to native speakers and repeat what they say with the same intonation and rhythm.",
                "Practicing formal vs. informal speech": "Take casual sentences and rewrite them in formal speech (and vice versa).",
                "Creating a mind map of related vocabulary": "Choose a theme like 'travel' and create a network of related words and phrases.",
            }

            tip = application_tips.get(
                selected,
                "Actively applying your French knowledge reinforces learning and builds real communication skills.",
            )
            self.application_tip_text.config(text=f"{tip}")
        else:
            self.application_tip_text.config(
                text="No Activities: No application activities available in the database."
            )
