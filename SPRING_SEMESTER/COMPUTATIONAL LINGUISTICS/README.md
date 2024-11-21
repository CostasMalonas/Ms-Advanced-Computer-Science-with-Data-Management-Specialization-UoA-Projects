# Voice-Controlled Mouse Navigation Application

## Project Overview
This project introduces a **Voice-Controlled Mouse Navigation System**, allowing users to control their mouse, interact with search engines, and navigate websites using only voice commands. The application is designed to assist users with accessibility needs and those seeking hands-free interaction with computers and the internet. The system supports voice-based mouse navigation, text input, and web interaction.

---

## Features
- **Mouse Control**: Navigate the mouse cursor (e.g., move up, down, left, right).
- **Search Automation**: Perform Google searches by speaking the desired term.
- **Typing Assistance**: Type text into search bars or other fields using voice commands.
- **Click and Press**: Perform clicks on elements or press buttons using their text labels.
- **Precision Navigation**: Enable a transparent grid for accurate cursor placement.
- **Multilingual Support**: The application processes Greek commands and converts voice to text.

---

## Voice Commands

### Mouse Movement
- **Πάνω/Κάτω/Αριστερά/Δεξιά [αριθμός]**: Move the mouse in the specified direction by the given number of pixels.  
  **Example**: *"Δεξιά 100"* moves the cursor 100 pixels to the right.

---

### Search and Typing
- **Νέα Αναζήτηση**: Start a new search.  
- **Type [κείμενο]**: Type the specified text into a search bar.  
- **Delete/Διαγραφή**: Clear existing text from a search bar.

---

### Click and Press
- **Click/Κλικ**: Perform a mouse click on the current cursor position.  
- **Click [κείμενο]**: Click on a link with the specified text.  
- **Press [κείμενο]**: Press a button element with the specified text (e.g., *"Press Accept Cookies"*).

---

### Grid Management
- **Open/Open Grid**: Enable a transparent grid for more precise navigation.  
- **Close/Close Grid**: Disable the grid.

---

### Other Commands
- **Πίσω**: Go back to the previous page.  
- **Exit**: Close the application.

---

## Instructions to Run
1. Install Python 3 and required dependencies:
   bash
   **pip install -r requirements.txt**

## Navigate to the directory containing the program.
**Execute the application by running the main.py script**:
bash --> python main.py
