import tkinter as tk
from pathlib import Path
from spade.ui.status_panel import StatusPanel
from spade.ui.setup_view import SetupView
from spade.ui.recorder import WindowRecorder
from spade.monitoring.api import Monitor, Preview

class SPADEApp(tk.Tk):
    def __init__(self, printer, monitor: Monitor):
        super().__init__()
        self.printer = printer
        self.monitor = monitor
        self.printer_connected = False
        self.recorder = None
        self.recordings_folder = Path.home() / "Documents" / "SPADE_UI_Recordings"
        self.title("SPADE Application")
        self.geometry("1050x600")
        self.resizable(True,True)
        self.configure(bg="#F3F4F6")
        self.create_header()
        self.create_layout()
        self.show_setup()
        self.protocol("WM_DELETE_WINDOW", self.close_application)
        self.after(800, self.start_recording)
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
        body.grid_columnconfigure(0, weight=18, uniform="panels")
        body.grid_columnconfigure(1, weight=40, uniform="panels")
        body.grid_columnconfigure(2, weight=42, uniform="panels")
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

        self.resume_video_button = tk.Button(self.sidebar, text="Resume Video", font=("Arial", 12, "bold"), bg="#0080FE", fg="white", command=self.monitor.resume, state="disabled")
        self.resume_video_button.pack(pady=20, padx=10, fill="x")

        self.main_content = tk.Frame(body, bg="#FFFFFF", highlightbackground="#D1D5DB", highlightthickness=1)
        self.main_content.grid(row=0, column=1, sticky="nsew")

        self.status_panel = StatusPanel(body, on_live_camera=self.switch_to_live_camera, on_recorded_video=self.switch_to_recorded_video)
        self.status_panel.grid(row=0, column=2, sticky="nsew")

    def clear_main_content_frame(self):
        for widget in self.main_content.winfo_children():
            widget.destroy()

    def show_setup(self):
        self.clear_main_content_frame()
        self.setup_view = SetupView(self.main_content)
        self.setup_view.pack(fill="both", expand=True)
        self.setup_view.update_printer_status(self.printer_connected)
        self.setup_view.update_camera_status(self.monitor.connected)
        self.setup_view.update_connection_warning(self.printer_connected, self.monitor.connected)

    def update_printer_status(self):
        status = self.printer.get_status()
        self.printer_connected = status.connected
        self.status_panel.update_printer_status(status.connected)
        if hasattr(self, "setup_view") and self.setup_view.winfo_exists():
            self.setup_view.update_printer_status(status.connected)
            self.setup_view.update_connection_warning(self.printer_connected, self.monitor.connected)
        self.after(3000, self.update_printer_status)

    def update_camera_status(self):
        if not self.monitor.connected:
            self.monitor.connect()
        self.status_panel.update_camera_status(self.monitor.connected)
        if hasattr(self, "setup_view") and self.setup_view.winfo_exists():
            self.setup_view.update_camera_status(self.monitor.connected)
            self.setup_view.update_connection_warning(self.printer_connected, self.monitor.connected)
        self.after(3000, self.update_camera_status)
    
    def update_live_camera_preview(self):
        if self.monitor.connected:
            preview = self.monitor.read_preview()
        else:
            preview = Preview()
        self.status_panel.update_camera_preview(preview)

        if self.monitor.paused:
            self.resume_video_button.config(
                state="normal",
                text="Resume Video")
            self.status_panel.system_monitoring_status.config(
                text="● Failure Detected",
                fg="#DC2626")
        elif preview.error:
            self.resume_video_button.config(state="disabled")
            self.status_panel.system_monitoring_status.config(
                text="● Analysis Unavailable", fg="#B7791F")
        else:
            self.resume_video_button.config(state="disabled")
            scanning = self.monitor.connected and self.monitor.analysis_enabled
            self.status_panel.system_monitoring_status.config(
                text="● Scanning" if scanning else "● Not Active",
                fg="#16803C" if scanning else "#B7791F")

        self.after(67, self.update_live_camera_preview)

    def get_window_region(self):
        self.update_idletasks()
        return {"left": self.winfo_rootx(), "top": self.winfo_rooty(), "width": self.winfo_width(), "height": self.winfo_height(),}

    def start_recording(self):
        try:
            self.recorder = WindowRecorder(self.recordings_folder, fps=10)
            self.recorder.start(self.get_window_region())
            print(f"UI recording started: {self.recorder.output_path}")
        except Exception as error:
            print(f"UI recording failed to start: {error}")

    def close_application(self):
        try:
            if self.recorder is not None:
                self.recorder.stop()
                print(f"UI recording saved: {self.recorder.output_path}")
        except Exception as error:
            print(f"Error while stopping recorder: {error}")

        try:
            self.monitor.disconnect()
        except Exception:
            pass

        self.destroy()

    def switch_to_recorded_video(self):
        self.monitor.select_recorded_video()
        self.status_panel.update_camera_preview(Preview())

    def switch_to_live_camera(self):
        self.monitor.select_live_camera()
        self.status_panel.update_camera_preview(Preview())
