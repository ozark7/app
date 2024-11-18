import cv2
import os

dataPath = '../reconocimientoFacial/data'  # Cambia a la ruta donde hayas almacenado Data
imagePaths = os.listdir(dataPath)
print('imagePaths=', imagePaths)


def iniciar():
    
    # Inicializar la captura de video desde la cámara
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)  # Para la cámara predeterminada
    if not cap.isOpened():
        print("Error al abrir la cámara.")
        exit()

    # Cargar el clasificador de rostros
    faceClassif = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    # Cargar el modelo LBPH
    face_recognizer = cv2.face.LBPHFaceRecognizer_create()  # Inicializa el modelo LBPH
    face_recognizer.read('../reconocimientoFacial/modeloLBPHFace.xml')  # Carga el modelo previamente entrenado

    while True:
        ret, frame = cap.read()
        if not ret:  # Si no se pudo leer el frame
            print("Error al leer el frame.")
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        auxFrame = gray.copy()
        faces = faceClassif.detectMultiScale(gray, 1.3, 5)
        
        for (x, y, w, h) in faces:
            rostro = auxFrame[y:y + h, x:x + w]
            rostro = cv2.resize(rostro, (150, 150), interpolation=cv2.INTER_CUBIC)

            # Realiza la predicción usando el modelo cargado
            label, confidence = face_recognizer.predict(rostro)  # Devuelve la etiqueta y la confianza de la predicción
            
            # Mostrar el resultado
            if confidence < 70:  # Ajusta el umbral según el modelo
                cv2.putText(frame, '{}'.format(imagePaths[label]), (x, y - 25), 2, 1.1, (0, 255, 0), 1, cv2.LINE_AA)
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            else:
                cv2.putText(frame, 'Desconocido', (x, y - 20), 2, 0.8, (0, 0, 255), 1, cv2.LINE_AA)
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)

        cv2.imshow('frame', frame)
        k = cv2.waitKey(1)
        if k == 27:  # Si presionas ESC, sale del loop
            break

    cap.release()
    cv2.destroyAllWindows()
