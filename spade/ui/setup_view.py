import tkinter as tk


class SetupView(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg="#FFFFFF")
        self.create_widgets()

    def create_widgets(self):
        setup_title = tk.Label(self, text="Setup", bg="#FFFFFF", font=("Arial", 20, "bold"))
        setup_title.pack(anchor="w", padx=16, pady=(16, 4))

        setup_description = tk.Label(self, text="Connect the printer and camera\nbefore monitoring starts.", bg="#FFFFFF", font=("Arial", 14))
        
        setup_description.pack(anchor="w", padx=16)

        self.printer_frame = tk.Frame(self, bg="#FFFFFF", highlightbackground="#D1D5DB", highlightthickness=1)
        self.printer_frame.pack(fill="x", padx=16, pady=(20, 0), ipady=12)

        self.connect_printer_title = tk.Label(self.printer_frame, text="Printer Connection", bg="#FFFFFF", fg="#1D344A", font=("Arial", 12, "bold"))
        self.connect_printer_title.grid(row=0, column=0, sticky="w", padx=16, pady=(10, 2))

        self.printer_status_label = tk.Label(self.printer_frame, text="Not Connected", bg="#FFFFFF", fg="#B7791F", font=("Arial", 10))
        self.printer_status_label.grid(row=1, column=0, sticky="w", padx=16)

        self.camera_frame = tk.Frame(self, bg="#FFFFFF", highlightbackground="#D1D5DB", highlightthickness=1)
        self.camera_frame.pack(fill="x", padx=16, pady=(16, 0), ipady=12)

        self.connect_camera_title = tk.Label(self.camera_frame, text="Camera Connection", bg="#FFFFFF", fg="#1D344A", font=("Arial", 12, "bold"))
        self.connect_camera_title.grid(row=0, column=0, sticky="w", padx=16, pady=(10, 2))

        self.camera_status_label = tk.Label(self.camera_frame, text="Not Connected", bg="#FFFFFF", fg="#B7791F", font=("Arial", 10))
        self.camera_status_label.grid(row=1, column=0, sticky="w", padx=16)

        self.both_not_connected_frame = tk.Frame(self, bg="#FFF3D6", highlightbackground="#EBC66F", highlightthickness=1)
        self.both_not_connected_frame.pack(fill="x", padx=16, pady=(16, 0), ipady=12)

        both_not_connected_title = tk.Label(self.both_not_connected_frame, text="Both devices must be connected before monitoring can start.", bg="#FFF3D6", fg="#92600A", font=("Arial", 10))
        both_not_connected_title.place(relx=0.5, rely=0.5, anchor="center")

        self.continue_to_monitor_button = tk.Button(self, text="Continue to Monitor", bg="#0080FE", fg="white", font=("Arial", 12, "bold"))

    def update_printer_status(self, connected):
        if not connected:
            self.printer_frame.config(bg="#FFFFFF", highlightbackground="#D1D5DB")
            self.connect_printer_title.config(bg="#FFFFFF")
            self.printer_status_label.config(text="Not Connected", bg="#FFFFFF", fg="#B7791F")
        else:
            self.printer_frame.config(bg="#D0F0C0", highlightbackground="#38A169")
            self.connect_printer_title.config(bg="#D0F0C0")
            self.printer_status_label.config(text="Connected", bg="#D0F0C0", fg="#16803C")

    def update_camera_status(self, connected):
        if not connected:
            self.camera_frame.config(bg="#FFFFFF", highlightbackground="#D1D5DB")
            self.connect_camera_title.config(bg="#FFFFFF")
            self.camera_status_label.config(text="Not Connected", bg="#FFFFFF", fg="#B7791F")
        else:
            self.camera_frame.config(bg="#D0F0C0", highlightbackground="#38A169")
            self.connect_camera_title.config(bg="#D0F0C0")
            self.camera_status_label.config(text="Connected", bg="#D0F0C0", fg="#16803C")

    def update_connection_warning(self, printer_connected, camera_connected):
        if printer_connected and camera_connected:
            self.both_not_connected_frame.pack_forget()
            if not self.continue_to_monitor_button.winfo_manager():
                self.continue_to_monitor_button.pack(anchor="e", padx=16, pady=(20, 0))
        else:
            self.continue_to_monitor_button.pack_forget()
            if not self.both_not_connected_frame.winfo_manager():
                self.both_not_connected_frame.pack(fill="x", padx=16, pady=(16, 0), ipady=12)
