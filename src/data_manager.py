"""
Data management for the Pixel Quest application.
Handles loading, saving, and manipulating game data.
"""

import json
import os
import shutil
from datetime import datetime


class DataManager:
    """
    Manages game data loading, saving, and manipulation.
    """

    def __init__(self, data_file="quest_data.json"):
        """
        Initialize the data manager.

        Args:
            data_file: Path to the data file
        """
        self.data_file = data_file
        self.load_data()

    def load_data(self):
        """
        Load game data from JSON file or initialize if it doesn't exist.

        Returns:
            The loaded data dictionary
        """
        # Default data structure
        default_data = {
            "art": {
                "points": 0,
                "level": 1,
                "streak": 0,
                "last_practice": None,
                "health_status": True,
                "fundamentals_completed": 0,
                "sketchbook_pages": 0,
                "accountability_posts": 0,
                "rewards_unlocked": [],
                "exercises": {
                    "fundamentals": [
                        "Basic Mark Making - Line control exercises",
                        "Shape Accuracy - Drawing basic geometric forms",
                        "Proportion & Measurement techniques",
                        "Contour Drawing - Blind contour exercises",
                        "Texture Development - Various drawing techniques",
                        "Basic Volumes - Drawing 3D forms",
                        "Linear Perspective - One-point perspective",
                        "Linear Perspective - Two-point perspective",
                        "Foreshortening - Drawing objects in space",
                        "Value Scales - Creating value ranges",
                        "Basic Lighting - Core shadow, cast shadow",
                        "Rendering Techniques - Hatching methods",
                        "Rendering Techniques - Blending methods",
                        "Color Wheel - Primary and secondary colors",
                        "Color Mixing - Creating specific colors",
                        "Compositional Structures - Rule of thirds",
                        "Visual Flow - Leading the eye through artwork",
                        "Gesture Drawing - Capturing essence of pose",
                        "Structural Anatomy - Basic figure proportions",
                        "Master Studies - Copying works by artists",
                    ],
                    "sketchbook": [
                        "Free drawing",
                        "Still life",
                        "Landscape sketch",
                        "Character design",
                        "Animal sketches",
                        "Object studies",
                        "Urban sketching",
                        "Nature elements",
                        "Fantasy creatures",
                        "Portrait practice",
                    ],
                    "accountability": [
                        "Progress photo documentation",
                        "Create process video",
                        "Write about learning experience",
                        "Post progress on social media",
                        "Share before/after comparison",
                    ],
                },
            },
            "korean": {
                "points": 0,
                "level": 1,
                "streak": 0,
                "last_practice": None,
                "fundamentals_completed": 0,
                "immersion_hours": 0,
                "application_sessions": 0,
                "rewards_unlocked": [],
                "exercises": {
                    "fundamentals": [
                        "Hangul basics - Consonants",
                        "Hangul basics - Vowels",
                        "Hangul basics - Final consonants",
                        "Hangul syllable structure practice",
                        "Basic greetings and introduction",
                        "Numbers and counting system",
                        "Basic verbs and conjugation",
                        "Basic nouns and particles",
                        "Question formation",
                        "Simple present tense",
                        "Simple past tense",
                        "Simple future tense",
                        "Basic adjectives and descriptors",
                        "Basic sentence structure",
                        "Pronouns and demonstratives",
                        "Time expressions",
                        "Location and direction words",
                        "Basic honorifics",
                        "Family terms vocabulary",
                        "Food and dining vocabulary",
                    ],
                    "immersion": [
                        "Watch K-drama (30 min)",
                        "Listen to K-pop songs",
                        "Watch Korean YouTube videos",
                        "Read Korean webtoons",
                        "Listen to Korean podcast",
                        "Watch Korean news",
                        "Watch Korean variety show",
                        "Listen to Korean audiobook",
                        "Follow Korean social media",
                        "Korean children's books",
                    ],
                    "application": [
                        "Write journal entry in Hangul",
                        "Practice conversation with language partner",
                        "Record yourself speaking Korean",
                        "Translate simple text to Korean",
                        "Label items in your home in Korean",
                        "Order at Korean restaurant in Korean",
                        "Describe your day in Korean",
                        "Write short story in Korean",
                        "Text chat with Korean speaker",
                        "Teach someone basic Korean phrases",
                    ],
                },
            },
            "french": {
                "points": 0,
                "level": 1,
                "streak": 0,
                "last_practice": None,
                "fundamentals_completed": 0,
                "immersion_hours": 0,
                "application_sessions": 0,
                "rewards_unlocked": [],
                "exercises": {
                    "fundamentals": [
                        "Basic pronunciation - vowels",
                        "Basic pronunciation - consonants",
                        "Nasal sounds practice",
                        "Greetings and introductions",
                        "Numbers and counting",
                        "Present tense - regular verbs",
                        "Present tense - irregular verbs",
                        "Articles - definite and indefinite",
                        "Gender and agreement",
                        "Basic adjectives and placement",
                        "Question formation",
                        "Past tense - passé composé",
                        "Past tense - imparfait",
                        "Future tense - simple",
                        "Prepositions of place",
                        "Time expressions",
                        "Daily routine vocabulary",
                        "Food and dining vocabulary",
                        "Travel and directions",
                        "Body parts and health",
                    ],
                    "immersion": [
                        "Watch French film (30 min)",
                        "Listen to French music",
                        "Watch French YouTube videos",
                        "Read French news articles",
                        "Listen to French podcast",
                        "Watch French TV series",
                        "Listen to French radio",
                        "Read French comics/graphic novels",
                        "Follow French social media",
                        "French children's books",
                    ],
                    "application": [
                        "Write journal entry in French",
                        "Practice conversation with language partner",
                        "Record yourself speaking French",
                        "Translate simple text to French",
                        "Describe photos in French",
                        "Order at restaurant in French",
                        "Write shopping list in French",
                        "Text chat with French speaker",
                        "Teach someone basic French phrases",
                    ],
                },
            },
            # Add this to the initial data structure in DataManager.load_data() - after the "french" section and before the "health_status" section
            "diss": {
                "points": 0,
                "level": 1,
                "streak": 0,
                "last_practice": None,
                "tasks": {
                    "preparation": [
                        {
                            "name": "Literature review",
                            "start_date": "27.03.2025",
                            "end_date": "31.08.2025",
                            "total_hours": 100,
                            "hours_worked": 0,
                        },
                        {
                            "name": "Methodology development",
                            "start_date": "15.04.2025",
                            "end_date": "31.07.2025",
                            "total_hours": 80,
                            "hours_worked": 0,
                        },
                        {
                            "name": "Data collection and processing",
                            "start_date": "01.05.2025",
                            "end_date": "31.07.2025",
                            "total_hours": 120,
                            "hours_worked": 0,
                        },
                        {
                            "name": "Writing theoretical chapter",
                            "start_date": "01.06.2025",
                            "end_date": "15.10.2025",
                            "total_hours": 150,
                            "hours_worked": 0,
                        },
                    ],
                    "empirical": [
                        {
                            "name": "Qualitative discourse analysis",
                            "start_date": "01.08.2025",
                            "end_date": "15.01.2026",
                            "total_hours": 200,
                            "hours_worked": 0,
                        },
                        {
                            "name": "Writing results",
                            "start_date": "16.01.2026",
                            "end_date": "31.03.2026",
                            "total_hours": 100,
                            "hours_worked": 0,
                        },
                        {
                            "name": "Topic modeling",
                            "start_date": "16.01.2026",
                            "end_date": "31.05.2026",
                            "total_hours": 150,
                            "hours_worked": 0,
                        },
                        {
                            "name": "Writing results",
                            "start_date": "01.06.2026",
                            "end_date": "31.08.2026",
                            "total_hours": 100,
                            "hours_worked": 0,
                        },
                    ],
                    "integration": [
                        {
                            "name": "Finalizing methodology chapter",
                            "start_date": "01.06.2026",
                            "end_date": "15.09.2026",
                            "total_hours": 80,
                            "hours_worked": 0,
                        },
                        {
                            "name": "Writing discussion and conclusion",
                            "start_date": "01.09.2026",
                            "end_date": "15.01.2027",
                            "total_hours": 120,
                            "hours_worked": 0,
                        },
                        {
                            "name": "Revising introduction",
                            "start_date": "16.01.2027",
                            "end_date": "28.02.2027",
                            "total_hours": 60,
                            "hours_worked": 0,
                        },
                    ],
                    "finalization": [
                        {
                            "name": "Proofreading and revision",
                            "start_date": "01.03.2027",
                            "end_date": "15.06.2027",
                            "total_hours": 100,
                            "hours_worked": 0,
                        },
                        {
                            "name": "Layout and formatting",
                            "start_date": "16.06.2027",
                            "end_date": "15.08.2027",
                            "total_hours": 60,
                            "hours_worked": 0,
                        },
                        {
                            "name": "Corrections and printing",
                            "start_date": "16.08.2027",
                            "end_date": "31.10.2027",
                            "total_hours": 40,
                            "hours_worked": 0,
                        },
                    ],
                },
            },
            # New habit tracking data structure
            "habits": {
                "daily_habits": [
                    {
                        "name": "Early wakeup",
                        "icon": "☀️",
                        "active": True,
                        "frequency": "daily",
                        "streak": 0,
                        "completed_dates": []
                    },
                    {
                        "name": "Exercise",
                        "icon": "🏃",
                        "active": True,
                        "frequency": "daily",
                        "streak": 0,
                        "completed_dates": []
                    },
                    {
                        "name": "Reading",
                        "icon": "📚",
                        "active": True,
                        "frequency": "daily",
                        "streak": 0,
                        "completed_dates": []
                    },
                    {
                        "name": "Meditation",
                        "icon": "🧘",
                        "active": True,
                        "frequency": "daily", 
                        "streak": 0,
                        "completed_dates": []
                    },
                    {
                        "name": "Drink water",
                        "icon": "💧",
                        "active": True,
                        "frequency": "daily",
                        "streak": 0,
                        "completed_dates": []
                    }
                ],
                "custom_habits": [],
                "check_ins": [
                    {
                        "name": "Doctor Appointments",
                        "icon": "🩺",
                        "dates": [],
                        "notes": {}
                    },
                    {
                        "name": "Dentist",
                        "icon": "🦷",
                        "dates": [],
                        "notes": {}
                    }
                ]
            },
            "health_status": True,
            "last_health_check": None,
            "rewards": {
                "small": [
                    "New art supplies (pencils, pens)",
                    "Korean snacks package",
                    "French pastry treat",
                    "Download a new playlist",
                    "Movie night",
                    "Special coffee or tea",
                    "New stickers for journal",
                    "Bath bomb or relaxation item",
                    "Small plant or succulent",
                    "Art print or bookmark",
                ],
                "medium": [
                    "Art instruction book",
                    "Korean webtoon collection",
                    "French film collection",
                    "Nice sketchbook or journal",
                    "Language learning app subscription (1 month)",
                    "Art supply set (markers, paints)",
                    "Korean or French cuisine cookbook",
                    "Online class or workshop",
                    "Streaming service subscription (1 month)",
                    "Museum or gallery admission",
                ],
                "large": [
                    "Premium art course",
                    "TOPIK prep materials full set",
                    "Trip to a French cafe or restaurant",
                    "Art software or digital tools",
                    "Language tutoring session",
                    "Premium art supplies kit",
                    "Cultural experience or event ticket",
                    "Annual subscription to learning platform",
                    "Weekend creative retreat",
                    "Professional drawing tablet",
                ],
            },
        }

        if os.path.exists(self.data_file):
            with open(self.data_file, "r") as f:
                self.data = json.load(f)
                
                # Check for missing modules and add them if needed
                data_updated = False
                
                # Check for diss module
                if "diss" not in self.data:
                    self.data["diss"] = default_data["diss"]
                    data_updated = True
                
                # Check for habits module
                if "habits" not in self.data:
                    self.data["habits"] = default_data["habits"]
                    data_updated = True
                    
                # You can add checks for other modules here if needed
                
                # Save if any updates were made
                if data_updated:
                    self.save_data()
        else:
            # Initialize default data structure
            self.data = default_data
            self.save_data()

        return self.data

    def save_data(self):
        """Save game data to JSON file."""
        with open(self.data_file, "w") as f:
            json.dump(self.data, f, indent=4)

    def backup_data(self):
        """
        Create a backup of the current data.

        Returns:
            The path to the backup file
        """
        # Create backup filename with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_file = f"quest_data_backup_{timestamp}.json"

        try:
            shutil.copy2(self.data_file, backup_file)
            return backup_file
        except Exception as e:
            raise Exception(f"Failed to create backup: {str(e)}")

    def restore_from_backup(self, backup_file):
        """
        Restore data from a backup file.

        Args:
            backup_file: Path to the backup file

        Returns:
            True if successful, False otherwise
        """
        try:
            # Load backup data to verify it's valid
            with open(backup_file, "r") as f:
                backup_data = json.load(f)

            # Verify it has the expected structure
            if not all(key in backup_data for key in ["art", "korean", "french"]):
                return False

            # Copy backup to the data file
            shutil.copy2(backup_file, self.data_file)

            # Reload data
            self.load_data()
            return True

        except Exception:
            return False

    def export_data(self, filename=None):
        """
        Export statistics and logs to a file.

        Args:
            filename: Custom filename for export (optional)

        Returns:
            The path to the exported file
        """
        # Create export filename with timestamp
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"quest_data_export_{timestamp}.json"

        try:
            with open(filename, "w") as f:
                json.dump(self.data, f, indent=4)
            return filename
        except Exception as e:
            raise Exception(f"Failed to export data: {str(e)}")

    def reset_data(self):
        """
        Reset all data to default values.

        Returns:
            True if successful
        """
        # Delete the data file if it exists
        if os.path.exists(self.data_file):
            os.remove(self.data_file)

        # Reinitialize data
        self.load_data()
        return True
