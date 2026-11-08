from spade.ui.app import SPADEApp
from spade.mock_printer import MockPrinter
from spade.moonraker import Moonraker
from spade.camera import Camera

def main():
    printer = Moonraker()  
    camera = Camera()
    app = SPADEApp(printer, camera)
    app.mainloop()

if __name__ == "__main__":
    main()