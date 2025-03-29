"""
Check-in tab module for the Pixel Quest habit tracker.
Manages doctor appointments and other regular check-ins with date tracking.
"""

import tkinter as tk
from tkinter import ttk, messagebox
import calendar
from datetime import datetime, timedelta, date


class CheckInTab:
    """
    Manages the check-ins tab of the habit tracker.
    Displays a calendar view of check-ins and allows adding/editing appointments.
    """

    def __init__(self, habit_tracker, app, data_manager, theme):
        """
        Initialize the check-in tab module.

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

        # Current date for the calendar views
        self.current_date = datetime.now().date()
        self.selected_month = self.current_date.month
        self.selected_year = self.current_date.year

        # References to UI elements that need to be updated
        self.month_label = None
        self.month_frame = None
        self.events_list_frame = None

    def create_check_ins_view(self, parent):
        """
        Create the check-ins tab view with a calendar and event list.

        Args:
            parent: Parent frame to place the check-ins view
        """
        # Control panel with month navigation
        control_frame = tk.Frame(parent, bg=self.theme.bg_color)
        control_frame.pack(fill=tk.X, pady=5)

        # Previous month button
        prev_button = self.theme.create_pixel_button(
            control_frame,
            "<",
            self.prev_month,
            color="#9E9E9E",
            width=2,
        )
        prev_button.pack(side=tk.LEFT, padx=10)

        # Month/year label
        self.month_label = tk.Label(
            control_frame,
            text=f"{calendar.month_name[self.selected_month]} {self.selected_year}",
            font=self.theme.pixel_font,
            bg=self.theme.bg_color,
            fg=self.theme.text_color,
        )
        self.month_label.pack(side=tk.LEFT, padx=10, fill=tk.X, expand=True)

        # Next month button
        next_button = self.theme.create_pixel_button(
            control_frame,
            ">",
            self.next_month,
            color="#9E9E9E",
            width=2,
        )
        next_button.pack(side=tk.RIGHT, padx=10)

        # Add check-in button
        add_checkin_button = self.theme.create_pixel_button(
            control_frame,
            "Add Check-in",
            self.add_new_check_in,
            color=self.theme.habit_color,  # Use the theme's habit color
        )
        add_checkin_button.pack(side=tk.RIGHT, padx=10)

        # Calendar frame
        calendar_frame = tk.Frame(parent, bg=self.theme.bg_color)
        calendar_frame.pack(fill=tk.BOTH, expand=True, pady=10)

        # Days of week header
        days_frame = tk.Frame(calendar_frame, bg=self.theme.bg_color)
        days_frame.pack(fill=tk.X)

        days = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]
        for i, day in enumerate(days):
            tk.Label(
                days_frame,
                text=day,
                font=self.theme.small_font,
                bg=self.theme.bg_color,
                fg=self.theme.text_color,
                width=8,
            ).grid(row=0, column=i, padx=2, pady=5)

        # Calendar grid
        self.month_frame = tk.Frame(calendar_frame, bg=self.theme.bg_color)
        self.month_frame.pack(fill=tk.BOTH, expand=True)

        # Display current month
        self.display_month()

        # Events frame
        events_frame = tk.LabelFrame(
            parent,
            text="Check-in Details",
            font=self.theme.pixel_font,
            bg=self.theme.bg_color,
            fg=self.theme.habit_color,  # Use the theme's habit color
            padx=10,
            pady=10,
        )
        events_frame.pack(fill=tk.X, pady=10, padx=10)

        # Create a frame for the events list that will be updated
        self.events_list_frame = tk.Frame(events_frame, bg=self.theme.bg_color)
        self.events_list_frame.pack(fill=tk.BOTH, expand=True)

        # Display check-ins for current month
        self.display_check_ins()

        # Display upcoming appointments
        self.display_upcoming_appointments(parent)

    def prev_month(self):
        """Move to the previous month in the calendar."""
        if self.selected_month == 1:
            self.selected_month = 12
            self.selected_year -= 1
        else:
            self.selected_month -= 1

        self.update_calendar_view()

    def next_month(self):
        """Move to the next month in the calendar."""
        if self.selected_month == 12:
            self.selected_month = 1
            self.selected_year += 1
        else:
            self.selected_month += 1

        self.update_calendar_view()

    def update_calendar_view(self):
        """Update the calendar view with the selected month."""
        # Update month label
        self.month_label.config(
            text=f"{calendar.month_name[self.selected_month]} {self.selected_year}"
        )

        # Clear calendar grid
        for widget in self.month_frame.winfo_children():
            widget.destroy()

        # Display the month
        self.display_month()

        # Update check-ins list
        self.display_check_ins()

    def display_month(self):
        """Display the selected month in the calendar grid."""
        # Get calendar for selected month
        cal = calendar.monthcalendar(self.selected_year, self.selected_month)

        # Today's date for highlighting
        today = datetime.now().date()

        # Get all check-in dates
        check_in_dates = []
        for check_in in self.data.get("habits", {}).get("check_ins", []):
            for date_str in check_in.get("dates", []):
                check_in_dates.append(date_str)

        # Display calendar
        for week_idx, week in enumerate(cal):
            for day_idx, day in enumerate(week):
                if day == 0:
                    # Empty cell for days not in this month
                    frame = tk.Frame(
                        self.month_frame, bg=self.theme.bg_color, width=80, height=80
                    )
                    frame.grid(row=week_idx, column=day_idx, padx=2, pady=2)
                    frame.grid_propagate(False)
                else:
                    # Create frame for this day
                    date_obj = date(self.selected_year, self.selected_month, day)
                    date_str = date_obj.strftime("%Y-%m-%d")

                    # Check if this is today
                    is_today = date_obj == today

                    # Check if there are check-ins on this day
                    has_check_in = date_str in check_in_dates

                    # Set frame color based on conditions
                    if is_today:
                        bg_color = "#FFF9C4"  # Light yellow for today
                    elif has_check_in:
                        bg_color = "#E3F2FD"  # Light blue for check-in days
                    else:
                        bg_color = self.theme.bg_color

                    frame = tk.Frame(
                        self.month_frame,
                        bg=bg_color,
                        width=80,
                        height=80,
                        relief=tk.RIDGE if is_today else tk.FLAT,
                        bd=2 if is_today else 0,
                    )
                    frame.grid(row=week_idx, column=day_idx, padx=2, pady=2)
                    frame.grid_propagate(False)

                    # Day number
                    day_label = tk.Label(
                        frame,
                        text=str(day),
                        font=self.theme.small_font,
                        bg=bg_color,
                        fg="#FF5722" if is_today else self.theme.text_color,
                    )
                    day_label.pack(anchor="nw", padx=5, pady=2)

                    # If there are check-ins on this day, show indicators
                    if has_check_in:
                        # Find all check-ins for this day
                        day_check_ins = []
                        for check_in in self.data.get("habits", {}).get(
                            "check_ins", []
                        ):
                            if date_str in check_in.get("dates", []):
                                day_check_ins.append(check_in)

                        # Show up to 3 check-in icons with tooltips
                        for i, check_in in enumerate(day_check_ins[:3]):
                            icon_label = tk.Label(
                                frame,
                                text=check_in.get("icon", "🩺"),
                                font=("TkDefaultFont", 9),
                                bg=bg_color,
                                fg=self.theme.text_color,
                            )
                            icon_label.pack(anchor="w", padx=5, pady=0)

                            # Add binding for click to show details
                            icon_label.bind(
                                "<Button-1>",
                                lambda e, d=date_str: self.show_check_in_details(d),
                            )

                        # If more than 3, show a "more" indicator
                        if len(day_check_ins) > 3:
                            more_label = tk.Label(
                                frame,
                                text=f"+{len(day_check_ins) - 3} more",
                                font=("TkDefaultFont", 7),
                                bg=bg_color,
                                fg="#2196F3",
                            )
                            more_label.pack(anchor="w", padx=5, pady=0)

                            # Add binding for click to show details
                            more_label.bind(
                                "<Button-1>",
                                lambda e, d=date_str: self.show_check_in_details(d),
                            )

                    # Make the entire day clickable to add check-in
                    frame.bind(
                        "<Button-1>",
                        lambda e, d=date_str: self.show_check_in_details(d),
                    )
                    day_label.bind(
                        "<Button-1>",
                        lambda e, d=date_str: self.show_check_in_details(d),
                    )

    def show_check_in_details(self, date_str):
        """
        Show details of check-ins for a specific date.

        Args:
            date_str: Date string in YYYY-MM-DD format
        """
        # Clear the events list frame
        for widget in self.events_list_frame.winfo_children():
            widget.destroy()

        # Format the date for display
        try:
            date_obj = datetime.strptime(date_str, "%Y-%m-%d").date()
            formatted_date = date_obj.strftime("%B %d, %Y")
        except:
            formatted_date = date_str

        # Title with date
        title_frame = tk.Frame(self.events_list_frame, bg=self.theme.bg_color)
        title_frame.pack(fill=tk.X, pady=5)

        date_label = tk.Label(
            title_frame,
            text=f"Check-ins for {formatted_date}",
            font=self.theme.pixel_font,
            bg=self.theme.bg_color,
            fg=self.theme.text_color,
        )
        date_label.pack(side=tk.LEFT)

        # Add button for this date
        add_button = self.theme.create_pixel_button(
            title_frame,
            "Add Check-in",
            lambda: self.add_check_in_for_date(date_str),
            color=self.theme.habit_color,
            small=True,
        )
        add_button.pack(side=tk.RIGHT, padx=5)

        # Find check-ins for this date
        has_check_ins = False
        for check_in in self.data.get("habits", {}).get("check_ins", []):
            if date_str in check_in.get("dates", []):
                has_check_ins = True

                # Create a card for this check-in
                check_in_frame = tk.Frame(
                    self.events_list_frame,
                    bg=self.theme.darken_color(self.theme.bg_color),
                    relief=tk.RAISED,
                    bd=1,
                    padx=10,
                    pady=10,
                )
                check_in_frame.pack(fill=tk.X, pady=5, padx=5)

                # Header with icon and name
                header_frame = tk.Frame(
                    check_in_frame, bg=self.theme.darken_color(self.theme.bg_color)
                )
                header_frame.pack(fill=tk.X, pady=5)

                icon_label = tk.Label(
                    header_frame,
                    text=check_in.get("icon", "🩺"),
                    font=self.theme.pixel_font,
                    bg=self.theme.darken_color(self.theme.bg_color),
                    fg=self.theme.text_color,
                )
                icon_label.pack(side=tk.LEFT, padx=5)

                name_label = tk.Label(
                    header_frame,
                    text=check_in["name"],
                    font=self.theme.small_font,
                    bg=self.theme.darken_color(self.theme.bg_color),
                    fg=self.theme.text_color,
                )
                name_label.pack(side=tk.LEFT, padx=5)

                # Show category if exists
                if "category" in check_in:
                    category_frame = tk.Frame(
                        check_in_frame, bg=self.theme.darken_color(self.theme.bg_color)
                    )
                    category_frame.pack(fill=tk.X, pady=2)

                    category_label = tk.Label(
                        category_frame,
                        text=f"Category: {check_in['category']}",
                        font=("TkDefaultFont", 9),
                        bg=self.theme.darken_color(self.theme.bg_color),
                        fg=self.theme.text_color,
                    )
                    category_label.pack(anchor="w", padx=5)

                # Notes for this date if exists
                if date_str in check_in.get("notes", {}):
                    notes_frame = tk.Frame(
                        check_in_frame, bg=self.theme.darken_color(self.theme.bg_color)
                    )
                    notes_frame.pack(fill=tk.X, pady=5)

                    notes_label = tk.Label(
                        notes_frame,
                        text=f"Notes: {check_in['notes'][date_str]}",
                        font=("TkDefaultFont", 9),
                        bg=self.theme.darken_color(self.theme.bg_color),
                        fg=self.theme.text_color,
                        wraplength=400,
                        justify=tk.LEFT,
                    )
                    notes_label.pack(anchor="w", padx=5)

                # If it's a doctor appointment with subcategories, show details
                if (
                    check_in["name"] == "Doctor Appointments"
                    and "subcategories" in check_in
                ):
                    for subcat in check_in.get("subcategories", []):
                        # Check if this subcategory matches this date
                        if subcat.get("last_date") == date_str:
                            subcat_frame = tk.Frame(
                                check_in_frame,
                                bg=self.theme.darken_color(self.theme.bg_color),
                            )
                            subcat_frame.pack(fill=tk.X, pady=2)

                            subcat_label = tk.Label(
                                subcat_frame,
                                text=f"Type: {subcat['name']}",
                                font=("TkDefaultFont", 9, "bold"),
                                bg=self.theme.darken_color(self.theme.bg_color),
                                fg=self.theme.text_color,
                            )
                            subcat_label.pack(anchor="w", padx=5)

                            next_date_obj = datetime.strptime(
                                subcat.get("next_date", "2025-01-01"), "%Y-%m-%d"
                            ).date()
                            next_date_str = next_date_obj.strftime("%B %d, %Y")

                            next_date_label = tk.Label(
                                subcat_frame,
                                text=f"Next appointment: {next_date_str}",
                                font=("TkDefaultFont", 9),
                                bg=self.theme.darken_color(self.theme.bg_color),
                                fg="#FF5722",  # Orange for next date
                            )
                            next_date_label.pack(anchor="w", padx=5)

                # Action buttons
                button_frame = tk.Frame(
                    check_in_frame, bg=self.theme.darken_color(self.theme.bg_color)
                )
                button_frame.pack(fill=tk.X, pady=5)

                edit_button = tk.Button(
                    button_frame,
                    text="Edit Notes",
                    font=self.theme.small_font,
                    bg=self.theme.primary_color,
                    fg=self.theme.text_color,
                    relief=tk.FLAT,
                    command=lambda c=check_in, d=date_str: self.edit_check_in_notes(
                        c, d
                    ),
                )
                edit_button.pack(side=tk.LEFT, padx=5)

                delete_button = tk.Button(
                    button_frame,
                    text="Remove Check-in",
                    font=self.theme.small_font,
                    bg="#F44336",
                    fg="white",
                    relief=tk.FLAT,
                    command=lambda c=check_in, d=date_str: self.remove_check_in_date(
                        c, d
                    ),
                )
                delete_button.pack(side=tk.LEFT, padx=5)

        # Show message if no check-ins for this date
        if not has_check_ins:
            tk.Label(
                self.events_list_frame,
                text=f"No check-ins scheduled for {formatted_date}",
                font=self.theme.small_font,
                bg=self.theme.bg_color,
                fg=self.theme.text_color,
                pady=20,
            ).pack()

    def display_check_ins(self):
        """Display check-ins for the selected month."""
        # Clear the events list frame
        for widget in self.events_list_frame.winfo_children():
            widget.destroy()

        # Display month heading
        month_name = calendar.month_name[self.selected_month]
        year = self.selected_year

        tk.Label(
            self.events_list_frame,
            text=f"Check-ins for {month_name} {year}",
            font=self.theme.pixel_font,
            bg=self.theme.bg_color,
            fg=self.theme.text_color,
            pady=10,
        ).pack()

        # Find all check-ins for this month
        month_start = date(year, self.selected_month, 1)
        month_end = date(
            year, self.selected_month, calendar.monthrange(year, self.selected_month)[1]
        )

        found_check_ins = False

        # Create a scrollable frame for check-ins
        canvas = tk.Canvas(
            self.events_list_frame,
            bg=self.theme.bg_color,
            highlightthickness=0,
            height=200,
        )
        scrollbar = ttk.Scrollbar(
            self.events_list_frame,
            orient="vertical",
            command=canvas.yview,
        )
        scroll_frame = tk.Frame(canvas, bg=self.theme.bg_color)

        scroll_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all")),
        )

        canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True, padx=5, pady=5)
        scrollbar.pack(side="right", fill="y")

        # Iterate through check-ins
        for check_in in self.data.get("habits", {}).get("check_ins", []):
            for date_str in check_in.get("dates", []):
                try:
                    check_date = datetime.strptime(date_str, "%Y-%m-%d").date()
                    if month_start <= check_date <= month_end:
                        found_check_ins = True

                        # Create entry for this check-in
                        date_frame = tk.Frame(
                            scroll_frame, bg=self.theme.bg_color, pady=5
                        )
                        date_frame.pack(fill=tk.X)

                        # Format date as "Mon, Sep 15"
                        formatted_date = check_date.strftime("%a, %b %d")

                        date_label = tk.Label(
                            date_frame,
                            text=formatted_date,
                            font=self.theme.small_font,
                            bg=self.theme.bg_color,
                            fg=self.theme.text_color,
                            width=12,
                            anchor="w",
                        )
                        date_label.pack(side=tk.LEFT, padx=5)

                        check_in_label = tk.Label(
                            date_frame,
                            text=f"{check_in.get('icon', '🩺')} {check_in['name']}",
                            font=self.theme.small_font,
                            bg=self.theme.bg_color,
                            fg=self.theme.text_color,
                            anchor="w",
                        )
                        check_in_label.pack(
                            side=tk.LEFT, padx=5, fill=tk.X, expand=True
                        )

                        # Make the entire row clickable to view details
                        date_frame.bind(
                            "<Button-1>",
                            lambda e, d=date_str: self.show_check_in_details(d),
                        )
                        date_label.bind(
                            "<Button-1>",
                            lambda e, d=date_str: self.show_check_in_details(d),
                        )
                        check_in_label.bind(
                            "<Button-1>",
                            lambda e, d=date_str: self.show_check_in_details(d),
                        )
                except ValueError:
                    # Skip invalid dates
                    continue

        if not found_check_ins:
            tk.Label(
                scroll_frame,
                text=f"No check-ins found for {month_name} {year}",
                font=self.theme.small_font,
                bg=self.theme.bg_color,
                fg=self.theme.text_color,
                pady=20,
            ).pack()

    def display_upcoming_appointments(self, parent):
        """
        Display upcoming doctor appointments.

        Args:
            parent: Parent frame to place the upcoming appointments view
        """
        # Create frame for upcoming appointments
        upcoming_frame = tk.LabelFrame(
            parent,
            text="Upcoming Doctor Appointments",
            font=self.theme.pixel_font,
            bg=self.theme.bg_color,
            fg="#E91E63",  # Pink for medical
            padx=10,
            pady=10,
        )
        upcoming_frame.pack(fill=tk.X, pady=10, padx=10)

        # Find doctor appointments check-in
        doctor_appointments = None
        for check_in in self.data.get("habits", {}).get("check_ins", []):
            if check_in["name"] == "Doctor Appointments":
                doctor_appointments = check_in
                break

        if not doctor_appointments or "subcategories" not in doctor_appointments:
            tk.Label(
                upcoming_frame,
                text="No upcoming doctor appointments found",
                font=self.theme.small_font,
                bg=self.theme.bg_color,
                fg=self.theme.text_color,
                pady=10,
            ).pack()
            return

        # Create a grid layout for appointments
        appointment_frame = tk.Frame(upcoming_frame, bg=self.theme.bg_color)
        appointment_frame.pack(fill=tk.X, pady=5)

        # Headers
        tk.Label(
            appointment_frame,
            text="Doctor Type",
            font=self.theme.small_font,
            bg=self.theme.bg_color,
            fg=self.theme.text_color,
            width=15,
            anchor="w",
        ).grid(row=0, column=0, padx=5, pady=5, sticky="w")

        tk.Label(
            appointment_frame,
            text="Last Visit",
            font=self.theme.small_font,
            bg=self.theme.bg_color,
            fg=self.theme.text_color,
            width=15,
            anchor="w",
        ).grid(row=0, column=1, padx=5, pady=5, sticky="w")

        tk.Label(
            appointment_frame,
            text="Next Appointment",
            font=self.theme.small_font,
            bg=self.theme.bg_color,
            fg=self.theme.text_color,
            width=15,
            anchor="w",
        ).grid(row=0, column=2, padx=5, pady=5, sticky="w")

        tk.Label(
            appointment_frame,
            text="Actions",
            font=self.theme.small_font,
            bg=self.theme.bg_color,
            fg=self.theme.text_color,
            width=10,
            anchor="w",
        ).grid(row=0, column=3, padx=5, pady=5, sticky="w")

        # Display each subcategory
        today = datetime.now().date()
        row = 1

        for subcat in doctor_appointments.get("subcategories", []):
            # Get the last date
            last_date_str = subcat.get("last_date", "")
            next_date_str = subcat.get("next_date", "")

            try:
                last_date = datetime.strptime(last_date_str, "%Y-%m-%d").date()
                last_date_formatted = last_date.strftime("%b %d, %Y")
            except:
                last_date_formatted = "Not set"

            try:
                next_date = datetime.strptime(next_date_str, "%Y-%m-%d").date()
                next_date_formatted = next_date.strftime("%b %d, %Y")

                # Check if next appointment is soon (within 30 days)
                days_until = (next_date - today).days
                if days_until <= 30 and days_until >= 0:
                    next_date_color = "#F44336"  # Red for urgent
                elif days_until < 0:
                    next_date_color = "#9C27B0"  # Purple for overdue
                else:
                    next_date_color = "#4CAF50"  # Green for ok
            except:
                next_date_formatted = "Not scheduled"
                next_date_color = self.theme.text_color

            # Name
            tk.Label(
                appointment_frame,
                text=subcat["name"],
                font=self.theme.small_font,
                bg=self.theme.bg_color,
                fg=self.theme.text_color,
                anchor="w",
            ).grid(row=row, column=0, padx=5, pady=5, sticky="w")

            # Last date
            tk.Label(
                appointment_frame,
                text=last_date_formatted,
                font=self.theme.small_font,
                bg=self.theme.bg_color,
                fg=self.theme.text_color,
                anchor="w",
            ).grid(row=row, column=1, padx=5, pady=5, sticky="w")

            # Next date
            tk.Label(
                appointment_frame,
                text=next_date_formatted,
                font=self.theme.small_font,
                bg=self.theme.bg_color,
                fg=next_date_color,
                anchor="w",
            ).grid(row=row, column=2, padx=5, pady=5, sticky="w")

            # Actions
            actions_frame = tk.Frame(appointment_frame, bg=self.theme.bg_color)
            actions_frame.grid(row=row, column=3, padx=5, pady=5, sticky="w")

            update_button = tk.Button(
                actions_frame,
                text="Update",
                font=("TkDefaultFont", 8),
                bg=self.theme.primary_color,
                fg=self.theme.text_color,
                relief=tk.FLAT,
                command=lambda s=subcat: self.update_doctor_appointment(s),
            )
            update_button.pack(side=tk.LEFT, padx=2)

            row += 1

    def add_new_check_in(self):
        """Open a dialog to add a new check-in type."""
        # Create a dialog window
        dialog = tk.Toplevel(self.app.root)
        dialog.title("Add New Check-in Type")
        dialog.geometry("400x250")
        dialog.configure(bg=self.theme.bg_color)
        dialog.transient(self.app.root)
        dialog.grab_set()

        # Name input
        name_frame = tk.Frame(dialog, bg=self.theme.bg_color)
        name_frame.pack(fill=tk.X, padx=20, pady=10)

        tk.Label(
            name_frame,
            text="Check-in Name:",
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

        icon_var = tk.StringVar(value="🩺")
        icons = [
            "🩺",
            "🦷",
            "🩻",
            "💉",
            "💊",
            "🏥",
            "👩‍⚕️",
            "👨‍⚕️",
            "🧬",
            "🔬",
            "📋",
            "🧠",
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
            categories = ["Health"]  # Default if no categories

        category_var = tk.StringVar(value=categories[0] if categories else "Health")

        category_dropdown = ttk.Combobox(
            category_frame,
            textvariable=category_var,
            values=categories,
            font=self.theme.small_font,
            width=15,
        )
        category_dropdown.pack(side=tk.LEFT, padx=10)

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
            "Add Check-in",
            lambda: self.save_new_check_in(
                name_var.get(),
                icon_var.get(),
                category_var.get(),
                dialog,
            ),
            color=self.theme.habit_color,
        )
        add_button.pack(side=tk.LEFT, padx=10)

        # Focus the name entry
        name_entry.focus_set()

    def save_new_check_in(self, name, icon, category, dialog):
        """
        Save a new check-in type to the data.

        Args:
            name: Check-in name
            icon: Check-in icon
            category: Check-in category
            dialog: Dialog window to close after saving
        """
        # Validate input
        if not name:
            messagebox.showerror("Error", "Please enter a check-in name.")
            return

        # Check if check-in name already exists
        for check_in in self.data["habits"].get("check_ins", []):
            if check_in["name"] == name:
                messagebox.showerror(
                    "Error", f"A check-in named '{name}' already exists."
                )
                return

        # Create new check-in
        new_check_in = {
            "name": name,
            "icon": icon,
            "category": category,
            "dates": [],
            "notes": {},
        }

        # Add to check-ins
        self.data["habits"]["check_ins"].append(new_check_in)

        # Save data
        self.data_manager.save_data()

        # Close dialog
        dialog.destroy()

        # Refresh display
        self.habit_tracker.refresh_display()

        # Show confirmation
        messagebox.showinfo("Success", f"Check-in '{name}' has been added!")

    def add_check_in_for_date(self, date_str):
        """
        Add a check-in for a specific date.

        Args:
            date_str: Date string in YYYY-MM-DD format
        """
        # Format date for display
        try:
            date_obj = datetime.strptime(date_str, "%Y-%m-%d").date()
            formatted_date = date_obj.strftime("%B %d, %Y")
        except:
            formatted_date = date_str

        # Create a dialog window
        dialog = tk.Toplevel(self.app.root)
        dialog.title(f"Add Check-in for {formatted_date}")
        dialog.geometry("400x300")
        dialog.configure(bg=self.theme.bg_color)
        dialog.transient(self.app.root)
        dialog.grab_set()

        # Check-in type selection
        type_frame = tk.Frame(dialog, bg=self.theme.bg_color)
        type_frame.pack(fill=tk.X, padx=20, pady=10)

        tk.Label(
            type_frame,
            text="Check-in Type:",
            font=self.theme.small_font,
            bg=self.theme.bg_color,
            fg=self.theme.text_color,
        ).pack(side=tk.LEFT)

        # Get all check-in types
        check_in_names = []
        for check_in in self.data["habits"].get("check_ins", []):
            check_in_names.append(f"{check_in.get('icon', '🩺')} {check_in['name']}")

        if not check_in_names:
            messagebox.showinfo(
                "No Check-in Types",
                "Please add check-in types first.",
            )
            dialog.destroy()
            return

        type_var = tk.StringVar(value=check_in_names[0] if check_in_names else "")

        type_dropdown = ttk.Combobox(
            type_frame,
            textvariable=type_var,
            values=check_in_names,
            font=self.theme.small_font,
            width=30,
        )
        type_dropdown.pack(side=tk.LEFT, padx=10)

        # If it's a doctor appointment, add subcategory selection
        is_doctor_var = tk.BooleanVar(value=False)
        subcategory_var = tk.StringVar()
        subcategory_frame = tk.Frame(dialog, bg=self.theme.bg_color)

        # Function to update UI based on selection
        def on_type_change(*args):
            selected = type_var.get()
            is_doctor = "Doctor Appointments" in selected
            is_doctor_var.set(is_doctor)

            if is_doctor:
                # Get doctor subcategories
                subcategory_frame.pack(fill=tk.X, padx=20, pady=10)

                for check_in in self.data["habits"].get("check_ins", []):
                    if (
                        check_in["name"] == "Doctor Appointments"
                        and "subcategories" in check_in
                    ):
                        subcats = [
                            subcat["name"]
                            for subcat in check_in.get("subcategories", [])
                        ]
                        subcategory_dropdown["values"] = subcats
                        if subcats:
                            subcategory_var.set(subcats[0])
            else:
                subcategory_frame.pack_forget()

        # Create subcategory selection
        tk.Label(
            subcategory_frame,
            text="Doctor Type:",
            font=self.theme.small_font,
            bg=self.theme.bg_color,
            fg=self.theme.text_color,
        ).pack(side=tk.LEFT)

        subcategory_dropdown = ttk.Combobox(
            subcategory_frame,
            textvariable=subcategory_var,
            font=self.theme.small_font,
            width=20,
        )
        subcategory_dropdown.pack(side=tk.LEFT, padx=10)

        # Bind change event
        type_var.trace_add("write", on_type_change)

        # Notes input
        notes_frame = tk.Frame(dialog, bg=self.theme.bg_color)
        notes_frame.pack(fill=tk.X, padx=20, pady=10)

        tk.Label(
            notes_frame,
            text="Notes:",
            font=self.theme.small_font,
            bg=self.theme.bg_color,
            fg=self.theme.text_color,
        ).pack(anchor="w")

        notes_text = tk.Text(
            notes_frame,
            font=self.theme.small_font,
            bg=self.theme.primary_color,
            fg=self.theme.text_color,
            height=5,
            width=40,
        )
        notes_text.pack(pady=5)

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
            "Add Check-in",
            lambda: self.save_check_in_for_date(
                type_var.get(),
                date_str,
                notes_text.get("1.0", tk.END).strip(),
                is_doctor_var.get(),
                subcategory_var.get(),
                dialog,
            ),
            color=self.theme.habit_color,
        )
        add_button.pack(side=tk.LEFT, padx=10)

        # Trigger initial update
        on_type_change()

    def save_check_in_for_date(
        self, check_in_display, date_str, notes, is_doctor, subcategory, dialog
    ):
        """
        Save a check-in for a specific date.

        Args:
            check_in_display: Display string of check-in type (with icon)
            date_str: Date string in YYYY-MM-DD format
            notes: Notes for this check-in
            is_doctor: Whether this is a doctor appointment
            subcategory: Doctor subcategory if applicable
            dialog: Dialog window to close after saving
        """
        # Extract check-in name from display string
        check_in_name = (
            check_in_display.split(" ", 1)[1]
            if " " in check_in_display
            else check_in_display
        )

        # Find the check-in
        check_in = None
        check_in_index = -1

        for i, c in enumerate(self.data["habits"].get("check_ins", [])):
            if c["name"] == check_in_name:
                check_in = c
                check_in_index = i
                break

        if check_in is None:
            messagebox.showerror("Error", f"Check-in type '{check_in_name}' not found.")
            return

        # Add date to check-in dates if not already there
        if date_str not in check_in.get("dates", []):
            check_in["dates"].append(date_str)

        # Add notes if provided
        if notes:
            if "notes" not in check_in:
                check_in["notes"] = {}
            check_in["notes"][date_str] = notes

        # Handle doctor appointment subcategory
        if is_doctor and subcategory:
            # Find the subcategory
            for i, subcat in enumerate(check_in.get("subcategories", [])):
                if subcat["name"] == subcategory:
                    # Update last date
                    subcat["last_date"] = date_str

                    # Calculate next date (6 months later)
                    next_date = datetime.strptime(date_str, "%Y-%m-%d").date()
                    next_date = date(
                        next_date.year + ((next_date.month + 6) // 12),
                        ((next_date.month + 6) % 12) or 12,
                        next_date.day,
                    )
                    subcat["next_date"] = next_date.strftime("%Y-%m-%d")
                    break

        # Save data
        self.data_manager.save_data()

        # Close dialog
        dialog.destroy()

        # Refresh display and show check-in details
        self.update_calendar_view()
        self.show_check_in_details(date_str)

        # Show confirmation
        messagebox.showinfo("Success", f"Check-in added for {date_str}")

    def edit_check_in_notes(self, check_in, date_str):
        """
        Edit notes for a check-in on a specific date.

        Args:
            check_in: Check-in object
            date_str: Date string in YYYY-MM-DD format
        """
        # Format date for display
        try:
            date_obj = datetime.strptime(date_str, "%Y-%m-%d").date()
            formatted_date = date_obj.strftime("%B %d, %Y")
        except:
            formatted_date = date_str

        # Create a dialog window
        dialog = tk.Toplevel(self.app.root)
        dialog.title(f"Edit Notes for {check_in['name']} on {formatted_date}")
        dialog.geometry("500x300")
        dialog.configure(bg=self.theme.bg_color)
        dialog.transient(self.app.root)
        dialog.grab_set()

        # Notes input
        notes_frame = tk.Frame(dialog, bg=self.theme.bg_color)
        notes_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        tk.Label(
            notes_frame,
            text="Notes:",
            font=self.theme.small_font,
            bg=self.theme.bg_color,
            fg=self.theme.text_color,
        ).pack(anchor="w")

        # Get existing notes
        existing_notes = check_in.get("notes", {}).get(date_str, "")

        notes_text = tk.Text(
            notes_frame,
            font=self.theme.small_font,
            bg=self.theme.primary_color,
            fg=self.theme.text_color,
            height=10,
            width=50,
        )
        notes_text.insert("1.0", existing_notes)
        notes_text.pack(pady=5, fill=tk.BOTH, expand=True)

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

        # Save button
        save_button = self.theme.create_pixel_button(
            button_frame,
            "Save Notes",
            lambda: self.save_check_in_notes(
                check_in,
                date_str,
                notes_text.get("1.0", tk.END).strip(),
                dialog,
            ),
            color=self.theme.habit_color,
        )
        save_button.pack(side=tk.LEFT, padx=10)

        # Focus the text field
        notes_text.focus_set()

    def save_check_in_notes(self, check_in, date_str, notes, dialog):
        """
        Save notes for a check-in on a specific date.

        Args:
            check_in: Check-in object
            date_str: Date string in YYYY-MM-DD format
            notes: Notes text
            dialog: Dialog window to close after saving
        """
        # Update notes
        if "notes" not in check_in:
            check_in["notes"] = {}

        if notes:
            check_in["notes"][date_str] = notes
        elif date_str in check_in["notes"]:
            # Remove empty notes
            del check_in["notes"][date_str]

        # Save data
        self.data_manager.save_data()

        # Close dialog
        dialog.destroy()

        # Refresh the check-in details
        self.show_check_in_details(date_str)

        # Show confirmation
        messagebox.showinfo("Success", "Notes updated successfully")

    def remove_check_in_date(self, check_in, date_str):
        """
        Remove a check-in date.

        Args:
            check_in: Check-in object
            date_str: Date string in YYYY-MM-DD format
        """
        # Confirm deletion
        if not messagebox.askyesno(
            "Confirm Deletion",
            f"Are you sure you want to remove this check-in for {date_str}?",
        ):
            return

        # Remove date from check-in
        if date_str in check_in.get("dates", []):
            check_in["dates"].remove(date_str)

        # Remove notes for this date
        if date_str in check_in.get("notes", {}):
            del check_in["notes"][date_str]

        # Save data
        self.data_manager.save_data()

        # Refresh display
        self.update_calendar_view()

        # Show message
        messagebox.showinfo("Success", "Check-in removed successfully")

        # Display the month view
        self.display_check_ins()

    def update_doctor_appointment(self, subcategory):
        """
        Update a doctor appointment subcategory.

        Args:
            subcategory: Subcategory object
        """
        # Create a dialog window
        dialog = tk.Toplevel(self.app.root)
        dialog.title(f"Update {subcategory['name']} Appointment")
        dialog.geometry("400x300")
        dialog.configure(bg=self.theme.bg_color)
        dialog.transient(self.app.root)
        dialog.grab_set()

        # Last visit date
        last_date_frame = tk.Frame(dialog, bg=self.theme.bg_color)
        last_date_frame.pack(fill=tk.X, padx=20, pady=10)

        tk.Label(
            last_date_frame,
            text="Last Visit Date:",
            font=self.theme.small_font,
            bg=self.theme.bg_color,
            fg=self.theme.text_color,
        ).pack(anchor="w")

        # Get existing date
        try:
            last_date = datetime.strptime(
                subcategory.get("last_date", ""), "%Y-%m-%d"
            ).date()
        except:
            last_date = datetime.now().date()

        # Date entry with calendar picker
        last_date_var = tk.StringVar(value=last_date.strftime("%Y-%m-%d"))

        last_date_entry = tk.Entry(
            last_date_frame,
            textvariable=last_date_var,
            font=self.theme.small_font,
            bg=self.theme.primary_color,
            fg=self.theme.text_color,
            width=15,
        )
        last_date_entry.pack(side=tk.LEFT, padx=5, pady=5)

        tk.Label(
            last_date_frame,
            text="(YYYY-MM-DD)",
            font=("TkDefaultFont", 8),
            bg=self.theme.bg_color,
            fg=self.theme.text_color,
        ).pack(side=tk.LEFT, padx=5)

        # Next appointment date
        next_date_frame = tk.Frame(dialog, bg=self.theme.bg_color)
        next_date_frame.pack(fill=tk.X, padx=20, pady=10)

        tk.Label(
            next_date_frame,
            text="Next Appointment Date:",
            font=self.theme.small_font,
            bg=self.theme.bg_color,
            fg=self.theme.text_color,
        ).pack(anchor="w")

        # Get existing next date
        try:
            next_date = datetime.strptime(
                subcategory.get("next_date", ""), "%Y-%m-%d"
            ).date()
        except:
            next_date = last_date + timedelta(days=180)  # Default to 6 months

        # Date entry with calendar picker
        next_date_var = tk.StringVar(value=next_date.strftime("%Y-%m-%d"))

        next_date_entry = tk.Entry(
            next_date_frame,
            textvariable=next_date_var,
            font=self.theme.small_font,
            bg=self.theme.primary_color,
            fg=self.theme.text_color,
            width=15,
        )
        next_date_entry.pack(side=tk.LEFT, padx=5, pady=5)

        tk.Label(
            next_date_frame,
            text="(YYYY-MM-DD)",
            font=("TkDefaultFont", 8),
            bg=self.theme.bg_color,
            fg=self.theme.text_color,
        ).pack(side=tk.LEFT, padx=5)

        # Interval in months
        interval_frame = tk.Frame(dialog, bg=self.theme.bg_color)
        interval_frame.pack(fill=tk.X, padx=20, pady=10)

        tk.Label(
            interval_frame,
            text="Interval (months):",
            font=self.theme.small_font,
            bg=self.theme.bg_color,
            fg=self.theme.text_color,
        ).pack(side=tk.LEFT)

        interval_var = tk.StringVar(value=str(subcategory.get("interval_months", 6)))

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
        interval_entry.pack(side=tk.LEFT, padx=5)

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

        # Save button
        save_button = self.theme.create_pixel_button(
            button_frame,
            "Save",
            lambda: self.save_doctor_appointment(
                subcategory,
                last_date_var.get(),
                next_date_var.get(),
                interval_var.get(),
                dialog,
            ),
            color=self.theme.habit_color,
        )
        save_button.pack(side=tk.LEFT, padx=10)

    def save_doctor_appointment(
        self, subcategory, last_date_str, next_date_str, interval_str, dialog
    ):
        """
        Save updates to a doctor appointment subcategory.

        Args:
            subcategory: Subcategory object
            last_date_str: Last visit date as string
            next_date_str: Next appointment date as string
            interval_str: Interval in months as string
            dialog: Dialog window to close after saving
        """
        # Validate dates
        try:
            last_date = datetime.strptime(last_date_str, "%Y-%m-%d").date()
        except ValueError:
            messagebox.showerror(
                "Error", "Invalid last visit date format. Use YYYY-MM-DD."
            )
            return

        try:
            next_date = datetime.strptime(next_date_str, "%Y-%m-%d").date()
        except ValueError:
            messagebox.showerror(
                "Error", "Invalid next appointment date format. Use YYYY-MM-DD."
            )
            return

        try:
            interval = int(interval_str)
            if interval <= 0:
                raise ValueError("Interval must be positive")
        except ValueError:
            messagebox.showerror("Error", "Interval must be a positive number.")
            return

        # Update subcategory
        subcategory["last_date"] = last_date_str
        subcategory["next_date"] = next_date_str
        subcategory["interval_months"] = interval

        # Find doctor appointments check-in
        for check_in in self.data.get("habits", {}).get("check_ins", []):
            if check_in["name"] == "Doctor Appointments":
                # Make sure the last_date is in the dates list
                if last_date_str not in check_in.get("dates", []):
                    check_in["dates"].append(last_date_str)
                break

        # Save data
        self.data_manager.save_data()

        # Close dialog
        dialog.destroy()

        # Refresh display
        self.habit_tracker.refresh_display()

        # Show confirmation
        messagebox.showinfo(
            "Success",
            f"{subcategory['name']} appointment updated successfully.\nNext appointment: {next_date_str}",
        )
