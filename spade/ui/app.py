import tkinter as tk

class SPADEApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("SPADE Application")
        self.geometry("400x300")
        self.create_widgets()

    def create_widgets(self):
        self.label = tk.Label(self, text="Welcome to SPADE!")
        self.label.pack(pady=20)

        self.button = tk.Button(self, text="Click Me", command=self.on_button_click)
        self.button.pack(pady=10)

    def on_button_click(self):
        self.label.config(text="Button Clicked!")