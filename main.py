'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
 ' Lahiri ISO FLasher: An ISO to USB Flashing Tool
 ' Main script to run other scripts
 ' Copyright (c) 2025, 2026 Abhyudayaditya Studios
 '
 ' This program is free software; you can redistribute it and/or
 ' modify it under the terms of the GNU General Public License as
 ' published by the Free Software Foundation; either version 3 of the
 ' License, or (at your option) any later version.
 ' 
 ' This program is distributed in the hope that it will be useful, but
 ' WITHOUT ANY WARRANTY; without even the implied warranty of
 ' MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
 ' General Public License for more details.
 ' 
 ' You should have received a copy of the GNU General Public License
 ' along with this program; if not, see <http://www.gnu.org/licenses/>.
 '
 '''

''' Written by Mastered YT Aditya. '''

import customtkinter as ctk
import tkinter as tk
from tkinter import filedialog, messagebox
import threading
import os
import sys
import subprocess
import time
from pathlib import Path
from PIL import Image

# Import our modules
from ui.main_window import MainWindow
from core.iso_handler import ISOHandler
from core.usb_handler import USBHandler
from core.flasher import ISOFlasher
from ui.about_window import AboutWindow

def main():
    # Set appearance mode and color theme
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("green")
    
    # Create and run the application
    app = MainWindow()
    app.mainloop()

if __name__ == "__main__":
    main()
