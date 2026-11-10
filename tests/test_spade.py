import unittest
import tkinter as tk

from spade.moonraker import Moonraker
from spade.camera import Camera
from spade.ui.status_panel import StatusPanel
from spade.ui.setup_view import SetupView
from spade.ui.app import SPADEApp
from spade.ui.recorder import WindowRecorder
from spade.mock_printer import MockPrinter

class TestMoonraker(unittest.TestCase):

    # Tests that the Moonraker handles an unavailable printer connection.
    def test_get_status(self):
        printer = Moonraker("http://127.0.0.1:59999")
        status = printer.get_status()
        self.assertIsNotNone(status)
        self.assertFalse(status.connected)

class TestCamera(unittest.TestCase):

    # Tests that the when the camera is paused, get_frame() returns the paused frame.
    def test_pause_video(self):
        camera = Camera()
        camera.paused = True
        camera.frame = "Test Frame"
        result = camera.get_frame()
        self.assertEqual(result, "Test Frame")

class TestStatusPanel(unittest.TestCase):

    # Tests that the StatusPanel class can be initialized without errors.
    def test_status_panel_initialization(self):
        root = tk.Tk()
        try:
            panel = StatusPanel(root, on_live_camera=lambda: None, on_recorded_video=lambda: None)
            self.assertIsInstance(panel, StatusPanel)
        finally:
            root.destroy()

class TestSetupView(unittest.TestCase):

    # Tests that the SetupView class can be initialized without errors.
    def test_setup_view_initialization(self):
        root = tk.Tk()
        try:
            view = SetupView(root)
            self.assertIsInstance(view, SetupView)
        finally:
            root.destroy()

class TestSPADEApp(unittest.TestCase):

    # Tests that the SPADEApp class can be initialized without errors.
    def test_spade_app_initialization(self):
        printer = Moonraker("http://127.0.0.1:59999")
        model_camera = Camera()
        live_camera = Camera()
        app = SPADEApp(printer, model_camera, live_camera)
        try:
            self.assertIsInstance(app, SPADEApp)
        finally:
            app.destroy()

class TestWindowRecorder(unittest.TestCase):

    # Tests that the WindowRecorder class can be initialized with a specific fps value.
    def test_window_recorder_initialization(self):
        recorder = WindowRecorder("test_output", fps=10)
        self.assertEqual(recorder.fps, 10)

class TestMockPrinter(unittest.TestCase):

    # Tests that the MockPrinter class can be initialized and the connect method works as expected.
    def test_mock_printer_is_connected(self):
        mock_printer = MockPrinter()
        mock_printer.connect()
        self.assertTrue(mock_printer.connected)
