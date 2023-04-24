import json
import os
import win32api
import keyboard
import time
import threading
import pydirectinput
from pyfiglet import Figlet



DEFAULT_INCREMENT_VALUE = 45
TELEPORT_COOLDOWN = 0.05  # Cooldown time in seconds
SLEEP_TIME = 0.001  # Sleep time in seconds

DIRECTIONS = {}  # Dictionary to store the direction values for each key

# default values for if they dont get assigned in config
RESET_KEY = "left"
UP_KEY = "up"
DOWN_KEY = "down"
LEFT_CLICK_KEY = "u"
RIGHT_CLICK_KEY = "o"


def printlogo():
    f = Figlet(font='slant')
    print(f.renderText('PyMouseMove'))

def read_config(filename):
    global DIRECTIONS, RESET_KEY, UP_KEY, DOWN_KEY, LEFT_CLICK_KEY, RIGHT_CLICK_KEY

    try:
        with open(filename, "r") as file:
            config = json.load(file)
            DIRECTIONS = config.get("directions", {})
            """
            I know this looks weird, but for example for reset key
            it is not setting left as the reset key, its setting reset key from the json 
            as the reset key and then if it cant find reset key it will set left as the reset
            """
            RESET_KEY = config.get("reset_key", "left")
            UP_KEY = config.get("up_key", "up")
            DOWN_KEY = config.get("down_key", "down")
            LEFT_CLICK_KEY = config.get("left_click_key", "u")
            RIGHT_CLICK_KEY = config.get("right_click_key", "o")
    except Exception as e:
        print(f"Error loading config: {e}")


def move_mouse(x_change, y_change):
    current_x, current_y = win32api.GetCursorPos()
    new_x = current_x + x_change
    new_y = current_y + y_change
    win32api.SetCursorPos((new_x, new_y))


def handle_key_events():
    global TELEPORT_COOLDOWN, SLEEP_TIME, DEFAULT_INCREMENT_VALUE, DIRECTIONS, RESET_KEY, UP_KEY, DOWN_KEY, LEFT_CLICK_KEY, RIGHT_CLICK_KEY, LAST_CLICK, LAST_RCLICK, LAST_CHANGE
    # just to initialize last
    last_teleported = time.time() 
    LAST_CLICK = time.time()
    LAST_RCLICK = time.time()
    LAST_CHANGE = time.time()

    while True:
        current_time = time.time()

        if current_time - last_teleported >= TELEPORT_COOLDOWN:
            for key, direction in DIRECTIONS.items():
                if keyboard.is_pressed("alt") and keyboard.is_pressed(key):
                    x_delta, y_delta = direction
                    x_delta *= DEFAULT_INCREMENT_VALUE
                    y_delta *= DEFAULT_INCREMENT_VALUE
                    move_mouse(x_delta, y_delta)
                    last_teleported = current_time

            if keyboard.is_pressed("alt") and keyboard.is_pressed(UP_KEY):
                if current_time - LAST_CHANGE >= 0.3:
                    print("\ntoggled on faster mode via : alt + {}".format(UP_KEY), end = "")
                    DEFAULT_INCREMENT_VALUE = 90
                    LAST_CHANGE = time.time()
            if keyboard.is_pressed("alt") and keyboard.is_pressed(DOWN_KEY):
                if current_time - LAST_CHANGE >= 0.3:
                    print("\ntoggled on slower mode via: alt + {}".format(DOWN_KEY), end = "")
                    DEFAULT_INCREMENT_VALUE = 15
                    LAST_CHANGE = time.time()
            if keyboard.is_pressed("alt") and keyboard.is_pressed(RESET_KEY):
                if current_time - LAST_CHANGE >= 0.3:
                    print("\ntoggled on normal mode via: Alt + {}".format(RESET_KEY), end = "")
                    DEFAULT_INCREMENT_VALUE = 45
                    LAST_CHANGE = time.time()

            #TODO:
            # change to while loop
            # so that i can have fluid dragging while alt and left click key
            # are pressed
            # and i dont have to do all this stupid stuff 
            # i cant do this right now though because i have to have alt pressed
            # and a while loop would end the second it hit the line keyboard release alt 
            # would also like to do this for right click
            if keyboard.is_pressed("alt") and keyboard.is_pressed(LEFT_CLICK_KEY):
                if current_time - LAST_CLICK >= 0.2:
                    print("\nLeft click: alt + {}".format(LEFT_CLICK_KEY), end = "")
                    # you have to artificially release alt or else it doesnt work 
                    keyboard.release("alt")
                    pydirectinput.click()
                    keyboard.press("alt")
                    LAST_CLICK = time.time()

            if keyboard.is_pressed("alt") and keyboard.is_pressed(RIGHT_CLICK_KEY):
                if current_time - LAST_RCLICK >= 0.2:
                    print("\nRight click: alt + {}".format(RIGHT_CLICK_KEY), end = "")
                    keyboard.release("alt")  # Release the 'alt' key
                    pydirectinput.rightClick()
                    # TODO
                    # We cannot re-press the alt key, because that closes
                    # the right click menu.
                    # i would love better solutions via PR or just reccomendation
                    # This current implementation causes desync between your keyboard and windows
                    # real solution is to switch to a toggle mode, where you just hit alt rightalt and
                    # it toggles on movement mode
                    # and you just hit ijkl to move around or whatever your config dictates
                    # not alt + ijkl 
                    # but then i have to know how to do key suppression ( so it doesnt just type ijkl in whatever you're using )
                    # i do not
                    LAST_RCLICK = time.time()



        time.sleep(SLEEP_TIME)

def main():
    os.system('cls||clear')
    printlogo()

    global DEFAULT_INCREMENT_VALUE

    config_files = []
    for file in os.listdir("."):
        if file.endswith(".json"):
            config_files.append(file)

    if len(config_files) < 1:
        print("No config files found.")
        return
    if len(config_files) < 2:
        selection = 1
        read_config(config_files[0])
    else:

        print("Available config files:")
        
        for num,name in enumerate(config_files):
            print(str(num + 1) + ": " + name)

        while True:
            selection = input("Select a config file: ")

            try:
                selection = int(selection)
                if 1 <= selection <= len(config_files):
                    read_config(config_files[selection-1])
                    break
            # TODO: 
            # i want to add messages for each thing they
            # could do wrong
            # just havent yet. 
            # e.g. "that number is not in the list, pick a number 1-5"
            # or 
            # "Your selection should be the number related to the config" ( if they input a letter )
            except ValueError:
                pass
    os.system('cls||clear')
    printlogo()
    print(f"\n      KEYBINDS ({config_files[selection-1]})")
    print("-" * 32)
    for key, direction in DIRECTIONS.items():
        print(f"    - Move mouse {'up' if direction == [0, -1] else 'down' if direction == [0, 1] else 'left' if direction == [-1, 0] else 'right'}: alt + {key}")

    print(f"    - Set to faster speed: alt + {UP_KEY}")
    print(f"    - Set to slower speed: alt + {DOWN_KEY}")
    print(f"    - Reset speed: alt + {RESET_KEY}")
    print(f"    - Left click: alt + {LEFT_CLICK_KEY}")
    print(f"    - Right click: alt + {RIGHT_CLICK_KEY}")
    print("")
    print("")
    print("If you want to make your own config, go in the directory where you are running mousemove.py")
    print("and edit any of the json files, then load that config, or make your own json file and copy from the others")
    print("and play with the settings")

    key_event_thread = threading.Thread(target=handle_key_events)
    key_event_thread.daemon = True
    key_event_thread.start()

    while True:
        speed_input = input("Enter a new mouse speed (current speed: {}): ".format(DEFAULT_INCREMENT_VALUE))
        try:
            speed_input = int(speed_input)
            if speed_input > 0:
                DEFAULT_INCREMENT_VALUE = speed_input
        except ValueError:
            pass


if __name__ == "__main__":
    main()
