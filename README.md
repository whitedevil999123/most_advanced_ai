# most_advanced_ai
This AI assistant listens to voice commands, processes them, and performs various tasks such as opening applications, reading text from the screen, clicking on specific screen coordinates, typing text, and more.

Features
Voice command recognition using Google's speech recognition API.
Text-to-speech feedback.
Ability to perform various tasks like clicking on coordinates, typing text, reading from applications, etc.
Custom command addition and execution.
Task recording and replaying.
Requirements
Python Libraries
The following Python libraries are required:

pyautogui: For simulating mouse clicks and typing.
pyperclip: For clipboard operations.
pygetwindow: For window management.
pytesseract: For OCR (Optical Character Recognition).
speech_recognition: For speech recognition.
pyttsx3: For text-to-speech.
scikit-learn: For machine learning.
Pillow: For image operations.
Installation
To install the required Python libraries, you can use pip. Run the following command:

sh
Copy code
pip install -r requirements.txt
Additional Setup for Tesseract
Pytesseract requires Tesseract OCR to be installed on your system.

Windows:

Download the Tesseract installer from here.
Install Tesseract.
Add the Tesseract executable to your system PATH.
Linux:

sh
Copy code
sudo apt-get install tesseract-ocr
macOS:

sh
Copy code
brew install tesseract
Usage
To start the AI assistant, run the script:

sh
Copy code
python your_script_name.py
Voice Commands
Here are some example commands you can use:

"hello"
"how are you"
"what is your name"
"read screen"
"open notepad"
"click at 100, 200"
"type Hello World"
"read from notepad"
"click on OK"
"minimize window"
"make window small"
"cut the window"
"scroll down"
"create file example.txt"
"delete file example.txt"
"search file example.txt"
"start recording"
"stop recording task1"
"replay task task1"
"add custom command test with action speak('test')"
"execute custom command test"
"goodbye"
