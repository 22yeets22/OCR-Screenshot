import ctypes
import glob
import os
import sys
import time
from subprocess import Popen

import keyboard
import pyperclip
import pytesseract
from PIL import ImageGrab


def is_already_running(mutex_name="Global\\OCR_Screenshot_Singleton"):
    kernel32 = ctypes.windll.kernel32
    # try to create a mutex, if it doesnt work it'll return 183 - according to chatgpt lol
    handle = kernel32.CreateMutexW(None, False, mutex_name)
    if not handle:
        return False, handle
    already = kernel32.GetLastError() == 183
    return already, handle


def run_screenclip_and_ocr():
    # Launch Windows built-in snip GUI (Win+Shift+S)
    Popen(["explorer.exe", "ms-screenclip:"])

    # Give user time to snip (poll clipboard until image arrives)
    print("Select an area with the snipping tool...")
    image = None
    for _ in range(30):  # wait up to 15 seconds
        time.sleep(0.5)
        image = ImageGrab.grabclipboard()
        if image:
            break

    if not image:
        print("No image captured.")
        return
    else:
        print("captured")

    # Try to delete the saved screenshot file
    screenshots_dirs = [
        os.path.join(os.path.expanduser("~"), "Pictures", "Screenshots"),
        os.path.join(os.path.expanduser("~"), "OneDrive", "Pictures", "Screenshots"),
    ]
    try:
        deleted = False
        for sdir in screenshots_dirs:
            if not os.path.isdir(sdir):
                continue
            patterns = ("*.png", "*.jpg", "*.jpeg", "*.bmp")
            candidates = []
            for p in patterns:
                candidates.extend(glob.glob(os.path.join(sdir, p)))
            if not candidates:
                continue
            candidates.sort(key=lambda p: os.path.getmtime(p), reverse=True)
            most_recent = candidates[0]
            # only delete if it's very new (like ten secs)
            if time.time() - os.path.getmtime(most_recent) <= 10:
                try:
                    os.remove(most_recent)
                    print(f"Deleted screenshot file: {most_recent}")
                    deleted = True
                    break
                except Exception as e:
                    print(f"Could not delete screenshot file {most_recent}: {e}")

        if not deleted:
            pass  # nothing there but probably their settings or smth

    except Exception as e:
        print(f"Error while attempting to delete screenshot file: {e}")

    # run ocr with pytesseract then copy
    text = pytesseract.image_to_string(image)
    pyperclip.copy(text)
    print("Copied OCR text to clipboard:\n")
    print(text)


def main():
    print("Press Shift+Win+O to OCR a screen region.")
    keyboard.add_hotkey("shift+win+o", run_screenclip_and_ocr)

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    running, mutex_handle = is_already_running()
    if running:
        print("Another instance is already running. Exiting.")
        sys.exit(0)

    try:
        main()
    finally:
        # close mutex when done
        ctypes.windll.kernel32.CloseHandle(mutex_handle)
