# MRAC Finite-state machine(FSM) Tutorial
Author: [Huanyu Li](https://github.com/HuanyuL), ChatGPT

This repository provides a hands-on tutorial on implementing a finite-state machine (FSM) for the MRAC24/25 Hardware III seminar. It is designed to help students understand and apply FSM concepts through interactive examples using Grasshopper (GH), Rhino (3DM), and Python.

## Prerequisites

Before starting, make sure you have the following set up:

**Python3.9.10**: Download Python3.9.10(for 64-bit windwos) from the following link
 - [Install Python 3.9.10 on windows](https://www.python.org/ftp/python/3.9.10/python-3.9.10-amd64.exe)
 - Run the installer
 - Check the box that says "Add Python 3.9 to PATH"
 - Click Customize installation > make sure pip and venv are selected
 - Proceed with the installation

## Usage
To get started:

1. **Download or Clone the Repository**  
2. **Open File Explorer and Navigate to Your Project Folder**
 - Open File Explorer and locate the folder where you cloned the repository
 - Once inside the folder, hold the Shift key and right-click within the folder window
 - Select "Open PowerShell window here" or "Open Command window here"
3. **Create and Activate a Virtual Environment**  

Now that you're in the project folder, run the following commands:
```
python -m venv fsm_env
fsm_env\Scripts\activate
```
4. **Install Dependencies**
```
pip install -r requirements.txt

```
5. **Run the main tracking script**
```
python main_tracking.py
```

## FSM Structure

This script implements a vision-based Finite State Machine (FSM) for controlling interactive tasks using hand gestures and visual detection through a webcam. The system is designed to transition through a series of predefined states based on visual cues and timing, enabling hands-free interaction in real-time.

**FSM States**

| State         | Description                                                                 |
|---------------|-----------------------------------------------------------------------------|
| `start`       | Initial state. Waits for a **thumbs-up** gesture to begin the interaction. |
| `challenge1`  | User must hover their hand over a **colored circle** within a time limit.   |
| `retry`       | User must perform a **circular hand gesture** to restart the challenge.     |
| `win`     | Final state on successful task completion.                                  |
| `fail`        | Triggered if the user times out or performs invalid actions.                |

## Vision-Based Event Detection

- **Thumbs-Up Gesture**  
  Detected using MediaPipe's hand landmarks. Used to start the interaction.

- **Hand Over Bubble**  
  Uses HSV-based color detection to find a circle and checks if the hand is inside its bounds.

- **Circular Motion**  
  Hand positions are recorded in a short history buffer. The system calculates the variance from a circular path to detect circular motion for retries.



