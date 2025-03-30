"""
Pomodoro Timer module for the Pixel Quest application.
Implements a customizable pomodoro timer with module integration.
"""

import tkinter as tk
from tkinter import ttk, messagebox
import time
from datetime import datetime
import json
import random

try:
    from plyer import notification
    import winsound  # For Windows
except ImportError:
    # Fallback for systems without plyer or winsound
    notification = None
    winsound = None


class PomodoroModule:
    """
    Manages the Pomodoro Timer functionality.
    """

    def __init__(self, app, data_manager, theme):
        """
        Initialize the pomodoro timer module.

        Args:
            app: Main application instance
            data_manager: Data manager instance
            theme: Theme manager instance
        """
        self.app = app
        self.data_manager = data_manager
        self.data = data_manager.data
        self.theme = theme
        self.root = app.root

        # Initialize pomodoro data if not present
        if "pomodoro" not in self.data:
            self.data["pomodoro"] = {
                "work_time": 25,  # Work time in minutes
                "break_time": 5,  # Short break in minutes
                "long_break_time": 15,  # Long break in minutes
                "long_break_interval": 4,  # Number of pomodoros before long break
                "auto_start": True,  # Auto start next session
                "sound_enabled": True,  # Enable sound notifications
                "completed_pomodoros": 0,  # Total completed pomodoros
                "daily_pomodoros": {},  # Daily completed pomodoros
                "linked_modules": {},  # Modules to auto-update on completion
                "current_task": "",  # The current task being worked on
            }
            # Save the data
            self.data_manager.save_data()

        # Timer state variables
        self.timer_running = False
        self.current_timer = None
        self.time_left = 0
        self.pomodoro_count = 0
        self.is_break = False
        self.is_long_break = False
        self.timer_paused = False
        self.completed_today = self.get_completed_today()
        self.current_task = self.data["pomodoro"].get("current_task", "")

        # UI elements that will be initialized in show_module
        self.timer_label = None
        self.status_label = None
        self.progress_bar = None
        self.start_button = None
        self.pause_button = None
        self.reset_button = None
        self.module_integration_frame = None
        self.module_checkboxes = {}
        self.todo_tasks_var = None
        self.task_combobox = None
        self.task_label = None

        # Get notification module if available
        self.notification_available = notification is not None
        self.sound_available = winsound is not None

        # Pixel art border frame style
        self.pixel_border_style = {
            "relief": tk.RIDGE,
            "bd": 3,
            "bg": self.theme.bg_color,
        }

        # Motivational messages for work and break time
        self.work_messages = [
            "Focus on the task at hand!",
            "You've got this!",
            "Stay focused and productive!",
            "One pomodoro at a time!",
            "Keep going, you're doing great!",
        ]
        
        self.break_messages = [
            "Take a well-deserved break!",
            "Stretch, relax, and recharge!",
            "Time to rest your mind!",
            "Stand up and move around!",
            "Great work! Time to rest!"
        ]

    def show_module(self, parent):
        """
        Display the Pomodoro Timer interface.

        Args:
            parent: Parent widget to display the pomodoro timer
        """
        # Title
        title_frame = tk.Frame(parent, bg=self.theme.bg_color)
        title_frame.pack(pady=10)
        
        tk.Label(
            title_frame,
            text="⏱️ Pomodoro Timer",
            font=self.theme.heading_font,
            bg=self.theme.bg_color,
            fg=self.theme.text_color,
        ).pack(pady=5)

        # Subtitle description
        tk.Label(
            title_frame,
            text="Focus. Work. Rest. Repeat.",
            font=self.theme.pixel_font,
            bg=self.theme.bg_color,
            fg=self.theme.text_color,
        ).pack(pady=5)

        # Pack containing frame
        container = tk.Frame(parent, bg=self.theme.bg_color)
        container.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        # Create notebook with tabs
        tab_control = ttk.Notebook(container)
        tab_control.pack(expand=1, fill="both")

        # Timer tab
        timer_tab = tk.Frame(tab_control, bg=self.theme.bg_color)

        # Settings tab
        settings_tab = tk.Frame(tab_control, bg=self.theme.bg_color)

        # Stats tab
        stats_tab = tk.Frame(tab_control, bg=self.theme.bg_color)

        # Module integration tab
        integration_tab = tk.Frame(tab_control, bg=self.theme.bg_color)

        # Add tabs to notebook
        tab_control.add(timer_tab, text="Timer")
        tab_control.add(settings_tab, text="Settings")
        tab_control.add(stats_tab, text="Statistics")
        tab_control.add(integration_tab, text="Module Integration")

        # Create content for each tab
        self.create_timer_tab(timer_tab)
        self.create_settings_tab(settings_tab)
        self.create_stats_tab(stats_tab)
        self.create_integration_tab(integration_tab)

        # Bottom navigation - return to main menu
        back_button = self.theme.create_pixel_button(
            parent,
            "Back to Main Menu",
            self.app.show_main_menu,
            color=self.theme.primary_color,
        )
        back_button.pack(pady=10)

    def create_timer_tab(self, parent):
        """
        Create the main timer tab with controls.

        Args:
            parent: Parent widget for the timer tab
        """
        # Timer display frame
        timer_frame = tk.Frame(parent, **self.pixel_border_style)
        timer_frame.pack(pady=20)

        # Current session type indicator
        session_label = tk.Label(
            timer_frame,
            text="WORK SESSION" if not self.is_break else "BREAK TIME" if not self.is_long_break else "LONG BREAK",
            font=self.theme.pixel_font,
            bg=self.theme.bg_color,
            fg="#4CAF50" if not self.is_break else "#FF9800" if not self.is_long_break else "#2196F3",
        )
        session_label.pack(pady=(10, 5))

        # Timer display - large, easy to read
        self.timer_label = tk.Label(
            timer_frame,
            text="25:00",
            font=("DS-Digital", 72) if "DS-Digital" in tk.font.families() else ("Courier", 72, "bold"),
            bg=self.theme.bg_color,
            fg="#4CAF50" if not self.is_break else "#FF9800" if not self.is_long_break else "#2196F3",
        )
        self.timer_label.pack()

        # Status label with motivational message
        self.status_label = tk.Label(
            timer_frame,
            text="Ready to start",
            font=self.theme.pixel_font,
            bg=self.theme.bg_color,
            fg=self.theme.text_color,
            wraplength=400,
        )
        self.status_label.pack(pady=5)

        # Create a style for the progress bar
        style = ttk.Style()
        style.configure(
            "Pixel.Horizontal.TProgressbar",
            troughcolor=self.theme.bg_color,
            background="#4CAF50" if not self.is_break else "#FF9800" if not self.is_long_break else "#2196F3",
            thickness=25,
            borderwidth=2,
            relief="ridge",
        )

        # Progress bar
        self.progress_bar = ttk.Progressbar(
            timer_frame,
            orient="horizontal",
            length=400,
            mode="determinate",
            style="Pixel.Horizontal.TProgressbar",
        )
        self.progress_bar.pack(pady=10)

        # Task selection frame
        task_frame = tk.Frame(timer_frame, bg=self.theme.bg_color)
        task_frame.pack(pady=10, fill=tk.X)

        # Task selection label
        tk.Label(
            task_frame,
            text="Working on:",
            font=self.theme.small_font,
            bg=self.theme.bg_color,
            fg=self.theme.text_color,
        ).pack(side=tk.LEFT, padx=5)

        # Get todo tasks
        todo_tasks = []
        if "todo" in self.data and "tasks" in self.data["todo"]:
            todo_tasks = [
                task["title"] for task in self.data["todo"]["tasks"] 
                if task.get("status", "") == "active"
            ]

        # Add a blank option
        todo_tasks.insert(0, "")

        # Task selection dropdown
        self.todo_tasks_var = tk.StringVar(value=self.current_task)
        self.task_combobox = ttk.Combobox(
            task_frame,
            textvariable=self.todo_tasks_var,
            values=todo_tasks,
            font=self.theme.small_font,
            width=30,
            state="readonly",
        )
        self.task_combobox.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        self.task_combobox.bind("<<ComboboxSelected>>", self.update_current_task)

        # Daily pomodoro count
        daily_count_label = tk.Label(
            timer_frame,
            text=f"Pomodoros completed today: {self.completed_today}",
            font=self.theme.small_font,
            bg=self.theme.bg_color,
            fg=self.theme.text_color,
        )
        daily_count_label.pack(pady=5)

        # Control buttons
        controls_frame = tk.Frame(timer_frame, bg=self.theme.bg_color)
        controls_frame.pack(pady=10)

        # Start button
        self.start_button = self.theme.create_pixel_button(
            controls_frame,
            "▶ Start",
            self.start_timer,
            color="#4CAF50",  # Green
            width=8,
        )
        self.start_button.pack(side=tk.LEFT, padx=5)

        # Pause button
        self.pause_button = self.theme.create_pixel_button(
            controls_frame,
            "⏸ Pause",
            self.pause_timer,
            color="#FFC107",  # Amber
            width=8,
        )
        self.pause_button.pack(side=tk.LEFT, padx=5)
        self.pause_button.config(state=tk.DISABLED)

        # Reset button
        self.reset_button = self.theme.create_pixel_button(
            controls_frame,
            "⏹ Reset",
            self.reset_timer,
            color="#F44336",  # Red
            width=8,
        )
        self.reset_button.pack(side=tk.LEFT, padx=5)
        self.reset_button.config(state=tk.DISABLED)

        # Skip button (new)
        self.skip_button = self.theme.create_pixel_button(
            controls_frame,
            "⏭ Skip",
            self.skip_timer,
            color="#2196F3",  # Blue
            width=8,
        )
        self.skip_button.pack(side=tk.LEFT, padx=5)
        self.skip_button.config(state=tk.DISABLED)

        # Set initial timer value
        self.reset_timer_display()

    def update_current_task(self, event=None):
        """Update the current task being worked on."""
        self.current_task = self.todo_tasks_var.get()
        self.data["pomodoro"]["current_task"] = self.current_task
        self.data_manager.save_data()

    def skip_timer(self):
        """Skip the current timer and move to the next phase."""
        if not self.timer_running:
            return
            
        # Cancel current timer
        if self.current_timer:
            self.root.after_cancel(self.current_timer)
            self.current_timer = None
            
        # Force timer completion
        self.time_left = 0
        self.update_timer()

    def create_settings_tab(self, parent):
        """
        Create the settings tab for pomodoro timer.

        Args:
            parent: Parent widget for the settings tab
        """
        # Settings container
        settings_frame = tk.Frame(parent, bg=self.theme.bg_color)
        settings_frame.pack(pady=20, fill=tk.BOTH, expand=True)

        # Timer duration settings
        duration_frame = tk.LabelFrame(
            settings_frame,
            text="⏱️ Timer Duration (minutes)",
            font=self.theme.pixel_font,
            bg=self.theme.bg_color,
            fg=self.theme.text_color,
            padx=10,
            pady=10,
            **self.pixel_border_style,
        )
        duration_frame.pack(fill=tk.X, padx=10, pady=10)

        # Work time
        work_frame = tk.Frame(duration_frame, bg=self.theme.bg_color)
        work_frame.pack(fill=tk.X, pady=5)

        tk.Label(
            work_frame,
            text="Work time:",
            font=self.theme.small_font,
            bg=self.theme.bg_color,
            fg="#4CAF50",  # Green for work time
            width=15,
            anchor="w",
        ).pack(side=tk.LEFT)

        work_time_var = tk.IntVar(value=self.data["pomodoro"]["work_time"])
        work_time_spinbox = tk.Spinbox(
            work_frame,
            from_=1,
            to=60,
            textvariable=work_time_var,
            width=5,
            font=self.theme.small_font,
            bg=self.theme.bg_color,
            fg=self.theme.text_color,
            buttonbackground=self.theme.primary_color,
        )
        work_time_spinbox.pack(side=tk.LEFT)

        # Function to update work time
        def update_work_time(*args):
            self.data["pomodoro"]["work_time"] = work_time_var.get()
            self.data_manager.save_data()
            if not self.timer_running:
                self.reset_timer_display()

        work_time_var.trace("w", update_work_time)

        # Break time
        break_frame = tk.Frame(duration_frame, bg=self.theme.bg_color)
        break_frame.pack(fill=tk.X, pady=5)

        tk.Label(
            break_frame,
            text="Short break:",
            font=self.theme.small_font,
            bg=self.theme.bg_color,
            fg="#FF9800",  # Orange for short break
            width=15,
            anchor="w",
        ).pack(side=tk.LEFT)

        break_time_var = tk.IntVar(value=self.data["pomodoro"]["break_time"])
        break_time_spinbox = tk.Spinbox(
            break_frame,
            from_=1,
            to=30,
            textvariable=break_time_var,
            width=5,
            font=self.theme.small_font,
            bg=self.theme.bg_color,
            fg=self.theme.text_color,
            buttonbackground=self.theme.primary_color,
        )
        break_time_spinbox.pack(side=tk.LEFT)

        # Function to update break time
        def update_break_time(*args):
            self.data["pomodoro"]["break_time"] = break_time_var.get()
            self.data_manager.save_data()

        break_time_var.trace("w", update_break_time)

        # Long break time
        long_break_frame = tk.Frame(duration_frame, bg=self.theme.bg_color)
        long_break_frame.pack(fill=tk.X, pady=5)

        tk.Label(
            long_break_frame,
            text="Long break:",
            font=self.theme.small_font,
            bg=self.theme.bg_color,
            fg="#2196F3",  # Blue for long break
            width=15,
            anchor="w",
        ).pack(side=tk.LEFT)

        long_break_time_var = tk.IntVar(value=self.data["pomodoro"]["long_break_time"])
        long_break_time_spinbox = tk.Spinbox(
            long_break_frame,
            from_=5,
            to=60,
            textvariable=long_break_time_var,
            width=5,
            font=self.theme.small_font,
            bg=self.theme.bg_color,
            fg=self.theme.text_color,
            buttonbackground=self.theme.primary_color,
        )
        long_break_time_spinbox.pack(side=tk.LEFT)

        # Function to update long break time
        def update_long_break_time(*args):
            self.data["pomodoro"]["long_break_time"] = long_break_time_var.get()
            self.data_manager.save_data()

        long_break_time_var.trace("w", update_long_break_time)

        # Long break interval
        interval_frame = tk.Frame(duration_frame, bg=self.theme.bg_color)
        interval_frame.pack(fill=tk.X, pady=5)

        tk.Label(
            interval_frame,
            text="Pomodoros before long break:",
            font=self.theme.small_font,
            bg=self.theme.bg_color,
            fg=self.theme.text_color,
            width=25,
            anchor="w",
        ).pack(side=tk.LEFT)

        interval_var = tk.IntVar(value=self.data["pomodoro"]["long_break_interval"])
        interval_spinbox = tk.Spinbox(
            interval_frame,
            from_=2,
            to=10,
            textvariable=interval_var,
            width=5,
            font=self.theme.small_font,
            bg=self.theme.bg_color,
            fg=self.theme.text_color,
            buttonbackground=self.theme.primary_color,
        )
        interval_spinbox.pack(side=tk.LEFT)

        # Function to update interval
        def update_interval(*args):
            self.data["pomodoro"]["long_break_interval"] = interval_var.get()
            self.data_manager.save_data()

        interval_var.trace("w", update_interval)

        # Behavior settings
        behavior_frame = tk.LabelFrame(
            settings_frame,
            text="⚙️ Behavior",
            font=self.theme.pixel_font,
            bg=self.theme.bg_color,
            fg=self.theme.text_color,
            padx=10,
            pady=10,
            **self.pixel_border_style,
        )
        behavior_frame.pack(fill=tk.X, padx=10, pady=10)

        # Auto-start next session
        auto_start_var = tk.BooleanVar(value=self.data["pomodoro"]["auto_start"])
        auto_start_check = tk.Checkbutton(
            behavior_frame,
            text="Auto-start next session",
            variable=auto_start_var,
            font=self.theme.small_font,
            bg=self.theme.bg_color,
            fg=self.theme.text_color,
            selectcolor=self.theme.secondary_color,
            command=lambda: self.update_setting("auto_start", auto_start_var.get()),
        )
        auto_start_check.pack(anchor="w", pady=5)

        # Sound notifications
        sound_var = tk.BooleanVar(value=self.data["pomodoro"]["sound_enabled"])
        sound_check = tk.Checkbutton(
            behavior_frame,
            text="Enable sound notifications",
            variable=sound_var,
            font=self.theme.small_font,
            bg=self.theme.bg_color,
            fg=self.theme.text_color,
            selectcolor=self.theme.secondary_color,
            command=lambda: self.update_setting("sound_enabled", sound_var.get()),
        )
        sound_check.pack(anchor="w", pady=5)

        # Notification status
        notification_frame = tk.Frame(behavior_frame, bg=self.theme.bg_color)
        notification_frame.pack(fill=tk.X, pady=5)
        
        if not self.notification_available:
            notification_note = tk.Label(
                notification_frame,
                text="⚠️ Install 'plyer' for desktop notifications\n(pip install plyer)",
                font=self.theme.small_font,
                bg=self.theme.bg_color,
                fg="#FF5722",  # Orange warning color
            )
            notification_note.pack(pady=5)

        if not self.sound_available:
            sound_note = tk.Label(
                notification_frame,
                text="⚠️ Sound notifications only available on Windows",
                font=self.theme.small_font,
                bg=self.theme.bg_color,
                fg="#FF5722",  # Orange warning color
            )
            sound_note.pack(pady=5)

    def create_stats_tab(self, parent):
        """
        Create the statistics tab for the pomodoro timer.

        Args:
            parent: Parent widget for the statistics tab
        """
        # Statistics container
        stats_frame = tk.Frame(parent, bg=self.theme.bg_color)
        stats_frame.pack(pady=20, fill=tk.BOTH, expand=True)

        # Current statistics
        current_stats_frame = tk.LabelFrame(
            stats_frame,
            text="📊 Pomodoro Statistics",
            font=self.theme.pixel_font,
            bg=self.theme.bg_color,
            fg=self.theme.text_color,
            padx=10,
            pady=10,
            **self.pixel_border_style,
        )
        current_stats_frame.pack(fill=tk.X, padx=10, pady=10)

        # Create a visually appealing stats display
        stats_display = tk.Frame(current_stats_frame, bg=self.theme.bg_color)
        stats_display.pack(fill=tk.X, pady=10)
        
        # Total completed pomodoros with icon
        total_completed = self.data["pomodoro"]["completed_pomodoros"]
        
        total_frame = tk.Frame(stats_display, bg=self.theme.bg_color)
        total_frame.pack(fill=tk.X, pady=5)
        
        tk.Label(
            total_frame,
            text="🍅",
            font=("Segoe UI Emoji", 16),
            bg=self.theme.bg_color,
            fg=self.theme.text_color,
        ).pack(side=tk.LEFT, padx=5)
        
        tk.Label(
            total_frame,
            text="Total completed pomodoros:",
            font=self.theme.small_font,
            bg=self.theme.bg_color,
            fg=self.theme.text_color,
        ).pack(side=tk.LEFT, padx=5)
        
        tk.Label(
            total_frame,
            text=str(total_completed),
            font=self.theme.pixel_font,
            bg=self.theme.bg_color,
            fg="#4CAF50",  # Green
        ).pack(side=tk.LEFT, padx=5)

        # Display pomodoros completed today with icon
        today_frame = tk.Frame(stats_display, bg=self.theme.bg_color)
        today_frame.pack(fill=tk.X, pady=5)
        
        tk.Label(
            today_frame,
            text="📅",
            font=("Segoe UI Emoji", 16),
            bg=self.theme.bg_color,
            fg=self.theme.text_color,
        ).pack(side=tk.LEFT, padx=5)
        
        tk.Label(
            today_frame,
            text="Pomodoros completed today:",
            font=self.theme.small_font,
            bg=self.theme.bg_color,
            fg=self.theme.text_color,
        ).pack(side=tk.LEFT, padx=5)
        
        tk.Label(
            today_frame,
            text=str(self.completed_today),
            font=self.theme.pixel_font,
            bg=self.theme.bg_color,
            fg="#FF9800",  # Orange
        ).pack(side=tk.LEFT, padx=5)

        # Calculate total focused time with icon
        total_focus_minutes = total_completed * self.data["pomodoro"]["work_time"]
        hours = total_focus_minutes // 60
        minutes = total_focus_minutes % 60

        focus_frame = tk.Frame(stats_display, bg=self.theme.bg_color)
        focus_frame.pack(fill=tk.X, pady=5)
        
        tk.Label(
            focus_frame,
            text="⏱️",
            font=("Segoe UI Emoji", 16),
            bg=self.theme.bg_color,
            fg=self.theme.text_color,
        ).pack(side=tk.LEFT, padx=5)
        
        tk.Label(
            focus_frame,
            text="Total focus time:",
            font=self.theme.small_font,
            bg=self.theme.bg_color,
            fg=self.theme.text_color,
        ).pack(side=tk.LEFT, padx=5)
        
        tk.Label(
            focus_frame,
            text=f"{hours} hours and {minutes} minutes",
            font=self.theme.pixel_font,
            bg=self.theme.bg_color,
            fg="#2196F3",  # Blue
        ).pack(side=tk.LEFT, padx=5)

        # Recent activity section
        recent_frame = tk.LabelFrame(
            stats_frame,
            text="📅 Recent Activity",
            font=self.theme.pixel_font,
            bg=self.theme.bg_color,
            fg=self.theme.text_color,
            padx=10,
            pady=10,
            **self.pixel_border_style,
        )
        recent_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Create a frame for the daily stats
        daily_stats_frame = tk.Frame(recent_frame, bg=self.theme.bg_color)
        daily_stats_frame.pack(fill=tk.BOTH, expand=True, pady=5)

        # Get the last 7 days of activity
        daily_pomodoros = self.data["pomodoro"].get("daily_pomodoros", {})

        # Create a canvas for the bar chart
        if daily_pomodoros:
            # Sort dates in reverse order (most recent first)
            sorted_dates = sorted(daily_pomodoros.keys(), reverse=True)
            
            # Set display dates (last 7 days)
            display_dates = sorted_dates[:7]
            
            # Find the maximum value for scaling
            max_value = max([daily_pomodoros[date] for date in display_dates]) if display_dates else 0
            max_value = max(max_value, 1)  # Avoid division by zero
            
            # Create a canvas for the chart
            chart_height = 150
            chart_canvas = tk.Canvas(
                daily_stats_frame, 
                height=chart_height + 50,  # Extra space for labels
                bg=self.theme.bg_color,
                bd=0,
                highlightthickness=0
            )
            chart_canvas.pack(fill=tk.X, expand=True, pady=10)
            
            # Draw horizontal grid lines
            for i in range(5):
                y = chart_height - (i * (chart_height / 4))
                chart_canvas.create_line(
                    50, y, 550, y, 
                    fill=self.theme.darken_color(self.theme.bg_color),
                    dash=(2, 4)
                )
                value = int((i / 4) * max_value)
                chart_canvas.create_text(
                    30, y, text=str(value), 
                    fill=self.theme.text_color,
                    font=self.theme.small_font
                )
            
            # Draw bars for each date
            bar_width = 60
            spacing = 20
            x_start = 60
            
            for i, date in enumerate(display_dates):
                count = daily_pomodoros[date]
                bar_height = (count / max_value) * chart_height
                
                # Format date for display (MM-DD)
                try:
                    date_obj = datetime.strptime(date, "%Y-%m-%d")
                    display_date = date_obj.strftime("%m-%d")
                except ValueError:
                    display_date = date
                
                x = x_start + (i * (bar_width + spacing))
                
                # Draw the bar
                chart_canvas.create_rectangle(
                    x, chart_height,
                    x + bar_width, chart_height - bar_height,
                    fill="#4CAF50",
                    outline=self.theme.text_color,
                    width=2
                )
                
                # Draw the date label
                chart_canvas.create_text(
                    x + bar_width/2, chart_height + 20,
                    text=display_date,
                    fill=self.theme.text_color,
                    font=self.theme.small_font
                )
                
                # Draw the value on top of the bar
                chart_canvas.create_text(
                    x + bar_width/2, chart_height - bar_height - 10,
                    text=str(count),
                    fill=self.theme.text_color,
                    font=self.theme.small_font
                )
        else:
            # No data message
            tk.Label(
                daily_stats_frame,
                text="No pomodoro history yet. Complete your first pomodoro!",
                font=self.theme.small_font,
                bg=self.theme.bg_color,
                fg=self.theme.text_color,
            ).pack(pady=20)

    def create_integration_tab(self, parent):
        """
        Create the module integration tab.

        Args:
            parent: Parent widget for the integration tab
        """
        # Module integration container
        integration_frame = tk.Frame(parent, bg=self.theme.bg_color)
        integration_frame.pack(pady=20, fill=tk.BOTH, expand=True)

        # Explanation label
        tk.Label(
            integration_frame,
            text="🔄 Link the Pomodoro Timer with your skill modules",
            font=self.theme.pixel_font,
            bg=self.theme.bg_color,
            fg=self.theme.text_color,
        ).pack(pady=5)

        explanation_frame = tk.Frame(integration_frame, bg=self.theme.bg_color, relief=tk.RIDGE, bd=2)
        explanation_frame.pack(fill=tk.X, padx=20, pady=10)
        
        tk.Label(
            explanation_frame,
            text="When you complete a pomodoro, selected modules will automatically\n"
            "record progress toward their daily goals.",
            font=self.theme.small_font,
            bg=self.theme.bg_color,
            fg=self.theme.text_color,
            justify=tk.LEFT,
            padx=10,
            pady=10,
        ).pack()

        # Module selection frame
        self.module_integration_frame = tk.LabelFrame(
            integration_frame,
            text="🔗 Link with Modules",
            font=self.theme.pixel_font,
            bg=self.theme.bg_color,
            fg=self.theme.text_color,
            padx=10,
            pady=10,
            **self.pixel_border_style,
        )
        self.module_integration_frame.pack(fill=tk.X, padx=10, pady=10)

        # Add checkboxes for each module
        modules = [("art", "🎨 Art Quest"), 
                  ("korean", "🇰🇷 Korean Quest"), 
                  ("french", "🇫🇷 French Quest"), 
                  ("diss", "📚 Diss Quest")]

        # Get currently linked modules
        linked_modules = self.data["pomodoro"].get("linked_modules", {})

        # Use grid layout for better organization
        for i, (module_key, module_name) in enumerate(modules):
            # Create variable and set from saved state
            var = tk.BooleanVar(value=linked_modules.get(module_key, False))

            # Module frame with colored border based on theme
            module_frame = tk.Frame(
                self.module_integration_frame,
                bg=self.theme.bg_color,
                relief=tk.RIDGE,
                bd=2,
                padx=5,
                pady=5,
            )
            module_frame.grid(row=i//2, column=i%2, sticky="ew", padx=10, pady=5)

            # Create checkbox
            checkbox = tk.Checkbutton(
                module_frame,
                text=module_name,
                variable=var,
                bg=self.theme.bg_color,
                fg=self.theme.text_color,
                font=self.theme.small_font,
                selectcolor=self.theme.secondary_color,
                command=lambda key=module_key, v=var: self.toggle_module_link(
                    key, v.get()
                ),
            )
            checkbox.pack(fill=tk.X, padx=5, pady=5)

            # Save reference to variable
            self.module_checkboxes[module_key] = var

        # Configure grid to expand properly
        self.module_integration_frame.columnconfigure(0, weight=1)
        self.module_integration_frame.columnconfigure(1, weight=1)

        # Points per pomodoro frame
        points_frame = tk.LabelFrame(
            integration_frame,
            text="⚡ Progress Settings",
            font=self.theme.pixel_font,
            bg=self.theme.bg_color,
            fg=self.theme.text_color,
            padx=10,
            pady=10,
            **self.pixel_border_style,
        )
        points_frame.pack(fill=tk.X, padx=10, pady=10)

        # Points per pomodoro
        points_setting_frame = tk.Frame(points_frame, bg=self.theme.bg_color)
        points_setting_frame.pack(fill=tk.X, pady=5)

        tk.Label(
            points_setting_frame,
            text="Points per completed pomodoro:",
            font=self.theme.small_font,
            bg=self.theme.bg_color,
            fg=self.theme.text_color,
            width=25,
            anchor="w",
        ).pack(side=tk.LEFT)

        # Get or set default points value
        points_value = self.data["pomodoro"].get("points_per_pomodoro", 10)
        self.data["pomodoro"]["points_per_pomodoro"] = points_value

        points_var = tk.IntVar(value=points_value)
        points_spinbox = tk.Spinbox(
            points_setting_frame,
            from_=1,
            to=50,
            textvariable=points_var,
            width=5,
            font=self.theme.small_font,
            bg=self.theme.bg_color,
            fg=self.theme.text_color,
            buttonbackground=self.theme.primary_color,
        )
        points_spinbox.pack(side=tk.LEFT)

        # Function to update points
        def update_points(*args):
            self.data["pomodoro"]["points_per_pomodoro"] = points_var.get()
            self.data_manager.save_data()

        points_var.trace("w", update_points)

    def toggle_module_link(self, module_key, status):
        """
        Toggle the link with a skill module.

        Args:
            module_key: The module identifier
            status: True if linked, False if unlinked
        """
        # Initialize linked_modules if it doesn't exist
        if "linked_modules" not in self.data["pomodoro"]:
            self.data["pomodoro"]["linked_modules"] = {}

        # Update the link status
        self.data["pomodoro"]["linked_modules"][module_key] = status

        # Save the changes
        self.data_manager.save_data()

    def update_setting(self, setting_key, value):
        """
        Update a pomodoro setting.

        Args:
            setting_key: The setting key to update
            value: The new value for the setting
        """
        self.data["pomodoro"][setting_key] = value
        self.data_manager.save_data()

    def start_timer(self):
        """Start or resume the pomodoro timer."""
        if self.timer_paused:
            # Resume paused timer
            self.timer_paused = False
            self.status_label.config(
                text=random.choice(self.work_messages) if not self.is_break 
                    else random.choice(self.break_messages)
            )
            self.pause_button.config(text="⏸ Pause")
        else:
            # Start new timer
            if self.timer_running:
                return

            self.timer_running = True

            # Set timer type and duration
            if not self.is_break:
                # Start a work session
                self.time_left = self.data["pomodoro"]["work_time"] * 60
                self.status_label.config(text=random.choice(self.work_messages))
                
                # Update progress bar color
                style = ttk.Style()
                style.configure(
                    "Pixel.Horizontal.TProgressbar",
                    background="#4CAF50"  # Green for work
                )
            else:
                # Start a break
                if self.is_long_break:
                    self.time_left = self.data["pomodoro"]["long_break_time"] * 60
                    self.status_label.config(text=random.choice(self.break_messages))
                    
                    # Update progress bar color
                    style = ttk.Style()
                    style.configure(
                        "Pixel.Horizontal.TProgressbar",
                        background="#2196F3"  # Blue for long break
                    )
                else:
                    self.time_left = self.data["pomodoro"]["break_time"] * 60
                    self.status_label.config(text=random.choice(self.break_messages))
                    
                    # Update progress bar color
                    style = ttk.Style()
                    style.configure(
                        "Pixel.Horizontal.TProgressbar",
                        background="#FF9800"  # Orange for short break
                    )

            # Configure the progress bar
            self.progress_bar["maximum"] = self.time_left
            self.progress_bar["value"] = 0

        # Enable/disable buttons
        self.start_button.config(state=tk.DISABLED)
        self.pause_button.config(state=tk.NORMAL)
        self.reset_button.config(state=tk.NORMAL)
        self.skip_button.config(state=tk.NORMAL)

        # Start timer using Tkinter's after method instead of threading
        self.update_timer()

    def update_timer(self):
        """Update timer using Tkinter's after method (no threading)"""
        if not self.timer_running or self.timer_paused:
            return

        if self.time_left > 0:
            # Calculate minutes and seconds
            minutes, seconds = divmod(self.time_left, 60)

            # Update the timer display
            time_str = f"{minutes:02d}:{seconds:02d}"
            self.timer_label.config(text=time_str)

            # Update progress bar
            elapsed = self.progress_bar["maximum"] - self.time_left
            self.progress_bar["value"] = elapsed

            # Update timer color based on state
            if not self.is_break:
                self.timer_label.config(fg="#4CAF50")  # Green for work
            else:
                if self.is_long_break:
                    self.timer_label.config(fg="#2196F3")  # Blue for long break
                else:
                    self.timer_label.config(fg="#FF9800")  # Orange for short break

            # Decrement time
            self.time_left -= 1

            # Schedule the next update after 1000ms (1 second)
            self.current_timer = self.root.after(1000, self.update_timer)
        else:
            # Timer completed
            self.timer_running = False
            self.timer_label.config(text="00:00")
            self.progress_bar["value"] = self.progress_bar["maximum"]

            # Play sound notification
            self.play_sound()

            # Handle timer completion based on mode
            if not self.is_break:
                # Work session completed
                self.complete_pomodoro()

                # Increment pomodoro count
                self.pomodoro_count += 1

                # Determine next break type
                self.is_break = True
                if (
                    self.pomodoro_count % self.data["pomodoro"]["long_break_interval"]
                    == 0
                ):
                    self.is_long_break = True
                    self.status_label.config(text="Time for a long break!")
                else:
                    self.is_long_break = False
                    self.status_label.config(text="Time for a short break!")
            else:
                # Break completed
                self.is_break = False
                self.status_label.config(
                    text="Break finished. Ready for next pomodoro!"
                )

            # Auto-start next session if enabled
            if self.data["pomodoro"]["auto_start"]:
                self.reset_timer_display()
                self.start_timer()
            else:
                # Reset for manual start
                self.reset_timer_display()
                self.start_button.config(state=tk.NORMAL)
                self.pause_button.config(state=tk.DISABLED)
                self.reset_button.config(state=tk.DISABLED)
                self.skip_button.config(state=tk.DISABLED)

            # Show notification
            self.show_notification()

    def pause_timer(self):
        """Pause the running timer."""
        if not self.timer_running:
            return

        if not self.timer_paused:
            # Pause the timer
            self.timer_paused = True
            self.status_label.config(text="⏸ Paused")
            self.pause_button.config(text="▶ Resume")
            self.start_button.config(state=tk.NORMAL)
        else:
            # Resume the timer
            self.timer_paused = False
            self.status_label.config(
                text=random.choice(self.work_messages) if not self.is_break 
                    else random.choice(self.break_messages)
            )
            self.pause_button.config(text="⏸ Pause")
            self.start_button.config(state=tk.DISABLED)

    def reset_timer(self):
        """Reset the timer to initial states."""
        # Cancel any pending timer updates
        if self.current_timer:
            self.root.after_cancel(self.current_timer)
            self.current_timer = None

        # Stop the current timer
        self.timer_running = False
        self.timer_paused = False

        # Reset the display
        self.reset_timer_display()

        # Reset buttons
        self.start_button.config(state=tk.NORMAL)
        self.pause_button.config(state=tk.DISABLED)
        self.reset_button.config(state=tk.DISABLED)
        self.skip_button.config(state=tk.DISABLED)

    def reset_timer_display(self):
        """Reset the timer display to initial state."""
        # Set time based on current mode (work or break)
        if not self.is_break:
            minutes = self.data["pomodoro"]["work_time"]
            self.status_label.config(text="Ready to start")
            
            # Update color for work mode
            self.timer_label.config(fg="#4CAF50")  # Green
            
            style = ttk.Style()
            style.configure(
                "Pixel.Horizontal.TProgressbar",
                background="#4CAF50"  # Green
            )
        else:
            if self.is_long_break:
                minutes = self.data["pomodoro"]["long_break_time"]
                self.status_label.config(text="Ready for long break")
                
                # Update color for long break
                self.timer_label.config(fg="#2196F3")  # Blue
                
                style = ttk.Style()
                style.configure(
                    "Pixel.Horizontal.TProgressbar",
                    background="#2196F3"  # Blue
                )
            else:
                minutes = self.data["pomodoro"]["break_time"]
                self.status_label.config(text="Ready for break")
                
                # Update color for short break
                self.timer_label.config(fg="#FF9800")  # Orange
                
                style = ttk.Style()
                style.configure(
                    "Pixel.Horizontal.TProgressbar",
                    background="#FF9800"  # Orange
                )

        # Format time display
        self.time_left = minutes * 60
        self.timer_label.config(text=f"{minutes:02d}:00")

        # Reset progress bar
        if hasattr(self, "progress_bar") and self.progress_bar:
            self.progress_bar["value"] = 0

    def play_sound(self):
        """Play a sound notification when timer completes."""
        if not self.sound_available or not self.data["pomodoro"]["sound_enabled"]:
            return
            
        try:
            if not self.is_break:
                # Work completed sound (higher frequency)
                winsound.Beep(1000, 500)  # 1000Hz for 500ms
                winsound.Beep(1200, 500)  # 1200Hz for 500ms
                winsound.Beep(1500, 800)  # 1500Hz for 800ms
            else:
                # Break completed sound (lower frequency)
                winsound.Beep(800, 500)   # 800Hz for 500ms
                winsound.Beep(1000, 800)  # 1000Hz for 800ms
        except Exception as e:
            print(f"Sound error: {e}")

    def complete_pomodoro(self):
        """Record the completion of a pomodoro."""
        try:
            # Increment total pomodoro count
            self.data["pomodoro"]["completed_pomodoros"] += 1

            # Update daily pomodoro count
            today = datetime.now().strftime("%Y-%m-%d")
            daily_pomodoros = self.data["pomodoro"].get("daily_pomodoros", {})
            daily_pomodoros[today] = daily_pomodoros.get(today, 0) + 1
            self.data["pomodoro"]["daily_pomodoros"] = daily_pomodoros

            # Update completed today count for the UI
            self.completed_today = daily_pomodoros[today]

            # Update linked modules if any
            self.update_linked_modules()
            
            # If working on a task, add progress to the task
            if self.current_task:
                self.add_progress_to_task()

            # Save data
            self.data_manager.save_data()
        except Exception as e:
            print(f"Error completing pomodoro: {e}")
            messagebox.showerror("Error", f"Could not complete pomodoro: {e}")

    def add_progress_to_task(self):
        """Add progress to the current task being worked on."""
        if not self.current_task or "todo" not in self.data:
            return
            
        # Find the task
        for task in self.data["todo"].get("tasks", []):
            if task.get("title") == self.current_task and task.get("status") == "active":
                # Add a pomodoro to the task's progress
                if "pomodoros" not in task:
                    task["pomodoros"] = 0
                task["pomodoros"] += 1
                
                # Add note about the pomodoro
                if "notes" not in task:
                    task["notes"] = ""
                    
                now = datetime.now().strftime("%Y-%m-%d %H:%M")
                task["notes"] += f"\n[{now}] Completed 1 pomodoro ({self.data['pomodoro']['work_time']} min)"
                
                break

    def update_linked_modules(self):
        """Update progress for linked skill modules."""
        try:
            linked_modules = self.data["pomodoro"].get("linked_modules", {})
            points_per_pomodoro = self.data["pomodoro"].get("points_per_pomodoro", 10)

            for module_key, is_linked in linked_modules.items():
                if is_linked and module_key in self.data:
                    # Add points to the module
                    self.data[module_key]["points"] += points_per_pomodoro

                    # Update last activity date
                    today = datetime.now().strftime("%Y-%m-%d")
                    self.data[module_key]["last_activity"] = today

                    # Update streak if not already updated today
                    last_streak_update = self.data[module_key].get(
                        "last_streak_update", ""
                    )
                    if last_streak_update != today:
                        self.data[module_key]["streak"] += 1
                        self.data[module_key]["last_streak_update"] = today

                    # Check for level up
                    self.check_level_up(module_key)
        except Exception as e:
            print(f"Error updating linked modules: {e}")

    def check_level_up(self, module_key):
        """
        Check if a module should level up based on points.

        Args:
            module_key: The module to check for level up
        """
        try:
            current_level = self.data[module_key]["level"]
            current_points = self.data[module_key]["points"]

            # Simple level up formula: next level requires current_level * 100 points
            points_for_next_level = current_level * 100

            if current_points >= points_for_next_level:
                # Level up!
                self.data[module_key]["level"] += 1

                # Reset points (optional - can be changed to keep excess points)
                self.data[module_key]["points"] = current_points - points_for_next_level
        except Exception as e:
            print(f"Error checking level up for {module_key}: {e}")

    def show_notification(self):
        """Show a desktop notification."""
        # Only show if notifications are available and enabled
        if (
            not self.notification_available
            or not self.data["pomodoro"]["sound_enabled"]
        ):
            return

        try:
            # Notification for work completion
            if not self.is_break:
                notification.notify(
                    title="🍅 Pomodoro Complete!",
                    message=f"Good work! Take a break. You've completed {self.completed_today} pomodoros today.",
                    timeout=10,
                )
            else:
                # Notification for break completion
                notification.notify(
                    title="⏰ Break Complete!",
                    message="Break time is over. Ready for another focused pomodoro?",
                    timeout=10,
                )
        except Exception as e:
            print(f"Notification error: {e}")

    def get_completed_today(self):
        """Get the number of pomodoros completed today."""
        today = datetime.now().strftime("%Y-%m-%d")
        daily_pomodoros = self.data["pomodoro"].get("daily_pomodoros", {})
        return daily_pomodoros.get(today, 0)

    def create_pomodoro_tab(self, parent):
        """
        Create a preview of the Pomodoro timer for the main menu tab.

        Args:
            parent: Parent widget for the pomodoro tab
        """
        # Title
        tk.Label(
            parent,
            text="⏱️ Pomodoro Timer",
            font=self.theme.pixel_font,
            bg=self.theme.bg_color,
            fg=self.theme.text_color,
        ).pack(pady=10)

        # Status frame with pixelated border
        status_frame = tk.Frame(
            parent, 
            bg=self.theme.bg_color, 
            relief=tk.RIDGE, 
            bd=3
        )
        status_frame.pack(pady=10, fill=tk.X, padx=20)

        # Today's stats
        completed_today = self.get_completed_today()

        # Display pomodoros with icons
        stats_frame = tk.Frame(status_frame, bg=self.theme.bg_color)
        stats_frame.pack(pady=10)
        
        # Today's pomodoros
        today_frame = tk.Frame(stats_frame, bg=self.theme.bg_color)
        today_frame.pack(fill=tk.X, pady=5)
        
        tk.Label(
            today_frame,
            text="🍅",
            font=("Segoe UI Emoji", 14),
            bg=self.theme.bg_color,
            fg="#FF5722",
        ).pack(side=tk.LEFT, padx=5)
        
        tk.Label(
            today_frame,
            text=f"Today: {completed_today}",
            font=self.theme.small_font,
            bg=self.theme.bg_color,
            fg=self.theme.text_color,
        ).pack(side=tk.LEFT)

        # Total pomodoros
        total_frame = tk.Frame(stats_frame, bg=self.theme.bg_color)
        total_frame.pack(fill=tk.X, pady=5)
        
        tk.Label(
            total_frame,
            text="📊",
            font=("Segoe UI Emoji", 14),
            bg=self.theme.bg_color,
            fg="#2196F3",
        ).pack(side=tk.LEFT, padx=5)
        
        total_completed = self.data["pomodoro"]["completed_pomodoros"]
        tk.Label(
            total_frame,
            text=f"Total: {total_completed}",
            font=self.theme.small_font,
            bg=self.theme.bg_color,
            fg=self.theme.text_color,
        ).pack(side=tk.LEFT)

        # Current task display
        if self.current_task:
            task_frame = tk.Frame(status_frame, bg=self.theme.bg_color)
            task_frame.pack(fill=tk.X, pady=5, padx=10)
            
            tk.Label(
                task_frame,
                text="📝",
                font=("Segoe UI Emoji", 14),
                bg=self.theme.bg_color,
                fg="#FF9800",
            ).pack(side=tk.LEFT, padx=5)
            
            tk.Label(
                task_frame,
                text=f"Current task: {self.current_task}",
                font=self.theme.small_font,
                bg=self.theme.bg_color,
                fg=self.theme.text_color,
                wraplength=300,
            ).pack(side=tk.LEFT, fill=tk.X, expand=True)

        # Quick timer button
        start_button = self.theme.create_pixel_button(
            parent,
            "Start Pomodoro Timer",
            lambda: self.app.show_module("pomodoro"),
            color="#4CAF50",  # Green
        )
        start_button.pack(pady=10)
