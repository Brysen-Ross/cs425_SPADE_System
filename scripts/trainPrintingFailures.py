
from pathlib import Path
from ultralytics import YOLO
import torch

DATASET = Path(r"C:\Users\chris\Documents\detect-failure-in-3d-printing.v10i.yolo26\data.yaml")

def main():
    if not DATASET.is_file():
        print(f"Dataset not found: {DATASET}")
        return

    # use gpu with cuda
    device = 0 if torch.cuda.is_available() else "cpu"
    print(f"Training device: {device}")

    # Load pretrained model
    model = YOLO("yolo26n.pt")

    model.train(data=str(DATASET),
        epochs=20,
        imgsz=416,
        batch=4,
        device=device,
        patience=7,
        pretrained=True,
        fraction=0.5,
        project="SPADE_Training",
        name="SPADE_Quick_Test",
        exist_ok=False,
        plots=True)

    # Load best trained weights
    best_path = Path(r"C:\Users\chris\Documents\runs\detect"
        r"\SPADE_Training\SPADE_Quick_Test\weights\best.pt")

    best_model = YOLO(str(best_path))

    # Validate and print metrics
    metrics = best_model.val(data=str(DATASET))
    print(f"mAP50: {metrics.box.map50:.4f}")
    print(f"mAP50-95: {metrics.box.map:.4f}")
    print(f"\nBest model saved to: {best_path.resolve()}")

if __name__ == "__main__":
    main()
