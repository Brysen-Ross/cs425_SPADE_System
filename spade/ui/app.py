import tkinter as tk
import cv2
from PIL import Image, ImageTk

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

        self.status_panel = tk.Frame(body, bg="#FAFAFA", width=220)
        self.status_panel.grid(row=0, column=2, sticky="nsew")
        self.create_status_panel()

    def clear_main_content_frame(self):
        for widget in self.main_content.winfo_children():
            widget.destroy()

    def show_setup(self):
        self.clear_main_content_frame()

        setup_title =tk.Label(self.main_content, text="Setup", bg="#FFFFFF", font=("Arial", 20, "bold"))
        setup_title.pack(anchor="w", padx=16, pady=(16, 4))

        setup_description = tk.Label(self.main_content, text="Connect the printer and camera before monitoring starts.", bg="#FFFFFF", font=("Arial", 14))
        setup_description.pack(anchor="w", padx=16)

        self.printer_frame = tk.Frame(self.main_content, bg="#FFFFFF", highlightbackground="#D1D5DB", highlightthickness=1)
        self.printer_frame.pack(fill="x", padx=16, pady=(20, 0), ipady=12)

        self.connect_printer_title = tk.Label(self.printer_frame, text="Printer Connection", bg="#FFFFFF", fg="#1D344A", font=("Arial", 12, "bold"))
        self.connect_printer_title.grid(row=0, column=0, sticky="w", padx=16, pady=(10, 2))

        self.printer_status_label = tk.Label(self.printer_frame, text="Not Connected", bg="#FFFFFF", fg="#B7791F", font=("Arial", 10))
        self.printer_status_label.grid(row=1, column=0, sticky="w", padx=16)

        self.connect_printer_button = tk.Button(self.printer_frame, text="Connect Printer", bg="#0080FE", fg="white", font=("Arial", 10, "bold"), command=self.connect_printer)
        self.connect_printer_button.grid(row=1, column=1, rowspan=2, sticky="e", padx=125)

        self.camera_frame = tk.Frame(self.main_content, bg="#FFFFFF", highlightbackground="#D1D5DB", highlightthickness=1)
        self.camera_frame.pack(fill="x", padx=16, pady=(16, 0), ipady=12)

        self.connect_camera_title = tk.Label(self.camera_frame, text="Camera Connection", bg="#FFFFFF", fg="#1D344A", font=("Arial", 12, "bold"))
        self.connect_camera_title.grid(row=0, column=0, sticky="w", padx=16, pady=(10, 2))

        self.camera_status_label = tk.Label(self.camera_frame, text="Not Connected", bg="#FFFFFF", fg="#B7791F", font=("Arial", 10))
        self.camera_status_label.grid(row=1, column=0, sticky="w", padx=16)

        self.connect_camera_button = tk.Button(self.camera_frame, text="Connect Camera", bg="#0080FE", fg="white", font=("Arial",10, "bold"), command=self.connect_camera)
        self.connect_camera_button.grid(row=1, column=1, rowspan=2, sticky="e", padx=125)

        self.both_not_connected_frame = tk.Frame(self.main_content, bg="#FFF3D6", highlightbackground="#EBC66F", highlightthickness=1)
        self.both_not_connected_frame.pack(fill="x", padx=16, pady=(16, 0), ipady=12)

        both_not_connected_title = tk.Label(self.both_not_connected_frame, text="Both devices must be connected before monitoring can start.", bg="#FFF3D6", fg="#92600a", font=("Arial", 10))
        both_not_connected_title.place(relx=0.5, rely=0.5, anchor="center")

        self.continue_to_monitor_button = tk.Button(self.main_content, text="Continue to Monitor", bg="#0080FE", fg="white", font=("Arial", 12, "bold"))
        
    def connect_printer(self):
        success = self.printer.connect()
        self.printer_connected = success
        if success:
            self.printer_frame.config(bg="#D0F0C0", highlightbackground="#38A169")
            self.connect_printer_title.config(bg="#D0F0C0")
            self.printer_status_label.config(text="Connected", fg="#16803C", bg="#D0F0C0")
            self.connect_printer_button.grid_remove()
        else:
            self.printer_status_label.config(text="Not Connected", fg="#B7791F")
        self.update_both_not_connected_frame(success)

    def update_printer_status(self):
        status = self.printer.get_status()
        self.printer_connected = status.connected
        if(hasattr(self, "printer_status_label") and self.printer_status_label.winfo_exists()):
            if not status.connected:
                self.printer_frame.config(bg="#FFFFFF", highlightbackground="#D1D5DB")
                self.connect_printer_title.config(bg="#FFFFFF")
                self.printer_status_label.config(text="Not Connected", bg="#FFFFFF", fg="#B7791F")
                self.system_printer_status.config(text="● Not Connected", fg="#B7791F")
                self.connect_printer_button.grid()
            else:
                self.printer_frame.config(bg="#D0F0C0", highlightbackground="#38A169")
                self.connect_printer_title.config(bg="#D0F0C0")
                self.printer_status_label.config(text="Connected", fg="#16803C", bg="#D0F0C0")
                self.system_printer_status.config(text="● Connected", fg="#16803C")
                self.connect_printer_button.grid_remove()
        self.update_both_not_connected_frame(status.connected)
        self.after(3000, self.update_printer_status)

    def connect_camera(self):
        success = self.camera.connect()
        if success:
            self.camera_frame.config(bg="#D0F0C0", highlightbackground="#38A169")
            self.connect_camera_title.config(bg="#D0F0C0")
            self.camera_status_label.config(text="Connected", fg="#16803C", bg="#D0F0C0")
            self.connect_camera_button.grid_remove()
        else:
            self.camera_status_label.config(text="Not Connected", fg="#B7791F")
        self.update_both_not_connected_frame(self.printer_connected)

    def update_camera_status(self):
        if not self.camera.connected:
            self.camera.connect()
        if(hasattr(self, "camera_status_label") and self.camera_status_label.winfo_exists()):
            if not self.camera.connected:
                self.camera_frame.config(bg="#FFFFFF", highlightbackground="#D1D5DB")
                self.connect_camera_title.config(bg="#FFFFFF")
                self.camera_status_label.config(text="Not Connected", bg="#FFFFFF", fg="#B7791F")
                self.connect_camera_button.grid()
            else:
                self.camera_frame.config(bg="#D0F0C0", highlightbackground="#38A169")
                self.connect_camera_title.config(bg="#D0F0C0")
                self.camera_status_label.config(text="Connected", fg="#16803C", bg="#D0F0C0")
                self.connect_camera_button.grid_remove()

        self.update_both_not_connected_frame(self.printer_connected)
        self.after(3000, self.update_camera_status)
    
    def update_both_not_connected_frame(self, printer_connected):
        if not self.both_not_connected_frame.winfo_exists():
            return
        if printer_connected and self.camera.connected:
            self.both_not_connected_frame.pack_forget()
            if not self.continue_to_monitor_button.winfo_manager():
                self.continue_to_monitor_button.pack(anchor="e", padx=16, pady=(20, 0))
        else:
            self.continue_to_monitor_button.pack_forget()
            if not self.both_not_connected_frame.winfo_manager():
                self.both_not_connected_frame.pack(fill="x", padx=16, pady=(16, 0), ipady=12)

    def create_status_panel(self):
        system_status_frame = tk.Frame(self.status_panel, bg="#FFFFFF", highlightbackground="#D1D5DB", highlightthickness=1)
        system_status_frame.pack(fill="x", padx=8, pady=(12, 8))

        system_status_title = tk.Label(system_status_frame, text="System Status", bg="#FFFFFF", fg="#1D344A", font=("Arial", 12, "bold"))
        system_status_title.pack(anchor="w", padx=12, pady=(12,8))

        printer_status_row = tk.Frame(system_status_frame, bg="#FFFFFF")
        printer_status_row.pack(fill="x", padx=12, pady=6)

        printer_name_label = tk.Label(printer_status_row, text="Printer", bg="#FFFFFF", fg="#1D344A", font=("Arial", 10))
        printer_name_label.pack(side="left")

        self.system_printer_status = tk.Label(printer_status_row, text="● Not Connected", bg="#FFFFFF", fg="#B7791F", font=("Arial", 10))
        self.system_printer_status.pack(side="right")

        self.preview_livecam_frame = tk.Frame(self.status_panel, bg="#FFFFFF", highlightbackground="#D1D5DB", highlightthickness=1)
        self.preview_livecam_frame.pack(fill="x", padx=8, pady=(8,12))

        preview_livecam_title = tk.Label(self.preview_livecam_frame, text="Live Camera Preview", bg="#FFFFFF", fg="#1D344A", font=("Arial", 12, "bold"))
        preview_livecam_title.pack(anchor="w", padx=12, pady=(12,8))

    def update_live_camera_preview(self):
        if self.camera.connected:
            frame = self.camera.get_frame()
            if frame is not None:
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                image = Image.fromarray(frame)
                image = image.resize((200, 150), Image.Resampling.LANCZOS)
                photo = ImageTk.PhotoImage(image)

                if hasattr(self, "live_camera_label"):
                    self.live_camera_label.config(image=photo)
                    self.live_camera_label.image = photo
                else:
                    self.live_camera_label = tk.Label(self.preview_livecam_frame, image=photo, bg="#FFFFFF")
                    self.live_camera_label.image = photo
                    self.live_camera_label.pack(padx=12, pady=(0, 12))
            else:
                if hasattr(self, "live_camera_label"):
                    self.live_camera_label.destroy()
                    del self.live_camera_label
        self.after(67, self.update_live_camera_preview)