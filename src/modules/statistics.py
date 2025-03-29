"""
Statistics module for the Pixel Quest application.
Handles displaying statistics and progress tracking.
"""

import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, timedelta
from src.utils import create_pixel_progress_bar
from src.modules.diss_module import DissModule


class StatisticsModule:
    """
    Manages the statistics display functionality.
    """

    def __init__(self, app, data_manager, theme):
        """
        Initialize the statistics module.

        Args:
            app: Main application instance
            data_manager: Data manager instance
            theme: Theme manager instance
        """
        self.app = app
        self.data_manager = data_manager
        self.data = data_manager.data
        self.theme = theme

    def create_statistics_tab(self, parent):
        """
        Create the statistics tab content with pixel art styling.

        Args:
            parent: Parent widget to place the statistics tab
        """
        # Title
        tk.Label(
            parent,
            text="Your Progress Statistics",
            font=self.theme.pixel_font,
            bg=self.theme.bg_color,
            fg=self.theme.text_color,
        ).pack(pady=10)

        # Create a notebook with tabs for each module
        stats_notebook = ttk.Notebook(parent)
        stats_notebook.pack(expand=1, fill="both", padx=10, pady=10)

        # Create tabs for each module
        overview_tab = tk.Frame(stats_notebook, bg=self.theme.bg_color)
        art_stats_tab = tk.Frame(stats_notebook, bg=self.theme.bg_color)
        korean_stats_tab = tk.Frame(stats_notebook, bg=self.theme.bg_color)
        french_stats_tab = tk.Frame(stats_notebook, bg=self.theme.bg_color)
        diss_stats_tab = tk.Frame(stats_notebook, bg=self.theme.bg_color)
        habits_stats_tab = tk.Frame(stats_notebook, bg=self.theme.bg_color)

        stats_notebook.add(overview_tab, text="Overview")
        stats_notebook.add(art_stats_tab, text="Art Stats")
        stats_notebook.add(korean_stats_tab, text="Korean Stats")
        stats_notebook.add(french_stats_tab, text="French Stats")
        stats_notebook.add(diss_stats_tab, text="Diss Stats")
        stats_notebook.add(habits_stats_tab, text="Habits")

        # === OVERVIEW TAB ===
        self.create_overview_stats(overview_tab)

        # === ART STATS TAB ===
        self.create_module_stats(art_stats_tab, "art")

        # === KOREAN STATS TAB ===
        self.create_module_stats(korean_stats_tab, "korean")

        # === FRENCH STATS TAB ===
        self.create_module_stats(french_stats_tab, "french")

        # === DISS STATS TAB ===
        self.create_module_stats(diss_stats_tab, "diss")
        
        # === HABITS STATS TAB ===
        self.create_habits_stats(habits_stats_tab)

        # Export button
        export_button = self.theme.create_pixel_button(
            parent, "Export Data", self.export_data, color="#607D8B"
        )
        export_button.pack(pady=10)

    def create_overview_stats(self, parent):
        """
        Create overview statistics display with pixel art styling.

        Args:
            parent: Parent widget for the overview statistics
        """
        # Calculate total stats
        total_points = (
            self.data["art"]["points"]
            + self.data["korean"]["points"]
            + self.data["french"]["points"]
            + self.data["diss"]["points"]
        )

        # Days active calculation
        active_days = set()
        for module in ["art", "korean", "french", "diss"]:
            if self.data[module]["last_practice"]:
                active_days.add(self.data[module]["last_practice"])
                
        # Add days from habits
        if "habits" in self.data:
            habits = self.data["habits"]
            for habit_type in ["daily_habits", "custom_habits"]:
                for habit in habits.get(habit_type, []):
                    for date in habit.get("completed_dates", []):
                        active_days.add(date)

        # Summary frame
        summary_frame = tk.LabelFrame(
            parent,
            text="Summary",
            font=self.theme.pixel_font,
            bg=self.theme.bg_color,
            fg=self.theme.text_color,
            padx=10,
            pady=10,
            relief=tk.RIDGE,
            bd=3,
        )
        summary_frame.pack(fill=tk.X, padx=10, pady=10)

        # Total points
        tk.Label(
            summary_frame,
            text=f"Total Points: {total_points}",
            font=self.theme.pixel_font,
            bg=self.theme.bg_color,
            fg=self.theme.text_color,
        ).pack(anchor="w", pady=5)

        # Days active
        tk.Label(
            summary_frame,
            text=f"Days Active: {len(active_days)}",
            font=self.theme.pixel_font,
            bg=self.theme.bg_color,
            fg=self.theme.text_color,
        ).pack(anchor="w", pady=5)

        # Current levels
        tk.Label(
            summary_frame,
            text=f"Current Levels: Art {self.data['art']['level']} | "
            f"Korean {self.data['korean']['level']} | "
            f"French {self.data['french']['level']} | "
            f"Diss {self.data['diss']['level']}",
            font=self.theme.pixel_font,
            bg=self.theme.bg_color,
            fg=self.theme.text_color,
        ).pack(anchor="w", pady=5)
        
        # Habits overview
        if "habits" in self.data:
            habits = self.data["habits"]
            
            # Count active habits
            active_habits = sum(
                1 for h in habits.get("daily_habits", []) + habits.get("custom_habits", [])
                if h.get("active", True)
            )
            
            # Find max streak
            max_streak = 0
            for habit_type in ["daily_habits", "custom_habits"]:
                for habit in habits.get(habit_type, []):
                    max_streak = max(max_streak, habit.get("streak", 0))
            
            tk.Label(
                summary_frame,
                text=f"Active Habits: {active_habits} | Longest Streak: {max_streak} days",
                font=self.theme.pixel_font,
                bg=self.theme.bg_color,
                fg=self.theme.habit_color,  # Use the theme's habit color
            ).pack(anchor="w", pady=5)

        # Distribution frame
        dist_frame = tk.LabelFrame(
            parent,
            text="Point Distribution",
            font=self.theme.pixel_font,
            bg=self.theme.bg_color,
            fg=self.theme.text_color,
            padx=10,
            pady=10,
            relief=tk.RIDGE,
            bd=3,
        )
        dist_frame.pack(fill=tk.X, padx=10, pady=10)

        # Calculate percentages
        art_percent = (
            (self.data["art"]["points"] / total_points * 100) if total_points > 0 else 0
        )
        korean_percent = (
            (self.data["korean"]["points"] / total_points * 100)
            if total_points > 0
            else 0
        )
        french_percent = (
            (self.data["french"]["points"] / total_points * 100)
            if total_points > 0
            else 0
        )

        diss_percent = (
            (self.data["diss"]["points"] / total_points * 100)
            if total_points > 0
            else 0
        )

        # Distribution labels with pixel art progress bars
        tk.Label(
            dist_frame,
            text=f"Art: {self.data['art']['points']} points ({art_percent:.1f}%)",
            font=self.theme.small_font,
            bg=self.theme.bg_color,
            fg=self.theme.art_color,
        ).pack(anchor="w", pady=5)

        # Create pixel art style progress bar for Art
        create_pixel_progress_bar(
            dist_frame,
            art_percent,
            self.theme.art_color,
            self.theme.bg_color,
            self.theme.text_color,
            self.theme.darken_color,
        )

        tk.Label(
            dist_frame,
            text=f"Korean: {self.data['korean']['points']} points ({korean_percent:.1f}%)",
            font=self.theme.small_font,
            bg=self.theme.bg_color,
            fg=self.theme.korean_color,
        ).pack(anchor="w", pady=5)

        # Create pixel art style progress bar for Korean
        create_pixel_progress_bar(
            dist_frame,
            korean_percent,
            self.theme.korean_color,
            self.theme.bg_color,
            self.theme.text_color,
            self.theme.darken_color,
        )

        tk.Label(
            dist_frame,
            text=f"French: {self.data['french']['points']} points ({french_percent:.1f}%)",
            font=self.theme.small_font,
            bg=self.theme.bg_color,
            fg=self.theme.french_color,
        ).pack(anchor="w", pady=5)

        # Create pixel art style progress bar for French
        create_pixel_progress_bar(
            dist_frame,
            french_percent,
            self.theme.french_color,
            self.theme.bg_color,
            self.theme.text_color,
            self.theme.darken_color,
        )

        tk.Label(
            dist_frame,
            text=f"Diss: {self.data['diss']['points']} points ({diss_percent:.1f}%)",
            font=self.theme.small_font,
            bg=self.theme.bg_color,
            fg=self.theme.diss_color,
        ).pack(anchor="w", pady=5)

        # Create pixel art style progress bar for Dissertation
        create_pixel_progress_bar(
            dist_frame,
            diss_percent,
            self.theme.diss_color,
            self.theme.bg_color,
            self.theme.text_color,
            self.theme.darken_color,
        )

        # Recent activity frame
        activity_frame = tk.LabelFrame(
            parent,
            text="Recent Activity",
            font=self.theme.pixel_font,
            bg=self.theme.bg_color,
            fg=self.theme.text_color,
            padx=10,
            pady=10,
            relief=tk.RIDGE,
            bd=3,
        )
        activity_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Collect all activity logs
        all_activities = []

        # Art activities
        if "completed_exercises" in self.data["art"]:
            for activity in self.data["art"]["completed_exercises"]:
                all_activities.append(
                    {
                        "module": "art",
                        "type": "fundamentals",
                        "description": f"Completed '{activity['exercise']}'",
                        "timestamp": activity["timestamp"],
                        "points": activity["points"],
                    }
                )

        if "drawing_log" in self.data["art"]:
            for activity in self.data["art"]["drawing_log"]:
                all_activities.append(
                    {
                        "module": "art",
                        "type": "sketchbook",
                        "description": f"Drew {activity['type']}",
                        "timestamp": activity["timestamp"],
                        "points": activity["points"],
                    }
                )

        if "accountability_log" in self.data["art"]:
            for activity in self.data["art"]["accountability_log"]:
                all_activities.append(
                    {
                        "module": "art",
                        "type": "accountability",
                        "description": f"Posted '{activity['title']}' on {activity['platform']}",
                        "timestamp": activity["timestamp"],
                        "points": activity["points"],
                    }
                )

        # Korean activities
        if "completed_lessons" in self.data["korean"]:
            for activity in self.data["korean"]["completed_lessons"]:
                all_activities.append(
                    {
                        "module": "korean",
                        "type": "fundamentals",
                        "description": f"Completed '{activity['lesson']}'",
                        "timestamp": activity["timestamp"],
                        "points": activity["points"],
                    }
                )

        if "immersion_log" in self.data["korean"]:
            for activity in self.data["korean"]["immersion_log"]:
                all_activities.append(
                    {
                        "module": "korean",
                        "type": "immersion",
                        "description": f"Immersed in {activity['type']} for {activity['duration']}",
                        "timestamp": activity["timestamp"],
                        "points": activity["points"],
                    }
                )

        if "application_log" in self.data["korean"]:
            for activity in self.data["korean"]["application_log"]:
                all_activities.append(
                    {
                        "module": "korean",
                        "type": "application",
                        "description": f"Applied Korean with {activity['type']}",
                        "timestamp": activity["timestamp"],
                        "points": activity["points"],
                    }
                )

        # French activities
        if "completed_lessons" in self.data["french"]:
            for activity in self.data["french"]["completed_lessons"]:
                all_activities.append(
                    {
                        "module": "french",
                        "type": "fundamentals",
                        "description": f"Completed '{activity['lesson']}'",
                        "timestamp": activity["timestamp"],
                        "points": activity["points"],
                    }
                )

        if "immersion_log" in self.data["french"]:
            for activity in self.data["french"]["immersion_log"]:
                all_activities.append(
                    {
                        "module": "french",
                        "type": "immersion",
                        "description": f"Immersed in {activity['type']} for {activity['duration']}",
                        "timestamp": activity["timestamp"],
                        "points": activity["points"],
                    }
                )

        if "application_log" in self.data["french"]:
            for activity in self.data["french"]["application_log"]:
                all_activities.append(
                    {
                        "module": "french",
                        "type": "application",
                        "description": f"Applied French with {activity['type']}",
                        "timestamp": activity["timestamp"],
                        "points": activity["points"],
                    }
                )

        # Dissertation activities
        for phase in ["preparation", "empirical", "integration", "finalization"]:
            for task in self.data["diss"]["tasks"][phase]:
                if "sessions" in task:
                    for session in task["sessions"]:
                        all_activities.append(
                            {
                                "module": "diss",
                                "type": phase,
                                "description": f"Worked on '{task['name']}' for {session['hours']} hours",
                                "timestamp": session["date"]
                                + " 12:00",  # Add time for sorting
                                "points": int(session["hours"] * 10),
                            }
                        )
                        
        # Habit activities
        if "habits" in self.data:
            habits = self.data["habits"]
            
            # Daily habits and custom habits
            for habit_type in ["daily_habits", "custom_habits"]:
                for habit in habits.get(habit_type, []):
                    for date in habit.get("completed_dates", []):
                        # Format as timestamp for consistency 
                        timestamp = f"{date} 12:00:00"
                        
                        all_activities.append(
                            {
                                "module": "habit",
                                "type": "daily",
                                "description": f"Completed '{habit['name']}' habit",
                                "timestamp": timestamp,
                                "points": 5,  # Assign a consistent point value
                            }
                        )
            
            # Check-ins
            for check_in in habits.get("check_ins", []):
                for date in check_in.get("dates", []):
                    # Format as timestamp for consistency
                    timestamp = f"{date} 12:00:00"
                    
                    all_activities.append(
                        {
                            "module": "habit",
                            "type": "check-in",
                            "description": f"{check_in['name']} check-in",
                            "timestamp": timestamp,
                            "points": 10,  # Assign a higher point value for check-ins
                        }
                    )

        # Reward claims
        if "unlocked_rewards" in self.data:
            for reward in self.data["unlocked_rewards"]:
                costs = {"small": 50, "medium": 200, "large": 500}
                all_activities.append(
                    {
                        "module": "reward",
                        "type": "claim",
                        "description": f"Claimed {reward['tier']} reward: {reward['reward']}",
                        "timestamp": reward["date"] + " 12:00",  # Add time for sorting
                        "points": -costs[reward["tier"]],
                    }
                )

        # Sort by timestamp (most recent first)
        all_activities.sort(key=lambda x: x["timestamp"], reverse=True)

        # If no activities are found
        if not all_activities:
            tk.Label(
                activity_frame,
                text="No activities recorded yet. Start completing tasks to see your activity!",
                font=self.theme.small_font,
                bg=self.theme.bg_color,
                fg=self.theme.text_color,
            ).pack(pady=20)
            return

        # Create scrollable frame for activities
        canvas = tk.Canvas(activity_frame, bg=self.theme.bg_color, highlightthickness=0)
        scrollbar = ttk.Scrollbar(
            activity_frame, orient="vertical", command=canvas.yview
        )
        scrollable_frame = tk.Frame(canvas, bg=self.theme.bg_color)

        scrollable_frame.bind(
            "<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Module icon/color indicator mapping
        module_colors = {
            "art": self.theme.art_color,
            "korean": self.theme.korean_color,
            "french": self.theme.french_color,
            "diss": self.theme.diss_color,
            "habit": self.theme.habit_color,  # Use the theme's habit color
            "reward": "#E91E63",
        }

        # Display recent activities (limit to 20 most recent)
        max_activities = min(20, len(all_activities))
        for i in range(max_activities):
            activity = all_activities[i]

            # Activity row
            row_frame = tk.Frame(scrollable_frame, bg=self.theme.bg_color)
            row_frame.pack(fill=tk.X, pady=2)

            # Apply alternating row colors
            if i % 2 == 0:
                row_bg = self.theme.bg_color
            else:
                row_bg = self.theme.darken_color(self.theme.bg_color)

            # Module icon/color indicator
            indicator = tk.Label(
                row_frame,
                text="■",
                font=self.theme.pixel_font,
                bg=row_bg,
                fg=module_colors.get(activity["module"], self.theme.text_color),
            )
            indicator.pack(side=tk.LEFT, padx=5)

            # Timestamp
            timestamp = tk.Label(
                row_frame,
                text=activity["timestamp"],
                font=self.theme.small_font,
                bg=row_bg,
                fg=self.theme.text_color,
                width=16,
                anchor="w",
            )
            timestamp.pack(side=tk.LEFT, padx=5)

            # Description
            description = tk.Label(
                row_frame,
                text=activity["description"],
                font=self.theme.small_font,
                bg=row_bg,
                fg=self.theme.text_color,
                anchor="w",
            )
            description.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)

            # Points (positive or negative)
            if activity["points"] > 0:
                points_text = f"+{activity['points']}"
                points_color = "#4CAF50"  # Green for positive
            else:
                points_text = f"{activity['points']}"
                points_color = "#F44336"  # Red for negative

            points = tk.Label(
                row_frame,
                text=points_text,
                font=self.theme.small_font,
                bg=row_bg,
                fg=points_color,
                width=5,
                anchor="e",
            )
            points.pack(side=tk.RIGHT, padx=5)

    def create_module_stats(self, parent, module):
        """
        Create statistics display for a specific module with pixel art styling.

        Args:
            parent: Parent widget for the module statistics
            module: Module name ('art', 'korean', 'french', or 'diss')
        """
        # Module color mapping
        colors = {
            "art": self.theme.art_color,
            "korean": self.theme.korean_color,
            "french": self.theme.french_color,
            "diss": self.theme.diss_color,  # Add this line
        }

        # Module display name mapping
        display_names = {
            "art": "Art",
            "korean": "Korean",
            "french": "French",
            "diss": "Dissertation",  # Add this line
        }

        # Summary frame
        summary_frame = tk.LabelFrame(
            parent,
            text=f"{display_names[module]} Summary",
            font=self.theme.pixel_font,
            bg=self.theme.bg_color,
            fg=self.theme.text_color,
            padx=10,
            pady=10,
            relief=tk.RIDGE,
            bd=3,
        )
        summary_frame.pack(fill=tk.X, padx=10, pady=10)

        # Common statistics for all modules
        tk.Label(
            summary_frame,
            text=f"Total Points: {self.data[module]['points']}",
            font=self.theme.small_font,
            bg=self.theme.bg_color,
            fg=self.theme.text_color,
        ).pack(anchor="w", pady=3)

        tk.Label(
            summary_frame,
            text=f"Current Level: {self.data[module]['level']}",
            font=self.theme.small_font,
            bg=self.theme.bg_color,
            fg=self.theme.text_color,
        ).pack(anchor="w", pady=3)

        tk.Label(
            summary_frame,
            text=f"Current Streak: {self.data[module]['streak']} days",
            font=self.theme.small_font,
            bg=self.theme.bg_color,
            fg="#FF5722",
        ).pack(anchor="w", pady=3)

        # Module-specific statistics
        if module == "art":
            tk.Label(
                summary_frame,
                text=f"Fundamentals Completed: {self.data[module]['fundamentals_completed']}",
                font=self.theme.small_font,
                bg=self.theme.bg_color,
                fg=self.theme.text_color,
            ).pack(anchor="w", pady=3)

            tk.Label(
                summary_frame,
                text=f"Sketchbook Pages: {self.data[module]['sketchbook_pages']}",
                font=self.theme.small_font,
                bg=self.theme.bg_color,
                fg=self.theme.text_color,
            ).pack(anchor="w", pady=3)

            tk.Label(
                summary_frame,
                text=f"Accountability Posts: {self.data[module]['accountability_posts']}",
                font=self.theme.small_font,
                bg=self.theme.bg_color,
                fg=self.theme.text_color,
            ).pack(anchor="w", pady=3)
        elif module in ["korean", "french"]:
            tk.Label(
                summary_frame,
                text=f"Lessons Completed: {self.data[module]['fundamentals_completed']}",
                font=self.theme.small_font,
                bg=self.theme.bg_color,
                fg=self.theme.text_color,
            ).pack(anchor="w", pady=3)

            tk.Label(
                summary_frame,
                text=f"Immersion Hours: {self.data[module]['immersion_hours']}",
                font=self.theme.small_font,
                bg=self.theme.bg_color,
                fg=self.theme.text_color,
            ).pack(anchor="w", pady=3)

            tk.Label(
                summary_frame,
                text=f"Application Sessions: {self.data[module]['application_sessions']}",
                font=self.theme.small_font,
                bg=self.theme.bg_color,
                fg=self.theme.text_color,
            ).pack(anchor="w", pady=3)
        elif module == "diss":
            # Calculate total hours worked across all phases
            total_hours = 0
            for phase in ["preparation", "empirical", "integration", "finalization"]:
                for task in self.data["diss"]["tasks"][phase]:
                    total_hours += task["hours_worked"]

            tk.Label(
                summary_frame,
                text=f"Total Hours Worked: {total_hours}",
                font=self.theme.small_font,
                bg=self.theme.bg_color,
                fg=self.theme.text_color,
            ).pack(anchor="w", pady=3)

        # Progress to next level
        progress_frame = tk.LabelFrame(
            parent,
            text="Progress to Next Level",
            font=self.theme.pixel_font,
            bg=self.theme.bg_color,
            fg=self.theme.text_color,
            padx=10,
            pady=10,
            relief=tk.RIDGE,
            bd=3,
        )
        progress_frame.pack(fill=tk.X, padx=10, pady=10)

        # Calculate progress
        points_per_level = 100
        current_level_points = self.data[module]["points"] % points_per_level
        progress_percent = (current_level_points / points_per_level) * 100

        tk.Label(
            progress_frame,
            text=f"Level {self.data[module]['level']} → Level {self.data[module]['level'] + 1}",
            font=self.theme.small_font,
            bg=self.theme.bg_color,
            fg=self.theme.text_color,
        ).pack(anchor="w", pady=5)

        tk.Label(
            progress_frame,
            text=f"{current_level_points}/{points_per_level} points",
            font=self.theme.small_font,
            bg=self.theme.bg_color,
            fg=self.theme.text_color,
        ).pack(anchor="w", pady=5)

        # Create pixel art progress bar for level progress
        create_pixel_progress_bar(
            progress_frame,
            progress_percent,
            colors[module],
            self.theme.bg_color,
            self.theme.text_color,
            self.theme.darken_color,
        )

        tk.Label(
            progress_frame,
            text=f"{progress_percent:.1f}% complete",
            font=self.theme.small_font,
            bg=self.theme.bg_color,
            fg=self.theme.text_color,
        ).pack(anchor="w", pady=5)

        # Activity breakdown
        activity_frame = tk.LabelFrame(
            parent,
            text="Activity Breakdown",
            font=self.theme.pixel_font,
            bg=self.theme.bg_color,
            fg=self.theme.text_color,
            padx=10,
            pady=10,
            relief=tk.RIDGE,
            bd=3,
        )
        activity_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Different breakdowns based on module
        if module == "art":
            self.create_art_activity_breakdown(activity_frame)
        elif module == "korean":
            self.create_language_activity_breakdown(activity_frame, "korean")
        elif module == "french":
            self.create_language_activity_breakdown(activity_frame, "french")
        elif module == "diss":
            # Create a temporary instance of DissModule to use its method
            diss_module = DissModule(self.app, self.data_manager, self.theme)
            diss_module.create_activity_breakdown(activity_frame)
    
    def create_habits_stats(self, parent):
        """
        Create statistics display for habit tracking.
        
        Args:
            parent: Parent widget for the habit statistics
        """
        # Check if habits data exists
        if "habits" not in self.data:
            tk.Label(
                parent,
                text="No habit data available yet. Start tracking habits to see statistics!",
                font=self.theme.pixel_font,
                bg=self.theme.bg_color,
                fg=self.theme.text_color,
                wraplength=400,
                justify="center",
            ).pack(pady=50)
            return
            
        habits = self.data["habits"]
        daily_habits = habits.get("daily_habits", [])
        custom_habits = habits.get("custom_habits", [])
        check_ins = habits.get("check_ins", [])
        
        all_habits = daily_habits + custom_habits
        
        # Summary frame
        summary_frame = tk.LabelFrame(
            parent,
            text="Habits Summary",
            font=self.theme.pixel_font,
            bg=self.theme.bg_color,
            fg=self.theme.habit_color,  # Use the theme's habit color
            padx=10,
            pady=10,
            relief=tk.RIDGE,
            bd=3,
        )
        summary_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # Stats grid (2x2)
        stats_grid = tk.Frame(summary_frame, bg=self.theme.bg_color)
        stats_grid.pack(fill=tk.X, pady=10)
        
        # Total habits
        total_habits = len(all_habits)
        active_habits = sum(1 for h in all_habits if h.get("active", True))
        
        # Count habits completed today
        today = datetime.now().date().strftime("%Y-%m-%d")
        completed_today = sum(
            1 for h in all_habits if h.get("active", True) and today in h.get("completed_dates", [])
        )
        
        # Completion rate
        completion_rate = (
            int((completed_today / active_habits) * 100) if active_habits > 0 else 0
        )
        
        # Calculate streaks
        longest_streak = max([h.get("streak", 0) for h in all_habits], default=0)
        
        # Top row stats
        stat_frame1 = tk.Frame(stats_grid, bg=self.theme.bg_color, padx=10, pady=5)
        stat_frame1.grid(row=0, column=0, padx=10, pady=5)
        
        tk.Label(
            stat_frame1,
            text="🧠 Total Habits",
            font=self.theme.small_font,
            bg=self.theme.bg_color,
            fg=self.theme.text_color,
        ).pack()
        
        tk.Label(
            stat_frame1,
            text=str(total_habits),
            font=self.theme.heading_font,
            bg=self.theme.bg_color,
            fg=self.theme.habit_color,  # Use the theme's habit color
        ).pack()
        
        # Active habits
        stat_frame2 = tk.Frame(stats_grid, bg=self.theme.bg_color, padx=10, pady=5)
        stat_frame2.grid(row=0, column=1, padx=10, pady=5)
        
        tk.Label(
            stat_frame2,
            text="✅ Active Habits",
            font=self.theme.small_font,
            bg=self.theme.bg_color,
            fg=self.theme.text_color,
        ).pack()
        
        tk.Label(
            stat_frame2,
            text=str(active_habits),
            font=self.theme.heading_font,
            bg=self.theme.bg_color,
            fg="#4CAF50",
        ).pack()
        
        # Today's completion
        stat_frame3 = tk.Frame(stats_grid, bg=self.theme.bg_color, padx=10, pady=5)
        stat_frame3.grid(row=1, column=0, padx=10, pady=5)
        
        tk.Label(
            stat_frame3,
            text="📅 Today's Completion",
            font=self.theme.small_font,
            bg=self.theme.bg_color,
            fg=self.theme.text_color,
        ).pack()
        
        completion_color = "#4CAF50" if completion_rate >= 80 else "#FFC107" if completion_rate >= 50 else "#F44336"
        
        tk.Label(
            stat_frame3,
            text=f"{completion_rate}%",
            font=self.theme.heading_font,
            bg=self.theme.bg_color,
            fg=completion_color,
        ).pack()
        
        # Longest streak
        stat_frame4 = tk.Frame(stats_grid, bg=self.theme.bg_color, padx=10, pady=5)
        stat_frame4.grid(row=1, column=1, padx=10, pady=5)
        
        tk.Label(
            stat_frame4,
            text="🔥 Longest Streak",
            font=self.theme.small_font,
            bg=self.theme.bg_color,
            fg=self.theme.text_color,
        ).pack()
        
        tk.Label(
            stat_frame4,
            text=f"{longest_streak} days",
            font=self.theme.heading_font,
            bg=self.theme.bg_color,
            fg="#FF5722",
        ).pack()
        
        # Weekly completion chart
        weekly_frame = tk.LabelFrame(
            parent,
            text="Weekly Habit Completion",
            font=self.theme.pixel_font,
            bg=self.theme.bg_color,
            fg=self.theme.habit_color,  # Use the theme's habit color
            padx=10,
            pady=10,
            relief=tk.RIDGE,
            bd=3,
        )
        weekly_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # Generate dates for the past 7 days
        today = datetime.now().date()
        past_dates = [(today - timedelta(days=i)).strftime("%Y-%m-%d") for i in range(6, -1, -1)]
        weekdays = [(today - timedelta(days=i)).strftime("%a") for i in range(6, -1, -1)]
        day_numbers = [(today - timedelta(days=i)).day for i in range(6, -1, -1)]
        
        # Create header with dates
        date_frame = tk.Frame(weekly_frame, bg=self.theme.bg_color)
        date_frame.pack(fill=tk.X, pady=5)
        
        # Create empty column for habit names
        empty_label = tk.Label(
            date_frame,
            text="",
            font=self.theme.small_font,
            bg=self.theme.bg_color,
            width=15,
        )
        empty_label.grid(row=0, column=0, padx=2)
        
        # Create date labels
        for i, (weekday, day_num) in enumerate(zip(weekdays, day_numbers)):
            date_column = tk.Frame(date_frame, bg=self.theme.bg_color)
            date_column.grid(row=0, column=i+1, padx=2)
            
            # Weekday
            tk.Label(
                date_column,
                text=weekday,
                font=self.theme.small_font,
                bg=self.theme.bg_color,
                fg=self.theme.text_color,
            ).pack()
            
            # Day number - highlight today
            is_today = day_num == today.day
            day_color = "#FF5722" if is_today else self.theme.text_color
            day_bg = self.theme.bg_color
            
            tk.Label(
                date_column,
                text=str(day_num),
                font=self.theme.small_font,
                bg=day_bg,
                fg=day_color,
                width=2,
            ).pack()
        
        # Create scrollable frame for habits
        canvas = tk.Canvas(weekly_frame, bg=self.theme.bg_color, highlightthickness=0)
        scrollbar = ttk.Scrollbar(weekly_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=self.theme.bg_color)
        
        scrollable_frame.bind(
            "<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True, padx=5, pady=5)
        scrollbar.pack(side="right", fill="y")
        
        # Show habit rows with completion status
        active_habits = [h for h in all_habits if h.get("active", True)]
        
        if not active_habits:
            tk.Label(
                scrollable_frame,
                text="No active habits to display.",
                font=self.theme.small_font,
                bg=self.theme.bg_color,
                fg=self.theme.text_color,
                pady=10,
            ).pack()
        else:
            # Display each habit's completion status for the past week
            for i, habit in enumerate(active_habits):
                # Row background alternates for better readability
                row_bg = self.theme.bg_color if i % 2 == 0 else self.theme.darken_color(self.theme.bg_color)
                
                row_frame = tk.Frame(scrollable_frame, bg=row_bg)
                row_frame.pack(fill=tk.X)
                
                # Habit name with icon
                habit_label = tk.Label(
                    row_frame,
                    text=f"{habit.get('icon', '📋')} {habit['name']}",
                    font=self.theme.small_font,
                    bg=row_bg,
                    fg=self.theme.text_color,
                    width=15,
                    anchor="w",
                )
                habit_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")
                
                # Show completion status for each day
                for j, date in enumerate(past_dates):
                    completed = date in habit.get("completed_dates", [])
                    
                    if completed:
                        status_color = "#4CAF50"  # Green for completed
                        status_text = "✓"
                    else:
                        status_color = self.theme.darken_color(self.theme.primary_color)
                        status_text = "·"
                        
                    # Create a small box to represent completion
                    tk.Label(
                        row_frame,
                        text=status_text,
                        font=("TkDefaultFont", 16),
                        bg=row_bg,
                        fg=status_color,
                        width=2,
                    ).grid(row=0, column=j+1, padx=5, pady=5)
                
                # Show streak
                streak = habit.get("streak", 0)
                streak_color = "#FF5722" if streak > 0 else self.theme.text_color
                
                tk.Label(
                    row_frame,
                    text=f"{streak}🔥",
                    font=self.theme.small_font,
                    bg=row_bg,
                    fg=streak_color,
                ).grid(row=0, column=8, padx=5, pady=5)
        
        # Check-ins section
        checkins_frame = tk.LabelFrame(
            parent,
            text="Recent Check-ins",
            font=self.theme.pixel_font,
            bg=self.theme.bg_color,
            fg=self.theme.habit_color,  # Use the theme's habit color
            padx=10,
            pady=10,
            relief=tk.RIDGE,
            bd=3,
        )
        checkins_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Collect all check-in events
        all_checkins = []
        
        for check_in in check_ins:
            for date in check_in.get("dates", []):
                all_checkins.append({
                    "name": check_in["name"],
                    "icon": check_in.get("icon", "🩺"),
                    "date": date,
                    "notes": check_in.get("notes", {}).get(date, "")
                })
        
        # Sort by date (most recent first)
        all_checkins.sort(key=lambda x: x["date"], reverse=True)
        
        if not all_checkins:
            tk.Label(
                checkins_frame,
                text="No check-ins recorded yet.",
                font=self.theme.small_font,
                bg=self.theme.bg_color,
                fg=self.theme.text_color,
                pady=10,
            ).pack()
        else:
            # Create scrollable frame for check-ins
            canvas = tk.Canvas(checkins_frame, bg=self.theme.bg_color, highlightthickness=0)
            scrollbar = ttk.Scrollbar(checkins_frame, orient="vertical", command=canvas.yview)
            scrollable_frame = tk.Frame(canvas, bg=self.theme.bg_color)
            
            scrollable_frame.bind(
                "<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
            )
            
            canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
            canvas.configure(yscrollcommand=scrollbar.set)
            
            canvas.pack(side="left", fill="both", expand=True, padx=5, pady=5)
            scrollbar.pack(side="right", fill="y")
            
            # Show up to 10 most recent check-ins
            max_to_show = min(10, len(all_checkins))
            
            for i in range(max_to_show):
                checkin = all_checkins[i]
                
                # Row background alternates for better readability
                row_bg = self.theme.bg_color if i % 2 == 0 else self.theme.darken_color(self.theme.bg_color)
                
                # Check-in row
                row_frame = tk.Frame(scrollable_frame, bg=row_bg, relief=tk.RIDGE, bd=1)
                row_frame.pack(fill=tk.X, pady=3, padx=5)
                
                # Header with name and date
                header_frame = tk.Frame(row_frame, bg=row_bg)
                header_frame.pack(fill=tk.X, padx=5, pady=3)
                
                # Icon and name
                name_label = tk.Label(
                    header_frame,
                    text=f"{checkin['icon']} {checkin['name']}",
                    font=self.theme.small_font,
                    bg=row_bg,
                    fg=self.theme.habit_color,  # Use the theme's habit color
                    anchor="w",
                )
                name_label.pack(side=tk.LEFT)
                
                # Date
                date_label = tk.Label(
                    header_frame,
                    text=checkin["date"],
                    font=self.theme.small_font,
                    bg=row_bg,
                    fg=self.theme.text_color,
                )
                date_label.pack(side=tk.RIGHT)
                
                # Notes if any
                if checkin["notes"]:
                    notes_frame = tk.Frame(row_frame, bg=row_bg, pady=3)
                    notes_frame.pack(fill=tk.X, padx=5)
                    
                    notes_text = tk.Text(
                        notes_frame,
                        height=2,
                        width=40,
                        font=self.theme.small_font,
                        bg=self.theme.primary_color,
                        fg=self.theme.text_color,
                        wrap=tk.WORD,
                    )
                    notes_text.insert(tk.END, checkin["notes"])
                    notes_text.config(state=tk.DISABLED)
                    notes_text.pack(fill=tk.X)

    def create_art_activity_breakdown(self, parent):
        """
        Create activity breakdown for art module.

        Args:
            parent: Parent widget for the art activity breakdown
        """
        # Calculate statistics
        total_activities = 0
        fundamentals_count = self.data["art"]["fundamentals_completed"]
        sketchbook_count = self.data["art"]["sketchbook_pages"]
        accountability_count = self.data["art"]["accountability_posts"]

        total_activities = fundamentals_count + sketchbook_count + accountability_count

        if total_activities == 0:
            # No activities yet
            tk.Label(
                parent,
                text="No art activities recorded yet. Start completing art tasks to see your breakdown!",
                font=self.theme.small_font,
                bg=self.theme.bg_color,
                fg=self.theme.text_color,
            ).pack(pady=20)
            return

        # Calculate percentages
        fundamentals_percent = (
            (fundamentals_count / total_activities * 100) if total_activities > 0 else 0
        )
        sketchbook_percent = (
            (sketchbook_count / total_activities * 100) if total_activities > 0 else 0
        )
        accountability_percent = (
            (accountability_count / total_activities * 100)
            if total_activities > 0
            else 0
        )

        # Create chart frame
        chart_frame = tk.Frame(parent, bg=self.theme.bg_color)
        chart_frame.pack(pady=10, fill=tk.X)

        # Left side - Text stats
        stats_frame = tk.Frame(chart_frame, bg=self.theme.bg_color)
        stats_frame.pack(side=tk.LEFT, padx=20, fill=tk.Y)

        tk.Label(
            stats_frame,
            text=f"Total Activities: {total_activities}",
            font=self.theme.small_font,
            bg=self.theme.bg_color,
            fg=self.theme.text_color,
        ).pack(anchor="w", pady=5)

        tk.Label(
            stats_frame,
            text=f"Fundamentals: {fundamentals_count} ({fundamentals_percent:.1f}%)",
            font=self.theme.small_font,
            bg=self.theme.bg_color,
            fg="#4CAF50",  # Green
        ).pack(anchor="w", pady=5)

        tk.Label(
            stats_frame,
            text=f"Sketchbook: {sketchbook_count} ({sketchbook_percent:.1f}%)",
            font=self.theme.small_font,
            bg=self.theme.bg_color,
            fg="#2196F3",  # Blue
        ).pack(anchor="w", pady=5)

        tk.Label(
            stats_frame,
            text=f"Accountability: {accountability_count} ({accountability_percent:.1f}%)",
            font=self.theme.small_font,
            bg=self.theme.bg_color,
            fg="#FF9800",  # Orange
        ).pack(anchor="w", pady=5)

        # Right side - Visual representation
        visual_frame = tk.Frame(chart_frame, bg=self.theme.bg_color)
        visual_frame.pack(side=tk.RIGHT, padx=20, fill=tk.BOTH, expand=True)

        # Create a stacked bar representation
        bar_width = 250
        bar_height = 30

        # Create canvas for the stacked bar
        bar_canvas = tk.Canvas(
            visual_frame,
            width=bar_width,
            height=bar_height,
            bg=self.theme.bg_color,
            highlightthickness=0,
        )
        bar_canvas.pack(pady=10)

        # Draw segments
        fundamentals_width = int((fundamentals_percent / 100) * bar_width)
        sketchbook_width = int((sketchbook_percent / 100) * bar_width)

        # Draw segments with pixelated edges
        bar_canvas.create_rectangle(
            0, 0, fundamentals_width, bar_height, fill="#4CAF50", outline=""
        )

        bar_canvas.create_rectangle(
            fundamentals_width,
            0,
            fundamentals_width + sketchbook_width,
            bar_height,
            fill="#2196F3",
            outline="",
        )

        bar_canvas.create_rectangle(
            fundamentals_width + sketchbook_width,
            0,
            bar_width,
            bar_height,
            fill="#FF9800",
            outline="",
        )

        # Add pixel-like edges
        for x in range(0, bar_width, 4):
            bar_canvas.create_rectangle(
                x, 0, x + 2, 2, fill=self.theme.darken_color("#4CAF50"), outline=""
            )
            bar_canvas.create_rectangle(
                x,
                bar_height - 2,
                x + 2,
                bar_height,
                fill=self.theme.darken_color("#FF9800"),
                outline="",
            )

        # Add legend
        legend_frame = tk.Frame(visual_frame, bg=self.theme.bg_color)
        legend_frame.pack(pady=5)

        # Fundamentals legend
        fund_frame = tk.Frame(legend_frame, bg=self.theme.bg_color)
        fund_frame.pack(side=tk.LEFT, padx=10)

        fund_color = tk.Label(
            fund_frame,
            text="■",
            font=self.theme.small_font,
            bg=self.theme.bg_color,
            fg="#4CAF50",
        )
        fund_color.pack(side=tk.LEFT)

        fund_label = tk.Label(
            fund_frame,
            text="Fundamentals",
            font=self.theme.small_font,
            bg=self.theme.bg_color,
            fg=self.theme.text_color,
        )
        fund_label.pack(side=tk.LEFT, padx=2)

        # Sketchbook legend
        sketch_frame = tk.Frame(legend_frame, bg=self.theme.bg_color)
        sketch_frame.pack(side=tk.LEFT, padx=10)

        sketch_color = tk.Label(
            sketch_frame,
            text="■",
            font=self.theme.small_font,
            bg=self.theme.bg_color,
            fg="#2196F3",
        )
        sketch_color.pack(side=tk.LEFT)

        sketch_label = tk.Label(
            sketch_frame,
            text="Sketchbook",
            font=self.theme.small_font,
            bg=self.theme.bg_color,
            fg=self.theme.text_color,
        )
        sketch_label.pack(side=tk.LEFT, padx=2)

        # Accountability legend
        acc_frame = tk.Frame(legend_frame, bg=self.theme.bg_color)
        acc_frame.pack(side=tk.LEFT, padx=10)

        acc_color = tk.Label(
            acc_frame,
            text="■",
            font=self.theme.small_font,
            bg=self.theme.bg_color,
            fg="#FF9800",
        )
        acc_color.pack(side=tk.LEFT)

        acc_label = tk.Label(
            acc_frame,
            text="Accountability",
            font=self.theme.small_font,
            bg=self.theme.bg_color,
            fg=self.theme.text_color,
        )
        acc_label.pack(side=tk.LEFT, padx=2)

        # Recent art activities (if available)
        recent_frame = tk.LabelFrame(
            parent,
            text="Recent Art Activities",
            font=self.theme.small_font,
            bg=self.theme.bg_color,
            fg=self.theme.text_color,
            padx=10,
            pady=10,
        )
        recent_frame.pack(fill=tk.BOTH, expand=True, pady=10)

        # Collect all art activities
        art_activities = []

        if "completed_exercises" in self.data["art"]:
            for activity in self.data["art"]["completed_exercises"]:
                art_activities.append(
                    {
                        "type": "Fundamentals",
                        "description": f"Completed '{activity['exercise']}'",
                        "timestamp": activity["timestamp"],
                        "points": activity["points"],
                    }
                )

        if "drawing_log" in self.data["art"]:
            for activity in self.data["art"]["drawing_log"]:
                art_activities.append(
                    {
                        "type": "Sketchbook",
                        "description": f"Drew {activity['type']}",
                        "timestamp": activity["timestamp"],
                        "points": activity["points"],
                    }
                )

        if "accountability_log" in self.data["art"]:
            for activity in self.data["art"]["accountability_log"]:
                art_activities.append(
                    {
                        "type": "Accountability",
                        "description": f"Posted '{activity['title']}' on {activity['platform']}",
                        "timestamp": activity["timestamp"],
                        "points": activity["points"],
                    }
                )

        # Sort by timestamp (most recent first)
        art_activities.sort(key=lambda x: x["timestamp"], reverse=True)

        # If no activities
        if not art_activities:
            tk.Label(
                recent_frame,
                text="No recent art activities recorded.",
                font=self.theme.small_font,
                bg=self.theme.bg_color,
                fg=self.theme.text_color,
            ).pack(pady=10)
            return

        # Create scrollable frame for activities
        canvas = tk.Canvas(recent_frame, bg=self.theme.bg_color, highlightthickness=0)
        scrollbar = ttk.Scrollbar(recent_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=self.theme.bg_color)

        scrollable_frame.bind(
            "<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Type color mapping
        type_colors = {
            "Fundamentals": "#4CAF50",
            "Sketchbook": "#2196F3",
            "Accountability": "#FF9800",
        }

        # Show up to 10 most recent activities
        max_to_show = min(10, len(art_activities))
        for i in range(max_to_show):
            activity = art_activities[i]

            # Activity row
            row_frame = tk.Frame(scrollable_frame, bg=self.theme.bg_color)
            row_frame.pack(fill=tk.X, pady=2)

            # Apply alternating row colors
            if i % 2 == 0:
                row_bg = self.theme.bg_color
            else:
                row_bg = self.theme.darken_color(self.theme.bg_color)

            # Type indicator
            type_label = tk.Label(
                row_frame,
                text=activity["type"],
                font=self.theme.small_font,
                bg=row_bg,
                fg=type_colors.get(activity["type"], self.theme.text_color),
                width=15,
                anchor="w",
            )
            type_label.pack(side=tk.LEFT, padx=5)

            # Description
            description = tk.Label(
                row_frame,
                text=activity["description"],
                font=self.theme.small_font,
                bg=row_bg,
                fg=self.theme.text_color,
                anchor="w",
            )
            description.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)

            # Points
            points = tk.Label(
                row_frame,
                text=f"+{activity['points']}",
                font=self.theme.small_font,
                bg=row_bg,
                fg="#4CAF50",
                width=4,
                anchor="e",
            )
            points.pack(side=tk.RIGHT, padx=5)

            # Date/time
            timestamp = tk.Label(
                row_frame,
                text=activity["timestamp"],
                font=self.theme.small_font,
                bg=row_bg,
                fg=self.theme.text_color,
                width=16,
                anchor="e",
            )
            timestamp.pack(side=tk.RIGHT, padx=5)

    def create_language_activity_breakdown(self, parent, module):
        """
        Create activity breakdown for language modules (Korean and French).

        Args:
            parent: Parent widget for the language activity breakdown
            module: Module name ('korean' or 'french')
        """

        # Calculate statistics
        total_activities = 0

        # Collect language activities
        language_activities = []

        # For fundamentals
        if "completed_lessons" in self.data[module]:
            for activity in self.data[module]["completed_lessons"]:
                language_activities.append(
                    {
                        "type": "Fundamentals",
                        "description": f"Completed '{activity['lesson']}'",
                        "timestamp": activity["timestamp"],
                        "points": activity["points"],
                    }
                )
                total_activities += 1

        # For immersion
        if "immersion_log" in self.data[module]:
            for activity in self.data[module]["immersion_log"]:
                language_activities.append(
                    {
                        "type": "Immersion",
                        "description": f"Immersed in {activity['type']} for {activity['duration']}",
                        "timestamp": activity["timestamp"],
                        "points": activity["points"],
                    }
                )
                total_activities += 1

        # For application
        if "application_log" in self.data[module]:
            for activity in self.data[module]["application_log"]:
                language_activities.append(
                    {
                        "type": "Application",
                        "description": f"Applied with {activity['type']}",
                        "timestamp": activity["timestamp"],
                        "points": activity["points"],
                    }
                )
                total_activities += 1

        # If no activities yet
        if total_activities == 0:
            tk.Label(
                parent,
                text=f"No {module.capitalize()} activities recorded yet. Start completing tasks to see your breakdown!",
                font=self.theme.small_font,
                bg=self.theme.bg_color,
                fg=self.theme.text_color,
                wraplength=400,
                justify="center",
            ).pack(pady=20)
            return

        # Sort by timestamp (most recent first)
        language_activities.sort(key=lambda x: x["timestamp"], reverse=True)

        # Create activity list frame
        activity_list_frame = tk.LabelFrame(
            parent,
            text=f"Recent {module.capitalize()} Activities",
            font=self.theme.small_font,
            bg=self.theme.bg_color,
            fg=self.theme.text_color,
            padx=10,
            pady=10,
        )
        activity_list_frame.pack(fill=tk.BOTH, expand=True, pady=10)

        # Create scrollable frame for activities
        canvas = tk.Canvas(
            activity_list_frame, bg=self.theme.bg_color, highlightthickness=0
        )
        scrollbar = ttk.Scrollbar(
            activity_list_frame, orient="vertical", command=canvas.yview
        )
        scrollable_frame = tk.Frame(canvas, bg=self.theme.bg_color)

        scrollable_frame.bind(
            "<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Type color mapping
        type_colors = {
            "Fundamentals": "#4CAF50",  # Green
            "Immersion": "#2196F3",  # Blue
            "Application": "#FF9800",  # Orange
        }

        # Show up to 15 most recent activities
        max_to_show = min(15, len(language_activities))
        for i in range(max_to_show):
            activity = language_activities[i]

            # Activity row
            row_frame = tk.Frame(scrollable_frame, bg=self.theme.bg_color)
            row_frame.pack(fill=tk.X, pady=2)

            # Apply alternating row colors
            if i % 2 == 0:
                row_bg = self.theme.bg_color
            else:
                row_bg = self.theme.darken_color(self.theme.bg_color)

            # Type indicator
            type_label = tk.Label(
                row_frame,
                text=activity["type"],
                font=self.theme.small_font,
                bg=row_bg,
                fg=type_colors.get(activity["type"], self.theme.text_color),
                width=12,
                anchor="w",
            )
            type_label.pack(side=tk.LEFT, padx=5)

            # Description
            description = tk.Label(
                row_frame,
                text=activity["description"],
                font=self.theme.small_font,
                bg=row_bg,
                fg=self.theme.text_color,
                anchor="w",
            )
            description.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)

            # Points
            points = tk.Label(
                row_frame,
                text=f"+{activity['points']}",
                font=self.theme.small_font,
                bg=row_bg,
                fg="#4CAF50",
                width=4,
                anchor="e",
            )
            points.pack(side=tk.RIGHT, padx=5)

            # Date/time
            timestamp = tk.Label(
                row_frame,
                text=activity["timestamp"],
                font=self.theme.small_font,
                bg=row_bg,
                fg=self.theme.text_color,
                width=16,
                anchor="e",
            )
            timestamp.pack(side=tk.RIGHT, padx=5)

    def export_data(self):
        """Export statistics and logs to a file."""
        try:
            # Export data using data manager
            filename = self.data_manager.export_data()
            messagebox.showinfo(
                "Export Successful", f"Data successfully exported to {filename}"
            )
        except Exception as e:
            messagebox.showerror("Export Error", f"Failed to export data: {str(e)}")
