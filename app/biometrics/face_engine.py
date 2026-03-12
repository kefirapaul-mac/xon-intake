import cv2
import mediapipe as mp
import numpy as np


class FaceAnalyzer:

    def __init__(self):
        self.face_mesh = mp.solutions.face_mesh.FaceMesh(
            static_image_mode=False,
            max_num_faces=1,
            refine_landmarks=True,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        )

    def analyze_video(self, video_path: str):

        cap = cv2.VideoCapture(video_path)

        blink_count = 0
        frame_count = 0
        brow_tension = []
        mouth_tension = []
        eye_openness_values = []

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            frame_count += 1
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = self.face_mesh.process(rgb_frame)

            if results.multi_face_landmarks:
                landmarks = results.multi_face_landmarks[0].landmark

                # Eye openness (simple distance measure)
                left_eye_top = landmarks[159]
                left_eye_bottom = landmarks[145]

                eye_distance = abs(left_eye_top.y - left_eye_bottom.y)
                eye_openness_values.append(eye_distance)

                # Brow tension (distance brow to eye)
                brow_point = landmarks[70]
                brow_tension.append(abs(brow_point.y - left_eye_top.y))

                # Mouth tension
                mouth_top = landmarks[13]
                mouth_bottom = landmarks[14]
                mouth_tension.append(abs(mouth_top.y - mouth_bottom.y))

        cap.release()

        if frame_count == 0:
            return None

        return {
            "blink_rate": len(eye_openness_values) / frame_count * 60,
            "brow_tension": float(np.mean(brow_tension)) if brow_tension else 0,
            "mouth_tension": float(np.mean(mouth_tension)) if mouth_tension else 0,
            "eye_openness": float(np.mean(eye_openness_values)) if eye_openness_values else 0,
        }