'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
 ' Lahiri ISO Flasher: An ISO to USB Flashing Tool
 ' USB Drive handling and listing code
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
 
import os
import subprocess
import psutil
import win32api
import win32file
from typing import List, Dict, Optional, Tuple

def run_cmd(cmd: List[str], capture_output: bool = True, check: bool = False) -> Tuple[int, str, str]:
    # Run commands to get a list
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    out, err = proc.communicate()
    if check and proc.returncode != 0:
        raise subprocess.CalledProcessError(proc.returncode, cmd, output=out, stderr=err)
    return proc.returncode, out.strip(), err.strip()

class USBHandler:
    def __init__(self):
        pass
        
    def list_physical_disks() -> List[Tuple[int, str]]:
        # List physical disks
        ps_cmd = [
            "powershell",
            "-NoProfile",
            "-Command",
            r"Get-CimInstance -ClassName Win32_DiskDrive | Where-Object {$_.DeviceID -notlike '\\.\PHYSICALDRIVE0'} | Select-Object -Property Index, Model | ConvertTo-Json -Depth 1"
        ]
        # \\.\PHYSICALDRIVE0 is the physical disk is used by the OS
        rc, out, err = run_cmd(ps_cmd)
        if rc != 0 or not out:
            # Fallback empty list on failure
            return []

        try:
            import json
            data = json.loads(out)
        except Exception:
            return []

        disks = []
        if isinstance(data, dict):
            idx = int(data.get("Index", data.get("index", 0)))
            model = (data.get("Model", "") or "").strip()
            disks.append((idx, model or f"Disk {idx}"))
        elif isinstance(data, list):
            for item in data:
                idx = int(item.get("Index", item.get("index", 0)))
                model = (item.get("Model", "") or "").strip()
                disks.append((idx, model or f"Disk {idx}"))
        disks.sort(key=lambda x: x[0])
        return disks

    def get_disk_display_list(self) -> List[str]:
        # List physical disks in a good form
        return [f"Disk {idx} - {name}" for idx, name in USBHandler.list_physical_disks()]

    def get_disk_size(display_string: str) -> Optional[str]:
        # Returns the disk size in bytes
        disk_number = USBHandler.parse_selected_disk(display_string)
        if disk_number is None:
            return None
        
        ps_cmd = [
            "powershell",
            "-NoProfile",
            "-Command",
            f"Get-Disk -Number {disk_number} | Select-Object -Property Size"
        ]
        disk_size = subprocess.run(ps_cmd, check=False)
        return disk_size

    def get_partition_letter(display_string: str) -> Optional[str]:
        # Returns primary partition letter 
        disk_number = USBHandler.parse_selected_disk(display_string)
        if disk_number is None:
            return None
        
        ps_cmd = [
            "powershell",
            "-NoProfile",
            "-Command",
            f"Get-Disk -Number {disk_number} | Get-Partition | Get-Volume | Select-Object -Property DriveLetter | ConvertTo-Json -Depth 2"
        ]
        rc, out, err = run_cmd(ps_cmd)
        if rc != 0 or not out:
            return None

        try:
            data = json.loads(out)
        except Exception:
            return None

        # Data can be single or list
        candidates = []
        if isinstance(data, dict):
            candidates.append(data.get("DriveLetter"))
        elif isinstance(data, list):
            for item in data:
                candidates.append(item.get("DriveLetter"))

        # Return the first partition letter as uppercase single character
        for d in candidates:
            if d and isinstance(d, str) and len(d) > 0:
                return d.strip().upper()

        return None
    
    def parse_selected_disk(display_string: str) -> Optional[int]:
        # Returns the disk number from a string shown in USB drive selection
        if not display_string:
            return None
        parts = display_string.split()
        if len(parts) >= 2 and parts[0].lower() == "disk":
            try:
                return int(parts[1])
            except ValueError:
                return None
        return None
