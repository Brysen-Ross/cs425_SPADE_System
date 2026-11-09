from pathlib import Path

from spade.ui.app import SPADEApp
from spade.mock_printer import MockPrinter
from spade.moonraker import Moonraker
from spade.camera import Camera


def main():
    #simulated_printer = MockPrinter()
    real_printer = Moonraker("http://localhost:7125")

    root = Path(__file__).resolve().parent.parent

    model_path = (root / "scripts" / "Weights"/ "SPADE_Spaghetti_Only-2"/ "weights" / "best.pt")
    
    model_camera = Camera(
        url=str(root / "scripts" / "spaghetti_failure.mp4"),
        model_path=model_path,
        confidence=0.75,
        image_size=512
    )

    live_camera = Camera(
        url="http://127.0.0.1:8081/snapshot",
        model_path=model_path,
        confidence=0.75,
        image_size=512
    )

    app = SPADEApp(real_printer, model_camera, live_camera)
    app.mainloop()


if __name__ == "__main__":
    main()