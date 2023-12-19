# ShadowSpy-Invisible-Keystroke-Tracker-with-Email-Alerts-and System Information Gatherer

This Python script acts as a keylogger and system information gatherer. It captures keystrokes, takes periodic screenshots, and collects system information to assist in troubleshooting and monitoring.

## Features

- **Keylogger:** Records alphanumeric keystrokes and stores them in a text file (`keystrokes.txt`).
- **Screenshot Capture:** Periodically captures screenshots and saves them as `screenshot.png`.
- **System Information:** Gathers and logs various system details into `system_info.txt`.

## Prerequisites

- Python 3.x
- Required Python packages: `pynput`, `Pillow`, `requests`, `pyperclip`, `geopy`

## Installation

1. Clone this repository:

   ```bash
   git clone https://github.com/
   cd 
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Configure the script:

   - Update the `OUTPUT_FOLDER` variable in `main.py` to specify the folder where output files will be saved.
   - Replace email credentials in the `send_email` function with your own SMTP server and email details.

## Usage

1. Run the script:

   ```bash
   python main.py
   ```

2. The keylogger and system information gathering will start in separate threads.

3. Press `ESC` to stop the keylogger.

## Notes

- Use this script responsibly and only for educational or authorized purposes.
- Be cautious not to violate privacy laws or ethical standards.

## Author

Abdullah Alsowadi

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
```
