"""
Habit tracker module for the Pixel Quest application.
Manages daily habits, check-ins, and streak tracking with various frequency options.
"""

import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, timedelta
import calendar

# Import tab modules with correct relative imports
from habit_tab import HabitTab
from check_in_tab import CheckInTab
from stats_tab import StatsTab
from categories_tab import CategoriesTab


class HabitTracker:
    """
    Manages the habit tracking functionality.
    Allows users to track habits with various frequencies and check-ins for important events.
    """

    def __init__(self, app, data_manager, theme):
        """
        Initialize the habit tracker module.

        Args:
            app: Main application instance
            data_manager: Data manager instance
            theme: Theme manager instance
        """
        self.app = app
        self.data_manager = data_manager
        self.data = data_manager.data
        self.theme = theme

        # Current date for the calendar views
        self.current_date = datetime.now().date()
        self.selected_month = self.current_date.month
        self.selected_year = self.current_date.year

        # Make sure the habits structure exists
        self.initialize_habits_data()

        # Initialize tabs
        self.habit_tab = HabitTab(self, app, data_manager, theme)
        self.check_in_tab = CheckInTab(self, app, data_manager, theme)
        self.stats_tab = StatsTab(self, app, data_manager, theme)
        self.categories_tab = CategoriesTab(self, app, data_manager, theme)

    def initialize_habits_data(self):
        """
        Ensure that the habit data structure exists in the data.
        If not, initialize it with default values.
        """
        if "habits" not in self.data:
            self.data["habits"] = {
                "categories": [
                    {"name": "Health", "color": "#4CAF50"},  # Green
                    {"name": "Productivity", "color": "#2196F3"},  # Blue
                    {"name": "Learning", "color": "#FF9800"},  # Orange
                    {"name": "Personal", "color": "#E91E63"},  # Pink
                ],
                "daily_habits": [
                    {
                        "name": "Early wakeup",
                        "icon": "☀️",
                        "active": True,
                        "category": "Productivity",
                        "frequency": "daily",
                        "streak": 0,
                        "completed_dates": [],
                    },
                    {
                        "name": "Exercise",
                        "icon": "🏃",
                        "active": True,
                        "category": "Health",
                        "frequency": "daily",
                        "streak": 0,
                        "completed_dates": [],
                    },
                    {
                        "name": "Reading",
                        "icon": "📚",
                        "active": True,
                        "category": "Learning",
                        "frequency": "daily",
                        "streak": 0,
                        "completed_dates": [],
                    },
                    {
                        "name": "Go to bed early",
                        "icon": "💤",
                        "active": True,
                        "category": "Health",
                        "frequency": "daily",
                        "streak": 0,
                        "completed_dates": [],
                    },
                ],
                "custom_habits": [
                    {
                        "name": "Learn Korean",
                        "icon": "🇰🇷",
                        "active": True,
                        "category": "Learning",
                        "frequency": "interval",
                        "interval": 2,
                        "streak": 0,
                        "completed_dates": [],
                    },
                    {
                        "name": "Learn French",
                        "icon": "🇫🇷",
                        "active": True,
                        "category": "Learning",
                        "frequency": "interval",
                        "interval": 2,
                        "streak": 0,
                        "completed_dates": [],
                    },
                    {
                        "name": "Clean",
                        "icon": "🧹",
                        "active": True,
                        "category": "Personal",
                        "frequency": "weekly",
                        "specific_days": [6],  # Saturday
                        "streak": 0,
                        "completed_dates": [],
                    },
                    {
                        "name": "Do Laundry",
                        "icon": "🧺",
                        "active": True,
                        "category": "Personal",
                        "frequency": "interval",
                        "interval": 5,
                        "streak": 0,
                        "completed_dates": [],
                    },
                    {
                        "name": "Water Plants",
                        "icon": "🌱",
                        "active": True,
                        "category": "Personal",
                        "frequency": "interval",
                        "interval": 10,
                        "streak": 0,
                        "completed_dates": [],
                    },
                    {
                        "name": "Be Creative",
                        "icon": "🎨",
                        "active": True,
                        "category": "Personal",
                        "frequency": "interval",
                        "interval": 2,
                        "streak": 0,
                        "completed_dates": [],
                    },
                ],
                "check_ins": [
                    {
                        "name": "Doctor Appointments",
                        "icon": "🩺",
                        "category": "Health",
                        "dates": [],
                        "notes": {},
                        "subcategories": [
                            {
                                "name": "Dermatologist",
                                "last_date": "2025-03-31",
                                "interval_months": 6,
                                "next_date": "2025-09-30",
                            },
                            {
                                "name": "Dentist",
                                "last_date": "2025-03-31",
                                "interval_months": 6,
                                "next_date": "2025-09-30",
                            },
                            {
                                "name": "Gynecologist",
                                "last_date": "2025-04-07",
                                "interval_months": 6,
                                "next_date": "2025-10-07",
                            },
                            {
                                "name": "GP",
                                "last_date": "2025-04-09",
                                "interval_months": 6,
                                "next_date": "2025-10-09",
                            },
                        ],
                    },
                ],
            }
            # Save the initialized data
            self.data_manager.save_data()
        else:
            # Update the data structure if it already exists
            self._update_existing_data()

    def _update_existing_data(self):
        """Update existing data structure with new features."""
        # Check if subcategories exist for doctor appointments
        needs_save = False

        # Add subcategories field if it doesn't exist
        for check_in in self.data["habits"].get("check_ins", []):
            if (
                check_in["name"] == "Doctor Appointments"
                and "subcategories" not in check_in
            ):
                check_in["subcategories"] = [
                    {
                        "name": "Dermatologist",
                        "last_date": "2025-03-31",
                        "interval_months": 6,
                        "next_date": "2025-09-30",
                    },
                    {
                        "name": "Dentist",
                        "last_date": "2025-03-31",
                        "interval_months": 6,
                        "next_date": "2025-09-30",
                    },
                    {
                        "name": "Gynecologist",
                        "last_date": "2025-04-07",
                        "interval_months": 6,
                        "next_date": "2025-10-07",
                    },
                    {
                        "name": "GP",
                        "last_date": "2025-04-09",
                        "interval_months": 6,
                        "next_date": "2025-10-09",
                    },
                ]
                needs_save = True

        # Ensure default categories exist
        if "categories" not in self.data["habits"]:
            self.data["habits"]["categories"] = [
                {"name": "Health", "color": "#4CAF50"},
                {"name": "Productivity", "color": "#2196F3"},
                {"name": "Learning", "color": "#FF9800"},
                {"name": "Personal", "color": "#E91E63"},
            ]
            needs_save = True

        # Update habit data with requested changes
        self._update_habits_list()

        # Save if changes were made
        if needs_save:
            self.data_manager.save_data()

    def _update_habits_list(self):
        """Update the habits list with the requested changes."""
        # Remove meditation and drink water habits
        daily_habits = self.data["habits"].get("daily_habits", [])
        custom_habits = self.data["habits"].get("custom_habits", [])

        for habit_list in [daily_habits, custom_habits]:
            to_remove = []
            for i, habit in enumerate(habit_list):
                if habit["name"] in ["Meditation", "Drink water"]:
                    to_remove.append(i)

            # Remove in reverse order to avoid index issues
            for i in sorted(to_remove, reverse=True):
                if i < len(habit_list):
                    del habit_list[i]

        # Add the new habits if they don't exist
        new_daily_habits = [
            {
                "name": "Go to bed early",
                "icon": "💤",
                "active": True,
                "category": "Health",
                "frequency": "daily",
                "streak": 0,
                "completed_dates": [],
            }
        ]

        new_custom_habits = [
            {
                "name": "Learn Korean",
                "icon": "🇰🇷",
                "active": True,
                "category": "Learning",
                "frequency": "interval",
                "interval": 2,
                "streak": 0,
                "completed_dates": [],
            },
            {
                "name": "Learn French",
                "icon": "🇫🇷",
                "active": True,
                "category": "Learning",
                "frequency": "interval",
                "interval": 2,
                "streak": 0,
                "completed_dates": [],
            },
            {
                "name": "Clean",
                "icon": "🧹",
                "active": True,
                "category": "Personal",
                "frequency": "weekly",
                "specific_days": [6],  # Saturday
                "streak": 0,
                "completed_dates": [],
            },
            {
                "name": "Do Laundry",
                "icon": "🧺",
                "active": True,
                "category": "Personal",
                "frequency": "interval",
                "interval": 5,
                "streak": 0,
                "completed_dates": [],
            },
            {
                "name": "Water Plants",
                "icon": "🌱",
                "active": True,
                "category": "Personal",
                "frequency": "interval",
                "interval": 10,
                "streak": 0,
                "completed_dates": [],
            },
            {
                "name": "Be Creative",
                "icon": "🎨",
                "active": True,
                "category": "Personal",
                "frequency": "interval",
                "interval": 2,
                "streak": 0,
                "completed_dates": [],
            },
        ]

        # Add new daily habits if they don't exist
        existing_daily_names = [h["name"] for h in daily_habits]
        for habit in new_daily_habits:
            if habit["name"] not in existing_daily_names:
                daily_habits.append(habit)

        # Add new custom habits if they don't exist
        existing_custom_names = [h["name"] for h in custom_habits]
        for habit in new_custom_habits:
            if habit["name"] not in existing_custom_names:
                custom_habits.append(habit)

        # Update the habits lists
        self.data["habits"]["daily_habits"] = daily_habits
        self.data["habits"]["custom_habits"] = custom_habits

        # Save the changes
        self.data_manager.save_data()

    def show_module(self, parent_frame):
        """
        Show the habit tracker interface.

        Args:
            parent_frame: Parent frame to place habit tracker content
        """
        # Title
        title_label = tk.Label(
            parent_frame,
            text="HABIT TRACKER",
            font=self.theme.heading_font,
            bg=self.theme.bg_color,
            fg=self.theme.habit_color,  # Use the theme's habit color
        )
        title_label.pack(pady=20)

        # Create tabs for different views
        tab_control = ttk.Notebook(parent_frame)
        tab_control.pack(expand=1, fill="both", padx=10, pady=10)

        # Create tabs
        habits_tab = tk.Frame(tab_control, bg=self.theme.bg_color)
        check_ins_tab = tk.Frame(tab_control, bg=self.theme.bg_color)
        stats_tab = tk.Frame(tab_control, bg=self.theme.bg_color)
        categories_tab = tk.Frame(tab_control, bg=self.theme.bg_color)

        tab_control.add(habits_tab, text="Daily Habits")
        tab_control.add(check_ins_tab, text="Check-ins")
        tab_control.add(stats_tab, text="Statistics")
        tab_control.add(categories_tab, text="Categories")

        # Fill the tabs with content
        self.habit_tab.create_habits_view(habits_tab)
        self.check_in_tab.create_check_ins_view(check_ins_tab)
        self.stats_tab.create_stats_view(stats_tab)
        self.categories_tab.create_categories_view(categories_tab)

        # Back button
        back_button = self.theme.create_pixel_button(
            parent_frame,
            "Back to Main Menu",
            self.app.show_main_menu,
            color="#9E9E9E",
        )
        back_button.pack(pady=20)

    def refresh_display(self):
        """Refresh the habit tracker display."""
        # Get the current notebook tab
        current_tab = self.app.main_frame.winfo_children()[1].index("current")

        # Clear the main frame
        self.app.clear_frame()

        # Recreate the habit tracker
        self.show_module(self.app.main_frame)

        # Set the active tab back to what it was
        self.app.main_frame.winfo_children()[1].select(current_tab)
