import json
import os
import tkinter as tk
from tkinter import filedialog, messagebox
import threading
from tkinter import ttk

import capturandoRostros
import usuario
import entrenandoRF
import reconocimientoScript
import pruebaReconocimiento

# Paleta de colores
PRIMARY_COLOR = "#ff9900"  # Naranja
SECONDARY_COLOR = "#ffd966"  # Amarillo claro
BACKGROUND_COLOR = "#ffffff"  # Blanco
TEXT_COLOR = "#333333"  # Texto gris oscuro

# Ventana Principal
class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        
        self.title("Reconocimiento Facial")
        self.geometry("600x600")
        self.configure(bg=BACKGROUND_COLOR)
        self.resizable(False, False)
        self.center_window()

        # Logo
        self.logo_label = tk.Label(self, text="Facial Recognition", font=("Helvetica", 24, "bold"), bg=BACKGROUND_COLOR, fg=PRIMARY_COLOR)
        self.logo_label.pack(pady=30)

        # Contenedor
        self.frame = tk.Frame(self, bg=BACKGROUND_COLOR)
        self.frame.pack(expand=True)

        # Botón Ingresar
        self.btn_login = tk.Button(
            self.frame, text="Ingresar", font=("Helvetica", 16), bg=PRIMARY_COLOR, fg="white",
            relief="flat", width=20, height=2, command=self.open_login_window
        )
        self.btn_login.pack(pady=15)

        # Botón Registrar Nuevo Usuario
        self.btn_register = tk.Button(
            self.frame, text="Registrar Nuevo Usuario", font=("Helvetica", 16), bg=SECONDARY_COLOR, fg="white",
            relief="flat", width=20, height=2, command=self.open_register_window
        )
        self.btn_register.pack(pady=15)

    def open_login_window(self):
        self.withdraw()  
        login_window = LoginWindow(self)
        login_window.grab_set()
        self.wait_window(login_window)
        self.deiconify()

    def open_register_window(self):
        self.withdraw()  
        register_window = RegisterWindow(self)
        register_window.grab_set()
        self.wait_window(register_window)
        self.deiconify()

    def center_window(self):
        window_width = 600
        window_height = 600
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        position_top = int(screen_height / 2 - window_height / 2)
        position_left = int(screen_width / 2 - window_width / 2)
        self.geometry(f'{window_width}x{window_height}+{position_left}+{position_top}')


# Ventana de Login
class LoginWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        
        self.title("Inicio de Sesión")
        self.geometry("400x400")
        self.configure(bg=BACKGROUND_COLOR)
        self.resizable(False, False)
        self.center_window()

        # Contenedor
        self.frame = tk.Frame(self, bg=BACKGROUND_COLOR, pady=20)
        self.frame.pack(expand=True)

        # Título
        self.title_label = tk.Label(self.frame, text="Iniciar Sesión", font=("Helvetica", 20, "bold"), bg=BACKGROUND_COLOR, fg=PRIMARY_COLOR)
        self.title_label.pack(pady=20)

        # Campo de usuario
        self.label_user = tk.Label(self.frame, text="Usuario", font=("Helvetica", 12), bg=BACKGROUND_COLOR, fg=TEXT_COLOR)
        self.label_user.pack()
        self.input_user = tk.Entry(self.frame, font=("Helvetica", 12), width=25, relief="solid")
        self.input_user.pack(pady=10)

        # Campo de contraseña
        self.label_password = tk.Label(self.frame, text="Contraseña", font=("Helvetica", 12), bg=BACKGROUND_COLOR, fg=TEXT_COLOR)
        self.label_password.pack()
        self.input_password = tk.Entry(self.frame, font=("Helvetica", 12), show="*", width=25, relief="solid")
        self.input_password.pack(pady=10)

        # Botones
        self.btn_login = tk.Button(self.frame, text="Iniciar Sesión", font=("Helvetica", 14), bg=PRIMARY_COLOR, fg="white", width=15, height=1, relief="flat", command=self.validate_login)
        self.btn_login.pack(pady=10)

        self.btn_test = tk.Button(self.frame, text="Prueba", font=("Helvetica", 14), bg=SECONDARY_COLOR, fg="white", width=15, height=1, relief="flat", command=lambda: pruebaReconocimiento.iniciar())
        self.btn_test.pack(pady=10)

    def validate_login(self):
        usuario = self.input_user.get()
        contra = self.input_password.get()

        if not usuario or not contra:
            messagebox.showwarning("Error", "Por favor, complete todos los campos.")
            return

        data_folder = f"./app/credentials/{usuario}"
        user_file = os.path.join(data_folder, "info.json")

        if not os.path.exists(user_file):
            messagebox.showerror("Error", "El usuario no existe.")
            return

        try:
            with open(user_file, "r") as file:
                user_data = json.load(file)
                if user_data["usuario"] == usuario and user_data["contra"] == contra:
                    #messagebox.showinfo("Inicio de Sesión", "¡Inicio de sesión exitoso!")
                    threading.Thread(target=self.start_recognition, daemon=True).start()
                else:
                    messagebox.showerror("Error", "Credenciales incorrectas.")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo validar el usuario: {str(e)}")

    def start_recognition(self):
        user = self.input_user.get()
        reconocimientoScript.recognize(user, validation=True)

    def center_window(self):
        window_width = 400
        window_height = 400
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        position_top = int(screen_height / 2 - window_height / 2)
        position_left = int(screen_width / 2 - window_width / 2)
        self.geometry(f'{window_width}x{window_height}+{position_left}+{position_top}')




# Ventana de Registro #2 ===============================================================
class RegisterWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        # Colores de diseño
        BACKGROUND_COLOR = "#f0f0f0"
        PRIMARY_COLOR = "#6fa8dc"
        SECONDARY_COLOR = "#a2c1d9"
        
        
        # Colores de diseño
        BACKGROUND_COLOR = "#f0f0f0"
        PRIMARY_COLOR = "#6fa8dc"
        SECONDARY_COLOR = "#a2c1d9"

        self.title("Registrar Nuevo Usuario")
        #self.geometry("900x900")
        self.configure(bg=BACKGROUND_COLOR)
        self.resizable(False, False)
        self.center_window()

     

        # Contenedor
        self.frame = tk.Frame(self, bg=BACKGROUND_COLOR)
        self.frame.pack(expand=True)

        # Usuario
        self.label_user = tk.Label(self.frame, text="Usuario:", font=("Helvetica", 16), bg=BACKGROUND_COLOR, fg=PRIMARY_COLOR)
        self.label_user.grid(row=0, column=0, padx=20, pady=10, sticky="w")
        self.input_user = tk.Entry(self.frame, font=("Helvetica", 14), width=25)
        self.input_user.grid(row=0, column=1, padx=20, pady=10, sticky="ew")

        # Contraseña
        self.label_password = tk.Label(self.frame, text="Contraseña:", font=("Helvetica", 16), bg=BACKGROUND_COLOR, fg=PRIMARY_COLOR)
        self.label_password.grid(row=1, column=0, padx=20, pady=10, sticky="w")
        self.input_password = tk.Entry(self.frame, font=("Helvetica", 14), width=25, show="*")
        self.input_password.grid(row=1, column=1, padx=20, pady=10, sticky="ew")

        # Botones
        self.btn_register = tk.Button(
            self.frame, text="Registrar", font=("Helvetica", 14), bg=PRIMARY_COLOR, fg="white",
            relief="flat", width=15, height=1, command=self.register_user
        )
        self.btn_register.grid(row=3, column=0, padx=10, pady=10, sticky="e")

        self.btn_video = tk.Button(
            self.frame, text="Video", font=("Helvetica", 14), bg=SECONDARY_COLOR, fg="white",
            relief="flat", width=15, height=1, command=self.video_user
        )
        self.btn_video.grid(row=3, column=1, padx=10, pady=10, sticky="w")

        self.btn_save = tk.Button(
            self.frame, text="Guardar", font=("Helvetica", 14), bg=PRIMARY_COLOR, fg="white",
            relief="flat", width=14, height=1, command=self.guardar_user
        )
        self.btn_save.grid(row=4, column=0, columnspan=2, pady=10, sticky="ew")
    
    def guardar_user(self):
        if self.input_user.get() == "" or self.input_password.get() == "":
            messagebox.showinfo("Error", "Usuario o contraseña inválido")
        else:
            entrenandoRF.entrenando()
            
    def video_user(self):
        usuario = self.input_user.get()
        contra = self.input_password.get()

        # Verificar que los campos no estén vacíos
        if not usuario or not contra:
            messagebox.showwarning("Error", "Por favor, complete todos los campos.")
            return

        # Ruta donde se almacenan los datos de los usuarios
        user_path = os.path.join("./credentials", usuario)

        # Verificar si el usuario ya existe
        if os.path.exists(user_path):
            messagebox.showerror("Error", "El usuario ya existe. Por favor, elija otro nombre o utilice otro método.")
            return

        # Crear carpeta para el usuario y guardar credenciales
        try:
            os.makedirs(user_path)
            user_data = {
                "usuario": usuario,
                "contra": contra
            }
            with open(os.path.join(user_path, "info.json"), "w") as file:
                json.dump(user_data, file)
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo registrar el usuario: {str(e)}")
            return

        # Abrir el explorador de archivos y seleccionar un archivo de video
        file_path = filedialog.askopenfilename(
            title="Seleccionar archivo de video",  # Título del explorador de archivos
            filetypes=(("Archivos de video", "*.mp4;*.avi;*.mov"), ("Todos los archivos", "*.*"))  # Filtros para los tipos de archivo
        )

        # Verificar si se seleccionó un archivo
        if file_path:
            print(f"Archivo seleccionado: {file_path}")
            # Procesar el video para capturar los datos faciales
            try:
                capturandoRostros.prueba(usuario, camara=False, video=file_path)
                #messagebox.showinfo("Registro", f"Usuario '{usuario}' registrado exitosamente con el video proporcionado.")
            except Exception as e:
                messagebox.showerror("Error", f"Hubo un problema al procesar el video: {str(e)}")
        else:
            print("No se seleccionó ningún archivo.")
            messagebox.showinfo("Información", "No se seleccionó ningún archivo.")

        print(file_path)

    """def video_user(self):
        usuario = self.input_user.get()
        # Abrir el explorador de archivos y seleccionar un archivo
        file_path = filedialog.askopenfilename(
            title="Seleccionar archivo de video",  # Título del explorador de archivos
            filetypes=(("Archivos de video", "*.mp4;*.avi;*.mov"), ("Todos los archivos", "*.*"))  # Filtros para los tipos de archivo
        )

        # Verifica si el usuario seleccionó un archivo (no presionó Cancelar)
        if file_path:
            print(f"Archivo seleccionado: {file_path}")
            # Aquí puedes agregar el código para procesar el archivo seleccionado, por ejemplo, abrir el video.
            capturandoRostros.prueba(usuario, camara=False, video=(file_path))
        else:
            print("No se seleccionó ningún archivo")
        print(file_path)"""

    def register_user(self):
        contra = self.input_password.get()
        usuario = self.input_user.get()

        if not usuario or not contra:
            messagebox.showwarning("Error", "Por favor, complete todos los campos.")
            return

        # Ruta donde se almacenan los datos de los usuarios (por ejemplo, la carpeta "data")
        
        user_path = os.path.join("./app/credentials", usuario)

        # Verificar si el usuario ya existe
        if os.path.exists(user_path):
            messagebox.showerror("Error", "El usuario ya existe. Por favor, elija otro nombre.")
            return

        # Crear carpeta para el usuario
        try:
            os.makedirs(user_path)
            user_data = {
                "usuario": usuario,
                "contra": contra
            }
            with open(os.path.join(user_path, "info.json"), "w") as file:
                json.dump(user_data, file)
            print(f"Usuario '{usuario}' registrado con éxito.")
            messagebox.showinfo("Registro", "Usuario registrado exitosamente.")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo registrar el usuario: {str(e)}")

        print(usuario)
        print(contra)
        print("Registrando usuario...")
        capturandoRostros.prueba(usuario, camara=True, video=None)
        messagebox.showinfo("Registro", "Usuario registrado exitosamente.")

    def center_window(self):
        window_width = 400
        window_height = 300
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        position_top = int(screen_height / 2 - window_height / 2)
        position_left = int(screen_width / 2 - window_width / 2)
        self.geometry(f'{window_width}x{window_height}+{position_left}+{position_top}')

# Ejecutar la ventana principal =======================================================
if __name__ == "__main__":
    app = MainWindow()
    app.mainloop()