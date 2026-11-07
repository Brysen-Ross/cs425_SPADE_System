import tkinter as tk


class SPADEApp(tk.Tk):
    def __init__(self, printer):
        super().__init__()
        self.printer = printer
        self.title("SPADE Application")
        self.geometry("900x600")
        self.resizable(True,True)
        self.configure(bg="#F3F4F6")
        self.create_header()
        self.create_layout()
        self.show_setup()
        self.after(1000, self.update_printer_status)
        
    def create_header(self):
        header = tk.Frame(self, bg="#1D405F", height=60)
        header.pack(fill="x")
        header.pack_propagate(False)

        title = tk.Label(header, text="3D Printing Failure Detection", bg="#1D405F", fg="white", font=("Arial", 16, "bold"))
        title.pack(side="left", padx=20, pady=12)

    def create_layout(self):
        body = tk.Frame(self, bg="#FFFFFF")
        body.pack(fill="both", expand=True)
        body.grid_columnconfigure(0, weight=20, uniform="panels")
        body.grid_columnconfigure(1, weight=55, uniform="panels")
        body.grid_columnconfigure(2, weight=25, uniform="panels")
        body.grid_rowconfigure(0, weight=1)

        self.sidebar = tk.Frame(body, bg="#F0F2F5", width=160, highlightbackground="#D1D5DB", highlightthickness=1)
        self.sidebar.grid(row=0, column=0, sticky="nsew")

        self.sidebar_setup_button = tk.Button(self.sidebar, text="Setup", font=("Arial", 14, "bold"), command=self.show_setup)
        self.sidebar_setup_button.pack(pady=10, padx=10, fill="x")
        self.sidebar_monitor_button = tk.Button(self.sidebar, text="Monitor", font=("Arial", 14, "bold"))
        self.sidebar_monitor_button.pack(pady=10, padx=10, fill="x")
        self.sidebar_event_history_button = tk.Button(self.sidebar, text="Event History", font=("Arial", 14, "bold"))
        self.sidebar_event_history_button.pack(pady=10, padx=10, fill="x")
        self.sidebar_help_button = tk.Button(self.sidebar, text="Help", font=("Arial", 14, "bold")) 
        self.sidebar_help_button.pack(pady=10, padx=10, fill="x")

        self.main_content = tk.Frame(body, bg="#FFFFFF", highlightbackground="#D1D5DB", highlightthickness=1)
        self.main_content.grid(row=0, column=1, sticky="nsew")

        self.status_panel = tk.Frame(body, bg="#FAFAFA", width=220)
        self.status_panel.grid(row=0, column=2, sticky="nsew")

    def clear_main_content_frame(self):
        for widget in self.main_content.winfo_children():
            widget.destroy()

    def show_setup(self):
        self.clear_main_content_frame()

        setup_title =tk.Label(self.main_content, text="Setup", bg="#FFFFFF", font=("Arial", 20, "bold"))
        setup_title.pack(anchor="w", padx=16, pady=(16, 4))

        setup_description = tk.Label(self.main_content, text="Connect the printer and camera before monitoring starts.", bg="#FFFFFF", font=("Arial", 14))
        setup_description.pack(anchor="w", padx=16)

        printer_frame = tk.Frame(self.main_content, bg="#FFFFFF", highlightbackground="#D1D5DB", highlightthickness=1)
        printer_frame.pack(fill="x", padx=16, pady=(20, 0), ipady=12)

        connect_printer_title = tk.Label(printer_frame, text="Printer Connection", bg="#FFFFFF", fg="#1D344A", font=("Arial", 12, "bold"))
        connect_printer_title.grid(row=0, column=0, sticky="w", padx=16, pady=(10, 2))

        self.printer_status_label = tk.Label(printer_frame, text="Not Connected", bg="#FFFFFF", fg="#B7791F", font=("Arial", 10))
        self.printer_status_label.grid(row=1, column=0, sticky="w", padx=16)

        connect_printer_button = tk.Button(printer_frame, text="Connect", bg="#0080FE", fg="white", font=("Arial", 10, "bold"), command=self.connect_printer)
        connect_printer_button.grid(row=1, column=1, rowspan=2, sticky="e", padx=150)

        camera_frame = tk.Frame(self.main_content, bg="#FFFFFF", highlightbackground="#D1D5DB", highlightthickness=1)
        camera_frame.pack(fill="x", padx=16, pady=(16, 0), ipady=12)

        connect_camera_title = tk.Label(camera_frame, text="Camera Connection", bg="#FFFFFF", fg="#1D344A", font=("Arial", 12, "bold"))
        connect_camera_title.grid(row=0, column=0, sticky="w", padx=16, pady=(10, 2))

        self.camera_status_label = tk.Label(camera_frame, text="Not Connected", bg="#FFFFFF", fg="#B7791F", font=("Arial", 10))
        self.camera_status_label.grid(row=1, column=0, sticky="w", padx=16)

        connect_camera_button = tk.Button(camera_frame, text="Connect", bg="#0080FE", fg="white", font=("Arial", 10, "bold"))
        connect_camera_button.grid(row=1, column=1, rowspan=2, sticky="e", padx=150)

        

    def connect_printer(self):
        success = self.printer.connect()
        if success:
            self.printer_status_label.config(text="Connected", fg="#16803C")
        else:
            self.printer_status_label.config(text="Not Connected", fg="#B7791F")

    def update_printer_status(self):
        status = self.printer.get_status()
        if(hasattr(self, "printer_status_label") and self.printer_status_label.winfo_exists()):
            if status.state == "Offline":
                self.printer_status_label.config(text="Not Connected", fg="#B7791F")
            else:
                self.printer_status_label.config(text="Connected", fg="#16803C")
        self.after(1000, self.update_printer_status)

    def connect_camera(self):
        pass