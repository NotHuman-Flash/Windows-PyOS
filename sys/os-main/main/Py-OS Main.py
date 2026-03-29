import tkinter as tk
import os
import sys
import calendar
import datetime
import serial
global exit_timer

root = tk.Tk()
root.attributes('-fullscreen', True)
root.configure(bg='white')

output = tk.Text(root, fg="white", bg="black", font=("Helvetica", 15), insertbackground="white")
output.pack(fill="both", expand=True) 

entry = tk.Entry(root, fg="white", bg="black", font=("Helvetica", 15), insertbackground="yellow")
entry.pack(fill="x")
entry.focus_set()

mode = "command" 
exit_timer = 0

def print(text):
    output.insert(tk.END, text + "\n")
    output.see(tk.END)

def process_command(event=None):
    global mode, exit_timer

    command = entry.get().strip().lower()
    entry.delete(0, tk.END)

    if not command:
        return

    print("user:   " + command)
    if command.startswith("calendar"):
        if "::" in command:
            parts = command.split("::")
            topic1 = parts[1].strip() if len(parts) > 1 else ""
            topic2 = parts[2].strip() if len(parts) > 2 else ""
            if topic1 == "day":
                print(f"day: {datetime.datetime.now().strftime('%A')}")
            if topic1 == "month":
                print(f"month: {datetime.datetime.now().strftime('%B')}")
            if topic1 == "year":
                print(f"year: {datetime.datetime.now().strftime('%Y')}")
            if topic1 == "week":
                print(f"week number: {datetime.datetime.now().strftime('%U')}")
            if topic1 == "calendar":
                if topic2 == "month":
                    now = datetime.datetime.now()
                    print(calendar.month(now.year, now.month))
                if topic2 == "year":
                    now = datetime.datetime.now()
                    print(calendar.calendar(now.year))
                if topic2 == "week":
                    now = datetime.datetime.now()
                    print(f"week number: {datetime.datetime.now().strftime('%U')}")
    if command.startswith("exit"):
        exit_topics = {
            "timer": "",
            "os": ""
        }
        if "::" in command:
            parts = command.split("::")
            topic1 = parts[1].strip() if len(parts) > 1 else ""
            topic2 = parts[2].strip() if len(parts) > 2 else ""
            topic3 = parts[3].strip() if len(parts) > 3 else ""

            if topic1 == "os":
                if topic2 == "timer":
                    exit_timer = int(topic3)
                    countdown()
                if topic2 == "os":
                    exit_timer = 10
                    countdown()
                    
            else:
                print(f"unknown command: {topic1}")
        else:
            print("available commands:")
            for cmd in exit_topics.keys():
                print(f"  {cmd}")
            print("use 'help :: all' to see all help, or 'help :: <command> for specific help.")
            
    elif command == "version":
        print("os version: 0.0.2-alpha (FIRST PUBLIC RELEASE)\n"
        "build date: 2026-03-22\n"
        "author: nothuman\n"
        "what's new? PyOS now has date capabilities! fixed bugs, too")
    
    elif command == "clear":
        output.delete(1.0, tk.END)
    
    elif command.startswith("usb"):
        if "::" in command:
            parts = command.split("::")
            topic1 = parts[1].strip() if len(parts) > 1 else ""
            topic2 = parts[2].strip() if len(parts) > 2 else ""
            topic3 = parts[3].strip() if len(parts) > 3 else ""
            if topic1 == "see":
                if topic2 == "data":
                    try:
                        ser = serial.Serial(topic3, 9600, timeout=1)
                        ser.flush()
                        print("reading from USB...")
                        while True:
                            if ser.in_waiting > 0:
                                line = ser.readline().decode('utf-8').rstrip()
                                print(f"USB data: {line}")
                    except Exception as e:
                        print(f"error reading USB: {e}")
    
    elif command.startswith("open"):
        if "::" in command:
            parts = command.split("::")
            path = parts[1].strip() if len(parts) > 1 else ""
            
            if path:
                try:
                    if os.path.isfile(path):
                        os.startfile(path)
                        print(f"opened file: {path}")
                    elif os.path.isdir(path):
                        os.startfile(path)
                        print(f"opened folder: {path}")
                        print(f"folder contents:")
                        for item in os.listdir(path):
                            item_path = os.path.join(path, item)
                            item_type = "folder" if os.path.isdir(item_path) else "file"
                            if item_type == "folder":
                                item_icon = "📁"
                            else:
                                item_icon = "📄"
                            print(f"  {item_icon}: [{item_type}] {item}")
                    else:
                        print(f"path not found: {path}")
                except Exception as e:
                    print(f"error opening: {e}")
            else:
                print("usage: open :: <path>")
        else:
            print("usage: open :: <path>")

    elif command.startswith("help"):
        help_topics = {
            "exit": "exits the os. usage: exit :: os or exit :: os :: timer",
            "clear": "clears the output screen.",
            "open": "opens a file or folder. usage: open :: <path>",
            "help": "display help information. use 'help :: all' to see all commands, or 'help :: <command>' for specific help.",
        }
        
        if "::" in command:
            parts = command.split("::")
            topic = parts[1].strip() if len(parts) > 1 else ""
            
            if topic == "all":
                print("available commands:")
                for cmd, desc in help_topics.items():
                    print(f"  {cmd}: {desc}")
            elif topic in help_topics:
                print(f"{topic}: {help_topics[topic]}")
            else:
                print(f"unknown command: {topic}")
        else:
            print("available commands:")
            for cmd in help_topics.keys():
                print(f"  {cmd}")
            print("use 'help :: all' to see all help, or 'help :: <command>' for specific help.")

def countdown():
    global exit_timer
    if exit_timer > 0:
        print(f"exiting in {exit_timer}")
        exit_timer -= 1
        root.after(1000, countdown)
    else:
        print("exited to windows.")
        root.destroy()
        sys.exit(0)


entry.bind("<Return>", process_command)
root.bind("<Return>", process_command)

# Optional button for users who may have trouble with Enter in fullscreen
btn = tk.Button(root, text="Send", fg="white", bg="gray20", command=process_command)
btn.pack(fill="x")

print("booting...")
print("welcome to the os. type 'help' to see a list of commands, and 'exit-os' to exit into windows.")

root.mainloop()