from pathlib import Path
from ultralytics import YOLO
import torch
import yaml
import shutil

SOURCE_DATASET = Path(r"C:\Users\chris\Documents"
    r"\detect-failure-in-3d-printing.v10i.yolo26")
OUTPUT_DATASET = Path(r"C:\Users\chris\Documents\SPADE_Spaghetti_Dataset")
TARGET_CLASS = "spaghetti"
EPOCHS = 50
IMAGE_SIZE = 512
BATCH_SIZE = 4
PATIENCE = 12

def prepare_dataset():

    original_yaml = SOURCE_DATASET / "data.yaml"

    if not original_yaml.is_file():
        raise FileNotFoundError(original_yaml)

    with original_yaml.open("r", encoding="utf-8") as f:
        config = yaml.safe_load(f)

    names = config["names"]

    if isinstance(names, dict): classes = {int(k): str(v) for k, v in names.items()}
    else: classes = dict(enumerate(names))

    print("Original classes:", classes)

    target_ids = [class_id
        for class_id, name in classes.items()
        if name.strip().lower() == TARGET_CLASS.lower()]

    if len(target_ids) != 1:
        raise ValueError(f"Expected exactly one '{TARGET_CLASS}' class. "
            f"Found IDs: {target_ids}")

    target_id = target_ids[0]

    if OUTPUT_DATASET.exists(): shutil.rmtree(OUTPUT_DATASET)
    counts = {}
    for split, candidates in {"train": ["train"], "val": ["valid", "val"], "test": ["test"]}.items():

        source_split = next(
            (SOURCE_DATASET / candidate
                for candidate in candidates
                if (SOURCE_DATASET / candidate / "images").is_dir()),None)

        if source_split is None:
            if split == "test":
                continue
            raise FileNotFoundError(f"Missing {split} images directory")

        source_images = source_split / "images"
        source_labels = source_split / "labels"

        destination_images = OUTPUT_DATASET / split / "images"
        destination_labels = OUTPUT_DATASET / split / "labels"

        destination_images.mkdir(parents=True, exist_ok=True)
        destination_labels.mkdir(parents=True, exist_ok=True)

        positives = 0
        negatives = 0
        skipped = 0

        for image in sorted(source_images.iterdir()):

            if image.suffix.lower() not in {".jpg", ".jpeg", ".png", ".bmp", ".webp"}:
                continue

            label_path = source_labels / f"{image.stem}.txt"

            if not label_path.exists():
                skipped += 1
                continue

            lines = label_path.read_text(encoding="utf-8").splitlines()
            spaghetti_labels = []

            for line in lines:

                parts = line.strip().split()
                if not parts: continue

                if int(parts[0]) == target_id:
                    parts[0] = "0"
                    spaghetti_labels.append(" ".join(parts))

            if spaghetti_labels: positives += 1
            elif not any(line.strip() for line in lines): negatives += 1
            else:
                skipped += 1
                continue

            shutil.copy2(image, destination_images / image.name)
            output_label = destination_labels / f"{image.stem}.txt"
            output_label.write_text("\n".join(spaghetti_labels), encoding="utf-8")

        counts[split] = positives + negatives

        print(f"{split}: {positives} spaghetti images, "
            f"{negatives} background images, "
            f"{skipped} skipped")

    dataset_config = {"path": str(OUTPUT_DATASET.resolve()), "train": "train/images", "val": "val/images", "names": {0: TARGET_CLASS}, "nc": 1}

    if "test" in counts:
        dataset_config["test"] = "test/images"
    output_yaml = OUTPUT_DATASET / "data.yaml"

    with output_yaml.open("w", encoding="utf-8") as f:
        yaml.safe_dump(dataset_config, f, sort_keys=False)

    if counts.get("train", 0) == 0:
        raise RuntimeError("No training images found.")

    if counts.get("val", 0) == 0:
        raise RuntimeError("No validation images found.")

    print(f"\nNew dataset created: {OUTPUT_DATASET}")
    return output_yaml


def main():

    data_yaml = prepare_dataset()
    device = 0 if torch.cuda.is_available() else "cpu"

    print(f"\nTraining device: {device}")
    print("Loading pretrained YOLO26 Nano...")

    model = YOLO("yolo26n.pt")
    model.train(data=str(data_yaml), epochs=EPOCHS, imgsz=IMAGE_SIZE, batch=BATCH_SIZE, device=device, patience=PATIENCE, pretrained=True,
        fraction=1.0, project=str(SOURCE_DATASET.parent / "SPADE_Training"), name="SPADE_Spaghetti_Only", exist_ok=False, plots=True, save=True)

    best_path = Path(model.trainer.best)
    print(f"\nBest model: {best_path.resolve()}")

    best_model = YOLO(str(best_path))
    metrics = best_model.val(data=str(data_yaml), split="val")

    print("\nSPADE SPAGHETTI MODEL RESULTS")
    print(f"mAP50: {metrics.box.map50:.4f}")
    print(f"mAP50-95: {metrics.box.map:.4f}")
    print("\nTraining complete!")


if __name__ == "__main__":
    main()
