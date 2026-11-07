
from pathlib import Path
from tkinter import Tk, filedialog, simpledialog
from time import perf_counter
from ultralytics import YOLO
import cv2

# SETTINGS
MODEL_PATH = Path(r"C:\Users\chris\Documents\SPADE_Training"
    r"\SPADE_Spaghetti_Only-2\weights\best.pt")
OUTPUT_FOLDER = Path(r"C:\Users\chris\Documents\SPADE_Video_Results")

CONFIDENCE = 0.75
IMAGE_SIZE = 512
DISPLAY_WIDTH = 1100
REQUIRED_FRAMES = 1
RESUME_COOLDOWN = 1.0

SAVE_VIDEO = True
RECORDING_NAME = "SPADE_Detection_Demo.mp4"


# SELECT VIDEO BOX
def select_video():
    root = Tk()
    root.withdraw()

    url = simpledialog.askstring("SPADE Video Detector", "Enter direct video URL or local file path.\n" "Leave blank to browse for a video:", parent=root)

    if url and url.strip():
        source = url.strip()
    else:
        source = filedialog.askopenfilename(
            parent=root,
            title="Select 3D Printing Video",
            filetypes=[("Video files", "*.mp4 *.avi *.mov *.mkv *.m4v"), ("All files", "*.*")])

    root.destroy()
    return source


# UTILITIES
def format_time(seconds):
    return f"{max(0, seconds):.2f}s"


def resize_frame(frame):
    height, width = frame.shape[:2]
    if width <= DISPLAY_WIDTH:
        return frame

    scale = DISPLAY_WIDTH / width
    return cv2.resize(frame, (DISPLAY_WIDTH, int(height * scale)))


def draw_status(frame, status, video_time, fps):
    frame = frame.copy()
    height, width = frame.shape[:2]

    cv2.rectangle(frame, (0, 0), (width, 90), (25, 25, 25), -1)
    cv2.putText(frame, f"SPADE | {status}", (15, 34), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2)
    cv2.putText(frame, f"Video: {format_time(video_time)} | FPS: {fps:.1f}", (15, 70), cv2.FONT_HERSHEY_SIMPLEX, 0.65, (255, 255, 255), 2)
    return frame


# VIDEO ANALYSIS
def main():

    if not MODEL_PATH.is_file():
        print(f"Model not found: {MODEL_PATH}")
        return

    source = select_video()

    if not source:
        print("No video selected.")
        return

    OUTPUT_FOLDER.mkdir(parents=True, exist_ok=True)

    print("Loading SPADE model...")
    model = YOLO(str(MODEL_PATH))

    print(f"Loaded model: {MODEL_PATH}")
    print(f"Model classes: {model.names}")

    print(f"Opening video: {source}")
    capture = cv2.VideoCapture(source)

    if not capture.isOpened():
        print("ERROR: Could not open video.")
        capture.release()
        return

    video_fps = capture.get(cv2.CAP_PROP_FPS)

    if video_fps <= 0 or video_fps > 240:
        video_fps = 30.0

    frame_delay = max(1, int(1000 / video_fps))

    print(f"Video FPS: {video_fps:.1f}")
    print("Controls:")
    print("  SPACE = Resume after detection")
    print("  S     = Save annotated snapshot")
    print("  Q     = Quit")

    window_name = "SPADE - Video Failure Detection"

    cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)

    frame_number = 0
    detection_count = 0
    consecutive_detections = 0
    snapshot_count = 0

    paused = False
    cooldown_until = -1.0

    current_display = None
    current_time = 0.0

    video_writer = None
    recording_path = OUTPUT_FOLDER / RECORDING_NAME

    # Track elapsed recording time for accurate pause duration
    recording_start = perf_counter()
    recorded_frames = 0

    def record_frame(frame):
        nonlocal video_writer, recorded_frames

        if not SAVE_VIDEO or frame is None:
            return

        if video_writer is None:
            height, width = frame.shape[:2]

            video_writer = cv2.VideoWriter(
                str(recording_path),
                cv2.VideoWriter_fourcc(*"mp4v"),
                video_fps,
                (width, height))

            if not video_writer.isOpened():
                raise RuntimeError(f"Could not create output video: {recording_path}")

            print(f"Recording video to: {recording_path}")

        # Record enough frames to reflect elapsed wall-clock time.
        # Repeat the currently displayed frame while paused.
        elapsed = perf_counter() - recording_start
        target_frames = int(elapsed * video_fps)

        while recorded_frames < target_frames:
            video_writer.write(frame)
            recorded_frames += 1

    try:
        while True:

            if not paused:
                success, frame = capture.read()

                if not success:
                    print("End of video or stream.")
                    break

                frame_number += 1
                current_time = frame_number / video_fps

                start = perf_counter()

                result = model.predict(
                    source=frame,
                    imgsz=IMAGE_SIZE,
                    conf=CONFIDENCE,
                    verbose=False)[0]

                annotated = result.plot()
                boxes = result.boxes

                elapsed = perf_counter() - start
                processing_fps = (1.0 / elapsed if elapsed > 0 else 0.0)

                has_detection = (boxes is not None and len(boxes) > 0)

                if has_detection:
                    best_confidence = max(float(box.conf[0]) for box in boxes)

                    print(f"Frame {frame_number} | "
                        f"Video {current_time:.2f}s | "
                        f"Spaghetti confidence {best_confidence:.1%}")

                if has_detection:
                    consecutive_detections += 1
                else:
                    consecutive_detections = 0

                should_pause = (consecutive_detections >= REQUIRED_FRAMES
                    and current_time >= cooldown_until)

                if should_pause:
                    paused = True
                    detection_count += 1

                    print("\n" + "=" * 55)
                    print(f"FAILURE EVENT #{detection_count}")
                    print(f"Video timestamp: "
                        f"{format_time(current_time)}")

                    for box in boxes:
                        class_id = int(box.cls[0])
                        confidence = float(box.conf[0])
                        class_name = model.names[class_id]

                        print(f"  {class_name}: {confidence:.2%}")

                    print("=" * 55)
                    print("VIDEO PAUSED - Press SPACE to resume")

                status = ("FAILURE DETECTED - PAUSED" if paused else "SCANNING VIDEO")

                current_display = draw_status(annotated, status, current_time, processing_fps)
                current_display = resize_frame(current_display)
                cv2.imshow(window_name, current_display)

            # Record the currently displayed frame.
            # While paused, this produces repeated frames.
            record_frame(current_display)

            key = cv2.waitKey(20 if paused else frame_delay) & 0xFF

            if key == ord("q"):
                break

            if key == ord("s") and current_display is not None:
                snapshot_count += 1

                filename = (f"detection_{snapshot_count:04d}.jpg")
                output_path = OUTPUT_FOLDER / filename
                cv2.imwrite(str(output_path), current_display)

                print(f"Snapshot saved: {output_path}")

            if key == 32 and paused:
                # Capture the final paused duration before resuming
                record_frame(current_display)

                paused = False
                consecutive_detections = 0
                cooldown_until = (current_time + RESUME_COOLDOWN)

                print("Resuming video...")

    finally:
        # Record the final displayed frame before closing
        record_frame(current_display)

        capture.release()

        if video_writer is not None:
            video_writer.release()
            print(f"Video saved: {recording_path}")

        cv2.destroyAllWindows()

        print("\nSPADE video analysis complete.")
        print(f"Failure events: {detection_count}")
        print(f"Snapshots saved: {snapshot_count}")
        print(f"Output folder: {OUTPUT_FOLDER}")


if __name__ == "__main__":
    main()
