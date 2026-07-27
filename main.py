import cv2
import math
import os
import urllib.request

# ==========================================
# 1. MATHEMATICAL MODEL PARAMETERS
# ==========================================
W_METERS = 0.15          # Real average face width (~0.14 - 0.16 m)
FOCAL_LENGTH_PX = 650.0  # Camera focal length in pixels (f)

# Ensure face detector XML file exists locally
CASCADE_FILE = "haarcascade_frontalface_default.xml"
CASCADE_URL = "https://raw.githubusercontent.com/opencv/opencv/master/data/haarcascades/haarcascade_frontalface_default.xml"

if not os.path.exists(CASCADE_FILE):
    print("Downloading face detection model file...")
    urllib.request.urlretrieve(CASCADE_URL, CASCADE_FILE)

face_cascade = cv2.CascadeClassifier(CASCADE_FILE)


def calculate_distance_and_angle(x_center, w_px, c_x, f=FOCAL_LENGTH_PX, W=W_METERS):
    """
    Mathematical Model (as requested in Task 2):
        Depth:  Z = (f * W) / w_px
        Angle:  theta = arctan((x - c_x) / f)
    """
    if w_px <= 0:
        return 0.0, 0.0

    # 1. Depth (Z in meters)
    Z = (f * W) / w_px

    # 2. Angle (theta in degrees)
    theta_rad = math.atan((x_center - c_x) / f)
    theta_deg = math.degrees(theta_rad)

    return Z, theta_deg


def main():
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Error: Could not open camera.")
        return

    print("Camera initialized successfully. Press 'q' or 'ESC' to exit.")

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Failed to grab camera frame.")
            break

        h, w, _ = frame.shape
        c_x = w / 2.0  # Image center x-coordinate (c_x)

        # Convert image to grayscale for face detection
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Detect face bounding boxes
        faces = face_cascade.detectMultiScale(
            gray, scaleFactor=1.1, minNeighbors=5, minSize=(50, 50)
        )

        for (x, y, face_w, face_h) in faces:
            # Face center pixel coordinates (x, y)
            face_center_x = x + (face_w / 2.0)
            face_center_y = y + (face_h / 2.0)

            # Calculate Depth (Z) and Angle (theta)
            Z, theta_deg = calculate_distance_and_angle(face_center_x, face_w, c_x)

            # Render visuals on frame
            cv2.rectangle(frame, (x, y), (x + face_w, y + face_h), (0, 255, 0), 2)
            cv2.circle(frame, (int(face_center_x), int(face_center_y)), 5, (0, 0, 255), -1)

            # Display Output Text: (depth, theta)
            text_disp = f"Z={Z:.2f}m ({Z*100:.1f}cm), Theta={theta_deg:.1f} deg"
            cv2.putText(frame, text_disp, (x, y - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)

            # Output stream matching expected tuple format: (depth, theta)
            print(f"Output: (depth={Z:.2f}m, theta={theta_deg:.2f}°)")

        # Draw vertical axis corresponding to image center (c_x)
        cv2.line(frame, (int(c_x), 0), (int(c_x), h), (255, 255, 255), 1)

        cv2.imshow("Monocular Face Distance Estimation", frame)

        key = cv2.waitKey(1) & 0xFF
        if key == ord('q') or key == 27:
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()