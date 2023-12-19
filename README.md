# ShadowSpy-Invisible-Keystroke-Tracker-with-Email-Alerts-and System Information Gatherer


This script is a keylogger and system information gatherer built in Python. It captures keystrokes, takes periodic screenshots, and collects system information, sending reports via email.

## Features

- **Keylogger:** Records alphanumeric keystrokes and stores them in a text file.
- **Screenshot Capture:** Periodically captures screenshots and saves them as images.
- **System Information:** Gathers system information including OS, hardware, network details, etc.
- **Email Reports:** Sends collected data (keystrokes, screenshots, system info) via email.

## Prerequisites

- Python 3.x
- Required Python packages: `pynput`, `Pillow`, `requests`, `pyperclip`

## Setup

1. Clone the repository:

   ```bash
   git clone https://github.com/your-username/keylogger-system-info.git
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Configure the script:

   - Open `main.py` and update the email credentials (`from_email`, `password`) and recipient email (`to_email`).
   - Ensure the SMTP server and port are correct.

4. Run the script:

   ```bash
   python main.py
   ```

## Configuration

- `OUTPUT_FOLDER`: Specifies the folder where files (keystrokes, screenshots, system_info) will be saved.
- `SCREENSHOT_INTERVAL`: Interval for periodic screenshot capture (in seconds).
- `SYSTEM_INFO_INTERVAL`: Interval for sending system information via email (in seconds).

## Disclaimer

This script is intended for educational purposes only. Use responsibly and only on systems you own or have explicit permission to monitor.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
```

Replace placeholders like `your-username` and update sections as needed. Additionally, include a `LICENSE` file if you choose a license for your project.

This README provides a brief overview of the script's features, setup instructions, configuration details, and a disclaimer. You can enhance or modify it based on your specific project details and requirements.
