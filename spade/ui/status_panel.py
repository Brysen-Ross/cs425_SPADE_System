import tkinter as tk
import cv2
from PIL import Image, ImageTk
from spade.monitoring.api import Preview

class StatusPanel(tk.Frame):
    def __init__(self, parent, on_live_camera, on_recorded_video):
        super().__init__(parent, bg="#FAFAFA", width=220)
        self.on_live_camera = on_live_camera
        self.on_recorded_video = on_recorded_video
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

        self.preview_livecam_header = tk.Frame(self.preview_livecam_frame, bg="#FFFFFF")
        self.preview_livecam_header.pack(fill="x", padx=12, pady=(12, 8))

        preview_livecam_title = tk.Label(self.preview_livecam_header, text="Live Camera Preview", bg="#FFFFFF", fg="#1D344A", font=("Arial", 12, "bold"))
        preview_livecam_title.pack(side="left")

        recorded_video_button = tk.Button(self.preview_livecam_header, text="Recorded Video", font=("Arial", 10, "bold"), bg="#0080FE", fg="white", command=self.on_recorded_video)
        recorded_video_button.pack(side="right", padx=(6, 0))

        live_camera_button = tk.Button(self.preview_livecam_header, text="Live Camera", font=("Arial", 10, "bold"), bg="#0080FE", fg="white", command=self.on_live_camera)
        live_camera_button.pack(side="right", padx=(12, 0))

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

    def update_camera_preview(self, preview: Preview):
        if preview.frame is None:
            self.live_camera_label.config(image="")
            self.live_camera_label.image = None
            return
        frame = preview.frame.image.copy()
        if preview.analysis is not None:
            for detection in preview.analysis.detections:
                x1, y1, x2, y2 = map(round, detection.xyxy)
                color = (30, 80, 230)
                label = f"{detection.label} {detection.confidence:.0%}"
                position = (x1, max(14, y1 - 5))
                cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
                cv2.putText(
                    frame, label, position, cv2.FONT_HERSHEY_SIMPLEX, 0.55, color, 2,
                )
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image = Image.fromarray(frame)
        image = image.resize((400, 300), Image.Resampling.LANCZOS)
        photo = ImageTk.PhotoImage(image)
        self.live_camera_label.config(image=photo)
        self.live_camera_label.image = photo
