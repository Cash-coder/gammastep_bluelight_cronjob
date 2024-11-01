#!/usr/bin/env python3

from datetime import datetime
import subprocess
from time import sleep
import json
import os

# WARNING: if using cronjobs with wayland, in 'crontab -e' file you must specify the wayland display like this:
# * * * * * WAYLAND_DISPLAY=wayland-1 DISPLAY=:1 /home/ggk/vscode_projects/gammastep_bluelight_cronjob/main.py 

# Define the night times
NIGHT_1 = "17:30"
NIGHT_2 = "18:25"
NIGHT_3 = "18:40"

NIGHT_TEMPRERATURE_1 = 3700
NIGHT_TEMPRERATURE_2 = 3000
NIGHT_TEMPRERATURE_3 = 2500


# Flag system is used to avoid restarting night_x when it's already on
# Complete file path is needed to execute from cron jobs
MEMORY_FLAGS_FILE = os.path.join(os.path.dirname(__file__), 'memory_flags.json')

# Get the current time
current_time = datetime.now().strftime("%H:%M")


def read_flags(flag=None):
    """Read flags from the memory file."""
    with open(MEMORY_FLAGS_FILE, 'r') as openfile:
        flags = json.load(openfile)
        return flags.get(flag) if flag else flags


def write_flags(flags_dict):
    """Write flags to the memory file."""
    flags_json = read_flags()
    flags_json.update(flags_dict)

    with open(MEMORY_FLAGS_FILE, "w") as outfile:
        json.dump(flags_json, outfile)


def set_gammastep(temp):
    """Execute gammastep with the specified temperature."""
    subprocess.run(['gammastep', '-O', str(temp)])


def kill_gammastep():
    """Kill any existing gammastep processes to restart with a new value."""
    subprocess.run(['pkill', 'gammastep'])


# Compare current time with night variables
if current_time >= NIGHT_3:
    if not read_flags('flag_night_3'):
        print(f"It's night time 3! {current_time}")
        
        kill_gammastep()
        sleep(0.5)

        # Set flag 3 to true, others to false
        write_flags({
            'flag_night_1': False,
            'flag_night_2': False,
            'flag_night_3': True
        })

        set_gammastep(NIGHT_TEMPRERATURE_3)

elif current_time >= NIGHT_2:
    if not read_flags('flag_night_2'):
        print(f"It's night time 2! {current_time}")
        
        kill_gammastep()
        sleep(0.5)

        # Set flag 2 to true
        write_flags({
            'flag_night_1': False,
            'flag_night_2': True,
            'flag_night_3': False
        })

        set_gammastep(NIGHT_TEMPRERATURE_2)

elif current_time >= NIGHT_1:
    if not read_flags('flag_night_1'):
        print(f"It's night time 1! {current_time}")
        
        kill_gammastep()
        sleep(0.5)

        write_flags({
            'flag_night_1': True,
            'flag_night_2': False,
            'flag_night_3': False
        })

        set_gammastep(NIGHT_TEMPRERATURE_1)

else:
    print(f"It's still daytime, no gammastep activation required. {current_time}")
