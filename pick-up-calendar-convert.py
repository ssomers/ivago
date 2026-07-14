import collections
import datetime
import vobject
import sys

path_in: str = sys.argv[1]
path_out: str = path_in.replace("-calendar-", "-todos-")
if path_in == path_out:
    print("geen -calendar- in pad!?")
    sys.exit(1)

todos = vobject.iCalendar()
with open(path_in, "r") as f:
    calendar = vobject.readOne(f.read())
for event in calendar.components():
    match event.summary.value:
        case "GLAS" | "PAPIER" | "PMD" | "RESTAFVAL":
            todo = todos.add("vtodo")
            todo.add(event.uid)
            todo.add(event.summary)
            dtstart = event.dtstart.value
            todo.add("dtstart").value = dtstart - datetime.timedelta(days=1)
            todo.add("due").value = dtstart
        case "GFT" | "GROFVUIL" | "KERSTBOMEN":
            pass
        case who:
            print(f'Onbekende soort "{who}"')

counts = collections.Counter([c.summary.value for c in todos.components()])
if counts:
    with open(path_out, "w", newline="\n") as f:
        f.write(todos.serialize())
    print(f"{path_out}:")
    for summary, count in counts.most_common():
        print(f"\t{count} {summary}")
