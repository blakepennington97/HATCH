import time
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler
from readGUI import Read


class Watchdog:
    def Start(self):
        # Create event handler (what to do when PDF received)
        patterns = ["*"]
        ignore_patterns = None
        ignore_directories = True
        case_sensitive = False
        eventHandlerPDF = PatternMatchingEventHandler(patterns, ignore_patterns, ignore_directories, case_sensitive)
        reader = Read()
        eventHandlerPDF.on_created = reader.on_PDF_received

        # Create observer (watches for new PDFs that are received)
        path = "../receivedPDFs/"
        observer = Observer()
        observer.schedule(eventHandlerPDF, path, recursive=False)

        observer.start()

        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            observer.stop()
            observer.join()
