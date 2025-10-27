# Lahiri ISO Flasher

![](https://img.shields.io/github/created-at/AbhyudayadityaStudios/LahiriISOFlasher?color=%2331F6E1&style=for-the-badge)
![](https://img.shields.io/github/v/release/AbhyudayadityaStudios/LahiriISOFlasher?color=%23a9e43a&style=for-the-badge)
![](https://img.shields.io/github/license/AbhyudayadityaStudios/LahiriISOFlasher?color=%23A42E2B&style=for-the-badge&logo=GNU)
![](https://img.shields.io/github/languages/top/AbhyudayadityaStudios/LahiriISOFlasher?style=for-the-badge&logo=Python&logoColor=white&color=3776AB)
![](https://img.shields.io/github/downloads/AbhyudayadityaStudios/LahiriISOFlasher/total?style=for-the-badge&color=01c45b)
![](https://img.shields.io/github/stars/AbhyudayadityaStudios/LahiriISOFlasher?style=for-the-badge&logo=GitHub&color=FF681A)

<img src="https://github.com/MYTAditya/LahiriISOFlasher/blob/master/ui/icon.png" alt="icon" width="360">

[![](https://img.youtube.com/vi/OvTpKhZJLkU/0.jpg)](https://youtu.be/OvTpKhZJLkU?si=k-NAldYZvZr8qiiC)


An user-friendly ISO flashing application for Windows, similar to [balenaEtcher](https://github.com/balena-io/etcher) but with additional [Rufus](https://github.com/pbatard/rufus)-like features.

## Features

- **Modern Dark UI with Light mode support**: Clean, professional dark interface but also supports light mode.
- **4-Layer Workflow**: 
  1. Select USB Drive
  2. Select Boot Method
  3. Configure Settings (Volume Name, Partition Scheme, File System and etc.)
  4. Flash ISO
- **ISO Validation**: Automatically validates ISO files and checks if they're bootable.
- **Auto Volume Detection**: Extracts volume name from ISO files when available.
- **Multiple Boot Options**: Support for MS-DOS, FreeDOS, Syslinux, Grub and etc.
- **Progress Tracking**: Real-time progress updates during flashing.
- **Safety Features**: Confirmation dialogs and drive validation.

## Requirements

- Windows 10/11
- Python 3.8+ (for development)

## Installation

### For Users
1. Download the [latest release](https://github.com/AbhyudayadityaStudios/LahiriISOFlasher/releases).
2. Run `LahiriISOFlasher.exe`.

### For Developers
1. Clone the repository
2. Install dependencies:
   ```cmd
   py -m pip install -r requirements.txt
   ```
3. Run the application:
   ```cmd
   py main.py
   ```

## Building from Source

To create a standalone executable:

```cmd
py build.py
```

## Usage

1. **Select USB Drive**: Choose your target USB drive from the dropdown
2. **Select ISO File**: Browse and select your ISO file
3. **Configure Settings**:
   - Volume Name: Set the name for your USB drive
   - Partition Scheme: Choose MBR or GPT
   - Target System: Select BIOS, UEFI, or hybrid compatibility
   - File System: Choose FAT32 or NTFS
4. **Flash**: Click the flash button to start the process

## Safety Features

- **Drive Validation**: Only shows removable USB drives
- **ISO Validation**: Checks for valid ISO format and bootability
- **Confirmation Dialog**: Confirms all settings before flashing
- **Progress Monitoring**: Shows real-time progress and status

## Disclaimer

This software can permanently erase data on USB drives. Always ensure you have backups of important data before using this application. Use at your own risk.
