import cv2
import pyautogui
import numpy as np
import time
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

# Define the regions of the screen to capture (left, top, width, height)
# screen_regions = [(100, 336, 219, 515), (592, 70, 762, 328), (154,547, 293, 624), (317, 331, 421, 474), (1954, 1271, 2039, 1293), (1065, 1153, 1119, 1167)]  # Example regions, change as needed
screen_regions = [(100, 336, 219, 515), (592, 70, 762, 328), (1954, 1271, 2039, 1293), (1065, 1153, 1119, 1167)]  # Example regions, change as needed

# Load the logo image to be detected
logo_image = cv2.imread('worldcuplogo.png')  # Replace 'logo.png' with your logo image file path
logo_image3 = cv2.imread('overs.png') 

# Function to check if the logo is present in a captured region
def is_logo_present(region):
    # Capture the screen region
    screenshot = pyautogui.screenshot(region=region)
    screenshot = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)

    max_val, max_val2, max_val3, max_val4 = 0,0,0,0

    if region == (100, 336, 219, 515) or region == (592, 70, 762, 328):

        # Match the logo using template matching
        result = cv2.matchTemplate(screenshot, logo_image, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

    if region == (1954, 1271, 2039, 1293) or region == (1065, 1153, 1119, 1167):

        # Match the logo using template matching
        result = cv2.matchTemplate(screenshot, logo_image3, cv2.TM_CCOEFF_NORMED)
        min_val, max_val4, min_loc, max_loc = cv2.minMaxLoc(result)

    # Define a threshold for logo detection
    threshold = 0.25

    # if max_val >= threshold or max_val2 >= 0.45 or max_val3 >= 0.45 or max_val4 >= 0.35:
    if max_val >= threshold or max_val4 >= 0.6:
        # print("CONTENT: " + str(max_val) + ", " + str(max_val2) + ", " + str(max_val3) + ", " + str(max_val4))
        print("CONTENT: " + str(max_val) + ", " + str(max_val4))
        return True
    else:
        # print("AD: " + str(max_val) + ", " + str(max_val2) + ", " + str(max_val3) + ", " + str(max_val4))
        print("AD: " + str(max_val) + ", " + str(max_val4))
        return False

def mute_volume():
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(
        IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = cast(interface, POINTER(IAudioEndpointVolume))
    volume.SetMute(1, None)  # Mute the volume

def unmute_volume():
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(
        IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = cast(interface, POINTER(IAudioEndpointVolume))
    volume.SetMute(0, None)  # Unmute the volume

# Initialize a flag to track the muted state
muted = False

# Main loop
while True:
    logo_detected = False  # Flag to track if the logo is detected in either region
    
    for region in screen_regions:
        if is_logo_present(region):
            logo_detected = True
            break  # Exit the loop if the logo is detected in any region
    
    if not logo_detected:
        if not muted:
            mute_volume()
            muted = True
    else:
        if muted:
            unmute_volume()
            muted = False
    
    # Add a delay to avoid excessive processing
    time.sleep(5)  # Delay for 1 second
