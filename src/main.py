from readGUI import Read
from pdfMonitor import Watchdog

if __name__ == "__main__":
    Watchdog().Start()  # begin looking for new PDFs
