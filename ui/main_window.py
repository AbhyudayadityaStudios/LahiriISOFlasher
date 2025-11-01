import customtkinter as ctk
import tkinter as tk
from tkinter import filedialog, messagebox
import threading
import os
import tempfile
import shutil
import sys
from pathlib import Path
from PIL import Image

from core.iso_handler import ISOHandler
from core.usb_handler import USBHandler
from core.flasher import ISOFlasher
from ui.about_window import AboutWindow

class MainWindow(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Configure window
        self.title("Lahiri ISO Flasher")
        self.geometry("800x750")
        self.wm_iconbitmap("res/icon.ico")

        # Set monospace font for entire application
        self.default_font = ctk.CTkFont(family="Courier New", size=12)

        # Theme state
        self.current_theme = "dark"  # default theme

        # Dark theme colors
        self.dark_theme = {
            "primary_color": "#a9e43a",
            "hover_color": "#01c45b",
            "bg_color": "#1a1a1a",
            "card_color": "#2b2b2b",
            "disabled_color": "#404040",
            "text_color": "white"
        }

        # Light theme colors
        self.light_theme = {
            "primary_color": "#01c45b",
            "hover_color": "#a9e43a",
            "bg_color": "#ffffff",
            "card_color": "#f0f0f0",
            "disabled_color": "#d0d0d0",
            "text_color": "black"
        }

        # Set current colors based on theme
        self.primary_color = self.dark_theme["primary_color"]
        self.hover_color = self.dark_theme["hover_color"]
        self.bg_color = self.dark_theme["bg_color"]
        self.card_color = self.dark_theme["card_color"]
        self.disabled_color = self.dark_theme["disabled_color"]
        self.text_color = self.dark_theme["text_color"]
        
        # Initialize handlers
        self.iso_handler = ISOHandler()
        self.usb_handler = USBHandler()
        self.flasher = ISOFlasher()
        
        # Application state
        self.selected_drive = None
        self.selected_iso = None
        self.boot_method = "ISO Image (Please Select)"  # Boot method selection
        self.volume_name = ""
        self.partition_scheme = "MBR"
        self.file_system = "FAT32"
        self.original_drive_letter = None  # Store original drive letter
        
        # Layer completion status
        self.layer_completed = {
            1: False,  # Drive selection
            2: False,  # Boot method selection
            3: False,  # Configuration
            4: False   # Flash
        }
        
        self.setup_menu()
        self.setup_scrollable_ui()
        self.refresh_drives()
        self.update_layer_states()
        
    def get_resource_path(self, relative_path):
        # Get absolute path to resource, works for dev and for PyInstaller
        try:
            # PyInstaller creates a temp folder and stores path in _MEIPASS
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")

        return os.path.join(base_path, relative_path)

    def setup_menu(self):
        # Setup menu bar
        self.menubar = tk.Menu(self)
        self.config(menu=self.menubar)

        # Theme selection
        self.theme_menu = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="Theme", menu=self.theme_menu)

        self.theme_var = tk.StringVar(value="dark")
        self.theme_menu.add_radiobutton(
            label="Dark Theme",
            variable=self.theme_var,
            value="dark",
            command=lambda: self.switch_theme("dark")
        )
        self.theme_menu.add_radiobutton(
            label="Light Theme",
            variable=self.theme_var,
            value="light",
            command=lambda: self.switch_theme("light")
        )

        # GitHub link
        self.menubar.add_command(label="GitHub", command=self.open_github)

        # Sponsor link
        self.menubar.add_command(label="Sponsor", command=self.open_support)

        # About window
        self.menubar.add_command(label="About", command=self.open_about)

    def switch_theme(self, theme):
        # Switch between light and dark themes
        self.current_theme = theme

        if theme == "dark":
            colors = self.dark_theme
            ctk.set_appearance_mode("dark")
        else:
            colors = self.light_theme
            ctk.set_appearance_mode("light")

        # Update colors
        self.primary_color = colors["primary_color"]
        self.hover_color = colors["hover_color"]
        self.bg_color = colors["bg_color"]
        self.card_color = colors["card_color"]
        self.disabled_color = colors["disabled_color"]
        self.text_color = colors["text_color"]

        # Recreate UI with new colors
        self.scrollable_main_frame.destroy()
        self.outer_frame.destroy()
        self.setup_scrollable_ui()
        self.refresh_drives()
        self.update_layer_states()

    def open_github(self):
        # Open GitHub Link
        try:
            os.startfile("https://github.com/MYTAditya")
        except Exception as e:
            messagebox.showerror("Error", f"Could not open GitHub link: {str(e)}")

    def open_support(self):
        # Open Sponsor Link
        try:
            os.startfile("https://ko-fi.com/MYTAditya")
        except Exception as e:
            messagebox.showerror("Error", f"Could not open sponsor link: {str(e)}")

    def open_about(self):
        # Open About Window
        try:
            parent = getattr(self, 'root', None) or getattr(self, 'master', None) or self
            AboutWindow(parent) 
        except Exception as e:
            messagebox.showerror("Error", f"Could not open about window: {str(e)}")
        
    def setup_scrollable_ui(self):
        # Outer main container (header + scrollable rest)
        self.outer_frame = ctk.CTkFrame(self, fg_color=self.bg_color)
        self.outer_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Header with icon and title (fixed)
        self.setup_header(self.outer_frame)

        # Scrollable area for the rest of the UI
        self.scrollable_main_frame = ctk.CTkScrollableFrame(self.outer_frame, fg_color=self.bg_color, scrollbar_button_color=self.primary_color, scrollbar_button_hover_color=self.hover_color)
        self.scrollable_main_frame.pack(fill="both", expand=True, pady=(10, 0))

        # All other content goes inside scrollable_main_frame
        self.setup_drive_selection(self.scrollable_main_frame)
        self.setup_boot_method(self.scrollable_main_frame)
        self.setup_configuration(self.scrollable_main_frame)
        self.setup_flash_section(self.scrollable_main_frame)
        self.setup_progress_section(self.scrollable_main_frame)
        
    def setup_header(self, parent=None):
        # Header frame
        header_frame = ctk.CTkFrame(parent if parent is not None else self.outer_frame, fg_color="transparent")
        header_frame.pack(fill="x", pady=(0, 30))
        
        # Get the correct path for the icon
        icon_path = self.get_resource_path("ui/icon.png")
            
        # Load and resize the icon
        icon_image = Image.open(icon_path)
        icon_image = icon_image.resize((100, 100), Image.Resampling.LANCZOS)
        self.icon_photo = ctk.CTkImage(light_image=icon_image, dark_image=icon_image, size=(100, 100))
                
        # Icon label
        icon_label = ctk.CTkLabel(
            header_frame,
            image=self.icon_photo,
            text=""
            )
        icon_label.pack(side="left", padx=(0, 15))
        
        # Title
        title_label = ctk.CTkLabel(
            header_frame,
            text="Lahiri ISO Flasher",
            font=ctk.CTkFont(family="Courier New", size=32, weight="bold"),
            text_color=self.primary_color
        )
        title_label.pack(side="left")
        
    def setup_drive_selection(self, parent):
        # Drive selection frame
        self.drive_frame = ctk.CTkFrame(parent, fg_color=self.card_color)
        self.drive_frame.pack(fill="x", pady=(0, 15))
        
        # Title with status indicator
        title_container = ctk.CTkFrame(self.drive_frame, fg_color="transparent")
        title_container.pack(fill="x", padx=20, pady=(15, 10))
        
        self.drive_title = ctk.CTkLabel(
            title_container,
            text="Select USB Drive",
            font=ctk.CTkFont(family="Courier New", size=18, weight="bold"),
            text_color=self.primary_color
        )
        self.drive_title.pack(side="left")
        
        self.drive_status = ctk.CTkLabel(
            title_container,
            text="⚪ Incomplete",
            font=ctk.CTkFont(family="Courier New", size=14),
            text_color="gray"
        )
        self.drive_status.pack(side="right")
        
        # Drive selection container
        drive_container = ctk.CTkFrame(self.drive_frame, fg_color="transparent")
        drive_container.pack(fill="x", padx=20, pady=(0, 15))
        
        # Drive dropdown
        self.drive_var = ctk.StringVar(value="Select a USB drive...")
        self.drive_dropdown = ctk.CTkComboBox(
            drive_container,
            variable=self.drive_var,
            values=["No drives found"],
            width=400,
            command=self.on_drive_selected,
            font=ctk.CTkFont(family="Courier New")
        )
        self.drive_dropdown.pack(side="left", padx=(0, 10))
        
        # Refresh button
        self.refresh_btn = ctk.CTkButton(
            drive_container,
            text="Refresh",
            width=100,
            command=self.refresh_drives,
            fg_color=self.primary_color,
            hover_color=self.hover_color,
            text_color="black",
            font=ctk.CTkFont(family="Courier New")
        )
        self.refresh_btn.pack(side="left")
        
    def setup_boot_method(self, parent):
        # Boot method frame
        self.boot_method_frame = ctk.CTkFrame(parent, fg_color=self.disabled_color)
        self.boot_method_frame.pack(fill="x", pady=(0, 15))

        # Title with status indicator
        title_container = ctk.CTkFrame(self.boot_method_frame, fg_color="transparent")
        title_container.pack(fill="x", padx=20, pady=(15, 10))

        self.boot_method_title = ctk.CTkLabel(
            title_container,
            text="Select Boot Method",
            font=ctk.CTkFont(family="Courier New", size=18, weight="bold"),
            text_color="gray"
        )
        self.boot_method_title.pack(side="left")

        self.iso_status = ctk.CTkLabel(
            title_container,
            text="⚪ Incomplete",
            font=ctk.CTkFont(family="Courier New", size=14),
            text_color="gray"
        )
        self.iso_status.pack(side="right")

        # Boot method selection container
        boot_method_container = ctk.CTkFrame(self.boot_method_frame, fg_color="transparent")
        boot_method_container.pack(fill="x", padx=20, pady=(0, 10))

        # Boot method dropdown
        self.boot_method_var = ctk.StringVar(value="ISO Image (Please Select)")
        self.boot_method_dropdown = ctk.CTkComboBox(
            boot_method_container,
            variable=self.boot_method_var,
            values=[ "Non Bootable", "ISO Image (Please Select)", "MS-DOS", "FreeDOS", "Syslinux 4.07", "Syslinux 6.04", "ReactOS", "Grub 2.12", "Grub4DOS 0.4.6a", "UEFI:NTFS"],
            width=300,
            command=self.on_boot_method_changed,
            font=ctk.CTkFont(family="Courier New")
        )
        self.boot_method_dropdown.pack(side="left", padx=(0, 10))
        
        # Boot method container
        boot_method_container = ctk.CTkFrame(self.boot_method_frame, fg_color="transparent")
        boot_method_container.pack(fill="x", padx=20, pady=(0, 15))

        # ISO path display
        self.iso_path_var = ctk.StringVar(value="ISO Image (Please Select)")
        self.iso_path_label = ctk.CTkLabel(
            boot_method_container,
            textvariable=self.iso_path_var,
            width=400,
            anchor="w",
            text_color="gray",
            font=ctk.CTkFont(family="Courier New", size=12)
        )
        self.iso_path_label.pack(side="left", padx=(0, 10))

        # Select button
        self.select_btn = ctk.CTkButton(
            boot_method_container,
            text="Select",
            width=100,
            command=self.select_iso,
            fg_color="gray",
            hover_color=self.hover_color,
            text_color="white",
            state="disabled",
            font=ctk.CTkFont(family="Courier New", size=12)
        )
        self.select_btn.pack(side="left")
        
    def setup_configuration(self, parent):
        # Configuration frame
        self.config_frame = ctk.CTkFrame(parent, fg_color=self.disabled_color)
        self.config_frame.pack(fill="x", pady=(0, 15))
        
        # Title with status indicator
        title_container = ctk.CTkFrame(self.config_frame, fg_color="transparent")
        title_container.pack(fill="x", padx=20, pady=(15, 10))
        
        self.config_title = ctk.CTkLabel(
            title_container,
            text="Configuration",
            font=ctk.CTkFont(family="Courier New", size=18, weight="bold"),
            text_color="gray"
        )
        self.config_title.pack(side="left")

        self.config_status = ctk.CTkLabel(
            title_container,
            text="⚪ Incomplete",
            font=ctk.CTkFont(family="Courier New", size=14),
            text_color="gray"
        )
        self.config_status.pack(side="right")
        
        # Configuration container
        config_container = ctk.CTkFrame(self.config_frame, fg_color="transparent")
        config_container.pack(fill="x", padx=20, pady=(0, 15))
        
        # Left column
        left_column = ctk.CTkFrame(config_container, fg_color="transparent")
        left_column.pack(side="left", fill="both", expand=True, padx=(0, 10))
        
        # Volume name
        self.volume_label = ctk.CTkLabel(
            left_column,
            text="Volume Name (max 11 chars):",
            text_color="gray",
            font=ctk.CTkFont(family="Courier New", size=12)
        )
        self.volume_label.pack(anchor="w", pady=(0, 5))

        self.volume_var = ctk.StringVar()
        self.volume_var.trace("w", self.on_volume_change)
        self.volume_entry = ctk.CTkEntry(
            left_column,
            textvariable=self.volume_var,
            width=200,
            state="disabled",
            font=ctk.CTkFont(family="Courier New", size=12)
        )
        self.volume_entry.pack(anchor="w", pady=(0, 15))
        
        # Partition scheme
        self.partition_label = ctk.CTkLabel(
            left_column,
            text="Partition Scheme:",
            text_color="gray",
            font=ctk.CTkFont(family="Courier New", size=12)
        )
        self.partition_label.pack(anchor="w", pady=(0, 5))

        self.partition_var = ctk.StringVar(value="MBR")
        self.partition_var.trace("w", self.on_config_change)
        self.partition_dropdown = ctk.CTkComboBox(
            left_column,
            variable=self.partition_var,
            values=["MBR", "GPT"],
            width=200,
            state="disabled",
            font=ctk.CTkFont(family="Courier New", size=12)
        )
        self.partition_dropdown.pack(anchor="w", pady=(0, 15))

        # Cluster size
        self.cluster_label = ctk.CTkLabel(
            left_column,
            text="Cluster Size:",
            text_color="gray",
            font=ctk.CTkFont(family="Courier New", size=12)
        )
        self.cluster_label.pack(anchor="w", pady=(0, 5))

        self.cluster_var = ctk.StringVar(value="4096 bytes (Default)")
        self.cluster_var.trace("w", self.on_config_change)
        self.cluster_dropdown = ctk.CTkComboBox(
            left_column,
            variable=self.cluster_var,
            values=["2048 bytes", "4096 bytes (Default)", "8192 bytes", "16 kilobytes", "32 kilobytes", "64 kilobytes"],
            width=200,
            state="disabled",
            font=ctk.CTkFont(family="Courier New", size=12)
        )
        self.cluster_dropdown.pack(anchor="w")
        
        # Right column
        right_column = ctk.CTkFrame(config_container, fg_color="transparent")
        right_column.pack(side="right", fill="both", expand=True, padx=(10, 0))
        
        # Target system
        self.target_label = ctk.CTkLabel(
            right_column,
            text="Target System:",
            text_color="gray",
            font=ctk.CTkFont(family="Courier New", size=12)
        )
        self.target_label.pack(anchor="w", pady=(0, 5))
            
        self.target_var = ctk.StringVar(value="BIOS or UEFI")
        self.target_text = ctk.CTkLabel(
            right_column,
            textvariable=self.target_var,
            width=400,
            anchor="w",
            text_color="gray",
            font=ctk.CTkFont(family="Courier New", size=12)
        )
        self.target_text.pack(anchor="w", pady=(0, 15))
        
        # File system
        self.system_label = ctk.CTkLabel(
            right_column,
            text="File System:",
            text_color="gray",
            font=ctk.CTkFont(family="Courier New", size=12)
        )
        self.system_label.pack(anchor="w", pady=(0, 5))

        self.system_var = ctk.StringVar(value="FAT32")
        self.system_var.trace("w", self.on_config_change)
        self.system_dropdown = ctk.CTkComboBox(
            right_column,
            variable=self.system_var,
            values=["FAT32", "NTFS", "UDF", "exFAT", "ext2", "ext3", "ext4"],
            width=200,
            state="disabled",
            font=ctk.CTkFont(family="Courier New", size=12)
        )
        self.system_dropdown.pack(anchor="w")
        
    def setup_flash_section(self, parent):
        # Flash section frame
        self.flash_frame = ctk.CTkFrame(parent, fg_color=self.disabled_color)
        self.flash_frame.pack(fill="x", pady=(0, 15))
        
        # Title with status indicator
        title_container = ctk.CTkFrame(self.flash_frame, fg_color="transparent")
        title_container.pack(fill="x", padx=20, pady=(15, 10))
        
        self.flash_title = ctk.CTkLabel(
            title_container,
            text="Flash ISO",
            font=ctk.CTkFont(family="Courier New", size=18, weight="bold"),
            text_color="gray"
        )
        self.flash_title.pack(side="left")

        self.flash_status = ctk.CTkLabel(
            title_container,
            text="⚪ Ready",
            font=ctk.CTkFont(family="Courier New", size=14),
            text_color="gray"
        )
        self.flash_status.pack(side="right")
        
        # Flash button container
        flash_container = ctk.CTkFrame(self.flash_frame, fg_color="transparent")
        flash_container.pack(fill="x", padx=20, pady=(0, 15))

        # Flash button
        self.flash_btn = ctk.CTkButton(
            flash_container,
            text="FLASH",
            width=200,
            height=50,
            font=ctk.CTkFont(family="Courier New", size=16, weight="bold"),
            command=self.start_flash,
            fg_color="gray",
            hover_color=self.hover_color,
            text_color="white",
            state="disabled"
        )
        self.flash_btn.pack(pady=(0, 10))

        # Progress bar and percentage container
        progress_container = ctk.CTkFrame(flash_container, fg_color="transparent")
        progress_container.pack(fill="x", pady=(0, 0))

        # Progress bar
        self.flash_progress_bar = ctk.CTkProgressBar(
            progress_container,
            width=600,
            height=15,
            progress_color="#00ff00"
        )
        self.flash_progress_bar.pack(padx=(0, 10))
        self.flash_progress_bar.set(0)

        # Percentage indicator
        self.percentage_var = ctk.StringVar(value="0%")
        self.percentage_label = ctk.CTkLabel(
            progress_container,
            textvariable=self.percentage_var,
            font=ctk.CTkFont(family="Courier New", size=14, weight="bold"),
            text_color=self.primary_color,
            width=100
        )
        self.percentage_label.pack()
        
    def setup_progress_section(self, parent):
        # Progress frame
        self.progress_frame = ctk.CTkFrame(parent, fg_color=self.card_color)
        
        # Progress bar
        self.progress_bar = ctk.CTkProgressBar(self.progress_frame, width=400)
        self.progress_bar.pack(pady=15)
        self.progress_bar.set(0)
        
        # Status label
        self.status_var = ctk.StringVar(value="Ready")
        self.status_label = ctk.CTkLabel(
            self.progress_frame,
            textvariable=self.status_var,
            font=ctk.CTkFont(family="Courier New", size=14)
        )
        self.status_label.pack(pady=(0, 15))
        
    def update_layer_states(self):
        # Update the visual state of all layers based on completion status
        
        # Layer 1 - Always enabled
        self.drive_frame.configure(fg_color=self.card_color)
        self.drive_title.configure(text_color=self.primary_color)
        self.drive_status.configure(
            text="✅ Complete" if self.layer_completed[1] else "⚪ Incomplete",
            text_color=self.primary_color if self.layer_completed[1] else "gray"
        )
        
        # Layer 2 - Enabled if Layer 1 is complete
        if self.layer_completed[1]:
            self.boot_method_frame.configure(fg_color=self.card_color)
            self.boot_method_title.configure(text_color=self.primary_color)
            self.iso_path_label.configure(text_color=self.text_color)
            self.boot_method_dropdown.configure(state="normal")
            # Enable select button only if "ISO Image (Please Select)" is selected
            if self.boot_method_var.get() == "ISO Image (Please Select)":
                self.select_btn.configure(
                    state="normal",
                    fg_color=self.primary_color,
                    text_color="black"
                )
            else:
                self.select_btn.configure(
                    state="disabled",
                    fg_color="gray",
                    text_color="white"
                )
        else:
            self.boot_method_frame.configure(fg_color=self.disabled_color)
            self.boot_method_title.configure(text_color="gray")
            self.iso_path_label.configure(text_color="gray")
            self.boot_method_dropdown.configure(state="disabled")
            self.select_btn.configure(
                state="disabled",
                fg_color="gray",
                text_color="white"
            )
            
        self.iso_status.configure(
            text="✅ Complete" if self.layer_completed[2] else "⚪ Incomplete",
            text_color=self.primary_color if self.layer_completed[2] else "gray"
        )
        
        # Layer 3 - Enabled if Layer 2 is complete
        if self.layer_completed[2]:
            self.config_frame.configure(fg_color=self.card_color)
            self.config_title.configure(text_color=self.primary_color)
            self.volume_label.configure(text_color=self.text_color)
            self.partition_label.configure(text_color=self.text_color)
            self.target_label.configure(text_color=self.text_color)
            self.system_label.configure(text_color=self.text_color)
            self.volume_entry.configure(state="normal")
            self.partition_dropdown.configure(state="normal")
            self.target_text.configure(text_color=self.text_color)
            self.system_dropdown.configure(state="normal")
            self.cluster_dropdown.configure(state="normal")
        else:
            self.config_frame.configure(fg_color=self.disabled_color)
            self.config_title.configure(text_color="gray")
            self.volume_label.configure(text_color="gray")
            self.partition_label.configure(text_color="gray")
            self.target_label.configure(text_color="gray")
            self.system_label.configure(text_color="gray")
            self.volume_entry.configure(state="disabled")
            self.partition_dropdown.configure(state="disabled")
            self.target_text.configure(text_color="gray")
            self.system_dropdown.configure(state="disabled")
            self.cluster_dropdown.configure(state="disabled")
            
        self.config_status.configure(
            text="✅ Complete" if self.layer_completed[3] else "⚪ Incomplete",
            text_color=self.primary_color if self.layer_completed[3] else "gray"
        )
        
        # Layer 4 - Enabled if Layer 3 is complete
        if self.layer_completed[3]:
            self.flash_frame.configure(fg_color=self.card_color)
            self.flash_title.configure(text_color=self.primary_color)
            self.flash_btn.configure(
                state="normal",
                fg_color=self.primary_color,
                hover_color=self.hover_color,
                text_color="black"
            )
            self.flash_status.configure(
                text="🚀 Ready to Flash",
                text_color=self.primary_color
            )
        else:
            self.flash_frame.configure(fg_color=self.disabled_color)
            self.flash_title.configure(text_color="gray")
            self.flash_btn.configure(
                state="disabled",
                fg_color="gray",
                text_color="white"
            )
            self.flash_status.configure(
                text="⚪ Ready",
                text_color="gray"
            )
        
    def refresh_drives(self):
        # Refresh the list of available USB drives
        drives = self.usb_handler.get_usb_drives()
        if drives:
            drive_list = [f"{drive['letter']} - {drive['label']} ({drive['size']})" for drive in drives]
            self.drive_dropdown.configure(values=drive_list)
            self.drive_var.set("Select a USB drive...")
        else:
            self.drive_dropdown.configure(values=["No USB drives found"])
            self.drive_var.set("No USB drives found")
            
    def on_drive_selected(self, selection):
        # Handle drive selection
        if selection and "No" not in selection and "Select" not in selection:
            drive_letter = selection.split(" - ")[0]
            self.selected_drive = drive_letter
            self.original_drive_letter = drive_letter  # Store original drive letter
            self.layer_completed[1] = True
        else:
            self.selected_drive = None
            self.original_drive_letter = None
            self.layer_completed[1] = False
            
        # Reset subsequent layers if drive changes
        if not self.layer_completed[1]:
            self.layer_completed[2] = False
            self.layer_completed[3] = False
            self.layer_completed[4] = False
            
        self.update_layer_states()
            
    def on_boot_method_changed(self, selection):
        # Handle boot method dropdown changes
        self.boot_method = selection

        if selection != "ISO Image (Please Select)":
            self.selected_iso = None
            self.iso_path_var.set(selection)
            self.layer_completed[2] = True
            self.select_btn.configure(
                state="disabled",
                fg_color="gray",
                text_color="white"
            )
            if selection == "Non Bootable":
                self.target_var.set("BIOS or UEFI")
            elif selection == "UEFI:NTFS":
                self.target_var.set("UEFI (non CSM)")
            else:
                self.target_var.set("BIOS (or UEFI-CSM)")
        else:
            # ISO selection is compulsory
            self.selected_iso = None
            self.iso_path_var.set("ISO Image (Please Select)")
            self.layer_completed[2] = False
            if self.layer_completed[1]:
                self.select_btn.configure(
                    state="normal",
                    fg_color=self.primary_color,
                    text_color="black"
                )

        # Reset subsequent layers
        if not self.layer_completed[2]:
            self.layer_completed[3] = False
            self.layer_completed[4] = False

        self.update_layer_states()

    def select_iso(self):
        # Select ISO file
        if not self.layer_completed[1]:
            return

        if self.boot_method_var.get() != "ISO Image (Please Select)":
            return

        file_path = filedialog.askopenfilename(
            title="Select ISO File",
            filetypes=[("ISO files", "*.iso"), ("All files", "*.*")]
        )

        if file_path:
            # Validate ISO file
            if self.iso_handler.validate_iso(file_path):
                self.selected_iso = file_path
                filename = os.path.basename(file_path)
                self.iso_path_var.set(filename)
                self.layer_completed[2] = True

                # Check if ISO is bootable
                if not self.iso_handler.is_bootable(file_path):
                    messagebox.showwarning(
                        "Warning",
                        "The selected ISO file may not be bootable. "
                        "The flashing process will continue, but the USB drive may not boot properly."
                    )
            else:
                messagebox.showerror("Error", "Invalid ISO file selected.")
                self.selected_iso = None
                self.iso_path_var.set("ISO Image (Please Select)")
                self.layer_completed[2] = False
        else:
            self.selected_iso = None
            self.iso_path_var.set("ISO Image (Please Select)")
            self.layer_completed[2] = False

        # Reset subsequent layers if ISO changes
        if not self.layer_completed[2]:
            self.layer_completed[3] = False
            self.layer_completed[4] = False

        self.update_layer_states()
        
    def on_volume_change(self, *args):
        # Handle volume name changes with character limit
        current_value = self.volume_var.get()
        
        # Limit to 11 characters
        if len(current_value) > 11:
            self.volume_var.set(current_value[:11])
            
        self.on_config_change()
        
    def on_config_change(self, *args):
        # Handle configuration changes
        if not self.layer_completed[2]:
            return
            
        # Check if volume name is provided
        if self.volume_var.get().strip():
            self.layer_completed[3] = True
        else:
            self.layer_completed[3] = False
            
        # Reset flash layer if config changes
        if not self.layer_completed[3]:
            self.layer_completed[4] = False
            
        self.update_layer_states()
        
    def start_flash(self):
        # Start the flashing process
        if not self.layer_completed[3]:
            return
            
        # Validate inputs one more time
        if not self.selected_drive:
            messagebox.showerror("Error", "Please select a USB drive.")
            return

        if self.boot_method_var.get() == "ISO Image (Please Select)" and not self.selected_iso:
            messagebox.showerror("Error", "Please select an ISO file.")
            return

        if not self.volume_var.get().strip():
            messagebox.showerror("Error", "Please enter a volume name.")
            return

        # Confirm action
        iso_info = f"ISO: {os.path.basename(self.selected_iso)}\n" if self.selected_iso else "Mode: Non Bootable (Format Only)\n"
        result = messagebox.askyesno(
            "Confirm Flash",
            f"This will erase all data on drive {self.selected_drive}.\n"
            f"{iso_info}"
            f"Volume: {self.volume_var.get()}\n"
            f"Partition: {self.partition_var.get()}\n"
            f"Target: {self.target_var.get()}\n"
            f"File system: {self.system_var.get()}\n\n"
            "Are you sure you want to continue?"
        )
        
        if result:
            # Show progress frame
            self.progress_frame.pack_forget()
            self.progress_frame.pack(fill="x", pady=(0, 15))
            
            # Update flash status
            self.flash_status.configure(
                text="🔄 Flashing...",
                text_color="orange"
            )
            
            # Disable flash button
            self.flash_btn.configure(state="disabled", text="FLASHING...")
            
            # Reset percentage
            self.percentage_var.set("0%")
            
            # Start flashing in separate thread
            flash_thread = threading.Thread(target=self.flash_iso)
            flash_thread.daemon = True
            flash_thread.start()
            
    def flash_iso(self):
        # Flash ISO to USB drive
        try:
            # Update status
            self.status_var.set("Preparing to flash...")
            self.progress_bar.set(0.1)
            
            # Use original drive letter to maintain consistency
            drive_letter = self.original_drive_letter if self.original_drive_letter else self.selected_drive
            
            # Flash the ISO
            success = self.flasher.flash_iso(
                iso_path=self.selected_iso,
                drive_letter=drive_letter,
                volume_name=self.volume_var.get(),
                partition_scheme=self.partition_var.get(),
                target_system=self.target_var.get(),
                file_system=self.system_var.get(),
                progress_callback=self.update_progress
            )
            
            if success:
                self.status_var.set("Flash completed successfully!")
                self.progress_bar.set(1.0)
                self.percentage_var.set("100%")
                self.layer_completed[4] = True
                self.flash_status.configure(
                    text="✅ Complete",
                    text_color=self.primary_color
                )
                messagebox.showinfo("Success", f"ISO has been successfully flashed to USB drive {drive_letter}!")
            else:
                self.status_var.set("Flash failed!")
                self.percentage_var.set("0%")
                self.flash_status.configure(
                    text="❌ Failed",
                    text_color="red"
                )
                messagebox.showerror("Error", "Failed to flash ISO to USB drive.")
                
        except Exception as e:
            self.status_var.set(f"Error: {str(e)}")
            self.percentage_var.set("0%")
            self.flash_status.configure(
                text="❌ Error",
                text_color="red"
            )
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
            
        finally:
            # Re-enable flash button
            self.flash_btn.configure(state="normal", text="FLASH")
            
    def update_progress(self, progress, status):
        # Update progress bar, status, and percentage
        self.progress_bar.set(progress / 100.0)
        self.flash_progress_bar.set(progress / 100.0)
        self.status_var.set(status)
        self.percentage_var.set(f"{int(progress)}%")
        self.update()
