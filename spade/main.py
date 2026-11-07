from spade.ui.app import SPADEApp
from spade.mock_printer import MockPrinter
from spade.moonraker import Moonraker

def main():
    printer = Moonraker()  
    app = SPADEApp(printer)
    app.mainloop()

if __name__ == "__main__":
    main()