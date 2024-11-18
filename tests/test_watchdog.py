import time
from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer

def on_created(event):
    print("created")

def on_deleted(event):
    print("deleted")

def on_modified(event):
    print("modified")

def on_moved(event):
    print("moved")

if __name__ == "__main__": 
    event_handler = FileSystemEventHandler()


    # Calling functions
    event_handler.on_created = on_created
    event_handler.on_modified = on_modified
    event_handler.on_deleted = on_deleted
    event_handler.on_moved = on_moved

    path="F:/Multimedia/Divertissement/Serie/"
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)

    observer.start()
    try:
        print("#####Monitoring#####")
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        print("#####Done#####")
    observer.join()