import os
import subprocess
import sys
import shutil
import PyInstaller
from pathlib import Path

def build():
    # Build Lahiri ISO Flasher
    
    # PyInstaller command to make Windows application 
    build_exe = [
        "pyinstaller",
        "--onefile",
        "--windowed",
        "--name=LahiriISOFlasher",
        "--add-data=ui;ui",
        "--add-data=core;core",
        "--uac-admin",
        "--hidden-import=customtkinter",
        "--hidden-import=PIL",
        "--hidden-import=psutil",
        "--hidden-import=win32api",
        "--hidden-import=win32file",
        "--icon=res/icon.ico",
        "--version-file=ver_info.txt",
        "main.py"
    ]

    # Robocopy command to copy files
    copy_files = [
        "robocopy",
        "res",
        "dist\\res",
        "/S",
        "/A-:H",
        "/COPY:DAT",
        "/XF",
        "readme.txt"
    ]
    
    print("Building executable...")
    try:
        # At first, build the executable
        subprocess.run(build_exe, check=True)
        print("Build completed successfully!")
        print("Executable created in 'dist' folder")
        print("Copying necessary files...")
        try:
            # After that, copy necessary files
            copy_done = subprocess.run(copy_files, check=False)
            # Return code greater than or equal to 8 is an error
            if not copy_done.returncode >= 8:
                print("Successfully copied!")
                print("Now you can run Lahiri ISO Flasher!")
            else:
                print(f"Task failed: {e}")
                return False
        except Exception as e:
            print(f"Task failed: {e}")
            return False
    except subprocess.CalledProcessError or Exception as e:
        print(f"Build failed: {e}")
        return False
    return True

if __name__ == "__main__":
    build()
