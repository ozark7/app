from tkinter import messagebox
import cv2
import os
import imutils
import entrenandoRF

def entrenar():
    entrenandoRF.entrenando()
    
def prueba(usuario, camara=False, video=None):

	
	dataPath = 'D:/UPC2024-2/IA/2 corte/reconocimientoFacial/data' #Cambia a la ruta donde hayas almacenado Data
	personPath = dataPath + '/' + usuario

	if not os.path.exists(personPath):
		print('Carpeta creada: ',personPath)
		os.makedirs(personPath)

	if camara:
		cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)  
	elif video is not None:
		cap = cv2.VideoCapture(video)
  
	

	faceClassif = cv2.CascadeClassifier(cv2.data.haarcascades+'haarcascade_frontalface_default.xml')
	count = 0

	while True:

		ret, frame = cap.read()
		if ret == False: break
		frame =  imutils.resize(frame, width=640)
		gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
		auxFrame = frame.copy()

		faces = faceClassif.detectMultiScale(gray,1.3,5)

		for (x,y,w,h) in faces:
			cv2.rectangle(frame, (x,y),(x+w,y+h),(0,255,0),2)
			rostro = auxFrame[y:y+h,x:x+w]
			rostro = cv2.resize(rostro,(150,150),interpolation=cv2.INTER_CUBIC)
			cv2.imwrite(personPath + '/rotro_{}.jpg'.format(count),rostro)
			count = count + 1
		cv2.imshow('frame',frame)

		k =  cv2.waitKey(1)
		if k == 27 or count >= 300:
			break

	cap.release()
	cv2.destroyAllWindows()
	messagebox.showinfo("Registro", f"Reconocimiento facial exitoso. No olvide GUARDAR. ")  

#prueba("pepi", True)