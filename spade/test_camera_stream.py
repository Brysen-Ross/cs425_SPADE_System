
import cv2

camera_url = "http://127.0.0.1:8081/stream"
camera = cv2.VideoCapture(camera_url)

if camera.isOpened():
    print("Camera connected successfully!")

    for i in range(10):
        success, frame = camera.read()

        if not success:
            print("Failed to read frame.")
            break

        print(
            f"Frame {i + 1}: "
            f"Min={frame.min()}, "
            f"Max={frame.max()}, "
            f"Mean={frame.mean():.2f}"
        )

        if i == 0:
            cv2.imwrite("/tmp/spade_camera_test.jpg", frame)

else:
    print("Could not connect to camera.")

camera.release()
