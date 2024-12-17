import cv2
import mediapipe as mp
from controller import Controller
import threading
import time

# Inicialización de la cámara y Mediapipe
cap = cv2.VideoCapture(0)
mpHands = mp.solutions.hands
hands = mpHands.Hands(max_num_hands=1, min_detection_confidence=0.7, min_tracking_confidence=0.7)
mpDraw = mp.solutions.drawing_utils

# Variables de control
lock = threading.Lock()  # Para asegurar la sincronización entre hilos
fps = 30  # Control de cuadros por segundo
last_update = time.time()

def execute_in_thread(target_function):
    """Ejecuta la función en un hilo independiente, con manejo seguro de concurrencia."""
    thread = threading.Thread(target=target_function, daemon=True)
    thread.start()

while True:
    start_time = time.time()  # Medir tiempo de inicio del cuadro
    success, img = cap.read()
    if not success:
        print("No se pudo acceder a la cámara.")
        break

    img = cv2.flip(img, 1)  # Voltear la imagen horizontalmente
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(imgRGB)

    if results.multi_hand_landmarks:
        with lock:  # Evitar conflictos entre hilos
            Controller.hand_Landmarks = results.multi_hand_landmarks[0]
            mpDraw.draw_landmarks(img, Controller.hand_Landmarks, mpHands.HAND_CONNECTIONS)

            # Actualizamos el estado de los dedos y ejecutamos funciones según sea necesario
            Controller.update_fingers_status()

            # Ejecutar acciones relevantes en hilos
            execute_in_thread(Controller.cursor_moving)
            execute_in_thread(Controller.detect_scrolling)
            execute_in_thread(Controller.detect_zoomming)
            execute_in_thread(Controller.detect_clicking)
            execute_in_thread(Controller.detect_dragging)

    # Mostrar la imagen procesada en pantalla
    cv2.imshow('Hand Tracker', img)

    # Controlar el FPS para evitar saturar el sistema
    elapsed_time = time.time() - start_time
    wait_time = max(1, int((1 / fps - elapsed_time) * 1000))
    if cv2.waitKey(wait_time) & 0xFF == 27:  # Salir con la tecla 'Esc'
        break

cap.release()
cv2.destroyAllWindows()
