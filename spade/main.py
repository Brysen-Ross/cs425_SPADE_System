from spade.ui.app import SPADEApp
from spade.mock_printer import MockPrinter

def main():
    simulated_printer = MockPrinter()
    app = SPADEApp(simulated_printer)
    app.mainloop()

if __name__ == "__main__":
    main()