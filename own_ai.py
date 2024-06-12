import pyautogui
import pyperclip
import pygetwindow as gw
import pytesseract
import json
import os
import time
import threading
import queue
import tkinter as tk
import speech_recognition as sr
import pyttsx3
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB

# Initialize recognizer and text-to-speech engine
recognizer = sr.Recognizer()
tts_engine = pyttsx3.init()

# Global variables
recorded_tasks = []
custom_commands = {}
unrecognized_commands = []
command_data = []  # For self-learning
feedback_queue = queue.Queue()

# Initialize vectorizer and model for command recognition
vectorizer = CountVectorizer()
model = MultinomialNB()

# Sample data for initial training
commands = [
    "hello", "how are you", "what is your name", "read screen", "open notepad",
    "click at 100, 200", "type Hello World", "read from notepad", "click on OK",
    "minimize window", "make window small", "cut the window", "scroll down",
    "create file example.txt", "delete file example.txt", "search file example.txt",
    "start recording", "stop recording task1", "replay task task1", "add custom command test with action speak('test')",
    "execute custom command test", "goodbye"
]
responses = [
    "hello_response", "how_are_you_response", "name_response", "read_screen_response", "open_application_response",
    "click_at_coordinates_response", "type_text_response", "read_from_application_response", "click_on_text_response",
    "minimize_window_response", "resize_window_response", "scroll_window_up_response", "scroll_window_down_response",
    "create_file_response", "delete_file_response", "search_file_response", "start_recording_response",
    "stop_recording_response", "replay_task_response", "add_custom_command_response", "execute_custom_command_response",
    "goodbye_response"
]
X = vectorizer.fit_transform(commands)
model.fit(X, responses)

# Function to listen for commands
def listen_command(q):
    try:
        with sr.Microphone() as source:
            print("Listening for commands...")
            audio = recognizer.listen(source)
        command = recognizer.recognize_google(audio)
        q.put(command.lower())
    except sr.UnknownValueError:
        q.put("")
    except sr.RequestError:
        q.put("")

# Function to start the Tkinter GUI for displaying spoken text
def start_spoken_text_display():
    root = tk.Tk()
    root.title("Spoken Text Display")

    label = tk.Label(root, text="Listening for commands...", font=("Helvetica", 16))
    label.pack(padx=20, pady=20)

    q = queue.Queue()
    threading.Thread(target=listen_command, args=(q,), daemon=True).start()

    def update_label():
        if not q.empty():
            command = q.get()
            label.config(text=f"You said: {command}")
            handle_command(command)
            threading.Thread(target=listen_command, args=(q,), daemon=True).start()
        root.after(100, update_label)

    root.after(100, update_label)
    root.mainloop()

# Function to provide spoken feedback
def speak(text):
    try:
        tts_engine.say(text)
        tts_engine.runAndWait()
    except Exception as e:
        print("Error occurred while speaking:", e)

# Function to process voice commands
def handle_command(command):
    try:
        command_vector = vectorizer.transform([command])
        response = model.predict(command_vector)[0]
        process_command(response, command)
    except:
        unrecognized_commands.append(command)
        prompt_for_new_command(command)

# Function to process recognized commands
def process_command(response, command):
    if response == "hello_response":
        speak("Hello! How can I assist you?")
    elif response == "how_are_you_response":
        speak("I'm doing well, thank you for asking!")
    elif response == "name_response":
        speak("I am your AI assistant.")
    elif response == "read_screen_response":
        screen_text = read_screen()
        speak(screen_text)
    elif response == "open_application_response":
        app_name = command.split("open", 1)[1].strip()
        open_application(app_name)
    elif response == "click_at_coordinates_response":
        coordinates = command.split("click at", 1)[1].strip().split(",")
        x, y = map(int, coordinates)
        click_on_screen(x, y)
    elif response == "type_text_response":
        text_to_type = command.split("type", 1)[1].strip()
        type_text(text_to_type)
    elif response == "read_from_application_response":
        app_name = command.split("read from", 1)[1].strip()
        app_text = read_from_application(app_name)
        speak(app_text)
    elif response == "click_on_text_response":
        text_to_click = command.split("click on", 1)[1].strip()
        click_on_text(text_to_click)
    elif response == "minimize_window_response":
        minimize_window()
    elif response == "resize_window_response":
        resize_window("small")
    elif response == "scroll_window_up_response":
        scroll_window("up")
    elif response == "scroll_window_down_response":
        scroll_window("down")
    elif response == "create_file_response":
        file_name = command.split("create file", 1)[1].strip()
        speak(create_file(file_name))
    elif response == "delete_file_response":
        file_name = command.split("delete file", 1)[1].strip()
        speak(delete_file(file_name))
    elif response == "search_file_response":
        file_name = command.split("search file", 1)[1].strip()
        speak(search_file(file_name))
    elif response == "start_recording_response":
        start_recording()
    elif response == "stop_recording_response":
        task_name = command.split("stop recording", 1)[1].strip()
        stop_recording(task_name)
    elif response == "replay_task_response":
        task_name = command.split("replay task", 1)[1].strip()
        replay_task(task_name)
    elif response == "add_custom_command_response":
        parts = command.split("add custom command", 1)[1].strip().split(" with action ", 1)
        cmd_name, cmd_action = parts
        add_custom_command(cmd_name.strip(), cmd_action.strip())
    elif response == "execute_custom_command_response":
        custom_cmd = command.split("execute custom command", 1)[1].strip()
        execute_custom_command(custom_cmd)
    elif response == "goodbye_response":
        speak("Goodbye! Have a great day.")
        os._exit(0)
    else:
        if response in custom_commands:
            eval(custom_commands[response])
        else:
            speak("Command not recognized.")

# Function to open an application
def open_application(app_name):
    try:
        os.system(f"start {app_name}.exe")
        speak(f"Opening {app_name}.")
    except Exception as e:
        print("Error occurred while opening application:", e)
        speak("Error occurred while opening application.")

# Function to read text from the screen
def read_screen():
    try:
        screenshot = pyautogui.screenshot()
        screenshot_gray = screenshot.convert('L')
        text = pytesseract.image_to_string(screenshot_gray)
        return text
    except Exception as e:
        print("Error occurred while reading screen:", e)
        return "Error occurred while reading screen."

# Function to click on a specific screen coordinate
def click_on_screen(x, y):
    try:
        pyautogui.click(x, y)
        record_click(x, y)
        speak(f"Clicked at coordinates {x}, {y}.")
    except Exception as e:
        print("Error occurred while clicking on screen:", e)
        speak("Error occurred while clicking on screen.")

# Function to type text
def type_text(text):
    try:
        pyautogui.typewrite(text)
        record_typing(text)
        speak(f"Typed: {text}")
    except Exception as e:
        print("Error occurred while typing text:", e)
        speak("Error occurred while typing text.")

# Function to read text from an application window
def read_from_application(app_name):
    try:
        windows = gw.getWindowsWithTitle(app_name)
        if not windows:
            return "No window with the specified name found."
        
        window = windows[0]
        window.activate()
        
        pyautogui.hotkey('ctrl', 'a')
        pyautogui.hotkey('ctrl', 'c')
        text = pyperclip.paste()
        
        return text if text else "No text found in the application window."
    except Exception as e:
        print("Error occurred while reading from application:", e)
        return "Error occurred while reading from application."

# Function to click on text found on the screen
def click_on_text(text):
    try:
        location = pyautogui.locateCenterOnScreen(f'{text}.png')
        if location:
            pyautogui.click(location)
            speak(f"Clicked on text: {text}")
        else:
            speak(f"Text '{text}' not found on screen.")
    except Exception as e:
        print("Error occurred while clicking on text:", e)
        speak("Error occurred while clicking on text.")

# Function to minimize the window
def minimize_window():
    try:
        active_window = gw.getActiveWindow()
        active_window.minimize()
        speak("Window minimized.")
    except Exception as e:
        print("Error occurred while minimizing window:", e)
        speak("Error occurred while minimizing window.")

# Function to resize the window
def resize_window(size):
    try:
        active_window = gw.getActiveWindow()
        if size == "small":
            active_window.resizeTo(800, 600)
        elif size == "large":
            active_window.resizeTo(1200, 800)
        speak(f"Window resized to {size}.")
    except Exception as e:
        print("Error occurred while resizing window:", e)
        speak("Error occurred while resizing window.")

# Function to scroll the window
def scroll_window(direction):
    try:
        if direction == "up":
            pyautogui.scroll(50)
        elif direction == "down":
            pyautogui.scroll(-50)
        speak(f"Window scrolled {direction}.")
    except Exception as e:
        print("Error occurred while scrolling window:", e)
        speak("Error occurred while scrolling window.")

# Function to create a file
def create_file(file_name):
    try:
        with open(file_name, 'w') as file:
            file.write('')
        return f"File {file_name} created successfully."
    except Exception as e:
        print("Error occurred while creating file:", e)
        return "Error occurred while creating file."

# Function to delete a file
def delete_file(file_name):
    try:
        if os.path.exists(file_name):
            os.remove(file_name)
            return f"File {file_name} deleted successfully."
        else:
            return f"File {file_name} does not exist."
    except Exception as e:
        print("Error occurred while deleting file:", e)
        return "Error occurred while deleting file."

# Function to search for a file
def search_file(file_name):
    try:
        if os.path.exists(file_name):
            return f"File {file_name} found."
        else:
            return f"File {file_name} not found."
    except Exception as e:
        print("Error occurred while searching for file:", e)
        return "Error occurred while searching for file."

# Functions for recording tasks
def start_recording():
    global recorded_tasks
    recorded_tasks = []
    speak("Started recording tasks.")

def stop_recording(task_name):
    try:
        with open("recorded_tasks.json", 'r') as file:
            tasks = json.load(file)
    except FileNotFoundError:
        tasks = {}
    tasks[task_name] = recorded_tasks
    try:
        with open("recorded_tasks.json", 'w') as file:
            json.dump(tasks, file)
        speak(f"Stopped recording and saved tasks as {task_name}.")
    except Exception as e:
        print("Error occurred while saving recorded tasks:", e)
        speak("Error occurred while saving recorded tasks.")

# Function to replay a task
def replay_task(task_name):
    try:
        with open('recorded_tasks.json', 'r') as file:
            tasks = json.load(file)
            if task_name in tasks:
                task = tasks[task_name]
                for action in task:
                    if action["action_type"] == "click":
                        pyautogui.click(action["details"]["x"], action["details"]["y"])
                    elif action["action_type"] == "type":
                        pyautogui.typewrite(action["details"]["text"])
                    elif action["action_type"] == "delay":
                        time.sleep(action["details"]["seconds"])
                speak(f"Task '{task_name}' replayed successfully.")
            else:
                speak(f"No recorded task found with the name '{task_name}'.")
    except Exception as e:
        print("Error occurred while replaying the task:", e)
        speak("Error occurred while replaying the task.")

# Helper functions to record actions
def record_click(x, y):
    recorded_tasks.append({'action_type': 'click', 'details': {'x': x, 'y': y}})

def record_typing(text):
    recorded_tasks.append({'action_type': 'type', 'details': {'text': text}})

# Functions to manage custom commands
def add_custom_command(cmd_name, cmd_action):
    custom_commands[cmd_name] = cmd_action
    speak(f"Custom command '{cmd_name}' added.")

def execute_custom_command(custom_cmd):
    if custom_cmd in custom_commands:
        exec(custom_commands[custom_cmd])
    else:
        speak(f"Custom command '{custom_cmd}' not found.")

# Function to prompt the user for new command action
def prompt_for_new_command(command):
    def submit_action():
        action = action_entry.get()
        feedback_queue.put((command, action))
        new_command_window.destroy()

    new_command_window = tk.Tk()
    new_command_window.title("New Command")

    prompt_label = tk.Label(new_command_window, text="New command detected. Please specify the action:")
    prompt_label.pack(padx=20, pady=20)

    action_entry = tk.Entry(new_command_window, width=50)
    action_entry.pack(padx=20, pady=20)

    submit_button = tk.Button(new_command_window, text="Submit", command=submit_action)
    submit_button.pack(padx=20, pady=20)

    new_command_window.mainloop()

# Function to handle and train on unrecognized commands
def train_on_unrecognized_commands():
    while True:
        command, action = feedback_queue.get()
        if command and action:
            commands.append(command)
            responses.append(action)
            X = vectorizer.fit_transform(commands)
            model.fit(X, responses)
            custom_commands[command] = action
            speak(f"New command '{command}' with action added and trained.")

# Start a thread to handle unrecognized commands training
threading.Thread(target=train_on_unrecognized_commands, daemon=True).start()

# Main function to start the application
if __name__ == "__main__":
    start_spoken_text_display()
