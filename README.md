# Password-Manager
A simple password manager application using tkinter for the GUI and cryptography.fernet for encryption

## Features
- Add Password: Enter website/app name, username, and password to securely store them.
- View passwords: Decrypt and view stored passwords using a master key.
- Encryption: Uses Fernet encryption for secure storage in a CSV file.

## Installation
- Make sure you have the latest version of Python installed
  ```bash
  git clone <repo-url>
  ```

  ```bash
  pip install -r requirements.txt
  ```
- Run the application
  ```bash
  python password_manager.py
  ```
- Use the application by adding passwords or viewing stored passwords with the master key, you can change
  the master key to whatever you want. It's "masterkey" by default
