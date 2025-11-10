# Lahiri ISO Flasher

![](https://img.shields.io/github/created-at/AbhyudayadityaStudios/LahiriISOFlasher?color=%2331F6E1&style=for-the-badge)
![](https://img.shields.io/github/v/release/AbhyudayadityaStudios/LahiriISOFlasher?color=%23a9e43a&style=for-the-badge)
![](https://img.shields.io/github/license/AbhyudayadityaStudios/LahiriISOFlasher?color=%23A42E2B&style=for-the-badge&logo=GNU)
![](https://img.shields.io/github/languages/top/AbhyudayadityaStudios/LahiriISOFlasher?style=for-the-badge&logo=Python&logoColor=white&color=3776AB)
![](https://img.shields.io/github/downloads/AbhyudayadityaStudios/LahiriISOFlasher/total?style=for-the-badge&color=01c45b)
![](https://img.shields.io/github/stars/AbhyudayadityaStudios/LahiriISOFlasher?style=for-the-badge&logo=GitHub&color=FF681A)

<img src="https://github.com/MYTAditya/LahiriISOFlasher/blob/master/ui/icon.png" alt="icon" width="360">

An ISO to USB flashing tool

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

## Installation
1. Download the [latest release](https://github.com/AbhyudayadityaStudios/LahiriISOFlasher/releases).
2. Run `LahiriISOFlasher.exe`.
(It is recommended to use Windows 10 22H2 and later).

## Compilation
1. Clone the repository or download the [latest source code](https://github.com/AbhyudayadityaStudios/LahiriISOFlasher/releases):
   ```cmd
   git clone https://github.com/AbhyudayadityaStudios/LahiriISOFlasher
   ```
2. Install dependencies:
   ```cmd
   py -m pip install -r requirements.txt
   ```
3. Run the application (optional):
   ```cmd
   py main.py
   ```
4. Create an executable:
   ```cmd
   py build.py
   ```
(It is recommended to use Python 3.13.2 or later).
