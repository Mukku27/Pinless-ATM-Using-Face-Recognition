import warnings
import cv2
import numpy as np
import face_recognition
import mediapipe as mp
import os
import serial
import time
import webbrowser
from collections import defaultdict

warnings.filterwarnings('ignore', message='SymbolDatabase.GetPrototype() is deprecated')

# Initialize serial communication
try:
    ser = serial.Serial('COM3', 9600, timeout=1)  # Replace 'COM3' with your Arduino's serial port
    print("Serial connection established")
except serial.SerialException as e:
    print(f"Error: {e}")
    exit()

# Load images for face recognition
path = 'E:/image_Folder'
images = []
classNames = []
myList = os.listdir(path)
for cl in myList:
    curImg = cv2.imread(f'{path}/{cl}')
    images.append(curImg)
    classNames.append(os.path.splitext(cl)[0])
print(f"Loaded class names: {classNames}")

def findEncodings(images):
    encodeList = []
    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodeList.append(encode)
    return encodeList

encodeListKnown = findEncodings(images)
print('Encoding Complete')

# Initialize Mediapipe Face Mesh
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(max_num_faces=1)
mp_drawing = mp.solutions.drawing_utils

# Initialize face detection
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# List to store recognized names
recognizedNames = []

# Function to run the face recognition and mesh detection
def run_face_recognition():
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Error: Could not open webcam.")
        return

    recognized_name = None

    while True:
        success, img = cap.read()
        if not success:
            print("Error: Failed to read frame from webcam.")
            break

        # Resize and convert image for face recognition
        imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
        imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

        # Perform face recognition
        facesCurFrame = face_recognition.face_locations(imgS)
        encodesCurFrame = face_recognition.face_encodings(imgS, facesCurFrame)

        for encodeFace, faceLoc in zip(encodesCurFrame, facesCurFrame):
            matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
            faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)
            matchIndex = np.argmin(faceDis)

            if matches[matchIndex]:
                recognized_name = classNames[matchIndex].upper()
                if recognized_name not in recognizedNames:
                    recognizedNames.append(recognized_name)
                    print(f"Recognized: {recognized_name}")
                y1, x2, y2, x1 = faceLoc
                y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
                cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.rectangle(img, (x1, y2 - 35), (x2, y2), (0, 255, 0), cv2.FILLED)
                cv2.putText(img, recognized_name, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)

        # Perform face detection
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.1, 4)
        for (x, y, w, h) in faces:
            cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)

        # Perform face mesh detection
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        result = face_mesh.process(imgRGB)
        if result.multi_face_landmarks:
            for face_landmarks in result.multi_face_landmarks:
                mp_drawing.draw_landmarks(
                    image=img,
                    landmark_list=face_landmarks,
                    connections=mp_face_mesh.FACEMESH_TESSELATION,
                    landmark_drawing_spec=None,
                    connection_drawing_spec=mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=1, circle_radius=1)
                )

        # Display the output
        cv2.imshow('Webcam', img)
        if recognized_name:
            break

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    print(f"Recognized names during the session: {recognizedNames}")

    return recognized_name

# Initialize a dictionary to store user balances
user_balances = defaultdict(lambda: 1000)  # Default balance is 1000 for simplicity

def atm_interface(recognized_name):
    while True:
        print("\nWelcome to the ATM")
        print(f"Hello, {recognized_name}!")
        print("1. Balance Inquiry")
        print("2. Withdraw")
        print("3. Deposit")
        print("4. Exit")
        choice = input("Select an option: ")

        if choice == "1":
            print(f"Your current balance is ${user_balances[recognized_name]}")

        elif choice == "2":
            amount = float(input("Enter amount to withdraw: "))
            if user_balances[recognized_name] >= amount:
                user_balances[recognized_name] -= amount
                print(f"Withdrew ${amount}. New balance: ${user_balances[recognized_name]}")
            else:
                print("Insufficient funds!")

        elif choice == "3":
            amount = float(input("Enter amount to deposit: "))
            user_balances[recognized_name] += amount
            print(f"Deposited ${amount}. New balance: ${user_balances[recognized_name]}")

        elif choice == "4":
            print("Thank you for using the ATM. Goodbye!")
            break

        else:
            print("Invalid option. Please try again.")

if __name__ == '_main_':
    # Wait for the 'rfid', 'rfid1', or 'rfid2' message from Arduino
    while True:
        if ser.in_waiting > 0:
            line = ser.readline().decode('utf-8').strip()
            if line == "rfid":
                print("Received 'rfid' message from Arduino. Starting face recognition...")
                recognized_name = run_face_recognition()
                ser.close()
                if recognized_name == 'HEMANTH':
                    if recognized_name:
                        webbrowser.open('http://192.168.43.237:8501')
                        atm_interface(recognized_name)
                else:
                    print("Hemanth face is not detected. Not allowed to access the account.")
                break
            elif line == "rfid1":
                print("Received 'rfid1' message from Arduino. Starting face recognition...")
                recognized_name = run_face_recognition()
                ser.close()
                if recognized_name == 'SAI KUMAR':
                    if recognized_name:
                        webbrowser.open('http://192.168.43.237:8501')
                        atm_interface(recognized_name)
                else:
                    print("Sai Kumar face is not detected. Not allowed to access the account.")
                break
            elif line == "rfid2":
                print("Received 'rfid2' message from Arduino. Starting face recognition...")
                recognized_name = run_face_recognition()
                ser.close()
                if recognized_name == 'BHARATH':
                    if recognized_name:
                        webbrowser.open('http://192.168.43.237:8501')
                        atm_interface(recognized_name)
                else:
                    print("Bharath face is not detected. Not allowed to access the account.")
                break
            else:
                print("No card is detected.")
