import time
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler
from readGUI import Read


class Consumer:
    def Start(self):
        # Create event handler (what to do when PDF received)
        patterns = ["*"]
        ignore_patterns = None
        ignore_directories = True
        case_sensitive = False
        eventHandler = PatternMatchingEventHandler(patterns, ignore_patterns, ignore_directories, case_sensitive)
        eventHandler.on_created = Read().on_files_received

        # Create observer (watches for new PDFs that are received)
        path = "../labFiles/"
        observer = Observer()
        observer.schedule(eventHandler, path, recursive=False)

        observer.start()

        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            observer.stop()
            observer.join()
