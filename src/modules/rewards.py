"""
Rewards module for the Pixel Quest application.
Handles rewards functionality, claiming, and management.
"""

import tkinter as tk
from tkinter import ttk, messagebox
import random
from datetime import datetime

class RewardsModule:
    """
    Manages the rewards functionality.
    """
    
    def __init__(self, app, data_manager, theme):
        """
        Initialize the rewards module.
        
        Args:
            app: Main application instance
            data_manager: Data manager instance
            theme: Theme manager instance
        """
        self.app = app
        self.data_manager = data_manager
        self.data = data_manager.data
        self.theme = theme
        
    def show_rewards(self):
        """Show rewards window with management options and pixel art styling."""
        rewards_window = tk.Toplevel(self.app.root)
        rewards_window.title("Quest Rewards")
        rewards_window.geometry("800x600")
        rewards_window.configure(bg=self.theme.bg_color)

        # Center the window
        rewards_window.transient(self.app.root)
        rewards_window.grab_set()

        # Create a notebook with tabs
        notebook = ttk.Notebook(rewards_window)
        notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Create tabs
        view_tab = tk.Frame(notebook, bg=self.theme.bg_color)
        manage_tab = tk.Frame(notebook, bg=self.theme.bg_color)
        history_tab = tk.Frame(notebook, bg=self.theme.bg_color)

        notebook.add(view_tab, text="View Rewards")
        notebook.add(manage_tab, text="Manage Rewards")
        notebook.add(history_tab, text="Reward History")

        # ----------------------------------------
        # TAB 1: VIEW REWARDS
        # ----------------------------------------
        tk.Label(
            view_tab,
            text="Your Quest Rewards",
            font=self.theme.pixel_font,
            bg=self.theme.bg_color,
            fg=self.theme.text_color,
        ).pack(pady=10)

        # Total points across all quests
        total_points = (
            self.data["art"]["points"]
            + self.data["korean"]["points"]
            + self.data["french"]["points"]
        )
        tk.Label(
            view_tab,
            text=f"Total Points: {total_points}",
            font=self.theme.pixel_font,
            bg=self.theme.bg_color,
            fg=self.theme.text_color,
        ).pack(pady=5)

        # Create a canvas with scrollbar
        canvas_frame = tk.Frame(view_tab, bg=self.theme.bg_color)
        canvas_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Create scrollable rewards list
        self.create_rewards_list(view_tab)

        # Claim reward button with pixel styling
        button_frame = tk.Frame(view_tab, bg=self.theme.bg_color)
        button_frame.pack(pady=10)

        if total_points >= 50:
            claim_button = self.theme.create_pixel_button(
                button_frame,
                "Claim a Reward",
                lambda: self.claim_reward(rewards_window),
                color="#E91E63",
            )
            claim_button.pack(side="left", padx=10)
        else:
            tk.Label(
                button_frame,
                text="Earn at least 50 points to claim rewards",
                font=self.theme.small_font,
                bg=self.theme.bg_color,
                fg=self.theme.text_color,
            ).pack(side="left", padx=10)

        # ----------------------------------------
        # TAB 2: MANAGE REWARDS
        # ----------------------------------------
        self.create_manage_rewards_tab(manage_tab)

        # ----------------------------------------
        # TAB 3: REWARD HISTORY
        # ----------------------------------------
        self.create_reward_history_tab(history_tab)
        
    def create_rewards_list(self, parent):
        """
        Create a scrollable list of rewards with pixel art styling.
        
        Args:
            parent: Parent widget for the rewards list
        """
        # Small rewards (50 points)
        small_frame = tk.LabelFrame(
            parent,
            text="Small Rewards (50 points)",
            font=self.theme.pixel_font,
            bg=self.theme.bg_color,
            fg=self.theme.text_color,
            padx=10,
            pady=10,
            relief=tk.RIDGE,
            bd=3,
        )
        small_frame.pack(fill=tk.X, expand=True, pady=5, padx=10)

        for i, reward in enumerate(self.data["rewards"]["small"]):
            reward_frame = tk.Frame(small_frame, bg=self.theme.bg_color)
            reward_frame.pack(anchor="w", pady=2)

            # Create a pixel art bullet point
            bullet = tk.Label(
                reward_frame,
                text="■",
                font=self.theme.small_font,
                bg=self.theme.bg_color,
                fg=self.theme.primary_color,
            )
            bullet.pack(side=tk.LEFT, padx=5)

            # Reward text
            text = tk.Label(
                reward_frame,
                text=reward,
                font=self.theme.small_font,
                bg=self.theme.bg_color,
                fg=self.theme.text_color,
            )
            text.pack(side=tk.LEFT)

        # Medium rewards (200 points)
        medium_frame = tk.LabelFrame(
            parent,
            text="Medium Rewards (200 points)",
            font=self.theme.pixel_font,
            bg=self.theme.bg_color,
            fg=self.theme.text_color,
            padx=10,
            pady=10,
            relief=tk.RIDGE,
            bd=3,
        )
        medium_frame.pack(fill=tk.X, expand=True, pady=5, padx=10)

        for i, reward in enumerate(self.data["rewards"]["medium"]):
            reward_frame = tk.Frame(medium_frame, bg=self.theme.bg_color)
            reward_frame.pack(anchor="w", pady=2)

            # Create a pixel art bullet point
            bullet = tk.Label(
                reward_frame,
                text="■",
                font=self.theme.small_font,
                bg=self.theme.bg_color,
                fg=self.theme.secondary_color,
            )
            bullet.pack(side=tk.LEFT, padx=5)

            # Reward text
            text = tk.Label(
                reward_frame,
                text=reward,
                font=self.theme.small_font,
                bg=self.theme.bg_color,
                fg=self.theme.text_color,
            )
            text.pack(side=tk.LEFT)

        # Large rewards (500 points)
        large_frame = tk.LabelFrame(
            parent,
            text="Large Rewards (500 points)",
            font=self.theme.pixel_font,
            bg=self.theme.bg_color,
            fg=self.theme.text_color,
            padx=10,
            pady=10,
            relief=tk.RIDGE,
            bd=3,
        )
        large_frame.pack(fill=tk.X, expand=True, pady=5, padx=10)

        for i, reward in enumerate(self.data["rewards"]["large"]):
            reward_frame = tk.Frame(large_frame, bg=self.theme.bg_color)
            reward_frame.pack(anchor="w", pady=2)

            # Create a pixel art bullet point
            bullet = tk.Label(
                reward_frame,
                text="■",
                font=self.theme.small_font,
                bg=self.theme.bg_color,
                fg="#E91E63",
            )
            bullet.pack(side=tk.LEFT, padx=5)

            # Reward text
            text = tk.Label(
                reward_frame,
                text=reward,
                font=self.theme.small_font,
                bg=self.theme.bg_color,
                fg=self.theme.text_color,
            )
            text.pack(side=tk.LEFT)
            
    def create_manage_rewards_tab(self, parent):
        """
        Create the reward management tab with functionality to add, edit, and delete rewards.
        
        Args:
            parent: Parent widget for the reward management tab
        """
        # Title
        tk.Label(
            parent,
            text="Manage Your Rewards",
            font=self.theme.pixel_font,
            bg=self.theme.bg_color,
            fg=self.theme.text_color,
        ).pack(pady=10)

        # Create notebook with tabs for each tier
        tier_notebook = ttk.Notebook(parent)
        tier_notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Create tabs for each reward tier
        small_tab = tk.Frame(tier_notebook, bg=self.theme.bg_color)
        medium_tab = tk.Frame(tier_notebook, bg=self.theme.bg_color)
        large_tab = tk.Frame(tier_notebook, bg=self.theme.bg_color)

        tier_notebook.add(small_tab, text="Small Rewards")
        tier_notebook.add(medium_tab, text="Medium Rewards")
        tier_notebook.add(large_tab, text="Large Rewards")

        # Populate each tab
        self.create_reward_management_list(small_tab, "small")
        self.create_reward_management_list(medium_tab, "medium")
        self.create_reward_management_list(large_tab, "large")
        
    def create_reward_management_list(self, parent, tier):
        """
        Create a list of rewards with edit/delete buttons for a specific tier.
        
        Args:
            parent: Parent widget for the reward management list
            tier: Reward tier ('small', 'medium', or 'large')
        """
        # Container frame
        container_frame = tk.Frame(parent, bg=self.theme.bg_color)
        container_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Scrollable frame for the reward list
        canvas = tk.Canvas(container_frame, bg=self.theme.bg_color, highlightthickness=0)
        scrollbar = ttk.Scrollbar(
            container_frame, orient="vertical", command=canvas.yview
        )
        scrollable_frame = tk.Frame(canvas, bg=self.theme.bg_color)

        scrollable_frame.bind(
            "<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Tier title with cost
        costs = {"small": 50, "medium": 200, "large": 500}
        tier_title = tk.Label(
            scrollable_frame,
            text=f"{tier.capitalize()} Rewards ({costs[tier]} points)",
            font=self.theme.pixel_font,
            bg=self.theme.bg_color,
            fg=self.theme.text_color,
        )
        tier_title.grid(row=0, column=0, columnspan=3, sticky="w", pady=10)

        # Reward list with edit/delete buttons
        for i, reward in enumerate(self.data["rewards"][tier]):
            # Reward text
            tk.Label(
                scrollable_frame,
                text=reward,
                font=self.theme.small_font,
                bg=self.theme.bg_color,
                fg=self.theme.text_color,
                wraplength=300,
                justify="left",
            ).grid(row=i + 1, column=0, sticky="w", pady=5, padx=5)

            # Edit button
            edit_button = self.theme.create_pixel_button(
                scrollable_frame,
                "Edit",
                lambda r=reward, t=tier: self.edit_reward(r, t),
                color=self.theme.accent_color,
                width=6,
            )
            edit_button.grid(row=i + 1, column=1, padx=5, pady=5)

            # Delete button
            delete_button = self.theme.create_pixel_button(
                scrollable_frame,
                "Delete",
                lambda r=reward, t=tier: self.delete_reward(r, t),
                color="#F44336",
                width=6,
            )
            delete_button.grid(row=i + 1, column=2, padx=5, pady=5)

        # Add new reward section
        add_frame = tk.LabelFrame(
            scrollable_frame,
            text="Add New Reward",
            font=self.theme.pixel_font,
            bg=self.theme.bg_color,
            fg=self.theme.text_color,
            padx=10,
            pady=10,
        )
        add_frame.grid(
            row=len(self.data["rewards"][tier]) + 1,
            column=0,
            columnspan=3,
            sticky="ew",
            pady=10,
        )

        # Entry for new reward
        entry_frame = tk.Frame(add_frame, bg=self.theme.bg_color)
        entry_frame.pack(fill=tk.X, pady=5)

        tk.Label(
            entry_frame,
            text="Reward Description:",
            font=self.theme.small_font,
            bg=self.theme.bg_color,
            fg=self.theme.text_color,
        ).pack(side=tk.LEFT, padx=5)

        new_reward_entry = tk.Entry(
            entry_frame,
            width=40,
            font=self.theme.small_font,
            bg=self.theme.primary_color,
            fg=self.theme.text_color,
        )
        new_reward_entry.pack(side=tk.LEFT, padx=5)

        # Add button
        add_button = self.theme.create_pixel_button(
            add_frame,
            "Add Reward",
            lambda e=new_reward_entry, t=tier: self.add_reward(e, t),
            color="#4CAF50",
        )
        add_button.pack(pady=10)
        
    def create_reward_history_tab(self, parent):
        """
        Create the reward history tab to display claimed rewards.
        
        Args:
            parent: Parent widget for the reward history tab
        """
        # Title
        tk.Label(
            parent,
            text="Your Claimed Rewards History",
            font=self.theme.pixel_font,
            bg=self.theme.bg_color,
            fg=self.theme.text_color,
        ).pack(pady=10)

        # Check if there are any claimed rewards
        if "unlocked_rewards" not in self.data or not self.data.get("unlocked_rewards"):
            # No history yet
            tk.Label(
                parent,
                text="You haven't claimed any rewards yet.",
                font=self.theme.small_font,
                bg=self.theme.bg_color,
                fg=self.theme.text_color,
            ).pack(pady=50)
            return

        # Container frame with scrollbar
        container_frame = tk.Frame(parent, bg=self.theme.bg_color)
        container_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        canvas = tk.Canvas(container_frame, bg=self.theme.bg_color, highlightthickness=0)
        scrollbar = ttk.Scrollbar(
            container_frame, orient="vertical", command=canvas.yview
        )
        scrollable_frame = tk.Frame(canvas, bg=self.theme.bg_color)

        scrollable_frame.bind(
            "<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Column headers
        header_frame = tk.Frame(scrollable_frame, bg=self.theme.bg_color)
        header_frame.grid(row=0, column=0, sticky="ew", pady=5)

        tk.Label(
            header_frame,
            text="Date Claimed",
            font=self.theme.pixel_font,
            bg=self.theme.bg_color,
            fg=self.theme.text_color,
        ).grid(row=0, column=0, padx=10, sticky="w")

        tk.Label(
            header_frame,
            text="Tier",
            font=self.theme.pixel_font,
            bg=self.theme.bg_color,
            fg=self.theme.text_color,
        ).grid(row=0, column=1, padx=10, sticky="w")

        tk.Label(
            header_frame,
            text="Reward",
            font=self.theme.pixel_font,
            bg=self.theme.bg_color,
            fg=self.theme.text_color,
        ).grid(row=0, column=2, padx=10, sticky="w")

        # Separator line
        separator = tk.Frame(scrollable_frame, height=2, bg=self.theme.text_color)
        separator.grid(row=1, column=0, sticky="ew", pady=5, columnspan=3)

        # Sort claimed rewards by date (newest first)
        sorted_rewards = sorted(
            self.data["unlocked_rewards"], key=lambda x: x["date"], reverse=True
        )

        # Display each claimed reward
        for i, claimed in enumerate(sorted_rewards):
            row_frame = tk.Frame(scrollable_frame, bg=self.theme.bg_color)
            row_frame.grid(row=i + 2, column=0, sticky="ew", pady=5)

            # Add highlighting for alternating rows
            if i % 2 == 0:
                row_bg = self.theme.bg_color
            else:
                row_bg = self.theme.darken_color(self.theme.bg_color)

            # Date
            date_label = tk.Label(
                row_frame,
                text=claimed["date"],
                font=self.theme.small_font,
                bg=row_bg,
                fg=self.theme.text_color,
                width=15,
                anchor="w",
            )
            date_label.grid(row=0, column=0, padx=10, sticky="w")

            # Tier with color coding
            tier_colors = {
                "small": self.theme.primary_color,
                "medium": self.theme.secondary_color,
                "large": "#E91E63",
            }

            tier_label = tk.Label(
                row_frame,
                text=claimed["tier"].capitalize(),
                font=self.theme.small_font,
                bg=row_bg,
                fg=tier_colors.get(claimed["tier"], self.theme.text_color),
                width=10,
                anchor="w",
            )
            tier_label.grid(row=0, column=1, padx=10, sticky="w")

            # Reward description
            reward_label = tk.Label(
                row_frame,
                text=claimed["reward"],
                font=self.theme.small_font,
                bg=row_bg,
                fg=self.theme.text_color,
                wraplength=300,
                justify="left",
                anchor="w",
            )
            reward_label.grid(row=0, column=2, padx=10, sticky="w")
            
    def add_reward(self, entry_widget, tier):
        """
        Add a new reward to a specific tier.
        
        Args:
            entry_widget: Entry widget containing the reward text
            tier: Reward tier ('small', 'medium', or 'large')
        """
        reward_text = entry_widget.get().strip()

        if not reward_text:
            messagebox.showwarning("Empty Reward", "Please enter a reward description.")
            return

        # Add to data if it doesn't already exist
        if reward_text not in self.data["rewards"][tier]:
            self.data["rewards"][tier].append(reward_text)
            self.data_manager.save_data()
            messagebox.showinfo(
                "Reward Added",
                f"Added new {tier} reward: {reward_text}",
            )

            # Clear entry field
            entry_widget.delete(0, tk.END)

            # Refresh the reward management tab
            self.show_rewards()
        else:
            messagebox.showinfo(
                "Already Exists",
                f"This reward already exists in your {tier} rewards list.",
            )
            
    def edit_reward(self, reward, tier):
        """
        Edit an existing reward.
        
        Args:
            reward: Current reward text
            tier: Reward tier ('small', 'medium', or 'large')
        """
        # Create a dialog window
        dialog = tk.Toplevel(self.app.root)
        dialog.title(f"Edit {tier.capitalize()} Reward")
        dialog.geometry("500x150")
        dialog.configure(bg=self.theme.bg_color)
        dialog.transient(self.app.root)
        dialog.grab_set()

        # Label and entry for editing reward
        tk.Label(
            dialog,
            text="Edit reward description:",
            font=self.theme.pixel_font,
            bg=self.theme.bg_color,
            fg=self.theme.text_color,
        ).pack(pady=10)

        entry = tk.Entry(
            dialog,
            width=50,
            font=self.theme.small_font,
            bg=self.theme.primary_color,
            fg=self.theme.text_color,
        )
        entry.insert(0, reward)
        entry.pack(pady=10, padx=20)
        entry.focus_set()

        # Button frame
        button_frame = tk.Frame(dialog, bg=self.theme.bg_color)
        button_frame.pack(pady=10)

        # Save button
        save_button = self.theme.create_pixel_button(
            button_frame,
            "Save Changes",
            lambda: self.save_edited_reward(dialog, reward, entry.get(), tier),
            color="#4CAF50",
        )
        save_button.pack(side=tk.LEFT, padx=10)

        # Cancel button
        cancel_button = self.theme.create_pixel_button(
            button_frame, "Cancel", dialog.destroy, color="#9E9E9E"
        )
        cancel_button.pack(side=tk.LEFT, padx=10)
        
    def save_edited_reward(self, dialog, old_reward, new_reward, tier):
        """
        Save the edited reward.
        
        Args:
            dialog: Dialog window to close after saving
            old_reward: Original reward text
            new_reward: New reward text
            tier: Reward tier ('small', 'medium', or 'large')
        """
        if not new_reward.strip():
            messagebox.showwarning("Empty Reward", "Please enter a reward description.")
            return

        if new_reward != old_reward:
            # Update the reward in the data
            index = self.data["rewards"][tier].index(old_reward)
            self.data["rewards"][tier][index] = new_reward

            # Also update any claimed rewards with this description
            if "unlocked_rewards" in self.data:
                for claimed in self.data["unlocked_rewards"]:
                    if claimed["reward"] == old_reward and claimed["tier"] == tier:
                        claimed["reward"] = new_reward

            self.data_manager.save_data()
            messagebox.showinfo(
                "Reward Updated",
                f"Updated {tier} reward successfully!",
            )

            # Close dialog
            dialog.destroy()

            # Refresh the rewards display
            self.show_rewards()
        else:
            # No changes made
            dialog.destroy()
            
    def delete_reward(self, reward, tier):
        """
        Delete an existing reward.
        
        Args:
            reward: Reward text to delete
            tier: Reward tier ('small', 'medium', or 'large')
        """
        # Confirm deletion
        if messagebox.askyesno(
            "Confirm Delete",
            f"Are you sure you want to delete the {tier} reward: '{reward}'?",
        ):
            # Remove from data
            self.data["rewards"][tier].remove(reward)
            self.data_manager.save_data()
            messagebox.showinfo(
                "Reward Deleted",
                f"Deleted {tier} reward: {reward}",
            )

            # Refresh the rewards display
            self.show_rewards()
            
    def claim_reward(self, window):
        """
        Process reward claim with pixel art styling.
        
        Args:
            window: Parent window for the claim dialog
        """
        total_points = (
            self.data["art"]["points"]
            + self.data["korean"]["points"]
            + self.data["french"]["points"]
        )

        # Determine available reward tiers
        available_tiers = []
        if total_points >= 50:
            available_tiers.append("small")
        if total_points >= 200:
            available_tiers.append("medium")
        if total_points >= 500:
            available_tiers.append("large")

        # Create reward claim window
        claim_window = tk.Toplevel(window)
        claim_window.title("Claim Reward")
        claim_window.geometry("400x300")
        claim_window.configure(bg=self.theme.bg_color)

        # Center the window
        claim_window.transient(window)
        claim_window.grab_set()

        tk.Label(
            claim_window,
            text="Claim Your Reward",
            font=self.theme.pixel_font,
            bg=self.theme.bg_color,
            fg=self.theme.text_color,
        ).pack(pady=10)

        # Select tier
        tier_frame = tk.Frame(claim_window, bg=self.theme.bg_color, relief=tk.RIDGE, bd=3)
        tier_frame.pack(pady=10, fill=tk.X, padx=20)

        tk.Label(
            tier_frame,
            text="Select reward tier:",
            font=self.theme.small_font,
            bg=self.theme.bg_color,
            fg=self.theme.text_color,
        ).pack(pady=5)

        selected_tier = tk.StringVar(value=available_tiers[0])

        # Create radio buttons with pixel art styling
        for tier in available_tiers:
            tier_name = {
                "small": "Small (50 points)",
                "medium": "Medium (200 points)",
                "large": "Large (500 points)",
            }

            radio_frame = tk.Frame(tier_frame, bg=self.theme.bg_color)
            radio_frame.pack(anchor="w", pady=2)

            radio = tk.Radiobutton(
                radio_frame,
                text=tier_name[tier],
                variable=selected_tier,
                value=tier,
                bg=self.theme.bg_color,
                fg=self.theme.text_color,
                font=self.theme.small_font,
                selectcolor=self.theme.secondary_color,
            )
            radio.pack(anchor="w")

        # Submit button
        submit_button = self.theme.create_pixel_button(
            claim_window,
            "Claim Reward",
            lambda: self.process_reward_claim(claim_window, selected_tier.get()),
            color="#E91E63",
        )
        submit_button.pack(pady=20)
        
    def process_reward_claim(self, window, tier):
        """
        Process reward claim.
        
        Args:
            window: Dialog window to close after processing
            tier: Selected reward tier ('small', 'medium', or 'large')
        """
        # Point costs
        costs = {"small": 50, "medium": 200, "large": 500}

        # Get a random reward from the selected tier
        reward = random.choice(self.data["rewards"][tier])

        # Deduct points (for now, just deduct from art)
        total_points = (
            self.data["art"]["points"]
            + self.data["korean"]["points"]
            + self.data["french"]["points"]
        )
        cost = costs[tier]

        # Distribute the cost proportionally across all three areas
        art_ratio = (
            self.data["art"]["points"] / total_points if total_points > 0 else 0.33
        )
        korean_ratio = (
            self.data["korean"]["points"] / total_points if total_points > 0 else 0.33
        )
        french_ratio = (
            self.data["french"]["points"] / total_points if total_points > 0 else 0.34
        )

        art_deduction = int(cost * art_ratio)
        korean_deduction = int(cost * korean_ratio)
        french_deduction = cost - art_deduction - korean_deduction

        self.data["art"]["points"] -= art_deduction
        self.data["korean"]["points"] -= korean_deduction
        self.data["french"]["points"] -= french_deduction

        # Add to unlocked rewards
        if "unlocked_rewards" not in self.data:
            self.data["unlocked_rewards"] = []

        self.data["unlocked_rewards"].append(
            {
                "tier": tier,
                "reward": reward,
                "date": datetime.now().strftime("%Y-%m-%d"),
            }
        )

        # Show confirmation
        messagebox.showinfo(
            "Reward Claimed",
            f"Congratulations! You have claimed: {reward}\n\nRemember to actually get this reward for yourself!",
        )

        # Save data and refresh
        self.data_manager.save_data()
        window.destroy()
        self.app.show_main_menu()
