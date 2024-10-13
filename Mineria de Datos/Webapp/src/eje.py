import pandas as pd
import tkinter as tk
from tkinter import CENTER, ttk, messagebox
import psycopg2
from PIL import Image, ImageTk
import requests
from io import BytesIO
import webbrowser

class App:
        
    def __init__(self, root):
        self.root = root
        self.pantalla_web() 
        # Cargar los datos del archivo Excel
        self.ruta_archivo = r'C:\Users\danie\OneDrive\Documents\2024-1\Estilos y Lenguajes\src\Usuarios.xlsx'
        self.df_usuarios = pd.read_excel(self.ruta_archivo)
        
    def limpiar_pantalla(self):
        for widget in self.root.winfo_children():
            widget.destroy()
            
    def pantalla_web(self):
        """Muestra la pantalla de login para autenticación de usuarios."""
        self.limpiar_pantalla()
        self.root.geometry("3000x1000")
        self.root.configure(bg="black")

        # Header - Logo y Navegación
        self.header = tk.Frame(self.root, bg="black",width=3000, height=200)
        self.header.pack(fill="x", pady=10)

        self.logo = tk.Label(self.header, text="FC", font=("Arial", 24, "bold"), bg="black", fg="white")
        self.logo.pack(side="left", padx=20)

        self.nav = tk.Frame(self.header, bg="black", height=1000)
        self.nav.pack(side="right", padx=20, pady=7) 

        btn_acerca = tk.Button(self.nav, text="ACERCA DE", font=("Arial", 12,"bold"), bg="#3e3838", fg="white", bd=0, padx=20, pady=7, command=self.pantalla_acerca)
        btn_acerca.pack(side="left", padx=5)

        btn_registro = tk.Button(self.nav, text="REGISTRO", font=("Arial", 12,"bold"), bg="#3e3838", fg="white", bd=0, padx=20, pady=7, command=self.pantalla_registro)
        btn_registro.pack(side="left", padx=5)

        btn_login = tk.Button(self.nav, text="LOGIN", font=("Arial", 12,"bold"), bg="#3e3838", fg="white", bd=0, padx=20, pady=7, command=self.pantalla_login)
        btn_login.pack(side="left", padx=5)
        
        # Main content
        self.main = tk.Frame(self.root, bg="black", width=3000, height=800)
        self.main.pack(fill="both", expand=True)

        # Banner (derecha)
        self.banner = tk.Frame(self.main, bg="black", width=3000, height=100)
        self.banner.pack(side="left", fill="y",padx=100)

        # Cargar imagen principal
        img = Image.open("C:/Users/danie/OneDrive/Documents/2024-1/Estilos y Lenguajes/src/img/inicio.jpg")
        img = img.resize((678, 474), Image.LANCZOS)
        img = ImageTk.PhotoImage(img)

        # Mostrar imagen
        img_label = tk.Label(self.banner, image=img, bg="black")
        img_label.image = img
        img_label.pack(pady=70)
        
        # Cargar imagen appstore
        img2 = Image.open("C:/Users/danie/OneDrive/Documents/2024-1/Estilos y Lenguajes/src/img/appstore.jpg")
        img2 = img2.resize((190, 60), Image.LANCZOS)
        img2 = ImageTk.PhotoImage(img2)

        # Mostrar imagen en el banner usando pack en lugar de place
        img2_label = tk.Label(self.banner, image=img2)
        img2_label.image = img2
        img2_label.pack(pady=20) 
        img2_label.place(x=50, y=460)# Posiciona la imagen con margen superior
        
        # Enlazar la imagen de la App Store con el evento de clic
        img2_label.bind("<Button-1>", self.abrir_app_store)
        
        # Cargar imagen playstore
        img3 = Image.open("C:/Users/danie/OneDrive/Documents/2024-1/Estilos y Lenguajes/src/img/playstore.jpg")
        img3 = img3.resize((190, 60), Image.LANCZOS)
        img3 = ImageTk.PhotoImage(img3)

        # Mostrar imagen en el banner usando pack en lugar de place
        img3_label = tk.Label(self.banner, image=img3, bg="black")
        img3_label.image = img3
        img3_label.pack(pady=20) 
        img3_label.place(x=270, y=460)# Posiciona la imagen con margen superior
        
        # Enlazar la imagen de la Play Store con el evento de clic
        img3_label.bind("<Button-1>", self.abrir_play_store)
        
        title = tk.Label(self.banner, text="FilmCast", font=("SFUItext", 70,), fg="white", bg="black")
        title.pack(pady=20)
        title.place(x=40, y=150)

        subtitle = tk.Label(self.banner, text="Tu proyecto, nuestros actores.", font=("Heebo", 28), fg="white", bg="black")
        subtitle.pack(pady=20)
        subtitle.place(x=40, y=280)

        subtitle1 = tk.Label(self.banner, text="La conexión perfecta.", font=("Heebo", 28), fg="white", bg="black")
        subtitle1.pack(pady=20)
        subtitle1.place(x=40, y=350)
        
        subtitle2 = tk.Label(self.banner, text="Descubre a talentosos actores para tu próximo proyecto.", font=("Heebo", 14), fg="white", bg="black")
        subtitle2.pack(pady=20)
        subtitle2.place(x=10, y=558)
        
        btn_contacto = tk.Button(self.banner, text="CONTACTO", font=("Arial", 12, "bold"), bg="#3e3838", fg="white", bd=0, padx=20, pady=7, command=self.pantalla_contacto)
        btn_contacto.place(x=10, y=600)
        
        # Banner (derecha)
        self.banner = tk.Frame(self.main, bg="black", width=2000, height=800)
        self.banner.pack(side="right", fill="y", padx=0)

        # Cargar imagen celular
        img4 = Image.open("C:/Users/danie/OneDrive/Documents/2024-1/Estilos y Lenguajes/src/img/celular1.jpeg")
        img4 = img4.resize((329, 647), Image.LANCZOS)
        img4 = ImageTk.PhotoImage(img4)

        # Mostrar imagen en el banner usando pack en lugar de place
        img4_label = tk.Label(self.main, image=img4, bg="black")
        img4_label.image = img4
        img4_label.place(x=1145, y=20)  # Posiciona la imagen con margen superior
        
        # Cargar imagen celular
        img1 = Image.open("C:/Users/danie/OneDrive/Documents/2024-1/Estilos y Lenguajes/src/img/celular.jpeg")
        img1 = img1.resize((329, 657), Image.LANCZOS)
        img1 = ImageTk.PhotoImage(img1)

        # Mostrar imagen en el banner usando pack en lugar de place
        img1_label = tk.Label(self.main, image=img1, bg="black")
        img1_label.image = img1
        img1_label.place(x=830, y=20)  # Posiciona la imagen con margen superior
        
    def abrir_app_store(self, event):
        webbrowser.open("https://www.apple.com/app-store/")  # Enlace a la App Store

    def abrir_play_store(self, event):
        webbrowser.open("https://play.google.com/store")  # Enlace a la Play Store
        
    def pantalla_registro(self):
        """Muestra la pantalla de login para autenticación de usuarios."""
        self.limpiar_pantalla()
        self.root.geometry("3000x1000")
        self.root.configure(bg="black")  # Cambia el fondo de la ventana a negro

        # Header - Logo y Navegación
        self.header = tk.Frame(self.root, bg="black",width=3000, height=200)
        self.header.pack(fill="x", pady=10)

        self.logo = tk.Label(self.header, text="FC", font=("Arial", 24, "bold"), bg="black", fg="white")
        self.logo.pack(side="left", padx=20)

        self.nav = tk.Frame(self.header, bg="black", height=1000)
        self.nav.pack(side="right", padx=20, pady=7)  # Añadiendo margen

        btn_acerca = tk.Button(self.nav, text="ACERCA DE", font=("Arial", 12,"bold"), bg="#3e3838", fg="white", bd=0, padx=20, pady=7, command=self.pantalla_acerca)
        btn_acerca.pack(side="left", padx=5)

        btn_registro = tk.Button(self.nav, text="INICIO", font=("Arial", 12,"bold"), bg="#3e3838", fg="white", bd=0, padx=20, pady=7, command=self.pantalla_web)
        btn_registro.pack(side="left", padx=5)

        btn_login = tk.Button(self.nav, text="LOGIN", font=("Arial", 12,"bold"), bg="#3e3838", fg="white", bd=0, padx=20, pady=7, command=self.pantalla_login)
        btn_login.pack(side="left", padx=5)
        
        # Main content
        self.main = tk.Frame(self.root, bg="black", width=3000, height=800)
        self.main.pack(fill="both", expand=True)

        # Banner (izquierda)
        self.baner = tk.Frame(self.main, bg="black", width=1500, height=800)
        self.baner.pack(side="left", fill="y",padx=100)

        
        # Cargar imagen principal
        img = Image.open("C:/Users/danie/OneDrive/Documents/2024-1/Estilos y Lenguajes/src/img/inicio.jpg")
        img = img.resize((678, 474), Image.LANCZOS)
        img = ImageTk.PhotoImage(img)

        # Mostrar imagen
        img_label = tk.Label(self.baner, image=img, bg="black")
        img_label.image = img
        img_label.pack(pady=70)
        
        
        # Cargar imagen appstore
        img2 = Image.open("C:/Users/danie/OneDrive/Documents/2024-1/Estilos y Lenguajes/src/img/appstore.jpg")
        img2 = img2.resize((190, 60), Image.LANCZOS)
        img2 = ImageTk.PhotoImage(img2)

        # Mostrar imagen en el banner usando pack en lugar de place
        img2_label = tk.Label(self.baner, image=img2)
        img2_label.image = img2
        img2_label.pack(pady=20) 
        img2_label.place(x=50, y=460)# Posiciona la imagen con margen superior
        
        # Enlazar la imagen de la App Store con el evento de clic
        img2_label.bind("<Button-1>", self.abrir_app_store)
        
        # Cargar imagen playstore
        img3 = Image.open("C:/Users/danie/OneDrive/Documents/2024-1/Estilos y Lenguajes/src/img/playstore.jpg")
        img3 = img3.resize((190, 60), Image.LANCZOS)
        img3 = ImageTk.PhotoImage(img3)

        # Mostrar imagen en el banner usando pack en lugar de place
        img3_label = tk.Label(self.baner, image=img3, bg="black")
        img3_label.image = img3
        img3_label.pack(pady=20) 
        img3_label.place(x=270, y=460)# Posiciona la imagen con margen superior
        
        # Enlazar la imagen de la Play Store con el evento de clic
        img3_label.bind("<Button-1>", self.abrir_play_store)
        
        title = tk.Label(self.baner, text="FilmCast", font=("SFUItext", 70,), fg="white", bg="black")
        title.pack(pady=20)
        title.place(x=40, y=150)

        subtitle = tk.Label(self.baner, text="Tu proyecto, nuestros actores.", font=("Heebo", 28), fg="white", bg="black")
        subtitle.pack(pady=20)
        subtitle.place(x=40, y=280)

        subtitle1 = tk.Label(self.baner, text="La conexión perfecta.", font=("Heebo", 28), fg="white", bg="black")
        subtitle1.pack(pady=20)
        subtitle1.place(x=40, y=350)
        
        subtitle2 = tk.Label(self.baner, text="Descubre a talentosos actores para tu próximo proyecto.", font=("Heebo", 14), fg="white", bg="black")
        subtitle2.pack(pady=20)
        subtitle2.place(x=10, y=558)
        
        btn_contacto = tk.Button(self.baner, text="CONTACTO", font=("Arial", 12, "bold"), bg="#3e3838", fg="white", bd=0, padx=20, pady=7, command=self.pantalla_acerca)
        btn_contacto.place(x=10, y=600)
        
        # Banner (derecha)
        self.banner = tk.Frame(self.main, bg="black", width=1500, height=800)
        self.banner.pack(side="right", pady=0)
        self.banner.pack_propagate(0)
        self.logo = tk.Label(self.banner, text="Crea tu cuenta", font=("Heebo", 40, "bold"), bg="black", fg="white")
        self.logo.place(x=10, y=60)
    
        self.usuario =tk.Label(self.banner, text="Usuario:", font=("Heebo", 22), bg="black", fg="white")
        self.usuario.place(x=35, y=170)
        self.entry_usuario = tk.Entry(self.banner, font=("Heebo", 22))
        self.entry_usuario.place(x=35, y=210)

        self.contrasena=tk.Label(self.banner, text="Contraseña:", font=("Heebo", 22), bg="black", fg="white")
        self.contrasena.place(x=35, y=300)
        self.entry_contrasena = tk.Entry(self.banner, show="*", font=("Heebo", 22))
        self.entry_contrasena.place(x=35, y=340)
        
        self.confirma=tk.Label(self.banner, text="Confirmar Contraseña:", font=("Heebo", 22), bg="black", fg="white")
        self.confirma.place(x=35, y=430)
        self.entry_confirmar_contrasena = tk.Entry(self.banner, show="*", font=("Heebo", 22))
        self.entry_confirmar_contrasena.place(x=35, y=470)
        
         
        btn_regist = tk.Button(self.banner, text="Siguiente", font=("Arial", 14, "bold"), bg="#3e3838", fg="white",bd=0, padx=20, pady=7, command=self.Registrar_usuario_confirmar)
        btn_regist.place(x=450, y=570)

        btn_regresa = tk.Button(self.banner, text="Regresar", font=("Arial", 14, "bold"), bg="#3e3838", fg="white",bd=0, padx=20, pady=7, command=self.pantalla_web)
        btn_regresa.place(x=35, y=570)
        
        
        
        # Labels para mostrar informacion/errores
        self.mostrar_info = tk.Label(self.banner, text="", font=("Arial", 12), bg="black", fg="green")
        self.mostrar_info.pack(pady=5)

        self.error_usuario = tk.Label(self.banner, text="", font=("Arial", 12), bg="black", fg="red")
        self.error_usuario.place(x=35, y=250)

        self.error_contrasena = tk.Label(self.banner, text="", font=("Arial", 12), bg="black", fg="red")
        self.error_contrasena.place(x=35, y=380)

        self.error_confirmar_contrasena = tk.Label(self.banner, text="", font=("Arial", 12), bg="black", fg="red")
        self.error_confirmar_contrasena.place(x=35, y=510)
        
    def Registrar_usuario_confirmar1(self):
        """Confirma la creación de un nuevo usuario y lo guarda en el archivo."""
        usuario = self.entry_usuario.get()
        contrasena = self.entry_contrasena.get()
        confirmar_contrasena = self.entry_confirmar_contrasena.get()

        # Limpiar mensajes de error anteriores
        self.error_usuario.config(text="")
        self.error_contrasena.config(text="")
        self.error_confirmar_contrasena.config(text="")

        if not usuario:
            self.error_usuario.config(text="Ingrese un nombre de usuario.")
            return

        if not contrasena:
            self.error_contrasena.config(text="Ingrese una contraseña.")
            return

        if not confirmar_contrasena:
            self.error_confirmar_contrasena.config(text="Confirme la contraseña.")
            return

        if contrasena != confirmar_contrasena:
            self.error_confirmar_contrasena.config(text="Las contraseñas no coinciden.")
            return

        # Comprobar si el nombre de usuario ya existe en el DataFrame
        if usuario in self.df_usuarios['nombre'].values:
            self.error_usuario.config(text="El nombre de usuario ya existe.")
            return

        # Agregar un nuevo usuario al DataFrame
        nuevo_usuario = pd.DataFrame({
            "nombre": [usuario],
            "clave": [contrasena]
        })

        self.df_usuarios = pd.concat([self.df_usuarios, nuevo_usuario], ignore_index=True)

        # Guardar el DataFrame actualizado en el archivo
        self.df_usuarios.to_excel('Usuarios.xlsx', index=False)  # Sobrescribe el archivo Excel
        # Si es CSV, usa self.df_usuarios.to_csv('Usuarios.csv', index=False)

        # Mostrar mensaje de éxito
        self.mostrar_info.config(text="Usuario creado y guardado correctamente.")
        print(self.df_usuarios)  # Puedes quitar esto o usarlo para depurar
          
    def Registrar_usuario_confirmar(self):
        """Confirma la creación de un nuevo usuario."""
        usuario = self.entry_usuario.get()
        contrasena = self.entry_contrasena.get()
        confirmar_contrasena = self.entry_confirmar_contrasena.get()

        # Limpiar errores anteriores
        self.error_usuario.config(text="")
        self.error_contrasena.config(text="")
        self.error_confirmar_contrasena.config(text="")

        if not usuario:
            self.error_usuario.config(text="Ingrese un nombre de usuario.")
            return

        if not contrasena:
            self.error_contrasena.config(text="Ingrese una contraseña.")
            return

        if not confirmar_contrasena:
            self.error_confirmar_contrasena.config(text="Confirme la contraseña.")
            return

        if contrasena != confirmar_contrasena:
            self.error_confirmar_contrasena.config(text="Las contraseñas no coinciden.")
            return
        
        # Leer el archivo existente
        self.df_usuarios = pd.read_excel(self.ruta_archivo)

        # Verificar si el nombre de usuario ya existe
        if usuario in self.df_usuarios['nombre'].values:
            self.error_usuario.config(text="Ese nombre de usuario ya existe.")
        return

        # Agregar el nuevo usuario al DataFrame
        nuevo_usuario = pd.DataFrame({
            'nombre': [usuario],
            'clave': [contrasena]
        })

        # Leer el archivo existente
        self.df_usuarios = pd.read_excel(self.ruta_archivo)

        # Concatenar el nuevo usuario al DataFrame existente
        self.df_usuarios = pd.concat([self.df_usuarios, nuevo_usuario], ignore_index=True)

        # Guardar el DataFrame actualizado en el archivo
        self.df_usuarios.to_excel(self.ruta_archivo, index=False)  # Sobrescribe el archivo Excel

        self.mostrar_info.config(text="Usuario creado correctamente.")
        self.entry_usuario.delete(0, 'end')
        self.entry_contrasena.delete(0, 'end')
        self.entry_confirmar_contrasena.delete(0, 'end')
        print(self.df_usuarios)
    
    def pantalla_login(self):
        """Muestra la pantalla de login para autenticación de usuarios."""
        self.limpiar_pantalla()
        self.root.geometry("3000x1000")
        self.root.configure(bg="black")  # Cambia el fondo de la ventana a negro

        # Header - Logo y Navegación
        self.header = tk.Frame(self.root, bg="black",width=3000, height=200)
        self.header.pack(fill="x", pady=10)

        self.logo = tk.Label(self.header, text="FC", font=("Arial", 24, "bold"), bg="black", fg="white")
        self.logo.pack(side="left", padx=20)

        self.nav = tk.Frame(self.header, bg="black", height=1000)
        self.nav.pack(side="right", padx=20, pady=7)  # Añadiendo margen

        btn_acerca = tk.Button(self.nav, text="ACERCA DE", font=("Arial", 12,"bold"), bg="#3e3838", fg="white", bd=0, padx=20, pady=7, command=self.pantalla_acerca)
        btn_acerca.pack(side="left", padx=5)

        btn_registro = tk.Button(self.nav, text="REGISTRO", font=("Arial", 12,"bold"), bg="#3e3838", fg="white", bd=0, padx=20, pady=7, command=self.pantalla_registro)
        btn_registro.pack(side="left", padx=5)

        btn_login = tk.Button(self.nav, text="INICIO", font=("Arial", 12,"bold"), bg="#3e3838", fg="white", bd=0, padx=20, pady=7, command=self.pantalla_web)
        btn_login.pack(side="left", padx=5)
        
        # Main content
        self.main = tk.Frame(self.root, bg="black", width=3000, height=800)
        self.main.pack(fill="both", expand=True)

        # Banner (izquierda)
        self.baner = tk.Frame(self.main, bg="black", width=1500, height=800)
        self.baner.pack(side="left", fill="y",padx=100)

        
        # Cargar imagen principal
        img = Image.open("C:/Users/danie/OneDrive/Documents/2024-1/Estilos y Lenguajes/src/img/inicio.jpg")
        img = img.resize((678, 474), Image.LANCZOS)
        img = ImageTk.PhotoImage(img)

        # Mostrar imagen
        img_label = tk.Label(self.baner, image=img, bg="black")
        img_label.image = img
        img_label.pack(pady=70)
        
        
        # Cargar imagen appstore
        img2 = Image.open("C:/Users/danie/OneDrive/Documents/2024-1/Estilos y Lenguajes/src/img/appstore.jpg")
        img2 = img2.resize((190, 60), Image.LANCZOS)
        img2 = ImageTk.PhotoImage(img2)

        # Mostrar imagen en el banner usando pack en lugar de place
        img2_label = tk.Label(self.baner, image=img2)
        img2_label.image = img2
        img2_label.pack(pady=20) 
        img2_label.place(x=50, y=460)# Posiciona la imagen con margen superior
        
        # Enlazar la imagen de la App Store con el evento de clic
        img2_label.bind("<Button-1>", self.abrir_app_store)
        
        # Cargar imagen playstore
        img3 = Image.open("C:/Users/danie/OneDrive/Documents/2024-1/Estilos y Lenguajes/src/img/playstore.jpg")
        img3 = img3.resize((190, 60), Image.LANCZOS)
        img3 = ImageTk.PhotoImage(img3)

        # Mostrar imagen en el banner usando pack en lugar de place
        img3_label = tk.Label(self.baner, image=img3, bg="black")
        img3_label.image = img3
        img3_label.pack(pady=20) 
        img3_label.place(x=270, y=460)# Posiciona la imagen con margen superior
        
        # Enlazar la imagen de la Play Store con el evento de clic
        img3_label.bind("<Button-1>", self.abrir_play_store)
        
        title = tk.Label(self.baner, text="FilmCast", font=("SFUItext", 70,), fg="white", bg="black")
        title.pack(pady=20)
        title.place(x=40, y=150)

        subtitle = tk.Label(self.baner, text="Tu proyecto, nuestros actores.", font=("Heebo", 28), fg="white", bg="black")
        subtitle.pack(pady=20)
        subtitle.place(x=40, y=280)

        subtitle1 = tk.Label(self.baner, text="La conexión perfecta.", font=("Heebo", 28), fg="white", bg="black")
        subtitle1.pack(pady=20)
        subtitle1.place(x=40, y=350)
        
        subtitle2 = tk.Label(self.baner, text="Descubre a talentosos actores para tu próximo proyecto.", font=("Heebo", 14), fg="white", bg="black")
        subtitle2.pack(pady=20)
        subtitle2.place(x=10, y=558)
        
        btn_contacto = tk.Button(self.baner, text="CONTACTO", font=("Arial", 12, "bold"), bg="#3e3838", fg="white", bd=0, padx=20, pady=7, command=self.pantalla_acerca)
        btn_contacto.place(x=10, y=600)

        # Banner (derecha)
        frame_interno = tk.Frame(self.main, bg="black", width=1500, height=800)
        frame_interno.pack(side="right", pady=0)
        frame_interno.pack_propagate(0)
        
        self.logo=tk.Label(frame_interno, text="Inicio de Sesión", font=("Heebo", 40, "bold"), bg="black", fg="white")
        self.logo.place(x=10, y=60)
        
        self.entrausu=tk.Label(frame_interno, text="Usuario:", font=("Heebo", 22), bg="black", fg="white")
        self.entrausu.place(x=35, y=170)
        self.entrada_usuario = tk.Entry(frame_interno, font=("Heebo", 22))
        self.entrada_usuario.place(x=35, y=210)
        
        self.entrclave=tk.Label(frame_interno, text="Clave:", font=("Heebo", 22), bg="black", fg="white")
        self.entrclave.place(x=35, y=300)
        self.entrada_clave = tk.Entry(frame_interno, show="*", font=("Heebo", 22))
        self.entrada_clave.place(x=35, y=340)
        
        btn_regi = tk.Button(frame_interno, text="Volver", font=("Arial", 14, "bold"), bg="#3e3838", fg="white",bd=0, padx=20, pady=7, command=self.pantalla_web)
        btn_regi.place(x=35, y=500)
        
        btn_ini = tk.Button(frame_interno, text="Iniciar", font=("Arial", 14, "bold"), bg="#3e3838", fg="white",bd=0, padx=20, pady=7,  command=self.validar_login)
        btn_ini.place(x=450, y=500)       
      
    def validar_login(self):
        """Valida las credenciales del usuario contra los datos en Excel."""
        usuario = self.entrada_usuario.get()
        clave = self.entrada_clave.get()

        # Filtrar el DataFrame para comprobar si existen el usuario y la clave
        resultado = self.df_usuarios[(self.df_usuarios['nombre'] == usuario) & 
                                     (self.df_usuarios['clave'] == clave)]

        if not resultado.empty:
            
            # Si se encontró el usuario, guardar su información
            self.usuario_actual = {
                'nombre': resultado.iloc[0]['nombre'],
                'clave': resultado.iloc[0]['clave'],
                'email': resultado.iloc[0]['email'],  # Suponiendo que tienes una columna 'email'
                'telefono': resultado.iloc[0]['telefono'],  # Suponiendo que tienes una columna 'telefono'
                'descripcion': resultado.iloc[0]['descripcion'],  # Suponiendo que tienes una columna 'email'
                'Pais': resultado.iloc[0]['Pais']  # Suponiendo que tienes una columna 'telefono'
            }
            # Proceder al menú principal
            self.menu_principal()
            
        else:
            # Mostrar mensaje de error si el usuario o la clave no coinciden
            self.erro=tk.Label(self.root, text="Usuario o clave incorrectos", font=("Arial", 10), bg="black", fg="red")
            self.erro.place(x=915, y=328)
            self.ero=tk.Label(self.root, text="Usuario o clave incorrectos", font=("Arial", 10), bg="black", fg="red")
            self.ero.place(x=915, y=460)
            self.entrada_usuario.delete(0, tk.END)
            self.entrada_clave.delete(0, tk.END)
            self.entrada_usuario.focus()
            self.entrada_clave.focus()    
        
    def pantalla_acerca(self):
        """Muestra el menú principal con opciones para cada módulo."""
        self.limpiar_pantalla()
        self.root.geometry("3000x1000")
        self.root.configure(bg="black")
    
         # Header - Logo y Navegación
        self.header = tk.Frame(self.root, bg="black",width=3000, height=200)
        self.header.pack(fill="x", pady=10)

        self.logo = tk.Label(self.header, text="FC", font=("Arial", 24, "bold"), bg="black", fg="white")
        self.logo.pack(side="left", padx=20)

        self.nav = tk.Frame(self.header, bg="black", height=1000)
        self.nav.pack(side="right", padx=20, pady=7)  # Añadiendo margen

        btn_acerca = tk.Button(self.nav, text="INICIO", font=("Arial", 12,"bold"), bg="#3e3838", fg="white", bd=0, padx=20, pady=7, command=self.pantalla_web)
        btn_acerca.pack(side="left", padx=5)

        btn_registro = tk.Button(self.nav, text="REGISTRO", font=("Arial", 12,"bold"), bg="#3e3838", fg="white", bd=0, padx=20, pady=7, command=self.pantalla_registro)
        btn_registro.pack(side="left", padx=5)

        btn_login = tk.Button(self.nav, text="LOGIN", font=("Arial", 12,"bold"), bg="#3e3838", fg="white", bd=0, padx=20, pady=7, command=self.pantalla_login)
        btn_login.pack(side="left", padx=5)
        
        # Main content
        self.main = tk.Frame(self.root, bg="black", width=3000, height=800)
        self.main.pack(fill="both", expand=True)

        # Banner (derecha)
        self.baner = tk.Frame(self.main, bg="black", width=1200, height=800)
        self.baner.pack(side="right", fill="y",padx=50)

        
        # Cargar imagen principal
        img = Image.open("C:/Users/danie/OneDrive/Documents/2024-1/Estilos y Lenguajes/src/img/telon.jpg")
        img = img.resize((451, 881), Image.LANCZOS)
        img = ImageTk.PhotoImage(img)

        # Mostrar imagen
        img_label = tk.Label(self.baner, image=img, bg="black")
        img_label.image = img
        img_label.pack(pady=70,padx=70)
        
        # Banner (Izquierda)
        self.banner = tk.Frame(self.main, bg="black", width=1800, height=800)
        self.banner.pack(side="left", fill="y",padx=0)
        self.banner.pack_propagate(0)
        
        self.log = tk.Label(self.banner, text="Acerca de FilmCast", font=("Arial", 30, "bold"), bg="black", fg="white")
        self.log.place(x=285,y=45)
        
        self.lo = tk.Label(self.banner, text="Una aplicacion para conectar\nproductores con actores", font=("Arial", 40, "bold"), bg="black", fg="white")
        self.lo.place(x=100,y=175)
        
        self.l = tk.Label(self.banner, text="FilmCast es una plataforma diseñada para que\nlos productores puedan buscar actores según\nel perfil y las habilidades que requieran para\nsus proyectos.", font=("Arial", 25), bg="black", fg="white")
        self.l.place(x=130,y=345)
        
        btn_Contac = tk.Button(self.banner, text="Contacto", font=("Arial", 16,"bold"), bg="#641013", fg="black", bd=0, padx=20, pady=7, command=self.pantalla_contacto)
        btn_Contac.place(x=385,y=550)
        
    def pantalla_contacto(self):
        
        """Muestra el menú principal con opciones para cada módulo."""
        self.limpiar_pantalla()
        self.root.geometry("3000x1000")
        self.root.configure(bg="black")
    
         # Header - Logo y Navegación
        self.header = tk.Frame(self.root, bg="black",width=3000, height=200)
        self.header.pack(fill="x", pady=10)

        self.logo = tk.Label(self.header, text="FC", font=("Arial", 24, "bold"), bg="black", fg="white")
        self.logo.pack(side="left", padx=20)

        self.nav = tk.Frame(self.header, bg="black", height=1000)
        self.nav.pack(side="right", padx=20, pady=7)  # Añadiendo margen

        btn_acerca = tk.Button(self.nav, text="ACERCA DE", font=("Arial", 12,"bold"), bg="#3e3838", fg="white", bd=0, padx=20, pady=7, command=self.pantalla_acerca)
        btn_acerca.pack(side="left", padx=5)

        btn_registro = tk.Button(self.nav, text="REGISTRO", font=("Arial", 12,"bold"), bg="#3e3838", fg="white", bd=0, padx=20, pady=7, command=self.pantalla_registro)
        btn_registro.pack(side="left", padx=5)

        btn_login = tk.Button(self.nav, text="LOGIN", font=("Arial", 12,"bold"), bg="#3e3838", fg="white", bd=0, padx=20, pady=7, command=self.pantalla_login)
        btn_login.pack(side="left", padx=5)
        
        # Main content
        self.main = tk.Frame(self.root, bg="black", width=3000, height=590)
        self.main.pack(fill="both", expand=False)

        # Banner (derecha)
        self.baner = tk.Frame(self.main, bg="black", width=760, height=590)
        self.baner.pack(side="right", fill="y",padx=0)
        self.baner.pack_propagate(0)
        
        self.texo = tk.Label(self.baner, text="Si deseas formar parte de\nnuestro equipo, estamos\nen busca del mejor talento\nactoral.", font=("Arial", 28, "bold"), bg="black", fg="white")
        self.texo.place(x=160,y=25)
        
        # Cargar imagen principal
        img = Image.open("C:/Users/danie/OneDrive/Documents/2024-1/Estilos y Lenguajes/src/img/set.jpeg")
        img = img.resize((540, 340), Image.LANCZOS)
        img = ImageTk.PhotoImage(img)

        # Mostrar imagen
        img_label = tk.Label(self.baner, image=img, bg="black")
        img_label.image = img
        img_label.place(x=120, y=220)
        
        # Banner (Izquierda)
        self.banner = tk.Frame(self.main, bg="white", width=1800, height=590)
        self.banner.pack(side="left", fill="y",padx=0)
        self.banner.pack_propagate(0)
        
        self.cont = tk.Label(self.banner, text="Contáctanos", font=("Heebo", 40, "bold"), bg="white", fg="black")
        self.cont.place(x=85, y=20)
        self.conta = tk.Label(self.banner, text="Si tienes alguna consulta o", font=("Heebo", 15, "bold"), bg="white", fg="black")
        self.conta.place(x=85, y=100)

        self.contanos = tk.Label(self.banner, text="comentario, no dudes en ponerte en", font=("Heebo", 15, "bold"), bg="white", fg="black")
        self.contanos.place(x=85, y=130)
        
        self.contame = tk.Label(self.banner, text="contacto con nosotros", font=("Heebo", 15, "bold"), bg="white", fg="black")
        self.contame.place(x=85, y=160)
        
        self.nombre =tk.Label(self.banner, text="Nombre:", font=("Heebo", 16), bg="white", fg="black")
        self.nombre.place(x=85, y=220)
        self.entry_nombre = tk.Entry(self.banner, font=("Heebo", 16),bd=2, relief="groove")
        self.entry_nombre.place(x=85, y=260)

        self.apellid=tk.Label(self.banner, text="Apellido:", font=("Heebo", 16), bg="white", fg="black")
        self.apellid.place(x=400, y=220)
        self.entry_apellido = tk.Entry(self.banner, font=("Heebo", 16),bd=2, relief="groove")
        self.entry_apellido.place(x=400, y=260)
        
        self.email=tk.Label(self.banner, text="Email:", font=("Heebo", 16), bg="white", fg="black")
        self.email.place(x=85, y=300)
        self.entry_email = tk.Entry(self.banner, font=("Heebo", 16),bd=2, relief="groove")
        self.entry_email.place(x=85, y=340)
        
        self.comentario=tk.Label(self.banner, text="Deja tus comentarios:", font=("Heebo", 16), bg="white", fg="black")
        self.comentario.place(x=85, y=390)
        self.entry_comentario = tk.Text(self.banner, width=55, height=7, font=("Arial", 12), bd=2, relief="groove")
        self.entry_comentario.place(x=85, y=430)
        

        btn_regre = tk.Button(self.banner, text="Enviar", font=("Arial", 12, "bold"), bg="#3e3838", fg="white",bd=0, padx=20, pady=7, command=self.confirma_mensaje_Contacto)
        btn_regre.place(x=620, y=520)

        # Labels para mostrar informacion/errores
        self.mostrar_info = tk.Label(self.banner, text="", font=("Arial", 12), bg="white", fg="green")
        self.mostrar_info.place(x=85, y=563)

        self.error_nombre = tk.Label(self.banner, text="", font=("Arial", 12), bg="white", fg="red")
        self.error_nombre.place(x=170, y=223)

        self.error_apellido = tk.Label(self.banner, text="", font=("Arial", 12), bg="white", fg="red")
        self.error_apellido.place(x=484, y=223)

        self.error_email = tk.Label(self.banner, text="", font=("Arial", 12), bg="white", fg="red")
        self.error_email.place(x=150, y=303)
        
        self.error_confirmar_comentario = tk.Label(self.banner, text="", font=("Arial", 12), bg="white", fg="red")
        self.error_confirmar_comentario.place(x=295, y=393)
        
        
        # Banner (bajo)
        self.banr = tk.Frame(self.root, bg="white", width=3000, height=210,bd=5, relief="raised")
        self.banr.pack(side="right", fill="y",padx=0)
        self.banr.pack_propagate(0)
        
        self.te = tk.Label(self.banr, text="Contacto", font=("Arial", 13, "bold"), bg="white", fg="black")
        self.te.place(x=198,y=10)
        
        self.t = tk.Label(self.banr, text="Info@filmcast.com\nTel: +52-33-12345678\nCra. 4 #22-61, Bogotá", font=("Arial", 13), bg="white", fg="black")
        self.t.place(x=150,y=40)
        
        self.tes = tk.Label(self.banr, text="Redes Sociales", font=("Arial", 13, "bold"), bg="white", fg="black")
        self.tes.place(x=450,y=10)
        
        self.ts = tk.Label(self.banr, text="Discord\nTwitch\nFacebook", font=("Arial", 13), bg="white", fg="black")
        self.ts.place(x=420,y=40)
        
        self.tss = tk.Label(self.banr, text="Youtube\nTwitter\nLinkedIn", font=("Arial", 13), bg="white", fg="black")
        self.tss.place(x=530,y=40)
        
        self.teo = tk.Label(self.banr, text="Encuentranos en:", font=("Arial", 13, "bold"), bg="white", fg="black")
        self.teo.place(x=800,y=10)
        
        # Cargar imagen appstore
        img2 = Image.open("C:/Users/danie/OneDrive/Documents/2024-1/Estilos y Lenguajes/src/img/appstore.jpg")
        img2 = img2.resize((170, 50), Image.LANCZOS)
        img2 = ImageTk.PhotoImage(img2)

        # Mostrar imagen en el banner usando pack en lugar de place
        img2_label = tk.Label(self.banr, image=img2)
        img2_label.image = img2
        img2_label.pack(pady=20) 
        img2_label.place(x=980, y=40)# Posiciona la imagen con margen superior
        
        # Enlazar la imagen de la App Store con el evento de clic
        img2_label.bind("<Button-1>", self.abrir_app_store)
        
        # Cargar imagen playstore
        img3 = Image.open("C:/Users/danie/OneDrive/Documents/2024-1/Estilos y Lenguajes/src/img/playstore.jpg")
        img3 = img3.resize((170, 50), Image.LANCZOS)
        img3 = ImageTk.PhotoImage(img3)

        # Mostrar imagen en el banner usando pack en lugar de place
        img3_label = tk.Label(self.banr, image=img3, bg="black")
        img3_label.image = img3
        img3_label.pack(pady=20) 
        img3_label.place(x=1200, y=40)# Posiciona la imagen con margen superior
        
        # Enlazar la imagen de la Play Store con el evento de clic
        img3_label.bind("<Button-1>", self.abrir_play_store)
        
    def confirma_mensaje_Contacto(self):
        """Confirma la creación de un nuevo usuario."""
        nombre = self.entry_nombre.get()
        apellido = self.entry_apellido.get()
        email = self.entry_email.get()
        confirmar_comentario = self.entry_comentario.get("1.0", "end").strip()

        # Limpiar errores anteriores
        self.error_nombre.config(text="")
        self.error_apellido.config(text="")
        self.error_email.config(text="")
        self.error_confirmar_comentario.config(text="")

        if not nombre:
            self.error_nombre.config(text="Ingrese un nombre.")
            return

        if not apellido:
            self.error_apellido.config(text="Ingrese un apellido.")
            return

        if not email:
            self.error_email.config(text="Ingrese un email.")
            return
        
        if not confirmar_comentario:
            self.error_confirmar_comentario.config(text="Envie un comentario.")
            return
        
        self.mostrar_info.config(text="Mensaje enviado correctamente.")
        self.entry_nombre.delete(0, 'end')
        self.entry_apellido.delete(0, 'end')
        self.entry_email.delete(0, 'end')
        self.entry_comentario.delete('1.0', 'end')
        
    def menu_principal(self):
        """Muestra el menú principal con opciones para cada módulo."""
        self.limpiar_pantalla()
        self.root.geometry("3000x1000")
        self.root.configure(bg="black")

        # Main content
        self.main = tk.Frame(self.root, bg="black", width=3000, height=1000)
        self.main.pack(fill="both", expand=False)

        # Banner (izquierda)
        self.baner = tk.Frame(self.main, bg="white", width=200, height=1000)
        self.baner.pack(side="left", fill="y",padx=0)
        self.baner.pack_propagate(0)

        btn_inico = tk.Button(self.baner, text="INICIO", font=("Arial", 14,"bold"), bg="#3e3838", fg="white", bd=0, padx=20, pady=7, command=self.menu_principal)
        btn_inico.pack(side="left")
        btn_inico.place(x=10,y=100,width=190, height=50)
        
        # Cargar icono inicio
        img = Image.open("C:/Users/danie/OneDrive/Documents/2024-1/Estilos y Lenguajes/src/img/Inicio_icono.jpg")
        img = img.resize((100, 100), Image.LANCZOS)
        img = ImageTk.PhotoImage(img)

        # Mostrar imagen
        img_label = tk.Label(self.baner, image=img, bg="black")
        img_label.image = img
        img_label.place(x=0, y=100)
        

        btn_bsu = tk.Button(self.baner, text="BUSCAR", font=("Arial", 14,"bold"), bg="#3e3838", fg="white", bd=0, padx=20, pady=7, command=self.pantalla_buscar)
        btn_bsu.pack(side="left")
        btn_bsu.place(x=10,y=200,width=190, height=50)

        btn_mensaje = tk.Button(self.baner, text="MENSAJE", font=("Arial", 14,"bold"), bg="#3e3838", fg="white", bd=0, padx=20, pady=7, command=self.pantalla_cuenta)
        btn_mensaje.pack(side="left")
        btn_mensaje.place(x=10,y=300,width=190, height=50)
        
        btn_mensaje = tk.Button(self.baner, text="MENSAJE", font=("Arial", 14,"bold"), bg="#3e3838", fg="white", bd=0, padx=20, pady=7, command=self.pantalla_cuenta)
        btn_mensaje.pack(side="left")
        btn_mensaje.place(x=10,y=300,width=190, height=50)
        
        btn_login = tk.Button(self.baner, text="CUENTA", font=("Arial", 14,"bold"), bg="#3e3838", fg="white", bd=0, padx=20, pady=7, command=self.pantalla_cuenta)
        btn_login.pack(side="left")
        btn_login.place(x=10,y=400,width=190, height=50)
        
        # Banner (derecha)
        self.izquierda = tk.Frame(self.main, bg="pink", width=2800, height=1000)
        self.izquierda.pack(side="right", fill="y",padx=0)
        self.izquierda.pack_propagate(0)
        
    def pantalla_cuenta(self):
        """Muestra la pantalla de inicio de sesión."""
        self.limpiar_pantalla()
        self.root.geometry("3000x1000")
        self.root.configure(bg="black")
        
        # Header - Logo y Navegación
        self.header = tk.Frame(self.root, bg="black", width=3000, height=80)
        self.header.pack(fill="x", pady=0)
        self.header.pack_propagate(0)
        
        self.logo = tk.Label(self.header, text="FC", font=("Arial", 24, "bold"), bg="black", fg="white")
        self.logo.place(x=20, y=10)
        
        btn_bus = tk.Button(self.header, text="BUSCAR", font=("Arial", 12,"bold"), bg="#3e3838", fg="white", bd=0, padx=20, pady=7, command=self.pantalla_buscar)
        btn_bus.place(x=1285, y=9)

        btn_ini = tk.Button(self.header, text="INICIO", font=("Arial", 12,"bold"), bg="#3e3838", fg="white", bd=0, padx=20, pady=7, command=self.menu_principal)
        btn_ini.place(x=1415, y=9)
        
        
        
        # Main content
        self.main = tk.Frame(self.root, bg="black", width=3000, height=800)
        self.main.pack(fill="both", expand=False)

        # Banner (arriba)
        self.banr = tk.Frame(self.main, bg="black", width=3000, height=400)
        self.banr.pack(side="top", fill="x", padx=0)
        
        self.cuen = tk.Label(self.banr, text="Perfil", font=("Arial", 30, "bold"), bg="black", fg="white")
        self.cuen.place(x=70, y=0)
        
        btn_cerrar = tk.Button(self.banr, text="EDITAR", font=("Arial", 12,"bold"), bg="#3e3838", fg="white", bd=0, padx=20, pady=7, command=self.pantalla_editar)
        btn_cerrar.place(x=600, y=320)
        
        btn_cerrar = tk.Button(self.banr, text="CERRAR SESION", font=("Arial", 12,"bold"), bg="#3e3838", fg="white", bd=0, padx=20, pady=7, command=self.pantalla_web)
        btn_cerrar.place(x=750, y=320)
        
         # Cargar imagen principal
        img = Image.open("C:/Users/danie/OneDrive/Documents/2024-1/Estilos y Lenguajes/src/img/perfil.jpg")
        img = img.resize((274, 274), Image.LANCZOS)
        img = ImageTk.PhotoImage(img)

        # Mostrar imagen
        img_label = tk.Label(self.banr, image=img, bg="black")
        img_label.image = img
        img_label.place(x=190, y=80)
        
        # Mostrar información del usuario en el header
        if hasattr(self, 'usuario_actual'):
            info_nombre = self.usuario_actual['nombre']
            self.info_nombre = tk.Label(self.banr, text=info_nombre, font=("Arial", 45), bg="black", fg="white", justify="left")
            self.info_nombre.place(x=600, y=80)  # Ajusta la posición según sea necesario
            
            info_tel = f"Tel: {self.usuario_actual['telefono']}"
            self.info_tel = tk.Label(self.banr, text=info_tel, font=("Arial", 20), bg="black", fg="white", justify="left")
            self.info_tel.place(x=600, y=180)  # Ajusta la ubicación aquí sea necesario
            
            info_email = f"Email: {self.usuario_actual['email']}"
            self.info_email = tk.Label(self.banr, text=info_email, font=("Arial", 20), bg="black", fg="white", justify="left")
            self.info_email.place(x=600, y=220)
            
            info_descripcion = f"Descripcion: {self.usuario_actual['descripcion']}"
            self.info_descripcion = tk.Label(self.banr, text=info_descripcion, font=("Arial", 20), bg="black", fg="white", justify="left")
            self.info_descripcion.place(x=1000, y=220)
            
            
        # Banner (bajo)
        self.baner = tk.Frame(self.main, bg="#3e3838", width=3000, height=400)
        self.baner.pack(side="bottom", fill="x", padx=0)
        
        self.trab = tk.Label(self.baner, text="Historial", font=("Arial", 22, "bold"), bg="#3e3838", fg="black")
        self.trab.place(x=40, y=40)

    def pantalla_editar(self):
        """Muestra la pantalla de los datos del usuario que inicia sesión."""
        self.limpiar_pantalla()
        self.root.geometry("3000x1000")
        self.root.configure(bg="black")
        
    def pantalla_buscar(self):
        """Muestra la pantalla de busqueda."""
        self.limpiar_pantalla()
        self.root.geometry("3000x1000")
        self.root.configure(bg="black")
        
        
if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
