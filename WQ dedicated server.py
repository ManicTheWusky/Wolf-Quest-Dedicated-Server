import pyautogui
import time
import pygetwindow as gw
import subprocess
import threading
import os
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Ensure WolfQuestAE.exe is the active window
def focus_window(window_title):
    windows = gw.getWindowsWithTitle(window_title)
    if not windows:
        raise Exception(f"Window with title '{window_title}' not found.")
    window = windows[0]
    window.activate()
    window.maximize()
    time.sleep(1)  # Allow time for the window to focus and maximize

# Launch the game on Steam without showing the game window
def launch_game():
    steam_command = "start /min steam://rungameid/926990"  # Replace 926990 with the Steam App ID for WolfQuest
    subprocess.Popen(steam_command, shell=True)
    time.sleep(20)  # Allow time for the game to launch and for the loading screen

# Stop the game by ending the process
def stop_game():
    os.system("taskkill /f /im WolfQuestAE.exe")
    print("WolfQuestAE.exe task ended.")

# Perform the sequence of actions
def automate_wolfquest():
    try:
        # Step 1: Launch the game
        launch_game()

        # Step 2: Focus on the WolfQuestAE.exe window
        focus_window("WolfQuestAE")

        # Step 3: Press up arrow 10 times
        for _ in range(10):
            pyautogui.press("up")
            time.sleep(0.1)

        # Step 4: Press Enter
        pyautogui.press("enter")
        time.sleep(0.5)

        # Step 5: Press up arrow 6 times
        for _ in range(5):
            pyautogui.press("up")
            time.sleep(0.1)

        # Step 6: Press Enter
        pyautogui.press("enter")
        time.sleep(0.5)

        # Step 7: Press down arrow 1 time
        pyautogui.press("down")
        time.sleep(0.1)

        # Step 8: Press Enter
        pyautogui.press("enter")
        time.sleep(0.5)

        # Step 11: Click on "Game Name" and type "test"
        game_name_coordinates = (3151, 1219)  # Replace with the actual coordinates of "Game Name"
        pyautogui.click(game_name_coordinates)
        time.sleep(0.5)
        pyautogui.write("test")

        # Step 12: Click on "Set Up Game"
        setup_game_coordinates = (3000, 2034)  # Replace with the actual coordinates of "Set Up Game"
        pyautogui.click(setup_game_coordinates)

        print("Automation completed successfully!")

    except Exception as e:
        print(f"An error occurred: {e}")

# Flask routes
@app.route('/')
def index():
    return '''
        <html>
            <head>
                <style>
                    body {
                        font-family: Arial, sans-serif;
                        background-color: #f4f4f9;
                        margin: 0;
                        padding: 0;
                        display: flex;
                        justify-content: center;
                        align-items: center;
                        height: 100vh;
                    }
                    .container {
                        text-align: center;
                        background: #ffffff;
                        border-radius: 8px;
                        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
                        padding: 20px;
                        width: 300px;
                    }
                    h1 {
                        font-size: 1.5rem;
                        color: #333;
                        margin-bottom: 20px;
                    }
                    button {
                        background-color: #007bff;
                        color: #fff;
                        border: none;
                        border-radius: 4px;
                        padding: 10px 20px;
                        font-size: 1rem;
                        cursor: pointer;
                        margin: 10px 0;
                        width: 100%;
                    }
                    button:hover {
                        background-color: #0056b3;
                    }
                </style>
            </head>
            <body>
                <div class="container">
                    <h1>WolfQuest Automation</h1>
                    <button onclick="fetch('/start').then(response => response.json()).then(data => alert(data.message))">Start</button>
                    <button onclick="fetch('/stop').then(response => response.json()).then(data => alert(data.message))">Stop</button>
                </div>
            </body>
        </html>
    '''

@app.route('/start', methods=['GET'])
def start_script():
    threading.Thread(target=automate_wolfquest, daemon=True).start()
    return jsonify({"message": "Automation started!"})

@app.route('/stop', methods=['GET'])
def stop_script():
    stop_game()
    return jsonify({"message": "Game stopped!"})

if __name__ == "__main__":
    app.run(debug=True)
