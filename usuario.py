import tkinter as tk
from tkinter import ttk
import os
from tkinter import messagebox
import matplotlib.pyplot as plt


# Paleta de colores
PRIMARY_COLOR = "#ff9900"  # Naranja
SECONDARY_COLOR = "#ffd966"  # Amarillo claro
BACKGROUND_COLOR = "#ffffff"  # Blanco
TEXT_COLOR = "#333333"  # Texto gris oscuro


def cargar_histogramas(usuario):
    """
    Cargar y mostrar los histogramas (documentos de texto) de la carpeta de un usuario específico en lotes de 5.
    """
    url = "../reconocimientoFacial/histograms/" + usuario
    carpeta_usuario = url

    if not os.path.exists(carpeta_usuario):
        print(f"La carpeta para el usuario '{usuario}' no existe.")
        return

    # Crear la ventana principal
    ventana1 = tk.Tk()
    ventana1.geometry("800x600")
    ventana1.title(f"Histogramas de {usuario}")
    ventana1.configure(bg=BACKGROUND_COLOR)

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

    # Variables para control de paginación
    archivos = [f for f in os.listdir(carpeta_usuario) if f.endswith(".txt")]
    pagina_actual = 0
    tamanio_pagina = 5

    # Función para mostrar los histogramas de la página actual
    def mostrar_pagina():
        for widget in scrollable_frame.winfo_children():
            widget.destroy()

        inicio = pagina_actual * tamanio_pagina
        fin = inicio + tamanio_pagina
        archivos_pagina = archivos[inicio:fin]

        for archivo in archivos_pagina:
            ruta = os.path.join(carpeta_usuario, archivo)

            with open(ruta, 'r') as file:
                contenido = file.read()
                valores = [float(val) for val in contenido.split()]

            # Crear un marco para cada archivo
            frame = ttk.Frame(scrollable_frame, style="TFrame")
            frame.pack(pady=10, padx=10, fill="x")

            lbl_nombre = tk.Label(frame, text=archivo, font=("Arial", 12, "bold"), fg="#0078d4")
            lbl_nombre.pack()

            canvas_histograma = tk.Canvas(frame, width=400, height=300, bg="white")
            canvas_histograma.pack(pady=10)

            # Crear gráfico de barras
            max_valor = max(valores)
            ancho_barra = 30
            espacio_barras = 10
            for i, valor in enumerate(valores):
                canvas_histograma.create_rectangle(
                    i * (ancho_barra + espacio_barras),  # x1
                    300 - (valor / max_valor) * 250,  # y1
                    (i + 1) * (ancho_barra + espacio_barras),  # x2
                    300,  # y2
                    fill="skyblue"
                )

    # Funciones para cambiar de página
    def pagina_anterior():
        nonlocal pagina_actual
        if pagina_actual > 0:
            pagina_actual -= 1
            mostrar_pagina()

    def pagina_siguiente():
        nonlocal pagina_actual
        if (pagina_actual + 1) * tamanio_pagina < len(archivos):
            pagina_actual += 1
            mostrar_pagina()

    # Función para guardar las gráficas como imágenes en una carpeta
    def guardar_imagenes():
        messagebox.showinfo("Éxito", "Espere unos momentos...")
        carpeta_imagenes = "imagenes_histogramas"
        carpeta_usuario_imagenes = os.path.join(carpeta_imagenes, usuario)

        if not os.path.exists(carpeta_usuario_imagenes):
            os.makedirs(carpeta_usuario_imagenes)

        for archivo in archivos:
            ruta = os.path.join(carpeta_usuario, archivo)
            with open(ruta, 'r') as file:
                valores = [float(val) for val in file.read().split()]

            plt.figure(figsize=(6, 4))
            plt.bar(range(len(valores)), valores, color="skyblue")
            plt.title(archivo)
            plt.xlabel("Índice")
            plt.ylabel("Valor")
            nombre_imagen = os.path.join(carpeta_usuario_imagenes, f"{archivo.replace('.txt', '')}.png")
            plt.savefig(nombre_imagen, format="png")
            plt.close()

        messagebox.showinfo("Éxito", "Imágenes guardadas correctamente.")

    # Función para crear una gráfica de línea mostrando cómo fluctúan los valores
    def graficar_linea():
        plt.figure(figsize=(6, 4))
        all_values = []

        for archivo in archivos:
            ruta = os.path.join(carpeta_usuario, archivo)
            with open(ruta, 'r') as file:
                valores = [float(val) for val in file.read().split()]
                all_values.extend(valores)

        plt.plot(all_values, marker='o', color='b', linestyle='-', markersize=4)
        plt.title(f"Fluctuación de los Valores de los Histogramas de {usuario}")
        plt.xlabel("Índice")
        plt.ylabel("Valor")
        plt.grid(True)
        plt.show()

    # Botones de navegación
    btn_anterior = ttk.Button(
        ventana1,
        text="Página Anterior",
        command=pagina_anterior,
        style="TButton"
    )
    btn_anterior.pack(side="left", padx=10)

    btn_siguiente = ttk.Button(
        ventana1,
        text="Página Siguiente",
        command=pagina_siguiente,
        style="TButton"
    )
    btn_siguiente.pack(side="right", padx=10)

    # Botones para generar imágenes y gráficas
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

    # Mostrar la primera página
    mostrar_pagina()

    ventana1.mainloop()


# Prueba de la función (descomentar para probar)
#cargar_histogramas(usuario="silvia")
