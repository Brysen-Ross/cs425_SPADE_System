import tkinter as tk
from spade.ui.status_panel import StatusPanel
from spade.ui.setup_view import SetupView

class SPADEApp(tk.Tk):
    def __init__(self, printer, camera):
        super().__init__()
        self.printer = printer
        self.camera = camera
        self.printer_connected = False
        self.title("SPADE Application")
        self.geometry("900x600")
        self.resizable(True,True)
        self.configure(bg="#F3F4F6")
        self.create_header()
        self.create_layout()
        self.show_setup()
        self.after(1000, self.update_printer_status)
        self.after(1000, self.update_camera_status)
        self.after(1100, self.update_live_camera_preview)
        
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

        self.status_panel = StatusPanel(body)
        self.status_panel.grid(row=0, column=2, sticky="nsew")

    def clear_main_content_frame(self):
        for widget in self.main_content.winfo_children():
            widget.destroy()

    def show_setup(self):
        self.clear_main_content_frame()
        self.setup_view = SetupView(self.main_content)
        self.setup_view.pack(fill="both", expand=True)
        self.setup_view.update_printer_status(self.printer_connected)
        self.setup_view.update_camera_status(self.camera.connected)
        self.setup_view.update_connection_warning(self.printer_connected, self.camera.connected)

    def update_printer_status(self):
        status = self.printer.get_status()
        self.printer_connected = status.connected
        self.status_panel.update_printer_status(status.connected)
        if hasattr(self, "setup_view") and self.setup_view.winfo_exists():
            self.setup_view.update_printer_status(status.connected)
            self.setup_view.update_connection_warning(self.printer_connected, self.camera.connected)
        self.after(3000, self.update_printer_status)

    def update_camera_status(self):
        if not self.camera.connected:
            self.camera.connect()
        self.status_panel.update_camera_status(self.camera.connected)
        if hasattr(self, "setup_view") and self.setup_view.winfo_exists():
            self.setup_view.update_camera_status(self.camera.connected)
            self.setup_view.update_connection_warning(self.printer_connected, self.camera.connected)
        self.after(3000, self.update_camera_status)
    
    def update_live_camera_preview(self):
        if self.camera.connected:
            frame = self.camera.get_frame()
            self.status_panel.update_camera_preview(frame)
        else:
            self.status_panel.update_camera_preview(None)
        self.after(67, self.update_live_camera_preview)