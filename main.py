#!/usr/bin/env python3

from datetime import datetime
import subprocess
from time import sleep
import json
import os

# WARNING: in 'crontab -e' file you must specify the wayland display like this:
# * * * * * WAYLAND_DISPLAY=wayland-1 DISPLAY=:1 /home/ggk/vscode_projects/gammastep_bluelight_cronjob/main.py 

# method to set the flags to false when the program stops

# Define the night times
night_1 = "17:30"
night_2 = "18:00"
night_3 = "18:25"

# flag system is used to avoid restarting night_x when its already on
# complete file path is needed to execute from cron jobs
MEMORY_FLAGS_FILE = os.path.join(os.path.dirname(__file__), 'memory_flags.json')
flag_night_1 = False
flag_night_2 = False
flag_night_3 = False

# Get the current time
current_time = datetime.now().strftime("%H:%M")


# read flags from the memory file
def read_flags(flag=False):
    with open(MEMORY_FLAGS_FILE, 'r') as openfile:
        # if a flag as is specified return only that flag
        if flag:
            flags = json.load(openfile)
            return  flags[f'{flag}']
        
        # otherwise return all flags
        return json.load(openfile) 

def write_flag(flag, value):
    flags_json = read_flags()
    flags_json[f'{flag}'] = value

    with open(MEMORY_FLAGS_FILE, "w") as outfile:
        json.dump(flags_json, outfile)


# function to execute gammate blue light in terminal
def set_gammastep(temp):
    subprocess.run(['gammastep', '-O', str(temp)])

# to update gamma step temperature you have to kill the old gammastep process, if exist
def kill_gammastep():
    # Kill any existing gammastep processes
    subprocess.run(['pkill', 'gammastep'])


# Compare current time with night variable
if current_time >= night_3:
    if read_flags('flag_night_3') is False:
        print(f"It's night time 3! {current_time}")
        
        kill_gammastep()
        sleep(0.5)

        # set the flag 3 to true, others to false
        write_flag('flag_night_1', False)
        write_flag('flag_night_2', False)
        write_flag('flag_night_3', True)

        set_gammastep(2500) 
elif current_time >= night_2:
    if read_flags('flag_night_2') is False:
        print(f"It's night time 2! {current_time}")
        kill_gammastep()
        sleep(0.5)

        # set flag 2 to true
        write_flag('flag_night_1', False)
        write_flag('flag_night_2', True)
        write_flag('flag_night_3', False)

        set_gammastep(3000)
elif current_time >= night_1:
    if read_flags('flag_night_1') is False:
        print(f"It's night time 1! {current_time}")
        kill_gammastep()
        sleep(0.5)

        #set flag 1 to true
        write_flag('flag_night_1', True)
        write_flag('flag_night_2', False)
        write_flag('flag_night_3', False)

        set_gammastep(3600)
        flag_night_1 = True
else:
    print(f"It's still daytime. {current_time}")
