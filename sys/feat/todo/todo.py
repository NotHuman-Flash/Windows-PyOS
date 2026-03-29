command = input("to-do:   ").lower()
global to_do
if command.startswith("add"):
    if "::" in command:
        parts = command.split("::")
        topic1 = parts[1].strip() if len(parts) > 1 else ""
        topic2 = parts[2].strip() if len(parts) > 2 else ""
        todo = [
            topic1, topic2
        ]
        print(todo)
    else:
        print("err: unkown")
if command.startswith("remove"):
    if "::" in command:
        parts = command.split("::")
        topic1 = parts[1].strip() if len(parts) > 1 else ""
        if todo == 0:
            print("err: nothing in todo")
        elif topic1.isdigit:
            todo -= topic1
        else:
            print("err: not a digit.")
    else:
        print("err: unkown")