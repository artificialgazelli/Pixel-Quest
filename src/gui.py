"""
Main GUI components for the Pixel Quest application.
"""

import tkinter as tk
from tkinter import ttk
from datetime import datetime, timedelta
from src.theme import PixelTheme
from src.data_manager import DataManager
from src.modules.art_module import ArtModule
from src.modules.korean_module import KoreanModule
from src.modules.french_module import FrenchModule
from src.modules.diss_module import DissModule
from src.modules.statistics import StatisticsModule
from src.modules.settings import SettingsModule
from src.modules.rewards import RewardsModule
from src.modules.habit_tracker import HabitTracker
from src.modules.todo_list import TodoList


class QuestGame:
    """
    Main application class for the Pixel Quest game.
    Manages the main window, theme, and navigation between modules.
    """

    def __init__(self, root):
        """
        Initialize the Quest Game application.

        Args:
            root: The root Tkinter window
        """
        self.root = root
        self.root.title("Pixel Quest - Skill Development")
        self.root.geometry("800x600")  # Increased height for new functionality

        # Set up pixel art theme
        self.theme = PixelTheme(self.root)

        # Initialize data manager
        self.data_manager = DataManager()
        self.data = self.data_manager.data

        # Main frame
        self.main_frame = tk.Frame(self.root, bg=self.theme.bg_color)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Initialize modules
        self.initialize_modules()

        # Ensure all modules are initialized before showing the main menu
        self.show_main_menu()

    def initialize_modules(self):
        """Initialize all the application modules."""
        # Module initialization
        self.art_module = ArtModule(self, self.data_manager, self.theme)
        self.korean_module = KoreanModule(self, self.data_manager, self.theme)
        self.french_module = FrenchModule(self, self.data_manager, self.theme)
        self.diss_module = DissModule(self, self.data_manager, self.theme)
        self.statistics_module = StatisticsModule(self, self.data_manager, self.theme)
        self.settings_module = SettingsModule(self, self.data_manager, self.theme)
        self.rewards_module = RewardsModule(self, self.data_manager, self.theme)
        self.habit_tracker = HabitTracker(self, self.data_manager, self.theme)
        self.todo_list = TodoList(self, self.data_manager, self.theme)

    def clear_frame(self):
        """Clear all widgets from the main frame."""
        for widget in self.main_frame.winfo_children():
            widget.destroy()

    def show_main_menu(self):
        """Display the main menu with options for each module."""
        self.clear_frame()

        # Title
        title_label = tk.Label(
            self.main_frame,
            text="SKILL QUEST 2025",
            font=self.theme.heading_font,
            bg=self.theme.bg_color,
            fg=self.theme.text_color,
        )
        title_label.pack(pady=20)

        # Description
        desc_label = tk.Label(
            self.main_frame,
            text="Choose your skill adventure!",
            font=self.theme.pixel_font,
            bg=self.theme.bg_color,
            fg=self.theme.text_color,
        )
        desc_label.pack(pady=10)

        # Menu tabs with pixel art styling
        tab_control = ttk.Notebook(self.main_frame)
        tab_control.pack(expand=1, fill="both", padx=10, pady=10)

        # Create tabs
        modules_tab = tk.Frame(tab_control, bg=self.theme.bg_color)
        rewards_tab = tk.Frame(tab_control, bg=self.theme.bg_color)
        stats_tab = tk.Frame(tab_control, bg=self.theme.bg_color)
        settings_tab = tk.Frame(tab_control, bg=self.theme.bg_color)

        tab_control.add(modules_tab, text="Modules")
        tab_control.add(rewards_tab, text="Rewards")
        tab_control.add(stats_tab, text="Statistics")
        tab_control.add(settings_tab, text="Settings")

        # === MODULES TAB ===
        self.create_modules_tab(modules_tab)

        # === REWARDS TAB ===
        self.rewards_module.create_rewards_tab(rewards_tab)

        # === STATISTICS TAB ===
        self.statistics_module.create_statistics_tab(stats_tab)

        # === SETTINGS TAB ===
        self.settings_module.create_settings_tab(settings_tab)

    def create_modules_tab(self, parent):
        """
        Create the modules tab content with pixel art styling and centered buttons.

        Args:
            parent: Parent widget
        """
        # Module buttons frame - use pack instead of grid for better centering
        buttons_frame = tk.Frame(parent, bg=self.theme.bg_color)
        buttons_frame.pack(pady=10, fill=tk.BOTH, expand=True)

        # Center container frame for the modules
        center_frame = tk.Frame(buttons_frame, bg=self.theme.bg_color)
        center_frame.pack(expand=True)

        # Module buttons with status
        # Art module button
        art_frame = tk.Frame(
            center_frame,
            bg=self.theme.bg_color,
            padx=10,
            pady=10,
            relief=tk.RIDGE,
            bd=3,
        )
        art_frame.pack(side=tk.LEFT, padx=10, pady=10)

        art_button = self.theme.create_pixel_button(
            art_frame,
            "Art Quest",
            lambda: self.show_module("art"),
            color=self.theme.art_color,
            width=10,
            height=2,
        )
        art_button.pack()

        art_status = tk.Label(
            art_frame,
            text=f"Level: {self.data['art']['level']} | Points: {self.data['art']['points']}",
            font=self.theme.small_font,
            bg=self.theme.bg_color,
            fg=self.theme.text_color,
        )
        art_status.pack(pady=5)

        # Add streak display
        art_streak = tk.Label(
            art_frame,
            text=f"Current Streak: {self.data['art']['streak']} days",
            font=self.theme.small_font,
            bg=self.theme.bg_color,
            fg="#FF5722",
        )
        art_streak.pack()

        # Korean module button
        korean_frame = tk.Frame(
            center_frame,
            bg=self.theme.bg_color,
            padx=10,
            pady=10,
            relief=tk.RIDGE,
            bd=3,
        )
        korean_frame.pack(side=tk.LEFT, padx=10, pady=10)

        korean_button = self.theme.create_pixel_button(
            korean_frame,
            "Korean Quest",
            lambda: self.show_module("korean"),
            color=self.theme.korean_color,
            width=10,
            height=2,
        )
        korean_button.pack()

        korean_status = tk.Label(
            korean_frame,
            text=f"Level: {self.data['korean']['level']} | Points: {self.data['korean']['points']}",
            font=self.theme.small_font,
            bg=self.theme.bg_color,
            fg=self.theme.text_color,
        )
        korean_status.pack(pady=5)

        # Add streak display
        korean_streak = tk.Label(
            korean_frame,
            text=f"Current Streak: {self.data['korean']['streak']} days",
            font=self.theme.small_font,
            bg=self.theme.bg_color,
            fg="#FF5722",
        )
        korean_streak.pack()

        # French module button
        french_frame = tk.Frame(
            center_frame,
            bg=self.theme.bg_color,
            padx=10,
            pady=10,
            relief=tk.RIDGE,
            bd=3,
        )
        french_frame.pack(side=tk.LEFT, padx=10, pady=10)

        french_button = self.theme.create_pixel_button(
            french_frame,
            "French Quest",
            lambda: self.show_module("french"),
            color=self.theme.french_color,
            width=10,
            height=2,
        )
        french_button.pack()

        french_status = tk.Label(
            french_frame,
            text=f"Level: {self.data['french']['level']} | Points: {self.data['french']['points']}",
            font=self.theme.small_font,
            bg=self.theme.bg_color,
            fg=self.theme.text_color,
        )
        french_status.pack(pady=5)

        # Add streak display
        french_streak = tk.Label(
            french_frame,
            text=f"Current Streak: {self.data['french']['streak']} days",
            font=self.theme.small_font,
            bg=self.theme.bg_color,
            fg="#FF5722",
        )
        french_streak.pack()

        # Dissertation module button
        diss_frame = tk.Frame(
            center_frame,
            bg=self.theme.bg_color,
            padx=10,
            pady=10,
            relief=tk.RIDGE,
            bd=3,
        )
        diss_frame.pack(side=tk.LEFT, padx=10, pady=10)

        diss_button = self.theme.create_pixel_button(
            diss_frame,
            "Diss Quest",
            lambda: self.show_module("diss"),
            color=self.theme.diss_color,
            width=10,
            height=2,
        )
        diss_button.pack()

        diss_status = tk.Label(
            diss_frame,
            text=f"Level: {self.data['diss']['level']} | Points: {self.data['diss']['points']}",
            font=self.theme.small_font,
            bg=self.theme.bg_color,
            fg=self.theme.text_color,
        )
        diss_status.pack(pady=5)

        # Add streak display
        diss_streak = tk.Label(
            diss_frame,
            text=f"Current Streak: {self.data['diss']['streak']} days",
            font=self.theme.small_font,
            bg=self.theme.bg_color,
            fg="#FF5722",
        )
        diss_streak.pack()

        # Daily Dashboard section - combines Habits and ToDo
        daily_dashboard = tk.LabelFrame(
            parent,
            text="Daily Dashboard",
            font=self.theme.pixel_font,
            bg=self.theme.bg_color,
            fg=self.theme.text_color,
            padx=10,
            pady=10,
            relief=tk.RIDGE,
            bd=3,
        )
        daily_dashboard.pack(fill=tk.BOTH, expand=True, pady=10, padx=20)

        # Create a two-column layout for habits and tasks
        dashboard_frame = tk.Frame(daily_dashboard, bg=self.theme.bg_color)
        dashboard_frame.pack(fill=tk.BOTH, expand=True)

        # Left column - Daily Habits
        habits_frame = tk.LabelFrame(
            dashboard_frame,
            text="Today's Habits",
            font=self.theme.pixel_font,
            bg=self.theme.bg_color,
            fg=self.theme.habit_color,
            padx=5,
            pady=5,
        )
        habits_frame.grid(row=0, column=0, padx=10, pady=5, sticky="nsew")

        # Display today's habits
        self.display_todays_habits(habits_frame)

        # Right column - Daily Tasks
        tasks_frame = tk.LabelFrame(
            dashboard_frame,
            text="Today's Tasks",
            font=self.theme.pixel_font,
            bg=self.theme.bg_color,
            fg=self.theme.todo_color,
            padx=5,
            pady=5,
        )
        tasks_frame.grid(row=0, column=1, padx=10, pady=5, sticky="nsew")

        # Display today's tasks
        self.display_todays_tasks(tasks_frame)

        # Set weight to make columns equal width
        dashboard_frame.columnconfigure(0, weight=1)
        dashboard_frame.columnconfigure(1, weight=1)

        # Bottom controls - quick access buttons
        controls_frame = tk.Frame(daily_dashboard, bg=self.theme.bg_color)
        controls_frame.pack(fill=tk.X, pady=10)

        # Habit Tracker button
        habit_button = self.theme.create_pixel_button(
            controls_frame,
            "Open Habit Tracker",
            lambda: self.show_module("habits"),
            color=self.theme.habit_color,
        )
        habit_button.pack(side=tk.LEFT, padx=20)

        # To Do List button
        todo_button = self.theme.create_pixel_button(
            controls_frame,
            "Open To Do List",
            lambda: self.show_module("todo"),
            color=self.theme.todo_color,
        )
        todo_button.pack(side=tk.LEFT, padx=20)

        # Add New Task button
        new_task_button = self.theme.create_pixel_button(
            controls_frame,
            "Add New Task",
            lambda: self.todo_list.todo_tab.add_new_task(),
            color="#4CAF50",
        )
        new_task_button.pack(side=tk.RIGHT, padx=20)

        # Add New Habit button
        new_habit_button = self.theme.create_pixel_button(
            controls_frame,
            "Add New Habit",
            lambda: self.habit_tracker.habit_tab.add_new_habit(),
            color="#2196F3",
        )
        new_habit_button.pack(side=tk.RIGHT, padx=20)

    def display_todays_habits(self, parent):
        """
        Display today's habits with checkboxes.

        Args:
            parent: Parent widget to place the habits
        """
        # Get today's date
        today = datetime.now().date().strftime("%Y-%m-%d")

        # Get habits that are active for today
        habits = self.data.get("habits", {})
        all_habits = []

        # Combine daily and custom habits
        for habit_type in ["daily_habits", "custom_habits"]:
            for habit in habits.get(habit_type, []):
                if habit.get("active", True):
                    all_habits.append(habit)

        # Filter habits that should be active today
        todays_habits = []
        for habit in all_habits:
            frequency = habit.get("frequency", "daily")
            if frequency == "daily":
                todays_habits.append(habit)
            elif frequency == "weekly":
                # Check if today's weekday is in specific days
                day_of_week = datetime.now().weekday()
                # Convert to 0=Sunday format to match the app's convention
                day_of_week = (day_of_week + 1) % 7
                if day_of_week in habit.get("specific_days", [0, 1, 2, 3, 4, 5, 6]):
                    todays_habits.append(habit)
            elif frequency == "interval":
                # This would require more complex logic to determine if today falls in the interval
                # For simplicity, we'll include it if it's not completed yet today
                if today not in habit.get("completed_dates", []):
                    todays_habits.append(habit)

        # Sort habits by completion status (incomplete first)
        todays_habits.sort(key=lambda h: today in h.get("completed_dates", []))

        if not todays_habits:
            tk.Label(
                parent,
                text="No habits for today.",
                font=self.theme.small_font,
                bg=self.theme.bg_color,
                fg=self.theme.text_color,
            ).pack(pady=20)
            return

        # Create a scrollframe if there are many habits
        canvas = tk.Canvas(parent, bg=self.theme.bg_color, highlightthickness=0)
        scrollbar = ttk.Scrollbar(parent, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=self.theme.bg_color)

        scrollable_frame.bind(
            "<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True, padx=5, pady=5)
        scrollbar.pack(side="right", fill="y")

        # Category colors for better visual organization
        category_colors = {}
        for category in habits.get("categories", []):
            category_colors[category["name"]] = category["color"]

        # Display each habit with a checkbox
        for i, habit in enumerate(todays_habits):
            # Row background alternates for better readability
            row_bg = (
                self.theme.bg_color
                if i % 2 == 0
                else self.theme.darken_color(self.theme.bg_color)
            )

            # Get category and color
            category = habit.get("category", "Personal")
            category_color = category_colors.get(category, self.theme.habit_color)

            # Create habit row
            habit_frame = tk.Frame(scrollable_frame, bg=row_bg, pady=2)
            habit_frame.pack(fill=tk.X)

            # Check if completed today
            completed = today in habit.get("completed_dates", [])

            # Checkbox for completion status
            if completed:
                status_btn = tk.Button(
                    habit_frame,
                    text="✓",
                    font=self.theme.small_font,
                    bg="#4CAF50",  # Green for completed
                    fg="white",
                    width=2,
                    relief=tk.FLAT,
                    command=lambda h=habit["name"]: self.toggle_habit_completion(h),
                )
            else:
                status_btn = tk.Button(
                    habit_frame,
                    text="☐",
                    font=self.theme.small_font,
                    bg=self.theme.primary_color,
                    fg=self.theme.text_color,
                    width=2,
                    relief=tk.FLAT,
                    command=lambda h=habit["name"]: self.toggle_habit_completion(h),
                )
            status_btn.pack(side=tk.LEFT, padx=5)

            # Category color indicator
            color_indicator = tk.Frame(
                habit_frame, bg=category_color, width=3, height=20
            )
            color_indicator.pack(side=tk.LEFT, padx=2)

            # Habit icon and name
            habit_label = tk.Label(
                habit_frame,
                text=f"{habit.get('icon', '📋')} {habit['name']}",
                font=self.theme.small_font,
                bg=row_bg,
                fg=self.theme.text_color if not completed else "#888888",
                anchor="w",
            )
            habit_label.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)

            # Streak display
            streak_label = tk.Label(
                habit_frame,
                text=f"🔥 {habit.get('streak', 0)}",
                font=self.theme.small_font,
                bg=row_bg,
                fg="#FF5722",
                width=5,
            )
            streak_label.pack(side=tk.RIGHT, padx=5)

        # Display habit completion summary
        completed_count = sum(
            1 for h in todays_habits if today in h.get("completed_dates", [])
        )
        total_count = len(todays_habits)
        completion_pct = (
            int((completed_count / total_count) * 100) if total_count > 0 else 0
        )

        summary_frame = tk.Frame(parent, bg=self.theme.bg_color)
        summary_frame.pack(fill=tk.X, pady=5)

        summary_label = tk.Label(
            summary_frame,
            text=f"Completed: {completed_count}/{total_count} ({completion_pct}%)",
            font=self.theme.small_font,
            bg=self.theme.bg_color,
            fg="#4CAF50"
            if completion_pct >= 80
            else "#FFC107"
            if completion_pct >= 50
            else "#F44336",
        )
        summary_label.pack(pady=5)

    def display_todays_tasks(self, parent):
        """
        Display today's tasks with checkboxes.

        Args:
            parent: Parent widget to place the tasks
        """
        # Get today's date
        today = datetime.now().date().strftime("%Y-%m-%d")

        # Get tasks due today or overdue
        tasks = self.data.get("todo", {}).get("tasks", [])
        active_tasks = [task for task in tasks if task.get("status") == "active"]

        # Filter tasks due today or overdue
        todays_tasks = []
        for task in active_tasks:
            due_date = task.get("due_date")
            if due_date:
                task_date = datetime.strptime(due_date, "%Y-%m-%d").date()
                today_date = datetime.now().date()
                if task_date <= today_date:
                    todays_tasks.append(task)

        # Sort tasks: overdue first, then by priority (high, medium, low)
        priority_map = {"high": 0, "medium": 1, "low": 2, None: 3}

        def task_sort_key(task):
            due_date = datetime.strptime(
                task.get("due_date", "9999-12-31"), "%Y-%m-%d"
            ).date()
            priority_value = priority_map.get(task.get("priority"))
            return (due_date, priority_value)

        todays_tasks.sort(key=task_sort_key)

        if not todays_tasks:
            tk.Label(
                parent,
                text="No tasks for today.",
                font=self.theme.small_font,
                bg=self.theme.bg_color,
                fg=self.theme.text_color,
            ).pack(pady=20)
            return

        # Create a scrollframe if there are many tasks
        canvas = tk.Canvas(parent, bg=self.theme.bg_color, highlightthickness=0)
        scrollbar = ttk.Scrollbar(parent, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=self.theme.bg_color)

        scrollable_frame.bind(
            "<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True, padx=5, pady=5)
        scrollbar.pack(side="right", fill="y")

        # Get group colors
        group_colors = {}
        for group in self.data["todo"].get("groups", []):
            group_colors[group["name"]] = group["color"]

        # Display each task with a checkbox
        for i, task in enumerate(todays_tasks):
            # Row background alternates for better readability
            row_bg = (
                self.theme.bg_color
                if i % 2 == 0
                else self.theme.darken_color(self.theme.bg_color)
            )

            # Get group and color
            group = task.get("group", "")
            group_color = group_colors.get(group, "#999999")

            # Get priority color
            priority = task.get("priority", "")
            priority_colors = {
                "high": "#F44336",  # Red
                "medium": "#FF9800",  # Orange
                "low": "#4CAF50",  # Green
            }
            priority_color = priority_colors.get(priority, self.theme.text_color)

            # Create task row
            task_frame = tk.Frame(scrollable_frame, bg=row_bg, pady=2)
            task_frame.pack(fill=tk.X)

            # Checkbox for completion
            status_btn = tk.Button(
                task_frame,
                text="☐",
                font=self.theme.small_font,
                bg=self.theme.primary_color,
                fg=self.theme.text_color,
                width=2,
                relief=tk.FLAT,
                command=lambda t=task["id"]: self.complete_task(t),
            )
            status_btn.pack(side=tk.LEFT, padx=5)

            # Priority indicator
            if priority == "high":
                priority_indicator = tk.Label(
                    task_frame,
                    text="⚑",
                    font=self.theme.small_font,
                    bg=row_bg,
                    fg=priority_color,
                )
                priority_indicator.pack(side=tk.LEFT)

            # Task title
            task_label = tk.Label(
                task_frame,
                text=task.get("title", ""),
                font=self.theme.small_font,
                bg=row_bg,
                fg=self.theme.text_color,
                anchor="w",
            )
            task_label.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)

            # Due date with color coding
            due_date = task.get("due_date", "")
            if due_date:
                try:
                    due_date_obj = datetime.strptime(due_date, "%Y-%m-%d").date()
                    today_date = datetime.now().date()

                    # Determine date color based on due date
                    if due_date_obj < today_date:
                        date_color = "#F44336"  # Red for overdue
                        date_text = f"⚠️ {due_date_obj.strftime('%m/%d')}"
                    elif due_date_obj == today_date:
                        date_color = "#FF9800"  # Orange for today
                        date_text = f"Today"
                    else:
                        date_color = self.theme.text_color
                        date_text = due_date_obj.strftime("%m/%d")

                    date_label = tk.Label(
                        task_frame,
                        text=date_text,
                        font=self.theme.small_font,
                        bg=row_bg,
                        fg=date_color,
                    )
                    date_label.pack(side=tk.RIGHT, padx=5)
                except ValueError:
                    pass

            # Group indicator (small colored circle)
            group_frame = tk.Frame(task_frame, bg=row_bg)
            group_frame.pack(side=tk.RIGHT, padx=5)

            group_indicator = tk.Frame(group_frame, bg=group_color, width=10, height=10)
            group_indicator.pack(side=tk.LEFT)

            group_label = tk.Label(
                group_frame,
                text=group,
                font=self.theme.small_font,
                bg=row_bg,
                fg=self.theme.text_color,
            )
            group_label.pack(side=tk.LEFT, padx=2)

        # Display task summary
        overdue_tasks = [
            task
            for task in todays_tasks
            if datetime.strptime(task.get("due_date", "9999-12-31"), "%Y-%m-%d").date()
            < datetime.now().date()
        ]
        due_today = [
            task
            for task in todays_tasks
            if datetime.strptime(task.get("due_date", "9999-12-31"), "%Y-%m-%d").date()
            == datetime.now().date()
        ]

        summary_frame = tk.Frame(parent, bg=self.theme.bg_color)
        summary_frame.pack(fill=tk.X, pady=5)

        summary_text = f"Due today: {len(due_today)}"
        if overdue_tasks:
            summary_text += f" | Overdue: {len(overdue_tasks)}"

        summary_label = tk.Label(
            summary_frame,
            text=summary_text,
            font=self.theme.small_font,
            bg=self.theme.bg_color,
            fg="#F44336" if overdue_tasks else self.theme.text_color,
        )
        summary_label.pack(pady=5)

    def toggle_habit_completion(self, habit_name):
        """
        Toggle a habit's completion status for today.

        Args:
            habit_name: Name of the habit to toggle
        """
        # Find the habit
        habit = None
        habit_list = None
        habit_index = -1

        # Get today's date
        today = datetime.now().date().strftime("%Y-%m-%d")

        # Check in daily habits
        for i, h in enumerate(self.data.get("habits", {}).get("daily_habits", [])):
            if h["name"] == habit_name:
                habit = h
                habit_list = "daily_habits"
                habit_index = i
                break

        # If not found in daily habits, check custom habits
        if habit is None:
            for i, h in enumerate(self.data.get("habits", {}).get("custom_habits", [])):
                if h["name"] == habit_name:
                    habit = h
                    habit_list = "custom_habits"
                    habit_index = i
                    break

        if habit is None:
            return

        # Get completed dates list
        completed_dates = habit.get("completed_dates", [])

        # Toggle the date
        if today in completed_dates:
            # Remove date if already completed
            completed_dates.remove(today)
        else:
            # Add date if not completed
            completed_dates.append(today)

        # Update the habit
        self.data["habits"][habit_list][habit_index]["completed_dates"] = (
            completed_dates
        )

        # Update the streak
        self.habit_tracker.habit_tab.update_habit_streak(habit_list, habit_index)

        # Save data
        self.data_manager.save_data()

        # Refresh the display
        self.show_main_menu()
