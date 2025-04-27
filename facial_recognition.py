from __future__ import annotations

import shutil
from pathlib import Path

import cv2
import pandas as pd
from fer import FER


def analyze_folder(folder: str | Path, save_csv: bool = True):
    folder = Path(folder)  # 🔑 cast to Path once
    detector = FER()
    analysed = []

    for img_path in sorted(folder.iterdir()):
        if img_path.suffix.lower() not in {'.jpg', '.jpeg', '.png'}:
            continue  # skip non-images

        img = cv2.imread(str(img_path))
        if img is None:
            print(f"⚠️  Could not read {img_path.name}; skipping")
            continue

        emotion, score = detector.top_emotion(img) or ('unknown', 0.0)
        analysed.append((emotion, score, img_path.name))

        print(img_path.name, emotion)
        if emotion == None:
            print(f"⚠️  Could not detect emotion in {img_path.name}; skipping")
            continue

        # --- move into emotion folder ---
        dest_dir = folder / emotion  # both are Path -> ‘/’ works
        dest_dir.mkdir(exist_ok=True)
        shutil.move(str(img_path), str(dest_dir / img_path.name))

    if save_csv:
        df = pd.DataFrame(analysed, columns=['emotion', 'score', 'file'])
        df.sort_values(['emotion', 'score'], ascending=[True, False]).to_csv(
            folder / 'emotion_report.csv', index=False
        )


if __name__ == '__main__':
    # objs = DeepFace.analyze(
    #     img_path="/Users/daiwenkai/Downloads/xiaoman_img/1c493e708fda48b1adbe3075bf8e1d82.jpg",
    #     actions=['age', 'gender', 'race', 'emotion'],
    #     enforce_detection=True,
    #     detector_backend='retinaface',  # optional, but better for multiple faces
    #     align=True
    # )
    # for i, face in enumerate(objs):
    #     print(f"Face {i+1}:")
    #     print("  Age:", face["age"])
    #     print("  Gender:", face["dominant_gender"])
    #     print("  Race:", face["dominant_race"])
    #     print("  Emotion:", face["dominant_emotion"])

    # detector = FER()
    # # img = cv2.imread("/Users/daiwenkai/Downloads/xiaoman_img/1c493e708fda48b1adbe3075bf8e1d82.jpg")
    # img = cv2.imread("/Users/daiwenkai/Downloads/xiaoman_img/4f51e41302d144f9af5b3eeb4e4e5e15.jpg")
    # emotion, score = detector.top_emotion(img)
    #
    # print("Detected Emotion:", emotion)
    # print("Score:", score)

    analyze_folder("/Users/daiwenkai/Downloads/xiaoman_img", save_csv=False)
