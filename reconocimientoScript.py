import threading
from tkinter import messagebox
import cv2
import os
import usuario
import interfaz

"""
def userFound():
    interfazUsuario.show_profile_window()
    print("user found")"""
    
def recognize(userValidate, validation):
    dataPath = 'D:/UPC2024-2/IA/2 corte/reconocimientoFacial/data'  # ruta  Data
    imagePaths = os.listdir(dataPath)
    print('imagePaths=', imagePaths)

    # reconocimiento de rostro
    face_recognizer = cv2.face.LBPHFaceRecognizer_create()
    # Leyendo el modelo
    face_recognizer.read('D:/UPC2024-2/IA/2 corte/reconocimientoFacial/modeloLBPHFace.xml')
    # ====================================================================
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)  # VIDEO CAMARA
    #cap = cv2.VideoCapture(f'D:/UPC2024-2/IA/2 corte/reconocimientoFacial/users/{user}.mp4')#USUARIOS EXISTENTES
    #cap = cv2.VideoCapture(f'D:/UPC2024-2/IA/2 corte/reconocimientoFacial/test/{user}.MP4')#PRUEBA
    faceClassif = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    # Configuración de la ventana
    cv2.namedWindow('frame', cv2.WINDOW_NORMAL)
    screen_width = 600  # Cambia según la resolución de tu pantalla
    screen_height = 600  # Cambia según la resolución de tu pantalla
    window_width = 600  # Ancho de la ventana de OpenCV
    window_height = 600  # Alto de la ventana de OpenCV

    # Calcula la posición para centrar la ventana
    pos_x = (screen_width - window_width) // 2
    pos_y = (screen_height - window_height) // 2

    # Mueve la ventana al centro
    cv2.resizeWindow('frame', window_width, window_height)
    cv2.moveWindow('frame', pos_x, pos_y)
    
        
    reconocida = False  # Inicializar como no reconocida
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        auxFrame = gray.copy()

        faces = faceClassif.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=6)

        for (x, y, w, h) in faces:
            rostro = auxFrame[y:y + h, x:x + w]
            rostro = cv2.resize(rostro, (150, 150), interpolation=cv2.INTER_CUBIC)
            result = face_recognizer.predict(rostro)

            cv2.putText(frame, '{}'.format(result), (x, y - 5), 1, 1.3, (255, 255, 0), 1, cv2.LINE_AA)

            # LBPHFace
            if result[1] < 70:

                cv2.putText(frame, '{}'.format(imagePaths[result[0]]), (x, y - 25), 2, 1.1, (0, 255, 0), 1, cv2.LINE_AA)
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                print(f"Persona reconocida: {imagePaths[result[0]]}")
                if validation:
                    if userValidate==imagePaths[result[0]]:
                        messagebox.showinfo("Resultado", f"Reconocimiento facial exitoso, bienvenido {imagePaths[result[0]]}.")
                        print("histogramas")
                        cap.release()
                        cv2.destroyAllWindows()
                        usuario.cargar_histogramas(imagePaths[result[0]])
                        
                        reconocida = True  # Marcar como reconocida

                    else:
                        print("error")
                        messagebox.showinfo("Error", f"Usuario incorrecto, usted no es: {userValidate}.")
                        cap.release()
                        cv2.destroyAllWindows()
                        
                else:
                    return
                #threading.Thread(target=User, daemon=True).start() # type: ignore
                #user_profile_window = UserProfileWindow(interfaz, imagePaths[result[0]])
                
                
                print("Si")
                print("no")
                #userFound()
                

                #cv2.destroyAllWindows()
                #break  # Salir del bucle de detección de rostros
            
            else:
                print("error")
                messagebox.showinfo("Error", f"Usuario incorrecto, usted no es: {userValidate}.")
                cap.release()
                cv2.destroyAllWindows()
                #cv2.putText(frame, 'Desconocido', (x, y - 20), 2, 0.8, (0, 0, 255), 1, cv2.LINE_AA)
                #cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
    

        if reconocida:
            print("que pasa con la interfaz")
            break  # Salir del bucle principal
        
        

        cv2.imshow('frame', frame)
        k = cv2.waitKey(1)
        if k == 27:  # Presionar 'ESC' para salir manualmente
            break

    # Fuera del bucle principal
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    recognize()
