import tkinter as tk
from tkinter import ttk
import os
from tkinter import messagebox
import matplotlib.pyplot as plt

def cargar_histogramas(usuario):
    """
    Cargar y mostrar los histogramas (documentos de texto) de la carpeta de un usuario específico.
    """
    url = "D:/UPC2024-2/IA/2 corte/reconocimientoFacial/histograms/" + usuario
    carpeta_usuario = os.path.join("carpeta_histogramas", url)  
    if not os.path.exists(carpeta_usuario):
        print(f"La carpeta para el usuario '{usuario}' no existe.")
        return

    # Crear la ventana principal
    ventana1 = tk.Tk()
    ventana1.geometry("800x600")
    ventana1.title(f"Histogramas de {usuario}")
    ventana1.configure(bg="#f0f0f0")
    
    # Centro la ventana en la pantalla
    ventana1.eval('tk::PlaceWindow %s center' % ventana1.winfo_toplevel())

    # Contenedor para scroll
    container = ttk.Frame(ventana1, style="TFrame")
    container.pack(fill="both", expand=True, padx=20, pady=20)

    canvas = tk.Canvas(container)
    scrollbar = ttk.Scrollbar(container, orient="vertical", command=canvas.yview)
    scrollable_frame = ttk.Frame(canvas)

    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )

    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    # Lista para almacenar los datos de los histogramas
    histogramas_datos = []

    # Función para guardar las gráficas como imágenes en una carpeta
    def guardar_imagenes():
        
        ventana1.destroy()
        messagebox.showinfo("Exito", "Espere unos momentos...")

        # Crear la carpeta de imágenes si no existe
        carpeta_imagenes = "imagenes_histogramas"
        
        # Crear la carpeta del usuario dentro de la carpeta principal de imágenes
        carpeta_usuario_imagenes = os.path.join(carpeta_imagenes, usuario)
        if not os.path.exists(carpeta_usuario_imagenes):
            os.makedirs(carpeta_usuario_imagenes)
            print(f"Carpeta del usuario '{usuario}' creada dentro de '{carpeta_imagenes}'.")

        # Leer los archivos de histogramas y mostrar
        for i, archivo in enumerate(os.listdir(carpeta_usuario)):
            if archivo.endswith(".txt"):  # Suponiendo que los histogramas están guardados como archivos .txt
                ruta = os.path.join(carpeta_usuario, archivo)

                # Abrir y leer el contenido del archivo de texto
                with open(ruta, 'r') as file:
                    contenido = file.read()
                    # Convertir el contenido en una lista de valores (suponiendo que son números decimales)
                    valores = [float(val) for val in contenido.split()]

                # Crear la gráfica
                plt.figure(figsize=(6, 4))
                plt.bar(range(len(valores)), valores, color="skyblue")
                plt.title(archivo)
                plt.xlabel("Índice")
                plt.ylabel("Valor")

                # Guardar la imagen en la carpeta del usuario
                nombre_imagen = os.path.join(carpeta_usuario_imagenes, f"{archivo.replace('.txt', '')}.png")  # Ruta completa
                plt.savefig(nombre_imagen, format="png")  # Guardar la gráfica como PNG
                print(f"Imagen guardada como {nombre_imagen}")
                
                # Limpiar la figura para la siguiente
                plt.close()

    # Función para crear una gráfica de línea mostrando cómo fluctúan los valores
    def graficar_linea():
        plt.figure(figsize=(6, 4))
        all_values = []

        # Leer los archivos de histogramas y extraer los valores
        for archivo in os.listdir(carpeta_usuario):
            if archivo.endswith(".txt"):
                ruta = os.path.join(carpeta_usuario, archivo)

                # Abrir y leer el contenido del archivo de texto
                with open(ruta, 'r') as file:
                    contenido = file.read()
                    # Convertir el contenido en una lista de valores (suponiendo que son números decimales)
                    valores = [float(val) for val in contenido.split()]
                    all_values.extend(valores)  # Agregar estos valores a la lista global

        # Crear la gráfica de línea
        plt.plot(all_values, marker='o', color='b', linestyle='-', markersize=4)
        plt.title(f"Fluctuación de los Valores de los Histogramas de {usuario}")
        plt.xlabel("Índice")
        plt.ylabel("Valor")
        plt.grid(True)

        # Mostrar la gráfica
        plt.show()

    # Botones
    btn_guardar_imagenes = ttk.Button(
        ventana1, 
        text="Generar Imágenes de Histogramas", 
        command=guardar_imagenes,
        style="TButton"
    )
    btn_guardar_imagenes.pack(pady=20, side="left", padx=10)

    btn_graficar_linea = ttk.Button(
        ventana1, 
        text="Generar Gráfica de Fluctuación de Valores", 
        command=graficar_linea,
        style="TButton"
    )
    btn_graficar_linea.pack(pady=20, side="left", padx=10)

    # Leer los archivos de histogramas y mostrar en la interfaz
    for archivo in os.listdir(carpeta_usuario):
        if archivo.endswith(".txt"):  
            ruta = os.path.join(carpeta_usuario, archivo)

            # Abrir y leer el contenido del archivo de texto
            with open(ruta, 'r') as file:
                contenido = file.read()
                # Convertir el contenido en una lista de valores (suponiendo que son números decimales)
                valores = [float(val) for val in contenido.split()]

            # Crear un marco para cada archivo
            frame = ttk.Frame(scrollable_frame, style="TFrame")
            frame.pack(pady=10, padx=10, fill="x")

            # Etiqueta para el nombre del archivo
            lbl_nombre = tk.Label(frame, text=archivo, font=("Arial", 12, "bold"), fg="#0078d4")
            lbl_nombre.pack()

            # Crear un gráfico de barras utilizando Canvas de Tkinter
            canvas_histograma = tk.Canvas(frame, width=400, height=300, bg="white")
            canvas_histograma.pack(pady=10)

            # Determinar el tamaño de las barras (cada barra será un rectángulo)
            max_valor = max(valores)
            ancho_barra = 30
            espacio_barras = 10
            for i, valor in enumerate(valores):
                # Dibujar la barra correspondiente
                canvas_histograma.create_rectangle(
                    i * (ancho_barra + espacio_barras),  # x1
                    300 - (valor / max_valor) * 250,  # y1
                    (i + 1) * (ancho_barra + espacio_barras),  # x2
                    300,  # y2
                    fill="skyblue"
                )
    
    ventana1.mainloop()
#cargar_histogramas(usuario="pepi")
