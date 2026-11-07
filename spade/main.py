from spade.ui.app import SPADEApp
from spade.mock_printer import MockPrinter

def main():
    simulated_printer = MockPrinter()
    simulated_printer.connect()  
    app = SPADEApp(simulated_printer)
    app.after(5000, simulated_printer.disconnect)  # Simulate printer disconnect after 5 seconds
    app.mainloop()

if __name__ == "__main__":
    main()