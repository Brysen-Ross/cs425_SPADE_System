import unittest
from spade.mock_printer import MockPrinter

class TestMockPrinter(unittest.TestCase):
    """Unit tests for the simulated mock printer class."""

    def setUp(self):
        self.printer = MockPrinter()

    def test_initial_connect_status(self):
        self.assertFalse(self.printer.connected)
    
    def test_connect_status_after_connect(self):
        self.assertTrue(self.printer.connect())

    def test_connect_update_state(self):
        self.printer.connect()
        self.assertTrue(self.printer.connected)

    def test_initial_status(self):
        status = self.printer.get_status()
        self.assertFalse(status.connected)
        self.assertEqual(status.state, "Offline")
        self.assertEqual(status.progress, 0.0)
        self.assertEqual(status.nozzle_temperature, 0.0)
        self.assertEqual(status.bed_temperature, 0.0)

    def test_status_after_connect(self):
        self.printer.connect()
        status = self.printer.get_status()
        self.assertTrue(status.connected)
        self.assertEqual(status.state, "Printing")
        self.assertEqual(status.progress, 0.32)
        self.assertEqual(status.nozzle_temperature, 200.0)
        self.assertEqual(status.bed_temperature, 60.0)
    
if __name__ == '__main__':
    unittest.main()