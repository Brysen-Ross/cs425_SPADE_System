import tkinter as tk
import cv2
from PIL import Image, ImageTk

class StatusPanel(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg="#FAFAFA", width=220)
        self.create_widgets()

    def create_widgets(self):
        system_status_frame = tk.Frame(self, bg="#FFFFFF", highlightbackground="#D1D5DB", highlightthickness=1)
        system_status_frame.pack(fill="x", padx=8, pady=(12, 8))

        system_status_title = tk.Label(system_status_frame, text="System Status", bg="#FFFFFF", fg="#1D344A", font=("Arial", 12, "bold"))
        system_status_title.pack(anchor="w", padx=12, pady=(12, 8))

        printer_status_row = tk.Frame(system_status_frame, bg="#FFFFFF")
        printer_status_row.pack(fill="x", padx=12, pady=6)

        printer_name_label = tk.Label(printer_status_row, text="Printer", bg="#FFFFFF", fg="#1D344A", font=("Arial", 10))
        printer_name_label.pack(side="left")

        self.system_printer_status = tk.Label(printer_status_row, text="● Not Connected", bg="#FFFFFF", fg="#B7791F", font=("Arial", 10))
        self.system_printer_status.pack(side="right")

        camera_status_row = tk.Frame(system_status_frame, bg="#FFFFFF")
        camera_status_row.pack(fill="x", padx=12, pady=6)

        camera_name_label = tk.Label(camera_status_row, text="Camera", bg="#FFFFFF", fg="#1D344A", font=("Arial", 10))
        camera_name_label.pack(side="left")

        self.system_camera_status = tk.Label(camera_status_row, text="● Not Connected", bg="#FFFFFF", fg="#B7791F", font=("Arial", 10))
        self.system_camera_status.pack(side="right")

        monitoring_status_row = tk.Frame(system_status_frame, bg="#FFFFFF")
        monitoring_status_row.pack(fill="x", padx=12, pady=6)

        monitoring_name_label = tk.Label(monitoring_status_row, text="Monitoring", bg="#FFFFFF", fg="#1D344A", font=("Arial", 10))
        monitoring_name_label.pack(side="left")

        self.system_monitoring_status = tk.Label(monitoring_status_row, text="● Not Active", bg="#FFFFFF", fg="#B7791F", font=("Arial", 10))
        self.system_monitoring_status.pack(side="right")

        self.preview_livecam_frame = tk.Frame(self, bg="#FFFFFF", highlightbackground="#D1D5DB", highlightthickness=1)
        self.preview_livecam_frame.pack(fill="x", padx=8, pady=(8, 12))

        preview_livecam_title = tk.Label(self.preview_livecam_frame, text="Live Camera Preview", bg="#FFFFFF", fg="#1D344A", font=("Arial", 12, "bold"))
        preview_livecam_title.pack(anchor="w", padx=12, pady=(12, 8))

        self.live_camera_label = tk.Label(self.preview_livecam_frame, bg="#FFFFFF")
        self.live_camera_label.pack(padx=12, pady=(0, 12))

    def update_printer_status(self, connected):
        if connected:
            self.system_printer_status.config(text="● Connected", fg="#16803C")
        else:
            self.system_printer_status.config(text="● Not Connected", fg="#B7791F")

    def update_camera_status(self, connected):
        if connected:
            self.system_camera_status.config(text="● Connected", fg="#16803C")
        else:
            self.system_camera_status.config(text="● Not Connected", fg="#B7791F")

    def update_camera_preview(self, frame):
        if frame is None:
            self.live_camera_label.config(image="")
            self.live_camera_label.image = None
            return
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image = Image.fromarray(frame)
        image = image.resize((200, 150), Image.Resampling.LANCZOS)
        photo = ImageTk.PhotoImage(image)
        self.live_camera_label.config(image=photo)
        self.live_camera_label.image = photo