# Pinless ATM with Secure Web Interface Using Face Recognition

## Project Overview
This project aims to create a secure ATM system that uses face recognition technology instead of traditional PINs for user authentication. The system integrates hardware and software components to offer a user-friendly banking experience.

## Features
- **Face Recognition Authentication**: Uses OpenCV and Mediapipe for secure and convenient user verification.
- **ATM Interface**: Options for balance inquiry, withdrawal, deposit, and transaction history.
- **Web Interface**: Built with Streamlit, allowing users to manage accounts, view balances, make transactions, and review history.
- **User Data Security**: User data stored securely in an SQLite database.

## Components

### Hardware Components
- **Arduino Uno**: Central controller for the ATM hardware.
- **LCD Display and Keypad**: Facilitate user interaction and provide feedback.
- **RFID Module and Reader**: Reads the unique ID of the user and verifies it against the face recognition system.

### Software Components
- **Python-based Face Recognition**: Using OpenCV and face_recognition libraries.
- **Streamlit-based Web Application**: For user interaction.
- **SQLite Database**: For user data and transaction history.
- **Arduino Code**: For handling ATM operations.

## Setup and Installation

### Hardware Setup
1. Connect the LCD display, keypad, and RFID module to the Arduino as per the pin configuration in the Arduino code.
2. Upload the Arduino code to the Arduino board.

### Software Setup
1. Install Python 3.12 from the official website if you haven't already.
2. Clone the repository or download the project files.
3. Open a terminal in the project directory and run:
    ```sh
    pip install -r requirements.txt
    ```
4. Set up the SQLite database:
    ```sh
    python database.py
    ```
5. Ensure you have face images stored in the specified folder for face recognition.
6. Start the web interface:
    ```sh
    streamlit run app.py
    ```

## Usage

### Running the Web Application
1. Start the web application:
    ```sh
    streamlit run webapp.py
    ```
2. Open the web application in your browser and log in with your credentials.

### Face Recognition and ATM Interface
1. Run the face recognition script:
    ```sh
    python face_recognition.py
    ```
2. Follow the on-screen instructions for authentication and ATM operations.

## Project Structure
- `ArduinoCode.ino`: Contains the Arduino code for controlling the ATM hardware.
- `app.py`: Streamlit web app for the user interface.
- `database.py`: Script to set up the SQLite database.
- `requirements.txt`: Lists all the Python dependencies required for the project.

## Contributing
Contributions are welcome! Please create a pull request with your proposed changes.

## License
This project is licensed under the MIT License. See the LICENSE file for more details.

## Authors
- [Mukesh Vemulapalli](https://github.com/VemulapalliMukesh27)

## Contact
For any questions or feedback, please contact [vemulapallimukesh@gmail.com](mailto:vemulapallimukesh@gmail.com).
