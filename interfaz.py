import json
import os
import tkinter as tk
import capturandoRostros
from tkinter import filedialog
import usuario
import entrenandoRF
from tkinter import messagebox
import threading
import pruebaReconocimiento
import reconocimientoScript  # Asegúrate de que este script esté disponible en el mismo directorio


# Ventana Principal =================================================================
class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        
        self.title("Reconocimiento Facial")
        self.geometry("600x600")
        self.resizable(False, False)
        self.configure(bg="#d0e6f5")

        self.center_window()

        # Frame principal
        self.frame = tk.Frame(self, bg="#a2c1d9", bd=10, relief="solid", padx=20, pady=20)
        self.frame.place(relx=0.5, rely=0.5, anchor="center")

        # Logo (imagen de ejemplo)
        self.logo_label = tk.Label(self.frame, bg="#a2c1d9")
        self.logo_label.grid(row=0, column=0, columnspan=2)

        # Botón Ingresar
        self.btn_login = tk.Button(self.frame, text="Ingresar", font=("Arial", 16), bg="#6fa8dc", fg="white", relief="solid", width=20, height=2, command=self.open_login_window)
        self.btn_login.grid(row=1, column=0, pady=10)

        # Botón Registrar Nuevo Usuario
        self.btn_register = tk.Button(self.frame, text="Registrar Nuevo Usuario", font=("Arial", 16), bg="#6fa8dc", fg="white", relief="solid", width=20, height=2, command=self.open_register_window)
        self.btn_register.grid(row=2, column=0, pady=10)

    def open_login_window(self):
        # Ocultar la ventana principal
        self.withdraw()  

        # Abrir la ventana de inicio de sesión
        login_window = LoginWindow(self)
        login_window.grab_set()  # Hacer la ventana modal
        self.wait_window(login_window)  # Esperar a que se cierre la ventana de login

        # Mostrar de nuevo la ventana principal cuando se cierre la ventana de login
        self.deiconify()  # Muestra la ventana principal nuevamente

    def open_register_window(self):
        # Ocultar la ventana principal
        self.withdraw()  

        # Abrir la ventana de registro
        register_window = RegisterWindow(self)
        register_window.grab_set()  # Hacer la ventana modal
        self.wait_window(register_window)  # Esperar a que se cierre la ventana de registro

        # Mostrar de nuevo la ventana principal cuando se cierre la ventana de registro
        self.deiconify()  # Muestra la ventana principal nuevamente

    def center_window(self):
        window_width = 600
        window_height = 600
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        position_top = int(screen_height / 2 - window_height / 2)
        position_left = int(screen_width / 2 - window_width / 2)
        self.geometry(f'{window_width}x{window_height}+{position_left}+{position_top}')


# Ventana Inicial #1 ==============================================================================
class LoginWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Inicio de sesion")
        self.geometry("400x300")
        self.resizable(False, False)
        self.configure(bg="#d0e6f5")

        self.center_window()

        # Frame de formulario
        self.frame = tk.Frame(self, bg="#a2c1d9", bd=10, relief="solid", padx=20, pady=20)
        self.frame.place(relx=0.5, rely=0.5, anchor="center")

        # Usuario
        self.label_user = tk.Label(self.frame, text="Usuario:", font=("Arial", 12), bg="#a2c1d9")
        self.label_user.grid(row=0, column=0, padx=10, pady=5)
        self.input_user = tk.Entry(self.frame, font=("Arial", 12))
        self.input_user.grid(row=0, column=1, padx=10, pady=5)

        # Contraseña
        self.label_password = tk.Label(self.frame, text="Contraseña:", font=("Arial", 12), bg="#a2c1d9")
        self.label_password.grid(row=1, column=0, padx=10, pady=5)
        self.input_password = tk.Entry(self.frame, font=("Arial", 12), show="*")
        self.input_password.grid(row=1, column=1, padx=10, pady=5)

        # Botón Iniciar Sesión
        self.btn_login = tk.Button(self.frame, text="Iniciar Sesión", font=("Arial", 12), bg="#6fa8dc", fg="white", width=10, height=2, command=self.validate_login)
        self.btn_login.grid(row=3, column=0, padx=2, pady=10)
        
        # Botón Prueba
        self.btn_prueba = tk.Button(self.frame, text="Prueba", font=("Arial", 12), bg="#6fa8dc", fg="white", width=10, height=2, command=lambda:pruebaReconocimiento.iniciar())
        self.btn_prueba.grid(row=3, column=1, padx=2, pady=10)
     
    def validate_login(self):
        usuario = self.input_user.get()
        contra = self.input_password.get()
        
        # Verificar si los campos están vacíos
        if not usuario or not contra:
            messagebox.showwarning("Error", "Por favor, complete todos los campos.")
            return

        # Ruta donde se almacenan los datos de los usuarios
        data_folder = "./data"
        user_file = os.path.join(data_folder, usuario, "info.json")  # Archivo JSON del usuario

        # Verificar si el usuario existe
        if not os.path.exists(user_file):
            messagebox.showerror("Error", "El usuario no existe. Por favor, registrese primero.")
            return

        # Leer el archivo JSON del usuario y validar credenciales
        try:
            with open(user_file, "r") as file:
                user_data = json.load(file)
                if user_data["usuario"] == usuario and user_data["contra"] == contra:
                    messagebox.showinfo("Inicio de Sesión", "¡Inicio de sesión exitoso!")
                    threading.Thread(target=self.start_recognition, daemon=True).start()
                else:
                    messagebox.showerror("Error", "Credenciales incorrectas. Intente de nuevo.")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo validar el usuario: {str(e)}")

    def start_recognition(self):
        user = self.input_user.get()
        # Llama a la función de reconocimiento facial en un hilo separado
        reconocimientoScript.recognize(user, validation=True)
        
        #messagebox.showinfo("Resultado", "Reconocimiento facial exitoso.")

    def center_window(self):
        window_width = 400
        window_height = 300
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        position_top = int(screen_height / 2 - window_height / 2)
        position_left = int(screen_width / 2 - window_width / 2)
        self.geometry(f'{window_width}x{window_height}+{position_left}+{position_top}')


# Ventana de Registro #2 ===============================================================
class RegisterWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Registrar Nuevo Usuario")
        self.geometry("400x300")
        self.resizable(False, False)
        self.configure(bg="#d0e6f5")

        self.center_window()

        # Frame de formulario
        self.frame = tk.Frame(self, bg="#a2c1d9", bd=10, relief="solid", padx=20, pady=20)
        self.frame.place(relx=0.5, rely=0.5, anchor="center")

        # Usuario
        self.label_user = tk.Label(self.frame, text="Usuario:", font=("Arial", 12), bg="#a2c1d9")
        self.label_user.grid(row=0, column=0, padx=10, pady=5)
        self.input_user = tk.Entry(self.frame, font=("Arial", 12))
        self.input_user.grid(row=0, column=1, padx=10, pady=5)

        # Contraseña
        self.label_password = tk.Label(self.frame, text="Contraseña:", font=("Arial", 12), bg="#a2c1d9")
        self.label_password.grid(row=1, column=0, padx=10, pady=5)
        self.input_password = tk.Entry(self.frame, font=("Arial", 12), show="*")
        self.input_password.grid(row=1, column=1, padx=10, pady=5)


        # Botones en fila
        self.btn_register = tk.Button(self.frame, text="Registrar", font=("Arial", 12), bg="#6fa8dc", fg="white", width=10, height=2, command=self.register_user)
        self.btn_register.grid(row=3, column=0, padx=2, pady=10, sticky="e")

        self.btn_video = tk.Button(self.frame, text="Video", font=("Arial", 12), bg="#6fa8dc", fg="white", width=10, height=2, command=self.video_user)
        self.btn_video.grid(row=3, column=1, padx=2, pady=10, sticky="ew")

        self.btn_save = tk.Button(self.frame, text="Guardar", font=("Arial", 12), bg="#6fa8dc", fg="white", width=10, height=2, command=self.guardar_user)
        self.btn_save.grid(row=3, column=2, padx=2, pady=10, sticky="w")

    def guardar_user(self):
        if self.input_user.get() == "" or self.input_password.get() == "":
            messagebox.showinfo("Error", "Usuario o contraseña inválido")
        else:
            entrenandoRF.entrenando()
        
    
    def video_user(self):
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
        print(file_path)
        
        
        
    def register_user(self):
        contra = self.input_password.get()
        usuario = self.input_user.get()
        """
        if not self.input_user.get() or not self.input_password.get():
            messagebox.showinfo("Error", "Usuario o contraseña inválidos.")
        else:
            messagebox.showinfo("Registro", "Usuario registrado exitosamente.")
            capturandoRostros.prueba(self.input_user.get(), camara=True, video=None)
        """
        
        
        if not usuario or not contra:
            messagebox.showwarning("Error", "Por favor, complete todos los campos.")
            return
        
        # Ruta donde se almacenan los datos de los usuarios (por ejemplo, la carpeta "data")
        data_folder = "./data"
        user_path = os.path.join(data_folder, usuario)
        
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
            # Aquí puedes guardar más información del usuario en su carpeta, como la contraseña
            # por ejemplo, en un archivo de texto cifrado.
            capturandoRostros.prueba(usuario, camara=True, video=None)
            #entrenandoRF.entrenando()
            
            print(f"Usuario '{usuario}' registrado con éxito.")
            messagebox.showinfo("Registro", "Usuario registrado exitosamente.")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo registrar el usuario: {str(e)}")
   
        print(usuario)
        print(contra)
        print("Registrando usuario...")
        
        

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