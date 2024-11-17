import tkinter as tk
import capturandoRostros
from tkinter import filedialog
import usuario
import entrenandoRF
from tkinter import messagebox
import threading
import reconocimientoScript  # Asegúrate de que este script esté disponible en el mismo directorio


# Ventana Principal =================================================================
class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Reconocimiento Facial")
        self.geometry("500x250")  # Ajusté el tamaño para una apariencia más cómoda
        self.resizable(False, False)
        self.configure(bg="#f0f0f0")  # Fondo neutro

        self.center_window()

        # Frame principal
        self.frame = tk.Frame(self, bg="#ffffff", bd=0, relief="flat", padx=20, pady=20)
        self.frame.place(relx=0.5, rely=0.5, anchor="center")

        # Título
        self.title_label = tk.Label(
            self.frame,
            text="Reconocimiento Facial",
            font=("Poppins", 20, "bold"),
            bg="#ffffff",
            fg="#4a4a4a",
        )
        self.title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20), padx=10)

        # Botón Ingresar
        self.btn_login = tk.Button(
            self.frame,
            text="Ingresar",
            font=("Poppins", 14),
            bg="#0078d4",
            fg="#ffffff",
            relief="flat",
            width=25,
            height=2,
            command=self.open_login_window,
        )
        self.btn_login.grid(row=1, column=0, pady=10, padx=10)

        # Botón Registrar Nuevo Usuario
        self.btn_register = tk.Button(
            self.frame,
            text="Registrar Usuario",
            font=("Poppins", 14),
            bg="#0078d4",
            fg="#ffffff",
            relief="flat",
            width=25,
            height=2,
            command=self.open_register_window,
        )
        self.btn_register.grid(row=2, column=0, pady=10, padx=10)

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
        window_width = 400
        window_height = 400
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        position_top = int(screen_height / 2 - window_height / 2)
        position_left = int(screen_width / 2 - window_width / 2)
        self.geometry(f"{window_width}x{window_height}+{position_left}+{position_top}")


# Ventana de Inicio de Sesión ========================================================
class LoginWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Inicio de Sesión")
        
        self.geometry("400x250")
        self.resizable(False, False)
        self.configure(bg="#f0f0f0")

        self.center_window()

        self.frame = tk.Frame(self, bg="#ffffff", bd=0, relief="flat", padx=20, pady=20)
        self.frame.place(relx=0.5, rely=0.5, anchor="center")

        # Usuario
        self.label_user = tk.Label(
            self.frame,
            text="Usuario:",
            font=("Poppins", 12),
            bg="#ffffff",
            fg="#4a4a4a",
        )
        self.label_user.grid(row=0, column=0, padx=10, pady=5, sticky="e")
        self.input_user = tk.Entry(self.frame, font=("Poppins", 12), width=20)
        self.input_user.grid(row=0, column=1, padx=10, pady=5)

        # Contraseña
        self.label_password = tk.Label(
            self.frame,
            text="Contraseña:",
            font=("Poppins", 12),
            bg="#ffffff",
            fg="#4a4a4a",
        )
        self.label_password.grid(row=1, column=0, padx=10, pady=5, sticky="e")
        self.input_password = tk.Entry(self.frame, font=("Poppins", 12), show="*", width=20)
        self.input_password.grid(row=1, column=1, padx=10, pady=5)

        # Botón Iniciar Sesión
        self.btn_login = tk.Button(
            self.frame,
            text="Iniciar Sesión",
            font=("Poppins", 12),
            bg="#0078d4",
            fg="#ffffff",
            relief="flat",
            width=15,
            height=1,
            command=self.validate_login,
        )
        self.btn_login.grid(row=2, column=0, columnspan=2, pady=20)

    def validate_login(self):
        if not self.input_user.get() or not self.input_password.get():
            messagebox.showinfo("Error", "Usuario o contraseña inválidos.")
        else:
            threading.Thread(target=self.start_recognition, daemon=True).start()

    def start_recognition(self):
        reconocimientoScript.recognize()

    def center_window(self):
        window_width = 400
        window_height = 250
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        position_top = int(screen_height / 2 - window_height / 2)
        position_left = int(screen_width / 2 - window_width / 2)
        self.geometry(f"{window_width}x{window_height}+{position_left}+{position_top}")


# Ventana de Registro de Usuario =====================================================
class RegisterWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Registrar Usuario")
        self.geometry("400x300")
        self.resizable(False, False)
        self.configure(bg="#f0f0f0")

        self.center_window()

        self.frame = tk.Frame(self, bg="#ffffff", bd=0, relief="flat", padx=20, pady=20)
        self.frame.place(relx=0.5, rely=0.5, anchor="center")

        # Usuario
        self.label_user = tk.Label(
            self.frame,
            text="Usuario:",
            font=("Poppins", 12),
            bg="#ffffff",
            fg="#4a4a4a",
        )
        self.label_user.grid(row=0, column=0, padx=10, pady=5, sticky="e")
        self.input_user = tk.Entry(self.frame, font=("Poppins", 12), width=20)
        self.input_user.grid(row=0, column=1, padx=10, pady=5)

        # Contraseña
        self.label_password = tk.Label(
            self.frame,
            text="Contraseña:",
            font=("Poppins", 12),
            bg="#ffffff",
            fg="#4a4a4a",
        )
        self.label_password.grid(row=1, column=0, padx=10, pady=5, sticky="e")
        self.input_password = tk.Entry(self.frame, font=("Poppins", 12), show="*", width=20)
        self.input_password.grid(row=1, column=1, padx=10, pady=5)

        # Botones
        self.btn_register = tk.Button(
            self.frame,
            text="Registrar",
            font=("Poppins", 12),
            bg="#0078d4",
            fg="#ffffff",
            relief="flat",
            width=15,
            command=self.register_user,
        )
        self.btn_register.grid(row=2, column=0, columnspan=2, pady=20)

    def register_user(self):
        if not self.input_user.get() or not self.input_password.get():
            messagebox.showinfo("Error", "Usuario o contraseña inválidos.")
        else:
            messagebox.showinfo("Registro", "Usuario registrado exitosamente.")
            capturandoRostros.prueba(self.input_user.get(), camara=True, video=None)

    def center_window(self):
        window_width = 300
        window_height = 300
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        position_top = int(screen_height / 2 - window_height / 2)
        position_left = int(screen_width / 2 - window_width / 2)
        self.geometry(f"{window_width}x{window_height}+{position_left}+{position_top}")


# Ejecutar la ventana principal =======================================================
if __name__ == "__main__":
    app = MainWindow()
    app.mainloop()
