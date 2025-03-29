"""
Main GUI components for the Pixel Quest application.
"""

import tkinter as tk
from tkinter import ttk
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
        self.root.geometry("800x500")

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
        stats_tab = tk.Frame(tab_control, bg=self.theme.bg_color)
        settings_tab = tk.Frame(tab_control, bg=self.theme.bg_color)

        tab_control.add(modules_tab, text="Modules")
        tab_control.add(stats_tab, text="Statistics")
        tab_control.add(settings_tab, text="Settings")

        # === MODULES TAB ===
        self.create_modules_tab(modules_tab)

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
        buttons_frame.pack(pady=20, fill=tk.BOTH, expand=True)

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

        # Add after the French module button in create_modules_tab() method
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

        # Habit Tracker
        habit_frame = tk.Frame(parent, bg=self.theme.bg_color, relief=tk.RIDGE, bd=3)
        habit_frame.pack(pady=10, fill=tk.X)

        habit_label = tk.Label(
            habit_frame,
            text="Habit Tracker",
            font=self.theme.pixel_font,
            bg=self.theme.bg_color,
            fg="#673AB7",  # Purple color for habit tracker
        )
        habit_label.pack(pady=5)

        # Get habit completion statistics for today
        habits = self.data.get("habits", {})
        daily_habits = habits.get("daily_habits", []) + habits.get("custom_habits", [])
        
        # Count active habits
        active_habits = [h for h in daily_habits if h.get("active", True)]
        total_active = len(active_habits)
        
        # Count completed habits for today
        today = datetime.now().date().strftime("%Y-%m-%d")
        completed_today = sum(
            1 for h in active_habits if today in h.get("completed_dates", [])
        )
        
        # Calculate completion percentage
        completion_pct = int((completed_today / total_active) * 100) if total_active > 0 else 0
        
        # Display habit completion status
        status_color = "#4CAF50" if completion_pct >= 80 else "#FFC107" if completion_pct >= 50 else "#F44336"
        
        habit_status_label = tk.Label(
            habit_frame,
            text=f"Today's completion: {completed_today}/{total_active} habits ({completion_pct}%)",
            font=self.theme.small_font,
            bg=self.theme.bg_color,
            fg=status_color,
        )
        habit_status_label.pack(pady=5)

        # Create a simple progress bar
        progress_frame = tk.Frame(habit_frame, bg=self.theme.bg_color)
        progress_frame.pack(fill=tk.X, padx=20, pady=5)
        
        progress_bg = tk.Frame(
            progress_frame,
            bg=self.theme.darken_color(self.theme.primary_color),
            height=10,
        )
        progress_bg.pack(fill=tk.X)
        
        progress_width = int((completion_pct / 100) * progress_bg.winfo_reqwidth())
        progress_bar = tk.Frame(
            progress_bg,
            bg=status_color,
            height=10,
            width=progress_width,
        )
        progress_bar.place(x=0, y=0)

        # Open Habit Tracker button
        habit_button = self.theme.create_pixel_button(
            habit_frame,
            "Open Habit Tracker",
            lambda: self.show_module("habits"),
            color="#673AB7",  # Purple
        )
        habit_button.pack(pady=5)

        # Rewards
        rewards_button = self.theme.create_pixel_button(
            parent, "View Rewards", self.rewards_module.show_rewards, color="#E91E63"
        )
        rewards_button.pack(pady=5)

    def show_module(self, module_name):
        """
        Show the selected module interface.

        Args:
            module_name: Name of the module to show ('art', 'korean', 'french', 'diss', or 'habits')
        """
        self.clear_frame()

        # Map module names to their corresponding modules
        modules = {
            "art": self.art_module,
            "korean": self.korean_module,
            "french": self.french_module,
            "diss": self.diss_module,
            "habits": self.habit_tracker,
        }

        # Display the selected module
        if module_name in modules:
            modules[module_name].show_module(self.main_frame)
