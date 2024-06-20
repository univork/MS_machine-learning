import base64
from typing import Optional
import numpy as np
import cv2 as cv
from PIL import Image, ImageOps


TARGET_SIZE = 60, 60


def resize_image(img) -> np.ndarray:
    img = Image.fromarray(img)
    if img.size[0] < TARGET_SIZE[0]:
        delta_width = 60 - img.size[0]
        delta_height = 60 - img.size[1]

        pad_width = delta_width // 2
        pad_height = delta_height // 2
        padding = (pad_width, pad_height, delta_width - pad_width, delta_height - pad_height)
        img = ImageOps.expand(img, padding)
    else:
        img.thumbnail((60, 60), Image.Resampling.LANCZOS)
    return np.asarray(img)


def extract_face(img: cv.typing.MatLike) -> tuple[Optional[np.array], Optional[cv.typing.MatLike]]:
    face_cascade = cv.CascadeClassifier(cv.data.haarcascades + 'haarcascade_frontalface_alt2.xml')
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(gray, 1.1, 3)
    if len(faces) == 0:
        return None, None
    x, y, w, h = faces[0]
    cv.rectangle(img, (x, y), (x+w, y+h),  
                (0, 0, 255), 2)
    face = img[y:y + h, x:x + w] 
    face_ready = resize_image(face).reshape(1, 60*60*3)
    _, buffer = cv.imencode('.png', img)
    png_as_text = "data:image/png;base64," + base64.b64encode(buffer).decode()
    return face_ready, png_as_text


def load_cv2_from_file(file) -> cv.typing.MatLike:
    npimg = np.frombuffer(file.read(), np.uint8)
    img = cv.imdecode(npimg, cv.IMREAD_COLOR)
    return img


def load_cv2_from_base64(base64_image: str):
    encoded_data = base64_image.split(',')[1]
    npimg = np.frombuffer(base64.b64decode(encoded_data), np.uint8)
    img = cv.imdecode(npimg, cv.IMREAD_COLOR)
    return img
