import tkinter as tk

class SPADEApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("SPADE Application")
        self.geometry("900x600")
        self.configure(bg="#F3F4F6")
        self.overrideredirect(True)
        self.create_header()
        self.create_layout()

    def create_header(self):
        header = tk.Frame(self, bg="#1D405F", height=45)
        header.pack(fill="x")
        header.pack_propagate(False)

        title = tk.Label(header, text="SPADE Application", bg="#1D405F", fg="white", font=("Arial", 16, "bold"))
        title.pack(side="left", padx=20, pady=12)

        exit_button = tk.Button(header, text="X", bg="#1D405F", fg="white", font=("Arial", 14, "bold"), command=self.destroy)
        exit_button.pack(side="right", padx=20, pady=5)

        header.bind("<ButtonPress-1>", self.start_move)
        header.bind("<B1-Motion>", self.move_window)
        title.bind("<ButtonPress-1>", self.start_move)
        title.bind("<B1-Motion>", self.move_window)

    def start_move(self, event):
        self.drag_x = event.x_root - self.winfo_x()
        self.drag_y = event.y_root - self.winfo_y()
        
    def move_window(self, event):
        x = event.x_root - self.drag_x
        y = event.y_root - self.drag_y
        self.geometry(f"+{x}+{y}")

    def create_layout(self):
        body = tk.Frame(self, bg="#FFFFFF")
        body.pack(fill="both", expand=True)

        self.sidebar = tk.Frame(body, bg="#F0F2F5", width=160, highlightbackground="#D1D5DB", highlightthickness=1)
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)

        self.sidebar_monitor_button = tk.Button(self.sidebar, text="Monitor", font=("Arial", 14, "bold"))
        self.sidebar_monitor_button.pack(pady=10, padx=10, fill="x")
        self.sidebar_settings_button = tk.Button(self.sidebar, text="Settings", font=("Arial", 14, "bold"))
        self.sidebar_settings_button.pack(pady=10, padx=10, fill="x")
        self.sidebar_event_history_button = tk.Button(self.sidebar, text="Event History", font=("Arial", 14, "bold"))
        self.sidebar_event_history_button.pack(pady=10, padx=10, fill="x")
        self.sidebar_help_button = tk.Button(self.sidebar, text="Help", font=("Arial", 14, "bold")) 
        self.sidebar_help_button.pack(pady=10, padx=10, fill="x")

        self.status_pannel = tk.Frame(body, bg="#FAFAFA", width=220)
        self.status_pannel.pack(side="right", fill="y")
        self.status_pannel.pack_propagate(False)

        self.main_content = tk.Frame(body, bg="#FFFFFF", highlightbackground="#D1D5DB", highlightthickness=1)
        self.main_content.pack(side="left", fill="both", expand=True)
