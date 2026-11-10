from rfdetr import RFDETRMedium


WEIGHTS_PATH = ""
DATASET_PATH = ""
OUTPUT_PATH = ""


def main():
    model = RFDETRMedium(
        pretrain_weights=WEIGHTS_PATH,
        num_classes=2,
        resolution=576,
        device="cuda",
    )
    model.train(
        dataset_dir=DATASET_PATH,
        dataset_file="roboflow",
        output_dir=OUTPUT_PATH,
        class_names=["spaghetti", "underextrusion"],
        epochs=24,
        batch_size=8,
        grad_accum_steps=1,
        seed=17,
        lr=1e-4,
        lr_encoder=1.5e-4,
        lr_scheduler="step",
        lr_scheduler_kwargs={"lr_drop": 18},
        warmup_epochs=0,
        use_ema=True,
        amp_dtype="bf16",
        num_workers=2,
        multi_scale=False,
        expanded_scales=False,
        run_test=False,
    )


if __name__ == "__main__":
    main()
