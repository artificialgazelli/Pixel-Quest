"""
Habit tab module for the Pixel Quest habit tracker.
Manages the main habit tracking view and functionality.
"""

import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, timedelta


class HabitTab:
    """
    Manages the habits tab of the habit tracker.
    Displays habits, allows for tracking, and provides management functions.
    """

    def __init__(self, habit_tracker, app, data_manager, theme):
        """
        Initialize the habit tab module.

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
        self.category_filter_var = None

    def create_habits_view(self, parent):
        """
        Create the habits tab view with a calendar and habit list.

        Args:
            parent: Parent frame to place the habits view
        """
        # Top control panel
        control_frame = tk.Frame(parent, bg=self.theme.bg_color)
        control_frame.pack(pady=5, fill=tk.X)

        # Add habit button
        add_habit_button = self.theme.create_pixel_button(
            control_frame,
            "Add New Habit",
            self.add_new_habit,
            color="#4CAF50",
        )
        add_habit_button.pack(side=tk.LEFT, padx=10)

        # Filter by category dropdown
        filter_frame = tk.Frame(control_frame, bg=self.theme.bg_color)
        filter_frame.pack(side=tk.LEFT, padx=20)

        tk.Label(
            filter_frame,
            text="Filter by Category:",
            font=self.theme.small_font,
            bg=self.theme.bg_color,
            fg=self.theme.text_color,
        ).pack(side=tk.LEFT, padx=5)

        # Get categories for dropdown
        categories = ["All"] + [
            c["name"] for c in self.data["habits"].get("categories", [])
        ]

        self.category_filter_var = tk.StringVar(value="All")
        category_dropdown = ttk.Combobox(
            filter_frame,
            textvariable=self.category_filter_var,
            values=categories,
            font=self.theme.small_font,
            width=15,
        )
        category_dropdown.pack(side=tk.LEFT, padx=5)

        # Add binding to refresh when filter changes
        category_dropdown.bind(
            "<<ComboboxSelected>>", lambda e: self.habit_tracker.refresh_display()
        )

        # Current week display
        today = datetime.now().date()
        start_of_week = today - timedelta(days=today.weekday())
        end_of_week = start_of_week + timedelta(days=6)

        week_label = tk.Label(
            control_frame,
            text=f"Week: {start_of_week.strftime('%b %d')} - {end_of_week.strftime('%b %d, %Y')}",
            font=self.theme.pixel_font,
            bg=self.theme.bg_color,
            fg=self.theme.text_color,
        )
        week_label.pack(side=tk.RIGHT, padx=10)

        # Main content frame
        content_frame = tk.Frame(parent, bg=self.theme.bg_color)
        content_frame.pack(pady=10, fill=tk.BOTH, expand=True)

        # Calendar header with days of week
        days_frame = tk.Frame(content_frame, bg=self.theme.bg_color)
        days_frame.pack(fill=tk.X, pady=5)

        days = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]
        # First column for habit names
        tk.Label(
            days_frame,
            text="Habit",
            font=self.theme.small_font,
            bg=self.theme.bg_color,
            fg=self.theme.text_color,
            width=16,
            anchor="w",
        ).grid(row=0, column=0, padx=5)

        # Day columns
        for i, day in enumerate(days):
            # Calculate date for this column
            date = start_of_week + timedelta(days=i)

            # Container frame for day header
            day_frame = tk.Frame(days_frame, bg=self.theme.bg_color)
            day_frame.grid(row=0, column=i + 1, padx=2)

            # Day name
            tk.Label(
                day_frame,
                text=day,
                font=self.theme.small_font,
                bg=self.theme.bg_color,
                fg=self.theme.text_color,
            ).pack()

            # Day number
            date_color = "#FF5722" if date == today else self.theme.text_color
            tk.Label(
                day_frame,
                text=str(date.day),
                font=self.theme.small_font,
                bg=self.theme.bg_color,
                fg=date_color,
            ).pack()

        # Create scrollable frame for habits
        habits_canvas = tk.Canvas(
            content_frame, bg=self.theme.bg_color, highlightthickness=0
        )
        scrollbar = ttk.Scrollbar(
            content_frame, orient="vertical", command=habits_canvas.yview
        )
        scrollable_frame = tk.Frame(habits_canvas, bg=self.theme.bg_color)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: habits_canvas.configure(scrollregion=habits_canvas.bbox("all")),
        )

        habits_canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        habits_canvas.configure(yscrollcommand=scrollbar.set)

        habits_canvas.pack(side="left", fill="both", expand=True, padx=5, pady=5)
        scrollbar.pack(side="right", fill="y")

        # Add habit rows
        self.display_habit_rows(scrollable_frame, start_of_week)

    def display_habit_rows(self, parent, start_date):
        """
        Display habit rows with toggles for each day of the week.

        Args:
            parent: Parent frame to place the habit rows
            start_date: Starting date of the displayed week
        """
        # Get all habits
        all_habits = self.data.get("habits", {}).get(
            "daily_habits", []
        ) + self.data.get("habits", {}).get("custom_habits", [])

        # Filter by category if needed
        selected_category = self.category_filter_var.get()
        if selected_category != "All":
            all_habits = [
                h for h in all_habits if h.get("category") == selected_category
            ]

        # If no habits exist yet, show a message
        if not all_habits:
            message = "No habits added yet. Click 'Add New Habit' to get started!"
            if selected_category != "All":
                message = f"No habits in the '{selected_category}' category. Try a different filter or add new habits."

            tk.Label(
                parent,
                text=message,
                font=self.theme.pixel_font,
                bg=self.theme.bg_color,
                fg=self.theme.text_color,
                pady=20,
            ).grid(row=0, column=0, columnspan=8)
            return

        # Get category colors
        category_colors = {}
        for category in self.data["habits"].get("categories", []):
            category_colors[category["name"]] = category["color"]

        # Create a row for each habit
        for i, habit in enumerate(all_habits):
            # Skip inactive habits
            if not habit.get("active", True):
                continue

            # Row background alternates for better readability
            row_bg = (
                self.theme.bg_color
                if i % 2 == 0
                else self.theme.darken_color(self.theme.bg_color)
            )

            # Get category color
            category = habit.get("category", "Personal")
            category_color = category_colors.get(category, self.theme.habit_color)

            # Habit info frame (first column)
            habit_frame = tk.Frame(parent, bg=row_bg, padx=5, pady=5)
            habit_frame.grid(row=i, column=0, sticky="ew")

            # Category color indicator
            category_indicator = tk.Frame(
                habit_frame, bg=category_color, width=5, height=20
            )
            category_indicator.pack(side=tk.LEFT, padx=2)

            # Habit icon and name
            icon_label = tk.Label(
                habit_frame,
                text=habit.get("icon", "📋"),
                font=self.theme.pixel_font,
                bg=row_bg,
                fg=self.theme.text_color,
            )
            icon_label.pack(side=tk.LEFT, padx=2)

            # Create a tooltip to show frequency
            frequency_text = self.get_frequency_display_text(habit)

            name_label = tk.Label(
                habit_frame,
                text=habit["name"],
                font=self.theme.small_font,
                bg=row_bg,
                fg=self.theme.text_color,
                anchor="w",
                width=12,
            )
            name_label.pack(side=tk.LEFT, padx=2, fill=tk.X, expand=True)

            # Create a label to show frequency info as a tooltip
            freq_label = tk.Label(
                habit_frame,
                text="ℹ️",
                font=self.theme.small_font,
                bg=row_bg,
                fg=self.theme.text_color,
            )
            freq_label.pack(side=tk.LEFT, padx=2)

            # Create tooltip hover binding
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

            freq_label.bind("<Enter>", show_tooltip)
            freq_label.bind("<Leave>", hide_tooltip)

            # Streak display
            streak_frame = tk.Frame(habit_frame, bg=row_bg)
            streak_frame.pack(side=tk.LEFT)

            streak_label = tk.Label(
                streak_frame,
                text=f"🔥 {habit.get('streak', 0)}",
                font=self.theme.small_font,
                bg=row_bg,
                fg="#FF5722",  # Orange for streak
            )
            streak_label.pack(side=tk.LEFT, padx=2)

            # Action buttons for edit and delete
            action_frame = tk.Frame(habit_frame, bg=row_bg)
            action_frame.pack(side=tk.RIGHT, padx=5)

            edit_button = tk.Button(
                action_frame,
                text="✏️",
                font=self.theme.small_font,
                bg=self.theme.primary_color,
                fg=self.theme.text_color,
                relief=tk.FLAT,
                command=lambda h=habit["name"]: self.edit_habit(h),
            )
            edit_button.pack(side=tk.LEFT, padx=2)

            delete_button = tk.Button(
                action_frame,
                text="🗑️",
                font=self.theme.small_font,
                bg="#F44336",
                fg="white",
                relief=tk.FLAT,
                command=lambda h=habit["name"]: self.remove_habit(h),
            )
            delete_button.pack(side=tk.LEFT, padx=2)

            # Toggle buttons for each day of the week
            for j in range(7):
                date = start_date + timedelta(days=j)
                date_str = date.strftime("%Y-%m-%d")

                # Check if this date should be active based on frequency
                is_active_date = self.is_active_date_for_habit(habit, date)

                # Check if habit was completed on this date
                completed = date_str in habit.get("completed_dates", [])

                # Cell background
                cell_frame = tk.Frame(
                    parent,
                    bg=row_bg,
                    padx=5,
                    pady=5,
                )
                cell_frame.grid(row=i, column=j + 1)

                # Different button styles for completed vs not completed
                if not is_active_date:
                    # Gray out days that don't match the frequency
                    button = tk.Label(
                        cell_frame,
                        text="",
                        font=self.theme.small_font,
                        bg=self.theme.darken_color(row_bg),
                        width=2,
                        height=1,
                        relief=tk.FLAT,
                    )
                elif completed:
                    # For completed habits, show a green checkmark button
                    button = tk.Button(
                        cell_frame,
                        text="✓",
                        font=self.theme.small_font,
                        bg="#4CAF50",  # Green
                        fg="white",
                        width=2,
                        height=1,
                        relief=tk.FLAT,
                        command=lambda h=habit["name"], d=date_str: self.toggle_habit(
                            h, d
                        ),
                    )
                else:
                    # For incomplete habits, show an empty button
                    button = tk.Button(
                        cell_frame,
                        text=" ",
                        font=self.theme.small_font,
                        bg=self.theme.primary_color,
                        fg=self.theme.text_color,
                        width=2,
                        height=1,
                        relief=tk.FLAT,
                        command=lambda h=habit["name"], d=date_str: self.toggle_habit(
                            h, d
                        ),
                    )

                # Disable buttons for future dates
                if date > datetime.now().date():
                    if isinstance(button, tk.Button):
                        button.config(state=tk.DISABLED)

                button.pack(padx=5, pady=5)

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

    def toggle_habit(self, habit_name, date_str):
        """
        Toggle a habit's completion status for a specific date.

        Args:
            habit_name: Name of the habit to toggle
            date_str: Date string in YYYY-MM-DD format
        """
        # Find the habit
        habit = None
        habit_list = None
        habit_index = -1

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
            messagebox.showerror("Error", f"Habit '{habit_name}' not found.")
            return

        # Check if this date is active for the habit
        date_obj = datetime.strptime(date_str, "%Y-%m-%d").date()
        if not self.is_active_date_for_habit(habit, date_obj):
            messagebox.showinfo(
                "Not Scheduled", f"This habit is not scheduled for {date_str}."
            )
            return

        # Get completed dates list
        completed_dates = habit.get("completed_dates", [])

        # Toggle the date
        if date_str in completed_dates:
            # Remove date if already completed
            completed_dates.remove(date_str)
        else:
            # Add date if not completed
            completed_dates.append(date_str)

        # Update the habit
        self.data["habits"][habit_list][habit_index]["completed_dates"] = (
            completed_dates
        )

        # Update the streak
        self.update_habit_streak(habit_list, habit_index)

        # Save data
        self.data_manager.save_data()

        # Refresh the display
        self.habit_tracker.refresh_display()

    def update_habit_streak(self, habit_list, habit_index):
        """
        Update a habit's streak based on completion history.

        Args:
            habit_list: Which list the habit belongs to (daily_habits or custom_habits)
            habit_index: Index of the habit in the list
        """
        habit = self.data["habits"][habit_list][habit_index]
        completed_dates = habit.get("completed_dates", [])

        # Sort dates
        date_objects = [
            datetime.strptime(d, "%Y-%m-%d").date() for d in completed_dates
        ]
        date_objects.sort(reverse=True)

        # Calculate streak
        streak = 0
        today = datetime.now().date()

        # If today is completed, start streak from today
        if today in date_objects:
            streak = 1
            check_date = today - timedelta(days=1)
        else:
            # If today is not completed, start from yesterday
            check_date = today - timedelta(days=1)
            if check_date in date_objects:
                streak = 1
            else:
                # No recent completions
                self.data["habits"][habit_list][habit_index]["streak"] = 0
                return

        # Check frequency to determine how to count streak
        frequency = habit.get("frequency", "daily")

        if frequency == "daily":
            # For daily habits, check consecutive days
            while True:
                if check_date in date_objects:
                    streak += 1
                    check_date -= timedelta(days=1)
                else:
                    break
        elif frequency == "weekly":
            # For weekly habits, consider weeks where all specified days were completed
            specific_days = habit.get("specific_days", [0, 1, 2, 3, 4, 5, 6])

            # Check week by week
            current_week = (today.isocalendar()[1], today.year)
            weeks_checked = 0
            consecutive_weeks = 0

            # Keep checking previous weeks as long as streak is maintained
            while True:
                # Create date range for the week being checked
                week_start = today - timedelta(
                    days=today.weekday() + (7 * weeks_checked)
                )
                week_dates = []

                for i in range(7):
                    day = week_start - timedelta(days=i)
                    # Only include days that are specified for this habit
                    day_of_week = (day.weekday() + 1) % 7  # Convert to 0=Sunday format
                    if day_of_week in specific_days:
                        week_dates.append(day)

                # Check if all required days in this week were completed
                if all(day in date_objects for day in week_dates):
                    consecutive_weeks += 1
                    weeks_checked += 1
                else:
                    break

            # Set streak as number of consecutive weeks
            streak = consecutive_weeks
        elif frequency == "monthly":
            # For monthly habits, consider months where all specified dates were completed
            specific_dates = habit.get("specific_dates", [1])

            # Check month by month
            months_checked = 0
            consecutive_months = 0

            # Keep checking previous months as long as streak is maintained
            while True:
                # Calculate the month to check
                check_year = today.year
                check_month = today.month - months_checked

                while check_month <= 0:
                    check_month += 12
                    check_year -= 1

                # Create date objects for the required dates in this month
                month_dates = []

                for date_num in specific_dates:
                    try:
                        # Create the date, handling month boundaries
                        if date_num > 28:  # Handle month length variations
                            import calendar

                            last_day = calendar.monthrange(check_year, check_month)[1]
                            date_num = min(date_num, last_day)

                        month_date = datetime(check_year, check_month, date_num).date()
                        if month_date <= today:  # Only include dates up to today
                            month_dates.append(month_date)
                    except ValueError:
                        continue  # Skip invalid dates like Feb 30

                # Check if all required dates in this month were completed
                if all(date in date_objects for date in month_dates) and month_dates:
                    consecutive_months += 1
                    months_checked += 1
                else:
                    break

            # Set streak as number of consecutive months
            streak = consecutive_months
        elif frequency == "interval":
            # For interval habits, check every Nth day
            interval = habit.get("interval", 1)

            # If interval is 1, it's effectively a daily habit
            if interval == 1:
                while True:
                    if check_date in date_objects:
                        streak += 1
                        check_date -= timedelta(days=1)
                    else:
                        break
            else:
                # Get earliest completion date to establish a baseline
                earliest_date = min(date_objects) if date_objects else today

                # Keep track of days to check
                next_date = today
                days_checked = 0

                # Check if the right dates were completed
                while next_date >= earliest_date:
                    if (
                        days_checked % interval == 0
                    ):  # This is a day that should be checked
                        if next_date in date_objects:
                            streak += 1
                        else:
                            break  # Streak is broken

                    next_date -= timedelta(days=1)
                    days_checked += 1

        # Update streak
        self.data["habits"][habit_list][habit_index]["streak"] = streak

    def add_new_habit(self):
        """Open a dialog to add a new custom habit."""
        # Create a dialog window
        dialog = tk.Toplevel(self.app.root)
        dialog.title("Add New Habit")
        dialog.geometry("500x450")  # Increased height for all options
        dialog.configure(bg=self.theme.bg_color)
        dialog.transient(self.app.root)
        dialog.grab_set()

        # Name input
        name_frame = tk.Frame(dialog, bg=self.theme.bg_color)
        name_frame.pack(fill=tk.X, padx=20, pady=10)

        tk.Label(
            name_frame,
            text="Habit Name:",
            font=self.theme.small_font,
            bg=self.theme.bg_color,
            fg=self.theme.text_color,
        ).pack(side=tk.LEFT)

        name_var = tk.StringVar()
        name_entry = tk.Entry(
            name_frame,
            textvariable=name_var,
            font=self.theme.small_font,
            bg=self.theme.primary_color,
            fg=self.theme.text_color,
            width=30,
        )
        name_entry.pack(side=tk.LEFT, padx=10)

        # Icon selection
        icon_frame = tk.Frame(dialog, bg=self.theme.bg_color)
        icon_frame.pack(fill=tk.X, padx=20, pady=10)

        tk.Label(
            icon_frame,
            text="Icon:",
            font=self.theme.small_font,
            bg=self.theme.bg_color,
            fg=self.theme.text_color,
        ).pack(side=tk.LEFT)

        icon_var = tk.StringVar(value="📋")
        icons = [
            "📋",
            "🏃",
            "📚",
            "💪",
            "🎨",
            "🎵",
            "💻",
            "🧘",
            "🥗",
            "💤",
            "💧",
            "🧠",
            "🇰🇷",
            "🇫🇷",
            "🧹",
            "🧺",
            "🌱",
        ]

        icon_dropdown = ttk.Combobox(
            icon_frame,
            textvariable=icon_var,
            values=icons,
            font=self.theme.small_font,
            width=5,
        )
        icon_dropdown.pack(side=tk.LEFT, padx=10)

        # Category selection
        category_frame = tk.Frame(dialog, bg=self.theme.bg_color)
        category_frame.pack(fill=tk.X, padx=20, pady=10)

        tk.Label(
            category_frame,
            text="Category:",
            font=self.theme.small_font,
            bg=self.theme.bg_color,
            fg=self.theme.text_color,
        ).pack(side=tk.LEFT)

        # Get categories
        categories = [c["name"] for c in self.data["habits"].get("categories", [])]
        if not categories:
            categories = ["Personal"]  # Default if no categories

        category_var = tk.StringVar(value=categories[0] if categories else "Personal")

        category_dropdown = ttk.Combobox(
            category_frame,
            textvariable=category_var,
            values=categories,
            font=self.theme.small_font,
            width=15,
        )
        category_dropdown.pack(side=tk.LEFT, padx=10)

        # Frequency selection
        freq_frame = tk.Frame(dialog, bg=self.theme.bg_color)
        freq_frame.pack(fill=tk.X, padx=20, pady=10)

        tk.Label(
            freq_frame,
            text="Frequency:",
            font=self.theme.small_font,
            bg=self.theme.bg_color,
            fg=self.theme.text_color,
        ).pack(side=tk.LEFT)

        freq_var = tk.StringVar(value="daily")
        frequencies = ["daily", "weekly", "monthly", "interval"]

        freq_dropdown = ttk.Combobox(
            freq_frame,
            textvariable=freq_var,
            values=frequencies,
            font=self.theme.small_font,
            width=10,
        )
        freq_dropdown.pack(side=tk.LEFT, padx=10)

        # Frame for frequency options (will change based on selection)
        options_container = tk.Frame(dialog, bg=self.theme.bg_color)
        options_container.pack(fill=tk.X, padx=20, pady=10)

        # Create frames for each frequency type
        daily_frame = tk.Frame(options_container, bg=self.theme.bg_color)
        weekly_frame = tk.Frame(options_container, bg=self.theme.bg_color)
        monthly_frame = tk.Frame(options_container, bg=self.theme.bg_color)
        interval_frame = tk.Frame(options_container, bg=self.theme.bg_color)

        # Daily frame (no extra options needed)
        tk.Label(
            daily_frame,
            text="This habit will be tracked every day.",
            font=self.theme.small_font,
            bg=self.theme.bg_color,
            fg=self.theme.text_color,
        ).pack(pady=5)

        # Weekly frame - checkboxes for days of week
        tk.Label(
            weekly_frame,
            text="Select days of the week:",
            font=self.theme.small_font,
            bg=self.theme.bg_color,
            fg=self.theme.text_color,
        ).pack(anchor="w", pady=5)

        days_frame = tk.Frame(weekly_frame, bg=self.theme.bg_color)
        days_frame.pack(fill=tk.X, pady=5)

        days_vars = []
        days_of_week = [
            "Sunday",
            "Monday",
            "Tuesday",
            "Wednesday",
            "Thursday",
            "Friday",
            "Saturday",
        ]

        for i, day in enumerate(days_of_week):
            var = tk.BooleanVar(value=True)
            days_vars.append(var)

            cb = tk.Checkbutton(
                days_frame,
                text=day,
                variable=var,
                font=self.theme.small_font,
                bg=self.theme.bg_color,
                fg=self.theme.text_color,
                selectcolor=self.theme.secondary_color,
            )
            cb.grid(row=i // 4, column=i % 4, sticky="w", padx=5, pady=2)

        # Monthly frame - entry for day of month
        tk.Label(
            monthly_frame,
            text="Enter day(s) of the month (1-31, comma separated):",
            font=self.theme.small_font,
            bg=self.theme.bg_color,
            fg=self.theme.text_color,
        ).pack(anchor="w", pady=5)

        monthly_var = tk.StringVar(value="1")
        monthly_entry = tk.Entry(
            monthly_frame,
            textvariable=monthly_var,
            font=self.theme.small_font,
            bg=self.theme.primary_color,
            fg=self.theme.text_color,
            width=30,
        )
        monthly_entry.pack(anchor="w", padx=5, pady=5)

        tk.Label(
            monthly_frame,
            text="Example: 1,15,30 for the 1st, 15th, and 30th day of each month",
            font=("TkDefaultFont", 8),
            bg=self.theme.bg_color,
            fg=self.theme.text_color,
        ).pack(anchor="w", padx=5)

        # Interval frame - entry for every N days
        tk.Label(
            interval_frame,
            text="Track every N days:",
            font=self.theme.small_font,
            bg=self.theme.bg_color,
            fg=self.theme.text_color,
        ).pack(anchor="w", pady=5)

        interval_var = tk.StringVar(value="2")

        vcmd = (
            dialog.register(lambda P: P.isdigit() and int(P) > 0 if P else True),
            "%P",
        )
        interval_entry = tk.Entry(
            interval_frame,
            textvariable=interval_var,
            validate="key",
            validatecommand=vcmd,
            font=self.theme.small_font,
            bg=self.theme.primary_color,
            fg=self.theme.text_color,
            width=5,
        )
        interval_entry.pack(side=tk.LEFT, padx=5, pady=5)

        tk.Label(
            interval_frame,
            text="days",
            font=self.theme.small_font,
            bg=self.theme.bg_color,
            fg=self.theme.text_color,
        ).pack(side=tk.LEFT, pady=5)

        # Show the appropriate frame based on initial selection
        daily_frame.pack(fill=tk.X, pady=5)

        # Function to update displayed options when frequency changes
        def on_frequency_change(*args):
            # Hide all frames
            daily_frame.pack_forget()
            weekly_frame.pack_forget()
            monthly_frame.pack_forget()
            interval_frame.pack_forget()

            # Show the appropriate frame
            frequency = freq_var.get()
            if frequency == "daily":
                daily_frame.pack(fill=tk.X, pady=5)
            elif frequency == "weekly":
                weekly_frame.pack(fill=tk.X, pady=5)
            elif frequency == "monthly":
                monthly_frame.pack(fill=tk.X, pady=5)
            elif frequency == "interval":
                interval_frame.pack(fill=tk.X, pady=5)

        # Bind the dropdown to the update function
        freq_var.trace_add("write", on_frequency_change)

        # Button frame
        button_frame = tk.Frame(dialog, bg=self.theme.bg_color)
        button_frame.pack(pady=20)

        # Cancel button
        cancel_button = self.theme.create_pixel_button(
            button_frame,
            "Cancel",
            dialog.destroy,
            color="#F44336",
        )
        cancel_button.pack(side=tk.LEFT, padx=10)

        # Add button
        add_button = self.theme.create_pixel_button(
            button_frame,
            "Add Habit",
            lambda: self.save_new_habit(
                name_var.get(),
                icon_var.get(),
                category_var.get(),
                freq_var.get(),
                days_vars,
                monthly_var.get(),
                interval_var.get(),
                dialog,
            ),
            color=self.theme.habit_color,  # Use the theme's habit color
        )
        add_button.pack(side=tk.LEFT, padx=10)

        # Focus the name entry
        name_entry.focus_set()

    def save_new_habit(
        self,
        name,
        icon,
        category,
        frequency,
        days_vars,
        monthly_dates,
        interval,
        dialog,
    ):
        """
        Save a new custom habit to the data.

        Args:
            name: Habit name
            icon: Habit icon
            category: Habit category
            frequency: Habit frequency
            days_vars: List of BooleanVar for weekly habit days
            monthly_dates: String of comma-separated dates for monthly habits
            interval: String containing interval value for interval habits
            dialog: Dialog window to close after saving
        """
        # Validate input
        if not name:
            messagebox.showerror("Error", "Please enter a habit name.")
            return

        # Initialize habits if not exist
        if "habits" not in self.data:
            self.data["habits"] = {
                "daily_habits": [],
                "custom_habits": [],
                "check_ins": [],
            }

        # Check if habit name already exists
        all_habits = self.data["habits"].get("daily_habits", []) + self.data[
            "habits"
        ].get("custom_habits", [])

        for habit in all_habits:
            if habit["name"] == name:
                messagebox.showerror("Error", f"A habit named '{name}' already exists.")
                return

        # Create new habit with base properties
        new_habit = {
            "name": name,
            "icon": icon,
            "category": category,
            "frequency": frequency,
            "active": True,
            "streak": 0,
            "completed_dates": [],
        }

        # Add frequency-specific properties
        if frequency == "weekly":
            # Convert days_vars to list of indices
            specific_days = [i for i, var in enumerate(days_vars) if var.get()]

            if not specific_days:
                messagebox.showerror(
                    "Error", "Please select at least one day of the week."
                )
                return

            new_habit["specific_days"] = specific_days
        elif frequency == "monthly":
            # Parse the monthly dates
            try:
                # Strip spaces and split by commas
                date_str = monthly_dates.strip()
                if "," in date_str:
                    dates = [int(d.strip()) for d in date_str.split(",")]
                else:
                    dates = [int(date_str)]

                # Validate date range
                invalid_dates = [d for d in dates if d < 1 or d > 31]
                if invalid_dates:
                    messagebox.showerror(
                        "Error",
                        f"Invalid day of month: {invalid_dates}. Please use numbers between 1 and 31.",
                    )
                    return

                new_habit["specific_dates"] = dates
            except ValueError:
                messagebox.showerror(
                    "Error",
                    "Invalid format for monthly dates. Please use comma-separated numbers.",
                )
                return
        elif frequency == "interval":
            # Parse the interval
            try:
                interval_val = int(interval)
                if interval_val < 1:
                    messagebox.showerror("Error", "Interval must be at least 1 day.")
                    return

                new_habit["interval"] = interval_val
            except ValueError:
                messagebox.showerror(
                    "Error", "Invalid interval value. Please enter a number."
                )
                return

        # Add to custom habits
        self.data["habits"]["custom_habits"].append(new_habit)

        # Save data
        self.data_manager.save_data()

        # Close dialog
        dialog.destroy()

        # Refresh display
        self.habit_tracker.refresh_display()

        # Show confirmation
        messagebox.showinfo("Success", f"Habit '{name}' has been added!")

    def edit_habit(self, habit_name):
        """Open a dialog to edit an existing habit."""
        # Find the habit
        habit = None
        habit_list = None
        habit_index = -1

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
            messagebox.showerror("Error", f"Habit '{habit_name}' not found.")
            return

        # Create a dialog window
        dialog = tk.Toplevel(self.app.root)
        dialog.title(f"Edit Habit: {habit_name}")
        dialog.geometry("500x450")  # Increased height for all options
        dialog.configure(bg=self.theme.bg_color)
        dialog.transient(self.app.root)
        dialog.grab_set()

        # Name input
        name_frame = tk.Frame(dialog, bg=self.theme.bg_color)
        name_frame.pack(fill=tk.X, padx=20, pady=10)

        tk.Label(
            name_frame,
            text="Habit Name:",
            font=self.theme.small_font,
            bg=self.theme.bg_color,
            fg=self.theme.text_color,
        ).pack(side=tk.LEFT)

        name_var = tk.StringVar(value=habit["name"])
        name_entry = tk.Entry(
            name_frame,
            textvariable=name_var,
            font=self.theme.small_font,
            bg=self.theme.primary_color,
            fg=self.theme.text_color,
            width=30,
        )
        name_entry.pack(side=tk.LEFT, padx=10)

        # Icon selection
        icon_frame = tk.Frame(dialog, bg=self.theme.bg_color)
        icon_frame.pack(fill=tk.X, padx=20, pady=10)

        tk.Label(
            icon_frame,
            text="Icon:",
            font=self.theme.small_font,
            bg=self.theme.bg_color,
            fg=self.theme.text_color,
        ).pack(side=tk.LEFT)

        icon_var = tk.StringVar(value=habit.get("icon", "📋"))
        icons = [
            "📋",
            "🏃",
            "📚",
            "💪",
            "🎨",
            "🎵",
            "💻",
            "🧘",
            "🥗",
            "💤",
            "💧",
            "🧠",
            "🇰🇷",
            "🇫🇷",
            "🧹",
            "🧺",
            "🌱",
        ]

        icon_dropdown = ttk.Combobox(
            icon_frame,
            textvariable=icon_var,
            values=icons,
            font=self.theme.small_font,
            width=5,
        )
        icon_dropdown.pack(side=tk.LEFT, padx=10)

        # Category selection
        category_frame = tk.Frame(dialog, bg=self.theme.bg_color)
        category_frame.pack(fill=tk.X, padx=20, pady=10)

        tk.Label(
            category_frame,
            text="Category:",
            font=self.theme.small_font,
            bg=self.theme.bg_color,
            fg=self.theme.text_color,
        ).pack(side=tk.LEFT)

        # Get categories
        categories = [c["name"] for c in self.data["habits"].get("categories", [])]
        if not categories:
            categories = ["Personal"]  # Default if no categories

        category_var = tk.StringVar(value=habit.get("category", "Personal"))

        category_dropdown = ttk.Combobox(
            category_frame,
            textvariable=category_var,
            values=categories,
            font=self.theme.small_font,
            width=15,
        )
        category_dropdown.pack(side=tk.LEFT, padx=10)

        # Frequency selection
        freq_frame = tk.Frame(dialog, bg=self.theme.bg_color)
        freq_frame.pack(fill=tk.X, padx=20, pady=10)

        tk.Label(
            freq_frame,
            text="Frequency:",
            font=self.theme.small_font,
            bg=self.theme.bg_color,
            fg=self.theme.text_color,
        ).pack(side=tk.LEFT)

        freq_var = tk.StringVar(value=habit.get("frequency", "daily"))
        frequencies = ["daily", "weekly", "monthly", "interval"]

        freq_dropdown = ttk.Combobox(
            freq_frame,
            textvariable=freq_var,
            values=frequencies,
            font=self.theme.small_font,
            width=10,
        )
        freq_dropdown.pack(side=tk.LEFT, padx=10)

        # Frame for frequency options (will change based on selection)
        options_container = tk.Frame(dialog, bg=self.theme.bg_color)
        options_container.pack(fill=tk.X, padx=20, pady=10)

        # Create frames for each frequency type
        daily_frame = tk.Frame(options_container, bg=self.theme.bg_color)
        weekly_frame = tk.Frame(options_container, bg=self.theme.bg_color)
        monthly_frame = tk.Frame(options_container, bg=self.theme.bg_color)
        interval_frame = tk.Frame(options_container, bg=self.theme.bg_color)

        # Daily frame (no extra options needed)
        tk.Label(
            daily_frame,
            text="This habit will be tracked every day.",
            font=self.theme.small_font,
            bg=self.theme.bg_color,
            fg=self.theme.text_color,
        ).pack(pady=5)

        # Weekly frame - checkboxes for days of week
        tk.Label(
            weekly_frame,
            text="Select days of the week:",
            font=self.theme.small_font,
            bg=self.theme.bg_color,
            fg=self.theme.text_color,
        ).pack(anchor="w", pady=5)

        days_frame = tk.Frame(weekly_frame, bg=self.theme.bg_color)
        days_frame.pack(fill=tk.X, pady=5)

        days_vars = []
        days_of_week = [
            "Sunday",
            "Monday",
            "Tuesday",
            "Wednesday",
            "Thursday",
            "Friday",
            "Saturday",
        ]

        specific_days = habit.get("specific_days", [0, 1, 2, 3, 4, 5, 6])

        for i, day in enumerate(days_of_week):
            var = tk.BooleanVar(value=i in specific_days)
            days_vars.append(var)

            cb = tk.Checkbutton(
                days_frame,
                text=day,
                variable=var,
                font=self.theme.small_font,
                bg=self.theme.bg_color,
                fg=self.theme.text_color,
                selectcolor=self.theme.secondary_color,
            )
            cb.grid(row=i // 4, column=i % 4, sticky="w", padx=5, pady=2)

        # Monthly frame - entry for day of month
        tk.Label(
            monthly_frame,
            text="Enter day(s) of the month (1-31, comma separated):",
            font=self.theme.small_font,
            bg=self.theme.bg_color,
            fg=self.theme.text_color,
        ).pack(anchor="w", pady=5)

        specific_dates = habit.get("specific_dates", [1])
        monthly_var = tk.StringVar(value=",".join(str(d) for d in specific_dates))

        monthly_entry = tk.Entry(
            monthly_frame,
            textvariable=monthly_var,
            font=self.theme.small_font,
            bg=self.theme.primary_color,
            fg=self.theme.text_color,
            width=30,
        )
        monthly_entry.pack(anchor="w", padx=5, pady=5)

        tk.Label(
            monthly_frame,
            text="Example: 1,15,30 for the 1st, 15th, and 30th day of each month",
            font=("TkDefaultFont", 8),
            bg=self.theme.bg_color,
            fg=self.theme.text_color,
        ).pack(anchor="w", padx=5)

        # Interval frame - entry for every N days
        tk.Label(
            interval_frame,
            text="Track every N days:",
            font=self.theme.small_font,
            bg=self.theme.bg_color,
            fg=self.theme.text_color,
        ).pack(anchor="w", pady=5)

        interval_var = tk.StringVar(value=str(habit.get("interval", 2)))

        vcmd = (
            dialog.register(lambda P: P.isdigit() and int(P) > 0 if P else True),
            "%P",
        )
        interval_entry = tk.Entry(
            interval_frame,
            textvariable=interval_var,
            validate="key",
            validatecommand=vcmd,
            font=self.theme.small_font,
            bg=self.theme.primary_color,
            fg=self.theme.text_color,
            width=5,
        )
        interval_entry.pack(side=tk.LEFT, padx=5, pady=5)

        tk.Label(
            interval_frame,
            text="days",
            font=self.theme.small_font,
            bg=self.theme.bg_color,
            fg=self.theme.text_color,
        ).pack(side=tk.LEFT, pady=5)

        # Show the appropriate frame based on current frequency
        if freq_var.get() == "daily":
            daily_frame.pack(fill=tk.X, pady=5)
        elif freq_var.get() == "weekly":
            weekly_frame.pack(fill=tk.X, pady=5)
        elif freq_var.get() == "monthly":
            monthly_frame.pack(fill=tk.X, pady=5)
        elif freq_var.get() == "interval":
            interval_frame.pack(fill=tk.X, pady=5)

        # Function to update displayed options when frequency changes
        def on_frequency_change(*args):
            # Hide all frames
            daily_frame.pack_forget()
            weekly_frame.pack_forget()
            monthly_frame.pack_forget()
            interval_frame.pack_forget()

            # Show the appropriate frame
            frequency = freq_var.get()
            if frequency == "daily":
                daily_frame.pack(fill=tk.X, pady=5)
            elif frequency == "weekly":
                weekly_frame.pack(fill=tk.X, pady=5)
            elif frequency == "monthly":
                monthly_frame.pack(fill=tk.X, pady=5)
            elif frequency == "interval":
                interval_frame.pack(fill=tk.X, pady=5)

        # Bind the dropdown to the update function
        freq_var.trace_add("write", on_frequency_change)

        # Button frame
        button_frame = tk.Frame(dialog, bg=self.theme.bg_color)
        button_frame.pack(pady=20)

        # Cancel button
        cancel_button = self.theme.create_pixel_button(
            button_frame,
            "Cancel",
            dialog.destroy,
            color="#F44336",
        )
        cancel_button.pack(side=tk.LEFT, padx=10)

        # Update button
        update_button = self.theme.create_pixel_button(
            button_frame,
            "Update Habit",
            lambda: self.update_habit(
                habit_list,
                habit_index,
                name_var.get(),
                icon_var.get(),
                category_var.get(),
                freq_var.get(),
                days_vars,
                monthly_var.get(),
                interval_var.get(),
                dialog,
            ),
            color=self.theme.habit_color,  # Use the theme's habit color
        )
        update_button.pack(side=tk.LEFT, padx=10)

        # Focus the name entry
        name_entry.focus_set()

    def update_habit(
        self,
        habit_list,
        habit_index,
        name,
        icon,
        category,
        frequency,
        days_vars,
        monthly_dates,
        interval,
        dialog,
    ):
        """
        Update an existing habit with new values.

        Args:
            habit_list: List containing the habit ("daily_habits" or "custom_habits")
            habit_index: Index of the habit in the list
            name: New habit name
            icon: New habit icon
            category: New habit category
            frequency: New habit frequency
            days_vars: List of BooleanVar for weekly habit days
            monthly_dates: String of comma-separated dates for monthly habits
            interval: String containing interval value for interval habits
            dialog: Dialog window to close after saving
        """
        # Validate input
        if not name:
            messagebox.showerror("Error", "Please enter a habit name.")
            return

        # Get the original habit name
        original_name = self.data["habits"][habit_list][habit_index]["name"]

        # Check if new name already exists (but skip if name hasn't changed)
        if name != original_name:
            all_habits = self.data["habits"].get("daily_habits", []) + self.data[
                "habits"
            ].get("custom_habits", [])

            for habit in all_habits:
                if habit["name"] == name:
                    messagebox.showerror(
                        "Error", f"A habit named '{name}' already exists."
                    )
                    return

        # Update base properties
        self.data["habits"][habit_list][habit_index]["name"] = name
        self.data["habits"][habit_list][habit_index]["icon"] = icon
        self.data["habits"][habit_list][habit_index]["category"] = category
        self.data["habits"][habit_list][habit_index]["frequency"] = frequency

        # Update frequency-specific properties
        if frequency == "weekly":
            # Convert days_vars to list of indices
            specific_days = [i for i, var in enumerate(days_vars) if var.get()]

            if not specific_days:
                messagebox.showerror(
                    "Error", "Please select at least one day of the week."
                )
                return

            self.data["habits"][habit_list][habit_index]["specific_days"] = (
                specific_days
            )
        elif frequency == "monthly":
            # Parse the monthly dates
            try:
                # Strip spaces and split by commas
                date_str = monthly_dates.strip()
                if "," in date_str:
                    dates = [int(d.strip()) for d in date_str.split(",")]
                else:
                    dates = [int(date_str)]

                # Validate date range
                invalid_dates = [d for d in dates if d < 1 or d > 31]
                if invalid_dates:
                    messagebox.showerror(
                        "Error",
                        f"Invalid day of month: {invalid_dates}. Please use numbers between 1 and 31.",
                    )
                    return

                self.data["habits"][habit_list][habit_index]["specific_dates"] = dates
            except ValueError:
                messagebox.showerror(
                    "Error",
                    "Invalid format for monthly dates. Please use comma-separated numbers.",
                )
                return
        elif frequency == "interval":
            # Parse the interval
            try:
                interval_val = int(interval)
                if interval_val < 1:
                    messagebox.showerror("Error", "Interval must be at least 1 day.")
                    return

                self.data["habits"][habit_list][habit_index]["interval"] = interval_val
            except ValueError:
                messagebox.showerror(
                    "Error", "Invalid interval value. Please enter a number."
                )
                return

        # Save data
        self.data_manager.save_data()

        # Close dialog
        dialog.destroy()

        # Refresh display
        self.habit_tracker.refresh_display()

        # Show confirmation
        messagebox.showinfo("Success", f"Habit '{name}' has been updated!")

    def remove_habit(self, habit_name):
        """Remove a habit from the tracker."""
        # Find the habit
        habit = None
        habit_list = None
        habit_index = -1

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
            messagebox.showerror("Error", f"Habit '{habit_name}' not found.")
            return

        # Confirm deletion
        if not messagebox.askyesno(
            "Confirm Deletion",
            f"Are you sure you want to delete the habit '{habit_name}'?",
        ):
            return

        # Remove the habit
        del self.data["habits"][habit_list][habit_index]

        # Save data
        self.data_manager.save_data()

        # Refresh display
        self.habit_tracker.refresh_display()

        # Show confirmation
        messagebox.showinfo("Success", f"Habit '{habit_name}' has been removed!")
