"""
SHARP Anti-Stealer by SharpStealer
"""


import os
import time
import platform
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import time
import sys
value = []
def val():
    """
    Проверка. 

    True:
       Если пользователь выбрал 3 пункт.
    False:
       Если 1 пункт.
    """
    for v in value:
        if v == '3':
            return True
    return False


SUSPICIOUS_DIRECTORIES = {
    "Browsers",
    "Telegram",
    "Files",
    "Discord", 
    "Steam",
    "Minecraft", 
    "browsers",
    "telegram", 
    "files", 
    "steam", 
    "Yandex",
    "Google", 
    "google", 
    "chrome",
    "browser",
    "Screen", 
    "screenshots",
    "screen", 
    "Log", 
    "log", 
    "information",
    "Information",
    "Logs", 
    "logs", 
    "Slimjet",
    "slimjet",
    "vivaldy",
    "Vivaldy",
    "IP",
    "ip",
    "Photos",
    "photos",
    "mine",
    "Mine",
    "Crypto",
    "crypto",
    "cryptowallets",
    "Cryptowallets",
    "Wallets",
    "wallets"
}#директории которые часто создет стиллер во время работы

class DirectoryCreationHandler(FileSystemEventHandler):
    def on_created(self, event):
        if event.is_directory:
            time.sleep(0.1)
            if val() == False:
                print(f"Новая директория создана: {event.src_path}")
            if is_suspicious_directory(event.src_path):
                print(f"Обнаружены папки стиллера: {event.src_path}")

def is_suspicious_directory(directory_path):
    """
    Проверка директории.

    True:
       Если подозрительная.
    False:
       Если подозрений нет.
    """
    base_name = os.path.basename(directory_path)
    return base_name in SUSPICIOUS_DIRECTORIES

def get_all_drives():
    """
    Получение всех дисков.
    """
    system = platform.system()
    drives = []
    if system == "Windows":
        import string
        from ctypes import windll

        bitmask = windll.kernel32.GetLogicalDrives()
        for letter in string.ascii_uppercase:
            if bitmask & 1:
                drive = f"{letter}:\\"
                if os.path.exists(drive):
                    drives.append(drive)
            bitmask >>= 1
    elif system == "Linux" or system == "Darwin":  # Darwin для MacOS
        drives = ["/"]
    return drives

def monitor_drives(drives):
    """
    Мониторинг.
    """
    observers = []
    for drive in drives:
        try:
            event_handler = DirectoryCreationHandler()
            observer = Observer()
            observer.schedule(event_handler, drive, recursive=True)
            observer.start()
            observers.append(observer)
            print(f"Начинаю мониторинг диска: {drive}")
        except PermissionError as e:
            print(f"Ошибка доступа к диску {drive}: {e}")
        except Exception as e:
            print(f"Не удалось запустить мониторинг для {drive}: {e}")
    print("\n\nData:\n")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        for observer in observers:
            observer.stop()
        for observer in observers:
            observer.join()

if __name__ == "__main__":
    res = input("""

░██████╗██╗░░██╗░█████╗░██████╗░██████╗░
██╔════╝██║░░██║██╔══██╗██╔══██╗██╔══██╗
╚█████╗░███████║███████║██████╔╝██████╔╝
░╚═══██╗██╔══██║██╔══██║██╔══██╗██╔═══╝░
██████╔╝██║░░██║██║░░██║██║░░██║██║░░░░░
╚═════╝░╚═╝░░╚═╝╚═╝░░╚═╝╚═╝░░╚═╝╚═╝░░░░░

1 - [начать мониторинг]
2 - [выйти]  
3 - [анти-стилллер (показывать только подозрительные папки)]
                
$=""")
    if res == "1":
        value.clear()
        drives = get_all_drives()
        monitor_drives(drives)
    if res == '2':
        sys.exit()
    if res == '3':
        value.append('3')
        drives = get_all_drives()
        monitor_drives(drives)
