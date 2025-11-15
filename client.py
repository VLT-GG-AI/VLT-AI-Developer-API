import requests
import urllib.parse
import threading
import itertools
import time
import sys
import random
import os

# Optional colors
try:
    from colorama import init, Fore, Style
    init()
    COLORAMA_AVAILABLE = True
except:
    COLORAMA_AVAILABLE = False

# -----------------------
# SETTINGS
# -----------------------

USE_COLOR = False
WORKER_URL = "https://aiapi.byjta.net"

ASCII_LOGO_LINES = [
" __      ___   _______            _____  ",
" \\ \\    / / | |__   __|     /\\   |_   _| ",
"  \\ \\  / /| |    | |       /  \\    | |   ",
"   \\ \\/ / | |    | |      / /\\ \\   | |   ",
"    \\  /  | |____| |     / ____ \\ _| |_  ",
"     \\/   |______|_|    /_/    \\_\\_____| ",
]

# -----------------------
# COLOR HELPERS
# -----------------------

def color(text, code):
    if USE_COLOR and COLORAMA_AVAILABLE:
        return code + text + Style.RESET_ALL
    return text

def cyan(t): return color(t, Fore.CYAN)
def magenta(t): return color(t, Fore.MAGENTA)
def yellow(t): return color(t, Fore.YELLOW)
def green(t): return color(t, Fore.GREEN)
def red(t): return color(t, Fore.RED)
def white(t): return color(t, Fore.WHITE)
def blue(t): return color(t, Fore.BLUE)

# -----------------------
# CURSOR HELPERS
# -----------------------

def cursor_up(n): sys.stdout.write(f"\033[{n}A")
def clear_line(): sys.stdout.write("\033[2K")

# -----------------------
# HOLOGRAM INTRO
# -----------------------

def hologram_intro():
    print()
    time.sleep(0.2)

    for line in ASCII_LOGO_LINES:
        print(magenta(line))
    time.sleep(0.2)

    total_frames = 45

    for frame in range(total_frames):
        cursor_up(len(ASCII_LOGO_LINES))

        for line in ASCII_LOGO_LINES:
            flicker = ""
            for c in line:
                if random.random() < 0.02:
                    flicker += random.choice("=-_")
                else:
                    flicker += c
            clear_line()
            print(magenta(flicker))

        if frame % 3 == 0:
            cursor_up(len(ASCII_LOGO_LINES))
            beam_pos = frame % len(ASCII_LOGO_LINES[0])

            for line in ASCII_LOGO_LINES:
                clear_line()
                arr = list(line)
                if beam_pos < len(arr):
                    arr[beam_pos] = cyan("█")
                print(" " + "".join(arr))
            time.sleep(0.02)
        else:
            time.sleep(0.03)

    cursor_up(len(ASCII_LOGO_LINES))
    for line in ASCII_LOGO_LINES:
        clear_line()
        print(magenta(line))

    print()
    print(green("   VLTGG AI CHAT INTERFACE READY"))
    print(green("   ------------------------------\n"))
    time.sleep(0.4)

# -----------------------
# HOLOGRAM OUTRO
# -----------------------

def closing_animation():
    fade_frames = 35

    print()
    for line in ASCII_LOGO_LINES:
        print(magenta(line))
    time.sleep(0.1)

    for frame in range(fade_frames):
        cursor_up(len(ASCII_LOGO_LINES))
        intensity = frame / fade_frames

        for line in ASCII_LOGO_LINES:
            clear_line()

            if intensity > 0.75:
                glitched = ""
                for c in line:
                    if random.random() < intensity * 0.4:
                        glitched += random.choice(" ░▒▓█")
                    else:
                        glitched += c
                print(white(glitched))
                continue

            glitched = ""
            for c in line:
                if random.random() < intensity * 0.15:
                    glitched += random.choice("░▒▓")
                else:
                    glitched += c
            print(magenta(glitched))

        cursor_up(len(ASCII_LOGO_LINES))
        beam_pos = (len(ASCII_LOGO_LINES[0]) - 1) - (frame % len(ASCII_LOGO_LINES[0]))

        for line in ASCII_LOGO_LINES:
            clear_line()
            arr = list(line)
            if beam_pos < len(arr):
                arr[beam_pos] = blue("█")
            print(" " + "".join(arr))

        time.sleep(0.03)

    cursor_up(len(ASCII_LOGO_LINES))
    for _ in ASCII_LOGO_LINES:
        clear_line()
        print()

    time.sleep(0.2)

    text = "made by JTA"
    for c in text:
        print(white(c), end="", flush=True)
        time.sleep(0.08)
    print("\n")
    time.sleep(0.3)

# -----------------------
# TYPEWRITER
# -----------------------

def typewriter(text, total_time=1.2):
    L = len(text)
    if L < 1:
        print()
        return
    delay = total_time / L
    for c in text:
        print(c, end="", flush=True)
        time.sleep(delay)
    print()

# -----------------------
# SPINNER
# -----------------------

thinking = False

def spinner():
    for c in itertools.cycle(['-', '\\', '|', '/']):
        if not thinking:
            break
        print(f'\r{yellow("Thinking " + c)}', end='', flush=True)
        time.sleep(0.1)

# -----------------------
# MAIN
# -----------------------

def main():
    hologram_intro()

    print(green("Connected to AI Worker Endpoint."))
    print(green("Type '/update' to update. Type '/reboot' to reboot. Type 'exit' to quit.\n"))

    history = []  # store last 10 messages (5 pairs)

    while True:
        user_input = input("You: ").strip()

        # -----------------------
        # /update
        # -----------------------
        if user_input.lower() == "/update":
            print(green("Running updater...\n"))
            try:
                os.system("update_vlt_ai.bat")
            except Exception as e:
                print(red("Failed to run updater: ") + str(e))
            continue

        # -----------------------
        # /reboot
        # -----------------------
        if user_input.lower() == "/reboot":
            print(green("\nRebooting VLTGG AI...\n"))
            closing_animation()
            os.system("cls" if os.name == "nt" else "clear")
            hologram_intro()
            print(green("Connected to AI Worker Endpoint."))
            print(green("Type '/update', '/reboot', or 'exit'.\n"))
            continue

        # -----------------------
        # exit
        # -----------------------
        if user_input.lower() == "exit":
            closing_animation()
            break

        # -----------------------
        # Add message to history
        # -----------------------
        history.append({"role": "user", "content": user_input})
        history = history[-10:]  # only last 5 exchanges

        # -----------------------
        # BUILD CONTEXT STRING
        # -----------------------
        context = ""
        for msg in history:
            if msg["role"] == "user":
                context += f"USER: {msg['content']}\n"
            else:
                context += f"ASSISTANT: {msg['content']}\n"

        # Final query text
        final_prompt = context + f"USER: {user_input}"

        # Encode for URL
        encoded = urllib.parse.quote(final_prompt)

        # -----------------------
        # spinner
        # -----------------------
        global thinking
        thinking = True
        t = threading.Thread(target=spinner)
        t.start()

        try:
            response = requests.get(f"{WORKER_URL}/?q={encoded}")
        except Exception as e:
            thinking = False
            t.join()
            print(red("Error: ") + str(e))
            continue

        thinking = False
        t.join()
        print("\r", end="")

        if response.status_code != 200:
            print(red("Worker Error: ") + response.text)
            continue

        answer = response.text.strip()

        # Save to history
        history.append({"role": "assistant", "content": answer})
        history = history[-10:]

        print("AI: ", end="")
        typewriter(answer)

if __name__ == "__main__":
    main()
