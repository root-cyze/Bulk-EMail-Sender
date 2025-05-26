# Bulk E-Mail Sender

## Description

This project is a Python-based tool designed for sending mass emails. It allows users to send emails quickly and efficiently while providing features to minimize the risk of spam filters blocking the messages.

## Visual

![IMG_20250526_073109~2](https://github.com/user-attachments/assets/ead7fc86-c9d4-4c42-a9af-a3ea9683dd95)


## Features

- Sends bulk emails to a list of recipients.
- Supports multiple sender email accounts to reduce spam flagging.
- Configurable email content and sending options.
- Reads from a `mail.txt` file containing email addresses and their SMTP keys for authentication.

## Important Note

Users must ensure they understand the `mail.txt` file format before running the program, as it is essential for the tool’s functionality.

## How to Get SMTP Key?

1. **Enable Two-Step Verification:** Activate two-step verification on your Google account.
2. **Create an App Password:** Search for "app password" in your Google account settings.
3. **Generate SMTP Password:** Create an app password named "SMTP" and copy it.
4. **SMTP Password Ready:** Use this password for SMTP authentication in the tool.

## `mail.txt` File Format

The `mail.txt` file should be structured as follows:

- Each line contains one entry in the format:
email:smtp_key

**Example:**

example1@example.com:smtp_key_1 example2@example.com:smtp_key_2 example3@example.com:smtp_key_3

*Ensure there are no extra spaces before or after the entries. Each email and SMTP key pair must be on its own line.*

## Installation

```
git clone https://github.com/root-cyze/Bulk-EMail-Sender
```
```
cd Bulk-EMail-Sender
```
```
python sender.py
```

Important Notes

Using multiple email accounts helps prevent spam filters from flagging your emails.

Make sure Python is installed and properly configured in your environment.

Use this tool responsibly and only for legitimate purposes.


Contribution

Contributions are welcome! Feel free to submit issues or pull requests to improve the project.
