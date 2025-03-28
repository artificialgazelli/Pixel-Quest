"""
Main GUI components for the Pixel Quest application.
"""

import tkinter as tk
from src.theme import PixelTheme
from src.data_manager import DataManager
from src.modules.art_module import ArtModule
from src.modules.korean_module import KoreanModule
from src.modules.french_module import FrenchModule
from src.modules.statistics import StatisticsModule
from src.modules.settings import SettingsModule
from src.modules.rewards import RewardsModule
from src.modules.health import HealthCheckModule

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

        # Show the main menu
        self.show_main_menu()
        
    def initialize_modules(self):
        """Initialize all the application modules."""
        # Module initialization
        self.art_module = ArtModule(self, self.data_manager, self.theme)
        self.korean_module = KoreanModule(self, self.data_manager, self.theme)
        self.french_module = FrenchModule(self, self.data_manager, self.theme)
        self.statistics_module = StatisticsModule(self, self.data_manager, self.theme)
        self.settings_module = SettingsModule(self, self.data_manager, self.theme)
        self.rewards_module = RewardsModule(self, self.data_manager, self.theme)
        self.health_module = HealthCheckModule(self, self.data_manager, self.theme)
        
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
            center_frame, bg=self.theme.bg_color, padx=10, pady=10, relief=tk.RIDGE, bd=3
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
            center_frame, bg=self.theme.bg_color, padx=10, pady=10, relief=tk.RIDGE, bd=3
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
            center_frame, bg=self.theme.bg_color, padx=10, pady=10, relief=tk.RIDGE, bd=3
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

        # Health check
        health_frame = tk.Frame(parent, bg=self.theme.bg_color, relief=tk.RIDGE, bd=3)
        health_frame.pack(pady=10, fill=tk.X)

        health_label = tk.Label(
            health_frame,
            text="Daily Health Check",
            font=self.theme.pixel_font,
            bg=self.theme.bg_color,
            fg=self.theme.text_color,
        )
        health_label.pack(pady=5)

        health_status = (
            "✓ Completed" if self.data["health_status"] else "✗ Not Completed"
        )
        status_color = "#4CAF50" if self.data["health_status"] else "#F44336"
        health_status_label = tk.Label(
            health_frame,
            text=f"Today's status: {health_status}",
            font=self.theme.small_font,
            bg=self.theme.bg_color,
            fg=status_color,
        )
        health_status_label.pack(pady=5)

        health_button = self.theme.create_pixel_button(
            health_frame, "Complete Health Check", self.health_module.do_health_check, color="#673AB7"
        )
        health_button.pack(pady=5)

        # Rewards
        rewards_button = self.theme.create_pixel_button(
            parent, "View Rewards", self.rewards_module.show_rewards, color="#E91E63"
        )
        rewards_button.pack(pady=5)
        
    def show_module(self, module_name):
        """
        Show the selected module interface.
        
        Args:
            module_name: Name of the module to show ('art', 'korean', or 'french')
        """
        self.clear_frame()

        # Map module names to their corresponding modules
        modules = {
            'art': self.art_module,
            'korean': self.korean_module,
            'french': self.french_module
        }
        
        # Display the selected module
        if module_name in modules:
            modules[module_name].show_module(self.main_frame)
