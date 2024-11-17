from tkinter import messagebox
import cv2
import os
import numpy as np
from skimage.feature import local_binary_pattern

def entrenando():
    # Configuraciones de LBP
    radius = 1  # Radio para LBP
    n_points = 8 * radius  # Puntos de vecinos para LBP

    # Rutas
    dataPath = 'D:/UPC2024-2/IA/2 corte/reconocimientoFacial/data'  # Ruta donde están las imágenes de cada persona
    outputPath = 'D:/UPC2024-2/IA/2 corte/reconocimientoFacial/histograms'  # Carpeta para guardar los histogramas

    # Crear la carpeta de histogramas si no existe
    if not os.path.exists(outputPath):
        os.makedirs(outputPath)

    # Obtener la lista de personas (carpetas en dataPath)
    peopleList = os.listdir(dataPath)
    print('Lista de personas:', peopleList)

    labels = []
    facesData = []
    label = 0

    # Recorremos cada carpeta de persona en el dataPath
    for nameDir in peopleList:
        personPath = os.path.join(dataPath, nameDir)
        personHistogramPath = os.path.join(outputPath, nameDir)
        
        # Crear la carpeta de histogramas de la persona si no existe
        if not os.path.exists(personHistogramPath):
            os.makedirs(personHistogramPath)
        
        print(f'Leyendo las imágenes de {nameDir}')
        
        for fileName in os.listdir(personPath):
            # Leer imagen en escala de grises
            imagePath = os.path.join(personPath, fileName)
            image = cv2.imread(imagePath, 0)
            
            # Añadir la imagen y el label a la lista para entrenamiento
            facesData.append(image)
            labels.append(label)
            
            # Generar el histograma LBP
            lbp = local_binary_pattern(image, n_points, radius, method="uniform")
            hist, _ = np.histogram(lbp.ravel(),
                                bins=np.arange(0, n_points + 3),
                                range=(0, n_points + 2))
            
            # Normalizar el histograma
            hist = hist.astype("float")
            hist /= (hist.sum() + 1e-6)  # Evitar división por cero
            
            # Guardar el histograma en un archivo de texto
            histogramPath = os.path.join(personHistogramPath, f"{fileName}_histogram.txt")
            np.savetxt(histogramPath, hist, fmt="%f")
            print(f"Histograma guardado en: {histogramPath}")
        
        label += 1

    # Crear el modelo de reconocimiento LBPH de OpenCV
    face_recognizer = cv2.face.LBPHFaceRecognizer_create()

    # Entrenar el modelo con las imágenes y etiquetas obtenidas
    print("Entrenando el modelo LBPH...")
    face_recognizer.train(facesData, np.array(labels))

    # Guardar el modelo entrenado
    modelPath = 'D:/UPC2024-2/IA/2 corte/reconocimientoFacial/modeloLBPHFace.xml'
    face_recognizer.write(modelPath)
    print(f"Modelo entrenado y guardado en {modelPath}")
    messagebox.showinfo("Correcto", "Usuario guardado correctamente")


#entrenando()