from pathlib import Path

from spade.ui.app import SPADEApp
from spade.mock_printer import MockPrinter
from spade.moonraker import Moonraker
from spade.camera import Camera


def main():
    printer = MockPrinter()

    root = Path(__file__).resolve().parent.parent

    camera = Camera(
        url=str(root / "scripts" / "spaghetti_failure.mp4"),
        model_path=(
            root / "scripts" / "Weights"
            / "SPADE_Spaghetti_Only-2"
            / "weights" / "best.pt"
        ),
        confidence=0.75,
        image_size=512
    )

    app = SPADEApp(printer, camera)
    app.mainloop()


if __name__ == "__main__":
    main()