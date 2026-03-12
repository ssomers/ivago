from datetime import timedelta
import vobject
import sys

path_in = sys.argv[1]
path_out = path_in.replace("calendar", "todos")
if path_in == path_out:
    print("wa est?")
    sys.exit(1)

with open(path_in, "r") as f:
    source = vobject.readOne(f.read())
todos = vobject.iCalendar()
for event in source.components():
    summary = event.summary.value
    dtstart = event.dtstart.value
    if summary in ["GLAS", "PAPIER", "PMD", "RESTAFVAL"]:
        todo = todos.add('vtodo')
        todo.add("uid").value = event.uid.value
        todo.add("summary").value = summary
        todo.add("dtstart").value = dtstart - timedelta(days=1)
        todo.add("due").value = dtstart
    elif summary not in ["GFT", "GROFVUIL", "KERSTBOMEN"]:
        print(f"Onbekend type \"{summary}\" overgeslagen")

count = sum(1 for _ in todos.components())
if count:
    with open(path_out, "w") as f:
        f.write(todos.serialize())
print(f"{count} todo's geschreven in {path_out}")
