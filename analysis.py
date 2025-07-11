import cv2
import numpy as np
import mediapipe as mp

mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(static_image_mode=True,
                                  max_num_faces=1,
                                  refine_landmarks=True)

def get_metrics(image_path, return_points=False):
    img = cv2.imread(image_path)
    h, w = img.shape[:2]
    results = face_mesh.process(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    if not results.multi_face_landmarks:
        return ({'error': 'Обличчя не знайдено'}, {}) if return_points else {'error': 'Обличчя не знайдено'}

    lm = results.multi_face_landmarks[0].landmark
    def P(i): return np.array([lm[i].x * w, lm[i].y * h])

    # Основні точки
    left_temple = P(162)#162
    right_temple = P(389)#389

    left_jaw = P(93)#93
    right_jaw = P(366)#366

    extra_left_1 = P(192)#192
    extra_right_1 = P(416)#416

    '''left_cheek = P(214)#58
    right_cheek = P(434)'''

    extra_left_2 = P(172)#172
    extra_right_2 = P(397)#397

    '''extra_left_3 = P(140)#176
    extra_right_3 = P(369)'''



    # Відстані
    temple_width = np.linalg.norm(left_temple - right_temple)
    #cheek_width = np.linalg.norm(left_cheek - right_cheek)
    jaw_width = np.linalg.norm(left_jaw - right_jaw)
    extra_width_1 = np.linalg.norm(extra_left_1 - extra_right_1)
    extra_width_2 = np.linalg.norm(extra_left_2 - extra_right_2)
    #extra_width_3 = np.linalg.norm(extra_left_3 - extra_right_3)

    '''combined_jaw_width = np.mean([
        jaw_width * 0.6,
        #cheek_width,
        extra_width_1 * 0.5,
        extra_width_2,
        #extra_width_3
    ])'''
    combined_jaw_width = (jaw_width*0.7 + extra_width_1*0.5 + extra_width_2*0.8) / 2

    ratio = (combined_jaw_width / temple_width)

    # Класифікація
    if ratio < 0.842:
        jaw_class = 'вузька'
    elif ratio > 0.866:
        jaw_class = 'широка'
    else:
        jaw_class = 'середня'

    metrics = {
        'Тип щелепи': jaw_class,
        'jaw/temple_ratio': round(ratio, 3)
    }

    if return_points:
        pts = {
            'left_temple': left_temple, 'right_temple': right_temple,
            'left_jaw': left_jaw, 'right_jaw': right_jaw,
            #'left_cheek': left_cheek, 'right_cheek': right_cheek,
            'extra_left_1': extra_left_1, 'extra_right_1': extra_right_1,
            'extra_left_2': extra_left_2, 'extra_right_2': extra_right_2,
            #'extra_left_3': extra_left_3, 'extra_right_3': extra_right_3,
        }
        return metrics, pts

    return metrics
