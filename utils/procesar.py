
import cv2
import mediapipe as mp
from PIL import Image

def detectar_ojos(image_path):
    mp_face_mesh = mp.solutions.face_mesh
    face_mesh = mp_face_mesh.FaceMesh(static_image_mode=True)
    
    image_cv = cv2.imread(image_path)
    rgb_image = cv2.cvtColor(image_cv, cv2.COLOR_BGR2RGB)
    results = face_mesh.process(rgb_image)

    if not results.multi_face_landmarks:
        return None

    # Ojos: punto 33 (izquierdo), 263 (derecho)
    h, w, _ = rgb_image.shape
    left_eye = results.multi_face_landmarks[0].landmark[33]
    right_eye = results.multi_face_landmarks[0].landmark[263]
    
    left = (int(left_eye.x * w), int(left_eye.y * h))
    right = (int(right_eye.x * w), int(right_eye.y * h))
    return left, right

def superponer_gafas(imagen_base_path, gafas_path):
    ojos = detectar_ojos(imagen_base_path)
    if not ojos:
        return Image.open(imagen_base_path)

    left, right = ojos
    imagen = Image.open(imagen_base_path).convert("RGBA")
    gafas = Image.open(gafas_path).convert("RGBA")

    # Calcular tamaño y posición
    distancia = int(((right[0] - left[0]) ** 2 + (right[1] - left[1]) ** 2) ** 0.5)
    escala = distancia * 2
    gafas = gafas.resize((escala, int(escala * 0.33)))

    # Posición centrada entre los ojos
    centro_x = int((left[0] + right[0]) / 2 - escala / 2)
    centro_y = int((left[1] + right[1]) / 2 - escala * 0.15)
    
    imagen.paste(gafas, (centro_x, centro_y), gafas)
    return imagen
