"""
Stats tab module for the Pixel Quest habit tracker.
Displays statistics, completion rates, and performance metrics for habits.
"""

import tkinter as tk
from tkinter import ttk
from datetime import datetime, timedelta


class StatsTab:
    """
    Manages the statistics tab of the habit tracker.
    Displays habit performance metrics, category breakdowns, and completion rates.
    """

    def __init__(self, habit_tracker, app, data_manager, theme):
        """
        Initialize the stats tab module.

        Args:
            habit_tracker: Main habit tracker instance
            app: Main application instance
            data_manager: Data manager instance
            theme: Theme manager instance
        """
        self.habit_tracker = habit_tracker
        self.app = app
        self.data_manager = data_manager
        self.data = data_manager.data
        self.theme = theme

    def create_stats_view(self, parent):
        """
        Create the statistics tab view with habit performance metrics.

        Args:
            parent: Parent frame to place the statistics view
        """
        # Create a scrollable container for all stats sections
        canvas = tk.Canvas(parent, bg=self.theme.bg_color, highlightthickness=0)
        scrollbar = ttk.Scrollbar(parent, orient="vertical", command=canvas.yview)

        scroll_frame = tk.Frame(canvas, bg=self.theme.bg_color)
        scroll_frame.bind(
            "<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Stats overview
        self.create_overview_section(scroll_frame)

        # Category breakdown
        self.create_category_section(scroll_frame)

        # Habit performance chart
        self.create_performance_section(scroll_frame)

    def create_overview_section(self, parent):
        """
        Create the overview section showing general habit statistics.

        Args:
            parent: Parent frame to place the overview section
        """
        overview_frame = tk.LabelFrame(
            parent,
            text="Habit Overview",
            font=self.theme.pixel_font,
            bg=self.theme.bg_color,
            fg=self.theme.habit_color,
        )
        overview_frame.pack(fill=tk.X, padx=10, pady=10)

        # Calculate stats
        habits = self.data.get("habits", {}).get("daily_habits", []) + self.data.get(
            "habits", {}
        ).get("custom_habits", [])

        total_habits = len(habits)
        active_habits = sum(1 for h in habits if h.get("active", True))

        # Today's date
        today = datetime.now().date().strftime("%Y-%m-%d")

        # Count habits completed today
        completed_today = sum(
            1
            for h in habits
            if h.get("active", True) and today in h.get("completed_dates", [])
        )

        completion_rate = (
            int((completed_today / active_habits) * 100) if active_habits > 0 else 0
        )

        # Calculate longest streak
        longest_streak = max([h.get("streak", 0) for h in habits], default=0)

        # Find habit with longest streak
        longest_streak_habit = None
        for h in habits:
            if h.get("streak", 0) == longest_streak and longest_streak > 0:
                longest_streak_habit = h["name"]
                break

        # Stats grid
        stats_grid = tk.Frame(overview_frame, bg=self.theme.bg_color)
        stats_grid.pack(fill=tk.X, padx=10, pady=10)

        # Total habits
        stat_frame = tk.Frame(stats_grid, bg=self.theme.bg_color, padx=10, pady=10)
        stat_frame.grid(row=0, column=0, padx=10, pady=10)

        tk.Label(
            stat_frame,
            text="📋 Total Habits",
            font=self.theme.small_font,
            bg=self.theme.bg_color,
            fg=self.theme.text_color,
        ).pack()

        tk.Label(
            stat_frame,
            text=str(total_habits),
            font=self.theme.heading_font,
            bg=self.theme.bg_color,
            fg=self.theme.habit_color,
        ).pack()

        # Active habits
        stat_frame = tk.Frame(stats_grid, bg=self.theme.bg_color, padx=10, pady=10)
        stat_frame.grid(row=0, column=1, padx=10, pady=10)

        tk.Label(
            stat_frame,
            text="✅ Active Habits",
            font=self.theme.small_font,
            bg=self.theme.bg_color,
            fg=self.theme.text_color,
        ).pack()

        tk.Label(
            stat_frame,
            text=str(active_habits),
            font=self.theme.heading_font,
            bg=self.theme.bg_color,
            fg="#4CAF50",  # Green
        ).pack()

        # Today's completion
        stat_frame = tk.Frame(stats_grid, bg=self.theme.bg_color, padx=10, pady=10)
        stat_frame.grid(row=0, column=2, padx=10, pady=10)

        tk.Label(
            stat_frame,
            text="🔄 Today's Completion",
            font=self.theme.small_font,
            bg=self.theme.bg_color,
            fg=self.theme.text_color,
        ).pack()

        tk.Label(
            stat_frame,
            text=f"{completion_rate}%",
            font=self.theme.heading_font,
            bg=self.theme.bg_color,
            fg="#2196F3",  # Blue
        ).pack()

        # Longest streak
        stat_frame = tk.Frame(stats_grid, bg=self.theme.bg_color, padx=10, pady=10)
        stat_frame.grid(row=0, column=3, padx=10, pady=10)

        tk.Label(
            stat_frame,
            text="🔥 Longest Streak",
            font=self.theme.small_font,
            bg=self.theme.bg_color,
            fg=self.theme.text_color,
        ).pack()

        tk.Label(
            stat_frame,
            text=f"{longest_streak} days",
            font=self.theme.heading_font,
            bg=self.theme.bg_color,
            fg="#FF5722",  # Orange
        ).pack()

        if longest_streak_habit:
            tk.Label(
                stat_frame,
                text=f"({longest_streak_habit})",
                font=("TkDefaultFont", 8),
                bg=self.theme.bg_color,
                fg=self.theme.text_color,
            ).pack()

        # Weekly statistics
        weekly_frame = tk.Frame(overview_frame, bg=self.theme.bg_color)
        weekly_frame.pack(fill=tk.X, padx=10, pady=10)

        tk.Label(
            weekly_frame,
            text="Weekly Progress",
            font=self.theme.pixel_font,
            bg=self.theme.bg_color,
            fg=self.theme.text_color,
        ).pack(anchor="w", pady=5)

        # Calculate completion rate for each day of the past week
        today = datetime.now().date()
        days = []
        completion_rates = []

        for i in range(6, -1, -1):
            day = today - timedelta(days=i)
            day_str = day.strftime("%Y-%m-%d")
            day_name = day.strftime("%a")

            # Count active habits for this day
            active_day_habits = 0
            completed_day_habits = 0

            for habit in habits:
                if not habit.get("active", True):
                    continue

                # Check if this habit should be active on this day
                is_active = self.is_active_date_for_habit(habit, day)

                if is_active:
                    active_day_habits += 1
                    if day_str in habit.get("completed_dates", []):
                        completed_day_habits += 1

            # Calculate completion rate
            day_rate = (
                int((completed_day_habits / active_day_habits) * 100)
                if active_day_habits > 0
                else 0
            )

            days.append(day_name)
            completion_rates.append(day_rate)

        # Create weekly progress bars
        weekly_grid = tk.Frame(weekly_frame, bg=self.theme.bg_color)
        weekly_grid.pack(fill=tk.X, pady=5)

        for i, (day, rate) in enumerate(zip(days, completion_rates)):
            day_frame = tk.Frame(weekly_grid, bg=self.theme.bg_color)
            day_frame.grid(row=0, column=i, padx=5, pady=5)

            # Day name
            tk.Label(
                day_frame,
                text=day,
                font=self.theme.small_font,
                bg=self.theme.bg_color,
                fg=self.theme.text_color,
                width=4,
            ).pack(anchor="w")

            # Progress bar background
            bar_bg = tk.Frame(
                day_frame,
                bg=self.theme.darken_color(self.theme.primary_color),
                height=100,
                width=20,
            )
            bar_bg.pack(pady=2)

            # Bar height based on completion rate
            bar_height = rate * 100 // 100

            # Determine color based on completion rate
            if rate >= 80:
                bar_color = "#4CAF50"  # Green for high completion
            elif rate >= 50:
                bar_color = "#FFC107"  # Yellow for medium completion
            else:
                bar_color = "#F44336"  # Red for low completion

            # Progress bar
            bar = tk.Frame(
                bar_bg,
                bg=bar_color,
                height=bar_height,
                width=20,
            )
            bar.place(x=0, y=100 - bar_height)

            # Percentage label
            tk.Label(
                day_frame,
                text=f"{rate}%",
                font=("TkDefaultFont", 8),
                bg=self.theme.bg_color,
                fg=self.theme.text_color,
            ).pack()

    def create_category_section(self, parent):
        """
        Create the category breakdown section.

        Args:
            parent: Parent frame to place the category breakdown
        """
        category_frame = tk.LabelFrame(
            parent,
            text="Habits by Category",
            font=self.theme.pixel_font,
            bg=self.theme.bg_color,
            fg=self.theme.habit_color,
        )
        category_frame.pack(fill=tk.X, padx=10, pady=10)

        # Get categories and counts
        categories = self.data["habits"].get("categories", [])
        habits = self.data.get("habits", {}).get("daily_habits", []) + self.data.get(
            "habits", {}
        ).get("custom_habits", [])

        category_counts = {}
        category_completion = {}
        today = datetime.now().date().strftime("%Y-%m-%d")

        for habit in habits:
            if not habit.get("active", True):
                continue

            category = habit.get("category", "Personal")

            # Initialize counter if needed
            if category not in category_counts:
                category_counts[category] = 0
                category_completion[category] = 0

            # Increment count
            category_counts[category] += 1

            # Check if completed today
            if today in habit.get("completed_dates", []):
                category_completion[category] += 1

        # Display categories
        category_grid = tk.Frame(category_frame, bg=self.theme.bg_color)
        category_grid.pack(fill=tk.X, padx=10, pady=10)

        # If no categories, show message
        if not categories:
            tk.Label(
                category_grid,
                text="No categories defined yet. Go to the Categories tab to add some!",
                font=self.theme.small_font,
                bg=self.theme.bg_color,
                fg=self.theme.text_color,
            ).pack(pady=10)
        else:
            # Get category colors
            category_colors = {}
            for category in categories:
                category_colors[category["name"]] = category["color"]

            # Show categories in a grid
            for i, category in enumerate(categories):
                name = category["name"]
                count = category_counts.get(name, 0)

                if count == 0:
                    continue  # Skip categories with no active habits

                # Calculate completion rate
                completed = category_completion.get(name, 0)
                completion_rate = int((completed / count) * 100) if count > 0 else 0

                # Category card
                card_frame = tk.Frame(
                    category_grid,
                    bg=self.theme.bg_color,
                    relief=tk.RIDGE,
                    bd=1,
                    padx=10,
                    pady=10,
                )
                card_frame.grid(
                    row=i // 2,
                    column=i % 2,
                    padx=10,
                    pady=10,
                    sticky="news",
                )

                # Color indicator and name
                header_frame = tk.Frame(card_frame, bg=self.theme.bg_color)
                header_frame.pack(fill=tk.X)

                color_indicator = tk.Frame(
                    header_frame,
                    bg=category_colors.get(name, self.theme.habit_color),
                    width=15,
                    height=15,
                )
                color_indicator.pack(side=tk.LEFT, padx=5)

                name_label = tk.Label(
                    header_frame,
                    text=name,
                    font=self.theme.small_font,
                    bg=self.theme.bg_color,
                    fg=self.theme.text_color,
                )
                name_label.pack(side=tk.LEFT, padx=5)

                # Count
                tk.Label(
                    card_frame,
                    text=f"Habits: {count}",
                    font=self.theme.small_font,
                    bg=self.theme.bg_color,
                    fg=self.theme.text_color,
                ).pack(anchor="w")

                # Completion
                completion_color = (
                    "#4CAF50"
                    if completion_rate >= 80
                    else "#FFC107"
                    if completion_rate >= 50
                    else "#F44336"
                )

                tk.Label(
                    card_frame,
                    text=f"Today: {completed}/{count} ({completion_rate}%)",
                    font=self.theme.small_font,
                    bg=self.theme.bg_color,
                    fg=completion_color,
                ).pack(anchor="w")

                # Add a simple bar to visualize completion
                bar_frame = tk.Frame(card_frame, bg=self.theme.bg_color, pady=5)
                bar_frame.pack(fill=tk.X)

                bar_bg = tk.Frame(
                    bar_frame,
                    bg=self.theme.darken_color(self.theme.primary_color),
                    height=10,
                    width=200,
                )
                bar_bg.pack(fill=tk.X)

                bar_width = int((completion_rate / 100) * 200)

                bar = tk.Frame(
                    bar_bg,
                    bg=completion_color,
                    height=10,
                    width=bar_width,
                )
                bar.place(x=0, y=0)

    def create_performance_section(self, parent):
        """
        Create the habit performance section showing completion rates.

        Args:
            parent: Parent frame to place the performance section
        """
        performance_frame = tk.LabelFrame(
            parent,
            text="Habit Performance",
            font=self.theme.pixel_font,
            bg=self.theme.bg_color,
            fg=self.theme.habit_color,
        )
        performance_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Get all habits
        habits = self.data.get("habits", {}).get("daily_habits", []) + self.data.get(
            "habits", {}
        ).get("custom_habits", [])

        # If no habits, show a message
        if not habits:
            tk.Label(
                performance_frame,
                text="No habits added yet. Add some habits to see statistics!",
                font=self.theme.pixel_font,
                bg=self.theme.bg_color,
                fg=self.theme.text_color,
                pady=30,
            ).pack()
            return

        # Create a canvas for the habit performance bars
        performance_canvas = tk.Canvas(
            performance_frame,
            bg=self.theme.bg_color,
            highlightthickness=0,
        )
        scrollbar = ttk.Scrollbar(
            performance_frame,
            orient="vertical",
            command=performance_canvas.yview,
        )
        scrollable_frame = tk.Frame(performance_canvas, bg=self.theme.bg_color)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: performance_canvas.configure(
                scrollregion=performance_canvas.bbox("all")
            ),
        )

        performance_canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        performance_canvas.configure(yscrollcommand=scrollbar.set)

        performance_canvas.pack(side="left", fill="both", expand=True, padx=5, pady=5)
        scrollbar.pack(side="right", fill="y")

        # Get category colors
        category_colors = {}
        for category in self.data["habits"].get("categories", []):
            category_colors[category["name"]] = category["color"]

        # Header row
        header_frame = tk.Frame(scrollable_frame, bg=self.theme.bg_color)
        header_frame.pack(fill=tk.X, pady=5)

        tk.Label(
            header_frame,
            text="Habit",
            font=self.theme.small_font,
            bg=self.theme.bg_color,
            fg=self.theme.text_color,
            width=25,
            anchor="w",
        ).pack(side=tk.LEFT, padx=5)

        tk.Label(
            header_frame,
            text="30-Day Completion",
            font=self.theme.small_font,
            bg=self.theme.bg_color,
            fg=self.theme.text_color,
            width=15,
            anchor="w",
        ).pack(side=tk.LEFT, padx=5)

        tk.Label(
            header_frame,
            text="Streak",
            font=self.theme.small_font,
            bg=self.theme.bg_color,
            fg=self.theme.text_color,
            width=10,
            anchor="w",
        ).pack(side=tk.LEFT, padx=5)

        # Display habit performance bars
        for i, habit in enumerate(habits):
            if not habit.get("active", True):
                continue

            # Calculate completion rate for the last 30 days
            today = datetime.now().date()
            dates_to_check = [
                (today - timedelta(days=i)).strftime("%Y-%m-%d") for i in range(30)
            ]

            # Count how many of these dates should have the habit active
            active_dates = []
            for date_str in dates_to_check:
                date_obj = datetime.strptime(date_str, "%Y-%m-%d").date()
                if self.is_active_date_for_habit(habit, date_obj):
                    active_dates.append(date_str)

            # Count completed dates
            completed_dates = habit.get("completed_dates", [])
            recent_completed = [d for d in active_dates if d in completed_dates]

            if active_dates:
                completion_rate = (len(recent_completed) / len(active_dates)) * 100
            else:
                completion_rate = 0

            # Get category and color
            category = habit.get("category", "Personal")
            category_color = category_colors.get(category, self.theme.habit_color)

            # Create a row for this habit
            row_bg = (
                self.theme.bg_color
                if i % 2 == 0
                else self.theme.darken_color(self.theme.bg_color)
            )
            row_frame = tk.Frame(scrollable_frame, bg=row_bg, padx=5, pady=8)
            row_frame.pack(fill=tk.X)

            # Habit name and icon
            name_frame = tk.Frame(row_frame, bg=row_bg, width=25)
            name_frame.pack(side=tk.LEFT, padx=5)

            # Category color indicator
            category_indicator = tk.Frame(
                name_frame, bg=category_color, width=5, height=20
            )
            category_indicator.pack(side=tk.LEFT, padx=2)

            # Add frequency info to the display
            frequency_text = self.get_frequency_display_text(habit)

            name_label = tk.Label(
                name_frame,
                text=f"{habit.get('icon', '📋')} {habit['name']}",
                font=self.theme.small_font,
                bg=row_bg,
                fg=self.theme.text_color,
                anchor="w",
                width=22,
            )
            name_label.pack(side=tk.LEFT)

            # Create tooltip binding
            def show_tooltip(event, text=frequency_text):
                tooltip = tk.Toplevel()
                tooltip.wm_overrideredirect(True)
                tooltip.geometry(f"+{event.x_root + 10}+{event.y_root + 10}")

                frame = tk.Frame(tooltip, bg="lightyellow", bd=1, relief=tk.SOLID)
                frame.pack()

                label = tk.Label(
                    frame,
                    text=text,
                    bg="lightyellow",
                    justify=tk.LEFT,
                    font=("TkDefaultFont", 9),
                    padx=5,
                    pady=2,
                )
                label.pack()

                # Store the tooltip reference
                event.widget.tooltip = tooltip

            def hide_tooltip(event):
                if hasattr(event.widget, "tooltip"):
                    event.widget.tooltip.destroy()

            name_label.bind("<Enter>", show_tooltip)
            name_label.bind("<Leave>", hide_tooltip)

            # Progress bar
            bar_frame = tk.Frame(row_frame, bg=row_bg)
            bar_frame.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=10)

            bar_bg = tk.Frame(
                bar_frame,
                bg=self.theme.darken_color(self.theme.primary_color),
                height=20,
                width=300,
            )
            bar_bg.pack(fill=tk.X)

            # Calculate progress bar width
            bar_width = int((completion_rate / 100) * 300)

            # Determine color based on completion rate
            if completion_rate >= 80:
                bar_color = "#4CAF50"  # Green for high completion
            elif completion_rate >= 50:
                bar_color = "#FFC107"  # Yellow for medium completion
            else:
                bar_color = "#F44336"  # Red for low completion

            bar = tk.Frame(
                bar_bg,
                bg=bar_color,
                height=20,
                width=bar_width,
            )
            bar.place(x=0, y=0)

            # Percentage label
            tk.Label(
                row_frame,
                text=f"{int(completion_rate)}%",
                font=self.theme.small_font,
                bg=row_bg,
                fg=self.theme.text_color,
                width=5,
            ).pack(side=tk.LEFT, padx=5)

            # Streak
            streak_frame = tk.Frame(row_frame, bg=row_bg)
            streak_frame.pack(side=tk.LEFT, padx=5)

            streak_label = tk.Label(
                streak_frame,
                text=f"🔥 {habit.get('streak', 0)}",
                font=self.theme.small_font,
                bg=row_bg,
                fg="#FF5722",  # Orange for streak
            )
            streak_label.pack()

    def is_active_date_for_habit(self, habit, date):
        """
        Check if a date is an active date for a habit based on its frequency.

        Args:
            habit: The habit object
            date: The date to check

        Returns:
            True if the date is active for this habit, False otherwise
        """
        frequency = habit.get("frequency", "daily")

        if frequency == "daily":
            return True
        elif frequency == "weekly":
            # Check if the day of week is in the specific days
            day_of_week = date.weekday()  # 0 = Monday, 6 = Sunday
            # Convert to 0 = Sunday, 6 = Saturday format
            day_of_week = (day_of_week + 1) % 7
            return day_of_week in habit.get("specific_days", [0, 1, 2, 3, 4, 5, 6])
        elif frequency == "monthly":
            # Check if the day of month is in the specific dates
            return date.day in habit.get("specific_dates", [1])
        elif frequency == "interval":
            # Check if today is an interval day
            interval = habit.get("interval", 1)
            if interval == 1:
                return True

            # Get the start date for this habit
            start_date = None
            completed_dates = habit.get("completed_dates", [])
            if completed_dates:
                # Sort dates and get the earliest
                date_objects = [
                    datetime.strptime(d, "%Y-%m-%d").date() for d in completed_dates
                ]
                start_date = min(date_objects)
            else:
                # If no completed dates, use today as start
                start_date = datetime.now().date()

            # Calculate days since start
            days_since_start = (date - start_date).days

            # Check if it's a multiple of the interval
            return days_since_start % interval == 0
        else:
            return True  # Default to active

    def get_frequency_display_text(self, habit):
        """
        Get a user-friendly display text for a habit's frequency.

        Args:
            habit: The habit object

        Returns:
            A string describing the frequency
        """
        frequency = habit.get("frequency", "daily")

        if frequency == "daily":
            return "Frequency: Daily"
        elif frequency == "weekly":
            days = habit.get("specific_days", [0, 1, 2, 3, 4, 5, 6])
            day_names = [
                "Sunday",
                "Monday",
                "Tuesday",
                "Wednesday",
                "Thursday",
                "Friday",
                "Saturday",
            ]
            selected_days = [day_names[day] for day in days]
            return f"Frequency: Weekly\nDays: {', '.join(selected_days)}"
        elif frequency == "monthly":
            dates = habit.get("specific_dates", [1])
            if len(dates) == 1:
                if dates[0] == 1:
                    suffix = "st"
                elif dates[0] == 2:
                    suffix = "nd"
                elif dates[0] == 3:
                    suffix = "rd"
                else:
                    suffix = "th"
                return (
                    f"Frequency: Monthly\nOn the {dates[0]}{suffix} day of each month"
                )
            else:
                date_str = ", ".join([str(d) for d in dates])
                return f"Frequency: Monthly\nOn days: {date_str}"
        elif frequency == "interval":
            interval = habit.get("interval", 1)
            if interval == 1:
                return "Frequency: Every day"
            else:
                return f"Frequency: Every {interval} days"
        else:
            return f"Frequency: {frequency.capitalize()}"
