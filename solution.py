import os

import cv2

from models import YOLOMODEL

model = YOLOMODEL(
    weights_path='./weights/model_gun.pt',
)

guns = ['short_weapons','long_weapons', 'knife']
people = ['man_with_weapon', 'man_without_weapon']

def check_noise(frame, noise_threshold = 50, overexposed_threshold = 200):

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    mean_brightness = cv2.mean(gray)[0]
    if mean_brightness < noise_threshold:
        print("Изображение зашумлено")
    else:
        print("Изображение не зашумлено")

    if mean_brightness > overexposed_threshold:
        print("Изображение засвечено")
    else:
        print("Изображение не засвечено")

import cv2
import os

output_folder = 'output'
output_folder_with_weapon = 'output_with_weapon'

output_folder = 'output'
output_folder_with_weapon = 'output_with_weapon'

def draw_bounding_box(frame, bboxes, labels, scores, keypoints, frame_number):
    conf_people_with_guns = (set(guns) & set(labels)) and ((set(people) & set(labels))) and False
    if conf_people_with_guns:
        print("search gun and people")
        has_weapon = False
        for bbox, label, score in zip(bboxes, labels, scores, keypoints):
            label_true = label
            if label in people:
                people_box = bbox
                xmin_people, ymin_people, xmax_people, ymax_people = map(int, people_box)
                for bbox, label, score in zip(bboxes, labels, scores):
                    if label in guns:
                        gun_box = bbox
                        xmin_guns, ymin_guns, xmax_guns, ymax_guns = map(int, gun_box)
                        if (xmin_people <= xmax_guns and xmax_people >= xmin_guns) and (
                                ymin_people <= ymax_guns and ymax_people >= ymin_guns):
                            label_true = 'man_with_weapon'
                            has_weapon = True
                            print("swap")
                            break
                        else:
                            label_true = 'man_without_weapon'
                            print("no swap")
                            break
            label = label_true
            xmin, ymin, xmax, ymax = map(int, bbox)
            cv2.rectangle(frame, (xmin, ymin), (xmax, ymax), (255, 0, 0), 2)
            cv2.putText(frame, f"{label}: {score:.2f}", (xmin, ymin - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)

        if has_weapon:
            print('if')
            if frame_number % 25 == 0:
                save_path = os.path.join(output_folder_with_weapon, f'frame_{frame_number:04d}_with_weapon.jpg')
                cv2.imwrite(save_path, frame)
                print(f"Saved frame {frame_number} with weapon to {save_path}")
        else:
            if frame_number % 25 == 0:
                save_path = os.path.join(output_folder, f'frame_{frame_number:04d}.jpg')
                cv2.imwrite(save_path, frame)
                print(f"Saved frame {frame_number} without weapon to {save_path}")
            print('else')
        cv2.namedWindow('custom window', cv2.WINDOW_KEEPRATIO)
        cv2.imshow('custom window', frame)
        cv2.resizeWindow('custom window', 700, 700)
        cv2.waitKey(1)

    # условие в IF Дорабатывается, менять все в else
    else:
        for bbox, label, score, kps in zip(bboxes, labels, scores, keypoints):
            if label in people:
                label = 'man_without_weapon'
            xmin, ymin, xmax, ymax = map(int, bbox)
            cv2.rectangle(frame, (xmin, ymin), (xmax, ymax), (255, 0, 0), 3)
            cv2.putText(frame, f"{label}: {score:.2f}", (xmin, ymin - 5), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 2)
            # вывод ключевых точек на сервисе не будет!
            """
            for kp in kps:
                for i in kp:
                    x, y = map(int, i)
                    cv2.circle(frame, (x, y), 3, (0, 0,255), -1)
            """
        if frame_number % 25 == 0:
            save_path = os.path.join(output_folder, f'frame_{frame_number:04d}.jpg')
            cv2.imwrite(save_path, frame)
            print(f"Saved frame {frame_number} without weapon to {save_path}")

        cv2.namedWindow('custom window', cv2.WINDOW_KEEPRATIO)
        cv2.imshow('custom window', frame)
        cv2.resizeWindow('custom window', 700, 700)
        cv2.waitKey(2)
        return frame



def main(video_path):
    source = video_path  # Use the provided video path
    output_folder = 'output'
    cap = cv2.VideoCapture(source)
    t = 0
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        bboxes, labels, scores, keypoints = model.predict(frame)
      #  draw_bounding_box(frame, bboxes, labels, scores, keypoints, t)
        t += 1

if __name__ == '__main__':
    import sys

    if len(sys.argv) != 2:
        print("Usage: python solution.py <video_path>")
        sys.exit(1)

    video_path = sys.argv[1]
    main(video_path)
