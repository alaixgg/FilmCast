
import tkinter as tk
from tkinter import CENTER, ttk, messagebox
import psycopg2
from PIL import Image, ImageTk
import requests
from io import BytesIO
import webbrowser

try:
    connection = psycopg2.connect(
        host="localhost",
        user="postgres",
        password="123",
        database="postgres"
    )
    print("Conexion exitosa")
    cursor = connection.cursor()
except Exception as ex:
    print(ex)

class App:
    def __init__(self, root):
        self.root = root
        self.pantalla_web()

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
        img1 = Image.open("C:/Users/danie/OneDrive/Documents/2024-1/Estilos y Lenguajes/src/img/celular.jpeg")
        img1 = img1.resize((339, 667), Image.LANCZOS)
        img1 = ImageTk.PhotoImage(img1)

        # Mostrar imagen en el banner usando pack en lugar de place
        img1_label = tk.Label(self.banner, image=img1, bg="black")
        img1_label.image = img1
        img1_label.place(x=100, y=20)  # Posiciona la imagen con margen superior
         
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
        self.mostrar_info = tk.Label(self.banner, text="", font=("Arial", 12), bg="black", fg="red")
        self.mostrar_info.pack(pady=5)

        self.error_usuario = tk.Label(self.banner, text="", font=("Arial", 12), bg="black", fg="red")
        self.error_usuario.place(x=35, y=250)

        self.error_contrasena = tk.Label(self.banner, text="", font=("Arial", 12), bg="black", fg="red")
        self.error_contrasena.place(x=35, y=380)

        self.error_confirmar_contrasena = tk.Label(self.banner, text="", font=("Arial", 12), bg="black", fg="red")
        self.error_confirmar_contrasena.place(x=35, y=510)
        
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
        """Valida las credenciales del usuario."""
        usuario = self.entrada_usuario.get()
        clave = self.entrada_clave.get()
        comprobar_usuario ="SELECT * FROM usuarios WHERE nombre = '{}' AND clave = '{}'".format(usuario, clave)
        cursor.execute(comprobar_usuario)
        resultado = cursor.fetchone()
        if resultado:
            self.nivel_usuario = resultado[0]
            self.menu_principal()
        else:
            self.erro=tk.Label(self.root, text="Usuario o clave incorrectos", font=("Arial", 10), bg="black", fg="red")
            self.erro.place(x=915, y=328)
            self.ero=tk.Label(self.root, text="Usuario o clave incorrectos", font=("Arial", 10), bg="black", fg="red")
            self.ero.place(x=915, y=460)
            self.entrada_usuario.delete(0, tk.END)
            self.entrada_clave.delete(0, tk.END)
            self.entrada_usuario.focus()
            self.entrada_clave.focus()
           
    def Registrar_usuario_confirmar(self):
        """Confirma la creación de un nuevo usuario."""
        usuario = self.entry_usuario.get()
        contrasena = self.entry_contrasena.get()
        confirmar_contrasena = self.entry_confirmar_contrasena.get()
        nivel_usuario = 3

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

        # Lógica para crear el usuario aquí
        # Ejemplo:
        insertar = "INSERT INTO public.usuarios(nivel, nombre, clave) VALUES (%s, %s, %s);"
        datos = (nivel_usuario,usuario,contrasena)
        cursor.execute(insertar, datos)
        connection.commit()
        self.mostrar_info.config(text="Usuario creado correctamente.")

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
        self.entry_apellid = tk.Entry(self.banner, font=("Heebo", 16),bd=2, relief="groove")
        self.entry_apellid.place(x=400, y=260)
        
        self.email=tk.Label(self.banner, text="Email:", font=("Heebo", 16), bg="white", fg="black")
        self.email.place(x=85, y=300)
        self.entry_emai = tk.Entry(self.banner, font=("Heebo", 16),bd=2, relief="groove")
        self.entry_emai.place(x=85, y=340)
        
        self.comen=tk.Label(self.banner, text="Deja tus comentarios:", font=("Heebo", 16), bg="white", fg="black")
        self.comen.place(x=85, y=390)
        self.entry_comen = tk.Text(self.banner, width=55, height=7, font=("Arial", 12), bd=2, relief="groove")
        self.entry_comen.place(x=85, y=430)
        

        btn_regre = tk.Button(self.banner, text="Enviar", font=("Arial", 12, "bold"), bg="#3e3838", fg="white",bd=0, padx=20, pady=7, command=self.pantalla_web)
        btn_regre.place(x=620, y=520)
        
        
        
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
        
    def menu_principal(self):
        """Muestra el menú principal con opciones para cada módulo."""
        self.limpiar_pantalla()
        self.root.geometry("3000x1000")
        self.root.configure(bg="black")
        
        # Header - Logo y Navegación
        self.header = tk.Frame(self.root, bg="white",width=3000, height=200)
        self.header.pack(fill="x", pady=0)

        tk.Label(self.header, text="Menú Principal", font=("Arial", 22, "bold"), bg="white", fg="black").pack(pady=20)
        
        # Ancho y alto de los botones
        button_width = 20
        button_height = 1
        
        

        # Botones alineados verticalmente
        tk.Button(self.root, text="Usuarios", command=self.pantalla_usuarios, font=("Arial", 18), bg="#4CAF50", fg="white", width=button_width, height=button_height).pack(pady=10)
        tk.Button(self.root, text="Clientes", command=self.pantalla_clientes, font=("Arial", 18), bg="#FF5722", fg="white", width=button_width, height=button_height).pack(pady=10)
        tk.Button(self.root, text="Proveedores", command=self.pantalla_proveedores, font=("Arial", 18), bg="#8c564b", fg="white", width=button_width, height=button_height).pack(pady=10)
        tk.Button(self.root, text="Inventarios", command=self.pantalla_inventarios, font=("Arial", 18), bg="#9467bd", fg="white", width=button_width, height=button_height).pack(pady=10)
        tk.Button(self.root, text="Ventas", command=self.pantalla_ventas, font=("Arial", 18), bg="#17becf", fg="white", width=button_width, height=button_height).pack(pady=10)

        # Botón de cerrar sesión en la parte inferior
        tk.Button(self.root, text="Cerrar Sesión", command=self.pantalla_web, font=("Arial", 18), bg="#DC143C", fg="white", width=button_width, height=button_height).pack(pady=20, side=tk.BOTTOM)


    """/***************************************************************************
    PANTALLAS GENERALES
    ****************************************************************************/"""
    def pantalla_usuarios(self):
        """Muestra la pantalla de gestión de usuarios."""
        if self.nivel_usuario != 1:
            messagebox.showerror("Error", "No tiene permiso para acceder a este módulo")
            return

        self.limpiar_pantalla()

        tk.Label(self.root, text="Gestión de Usuarios", font=("Arial", 22, "bold"), bg="#B0C4DE").pack(pady=20)
        
        # Ancho y alto de los botones
        button_width = 21
        button_height = 1
        
        tk.Button(self.root, text="Crear Usuario", command=self.crear_usuario, font=("Arial", 18), bg="#4CAF50", fg="white", width=button_width, height=button_height).pack(pady=10)
        tk.Button(self.root, text="Consultas", command=self.pantalla_consultas_usuarios, font=("Arial", 18), bg="#2196F3", fg="white", width=button_width, height=button_height).pack(pady=10)
        tk.Button(self.root, text="Actualizar Usuario", command=self.actualizar_usuario, font=("Arial", 18), bg="#FF9800", fg="white", width=button_width, height=button_height).pack(pady=10)

        if self.nivel_usuario == 1:
            tk.Button(self.root, text="Eliminar Usuario", command=self.eliminar_usuario, font=("Arial", 18), bg="#DC143C", fg="white", width=button_width, height=button_height).pack(pady=10)
        
        tk.Button(self.root, text="Regresar al Menú Principal", command=self.menu_principal, font=("Arial", 18), bg="#607D8B", fg="white", width=button_width, height=button_height).pack(pady=20)

    def pantalla_clientes(self):
        """Muestra la pantalla de gestión de clientes."""
        self.limpiar_pantalla()

        tk.Label(self.root, text="Gestión de Clientes", font=("Arial", 22, "bold"), bg="#B0C4DE").pack(pady=20)
        
        # Ancho y alto de los botones
        button_width = 21
        button_height = 1
        
        if self.nivel_usuario < 3:
            tk.Button(self.root, text="Crear Cliente", command=self.crear_cliente, font=("Arial", 18), bg="#4CAF50", fg="white", width=button_width, height=button_height).pack(pady=10)
        
        tk.Button(self.root, text="Consultas", command=self.pantalla_consultas_clientes, font=("Arial", 18), bg="#2196F3", fg="white", width=button_width, height=button_height).pack(pady=10)
        
        if self.nivel_usuario < 3:
            tk.Button(self.root, text="Actualizar Cliente", command=self.actualizar_cliente, font=("Arial", 18), bg="#FF9800", fg="white", width=button_width, height=button_height).pack(pady=10)
        
        if self.nivel_usuario == 1:
            tk.Button(self.root, text="Eliminar Cliente", command=self.eliminar_cliente, font=("Arial", 18), bg="#DC143C", fg="white", width=button_width, height=button_height).pack(pady=10)
        
        tk.Button(self.root, text="Regresar al Menú Principal", command=self.menu_principal, font=("Arial", 18), bg="#607D8B", fg="white", width=button_width, height=button_height).pack(pady=20)

    def pantalla_proveedores(self):
        """Muestra la pantalla de gestión de proveedores."""
        self.limpiar_pantalla()

        tk.Label(self.root, text="Gestión de Proveedores", font=("Arial", 22, "bold"), bg="#B0C4DE").pack(pady=20)
        
        # Ancho y alto de los botones
        button_width = 21
        button_height = 1
        
        if self.nivel_usuario < 3:
            tk.Button(self.root, text="Crear Proveedor", command=self.crear_proveedor, font=("Arial", 18), bg="#4CAF50", fg="white", width=button_width, height=button_height).pack(pady=10)
        
        tk.Button(self.root, text="Consultas", command=self.pantalla_consultas_proveedores, font=("Arial", 18), bg="#2196F3", fg="white", width=button_width, height=button_height).pack(pady=10)
        
        if self.nivel_usuario < 3:
            tk.Button(self.root, text="Actualizar Proveedor", command=self.actualizar_proveedor, font=("Arial", 18), bg="#FF9800", fg="white", width=button_width, height=button_height).pack(pady=10)
        
        if self.nivel_usuario == 1:
            tk.Button(self.root, text="Eliminar Proveedor", command=self.eliminar_proveedor, font=("Arial", 18), bg="#DC143C", fg="white", width=button_width, height=button_height).pack(pady=10)
        
        tk.Button(self.root, text="Regresar al Menú Principal", command=self.menu_principal, font=("Arial", 18), bg="#607D8B", fg="white", width=button_width, height=button_height).pack(pady=20)

    def pantalla_inventarios(self):
        """Muestra la pantalla de gestión de inventarios."""
        self.limpiar_pantalla()

        tk.Label(self.root, text="Gestión de Inventarios", font=("Arial", 22, "bold"), bg="#B0C4DE").pack(pady=20)
        
        # Ancho y alto de los botones
        button_width = 21
        button_height = 1
        
        if self.nivel_usuario < 3:
            tk.Button(self.root, text="Crear Inventario", command=self.crear_inventario, font=("Arial", 18), bg="#4CAF50", fg="white", width=button_width, height=button_height).pack(pady=10)
        
        tk.Button(self.root, text="Consultas", command=self.pantalla_consultas_inventarios, font=("Arial", 18), bg="#2196F3", fg="white", width=button_width, height=button_height).pack(pady=10)
        
        if self.nivel_usuario < 3:
            tk.Button(self.root, text="Actualizar Inventario", command=self.actualizar_inventario, font=("Arial", 18), bg="#FF9800", fg="white", width=button_width, height=button_height).pack(pady=10)
        
        if self.nivel_usuario == 1:
            tk.Button(self.root, text="Eliminar Inventario", command=self.eliminar_inventario, font=("Arial", 18), bg="#DC143C", fg="white", width=button_width, height=button_height).pack(pady=10)
        
        tk.Button(self.root, text="Regresar al Menú Principal", command=self.menu_principal, font=("Arial", 18), bg="#607D8B", fg="white", width=button_width, height=button_height).pack(pady=20)

    def pantalla_ventas(self):
        """Muestra la pantalla de gestión de ventas."""
        self.limpiar_pantalla()

        tk.Label(self.root, text="Gestión de Ventas", font=("Arial", 22, "bold"), bg="#B0C4DE").pack(pady=20)
        
        # Ancho y alto de los botones
        button_width = 21
        button_height = 1
        
        tk.Button(self.root, text="Ingresar Venta", command=self.ingresar_venta, font=("Arial", 18), bg="#4CAF50", fg="white", width=button_width, height=button_height).pack(pady=10)
        
        tk.Button(self.root, text="Consultas", command=self.pantalla_consultas_ventas, font=("Arial", 18), bg="#2196F3", fg="white", width=button_width, height=button_height).pack(pady=10)
        
        tk.Button(self.root, text="Regresar al Menú Principal", command=self.menu_principal, font=("Arial", 18), bg="#607D8B", fg="white", width=button_width, height=button_height).pack(pady=20)
        
    
    """/***************************************************************************
    PANTALLAS CONSULTAS
    ****************************************************************************/"""
    
    def pantalla_consultas_usuarios(self):
        """Muestra la pantalla de opciones de consulta para usuarios."""
        self.limpiar_pantalla()
        
        tk.Label(self.root, text="Consultas de Usuarios", font=("Arial", 22, "bold"), bg="#B0C4DE").pack(pady=20)
        
        # Ancho y alto de los botones
        button_width = 21
        button_height = 1
        
        tk.Button(self.root, text="Consulta General", command=self.consultar_usuarios, font=("Arial", 18), bg="#2196F3", fg="white", width=button_width, height=button_height).pack(pady=10)
        tk.Button(self.root, text="Consulta por ID", command=self.consulta_por_id_usuarios, font=("Arial", 18), bg="#2196F3", fg="white", width=button_width, height=button_height).pack(pady=10)
        
        tk.Button(self.root, text="Regresar", command=self.pantalla_usuarios, font=("Arial", 18), bg="#607D8B", fg="white", width=button_width, height=button_height).pack(pady=20)

    def pantalla_consultas_clientes(self):
        """Muestra la pantalla de opciones de consulta para clientes."""
        self.limpiar_pantalla()
        
        tk.Label(self.root, text="Consultas de Clientes", font=("Arial", 22, "bold"), bg="#B0C4DE").pack(pady=20)
        
        # Ancho y alto de los botones
        button_width = 21
        button_height = 1
        
        tk.Button(self.root, text="Consulta General", command=self.consultar_clientes, font=("Arial", 18), bg="#2196F3", fg="white", width=button_width, height=button_height).pack(pady=10)
        tk.Button(self.root, text="Consulta por ID", command=lambda: self.consulta_por_id_clientes("cliente"), font=("Arial", 18), bg="#2196F3", fg="white", width=button_width, height=button_height).pack(pady=10)
        
        tk.Button(self.root, text="Regresar", command=self.pantalla_clientes, font=("Arial", 18), bg="#607D8B", fg="white", width=button_width, height=button_height).pack(pady=20)

    def pantalla_consultas_proveedores(self):
        """Muestra la pantalla de opciones de consulta para proveedores."""
        self.limpiar_pantalla()
        
        tk.Label(self.root, text="Consultas de Proveedores", font=("Arial", 22, "bold"), bg="#B0C4DE").pack(pady=20)
        
        # Ancho y alto de los botones
        button_width = 21
        button_height = 1
        
        tk.Button(self.root, text="Consulta General", command=self.consultar_proveedores, font=("Arial", 18), bg="#2196F3", fg="white", width=button_width, height=button_height).pack(pady=10)
        tk.Button(self.root, text="Consulta por ID", command=lambda: self.consulta_por_id_proveedores("proveedor"), font=("Arial", 18), bg="#2196F3", fg="white", width=button_width, height=button_height).pack(pady=10)
        
        tk.Button(self.root, text="Regresar", command=self.pantalla_proveedores, font=("Arial", 18), bg="#607D8B", fg="white", width=button_width, height=button_height).pack(pady=20)

    def pantalla_consultas_inventarios(self):
        """Muestra la pantalla de opciones de consulta para inventarios."""
        self.limpiar_pantalla()
        
        tk.Label(self.root, text="Consultas de Inventarios", font=("Arial", 22, "bold"), bg="#B0C4DE").pack(pady=20)
        
        # Ancho y alto de los botones
        button_width = 21
        button_height = 1
        
        tk.Button(self.root, text="Consulta General", command=self.consultar_inventarios, font=("Arial", 18), bg="#2196F3", fg="white", width=button_width, height=button_height).pack(pady=10)
        tk.Button(self.root, text="Consulta por Código", command=lambda: self.consulta_por_id_inventarios("inventario"), font=("Arial", 18), bg="#2196F3", fg="white", width=button_width, height=button_height).pack(pady=10)
        
        tk.Button(self.root, text="Regresar", command=self.pantalla_inventarios, font=("Arial", 18), bg="#607D8B", fg="white", width=button_width, height=button_height).pack(pady=20)

    def pantalla_consultas_ventas(self):
        """Muestra la pantalla de opciones de consulta para ventas."""
        self.limpiar_pantalla()
        
        tk.Label(self.root, text="Consultas de Ventas", font=("Arial", 22, "bold"), bg="#B0C4DE").pack(pady=20)
        
        # Ancho y alto de los botones
        button_width = 21
        button_height = 1
        
        tk.Button(self.root, text="Consulta General", command=self.consultar_ventas, font=("Arial", 18), bg="#2196F3", fg="white", width=button_width, height=button_height).pack(pady=10)
        tk.Button(self.root, text="Consulta por ID", command=lambda: self.consulta_por_id_ventas("venta"), font=("Arial", 18), bg="#2196F3", fg="white", width=button_width, height=button_height).pack(pady=10)
        tk.Button(self.root, text="Consulta por Fecha", command=self.consulta_por_fecha, font=("Arial", 18), bg="#2196F3", fg="white", width=button_width, height=button_height).pack(pady=10)
        
        tk.Button(self.root, text="Regresar", command=self.pantalla_ventas, font=("Arial", 18), bg="#607D8B", fg="white", width=button_width, height=button_height).pack(pady=20)

    def consulta_por_id_usuarios(self):
        """Muestra una ventana para consultar un registro por ID."""
        self.limpiar_pantalla()

        tk.Label(self.root, text=f"Consulta de USUARIOS por nivel", font=("Arial", 22, "bold"), bg="#B0C4DE").pack(pady=10)
        
        # Ancho y alto de los botones
        button_width = 21
        button_height = 1
        
        tk.Label(self.root, text="ID:", font=("Arial", 18), bg="#B0C4DE").pack(pady=5)
        self.entrada_us = tk.Entry(self.root, font=("Arial", 18))
        self.entrada_us.pack(pady=5)

        tk.Button(self.root, text="Consultar", command=self.realizar_consulta_id_usuarios, font=("Arial", 16), bg="#2196F3", fg="white", width=button_width, height=button_height).pack(pady=20)
        tk.Button(self.root, text="Regresar", command=self.pantalla_usuarios, font=("Arial", 16), bg="#607D8B", fg="white", width=button_width, height=button_height).pack(pady=10)

    def consulta_por_id_clientes(self, tipo):
        """Muestra una ventana para consultar un registro por ID."""
        self.limpiar_pantalla()

        tk.Label(self.root, text=f"Consulta de {tipo.capitalize()} por ID", font=("Arial", 22, "bold"), bg="#B0C4DE").pack(pady=10)
        
        # Ancho y alto de los botones
        button_width = 21
        button_height = 1
        
        tk.Label(self.root, text="ID:", font=("Arial", 18), bg="#B0C4DE").pack(pady=5)
        self.entrada_id = tk.Entry(self.root, font=("Arial", 18))
        self.entrada_id.pack(pady=5)

        tk.Button(self.root, text="Consultar", command=self.realizar_consulta_id_cliente, font=("Arial", 16), bg="#2196F3", fg="white", width=button_width, height=button_height).pack(pady=20)
        tk.Button(self.root, text="Regresar", command=self.pantalla_clientes, font=("Arial", 16), bg="#607D8B", fg="white", width=button_width, height=button_height).pack(pady=10)

    def consulta_por_id_proveedores(self, tipo):
        """Muestra una ventana para consultar un registro por ID."""
        self.limpiar_pantalla()

        tk.Label(self.root, text=f"Consulta de {tipo.capitalize()} por ID", font=("Arial", 22, "bold"), bg="#B0C4DE").pack(pady=10)
        
        # Ancho y alto de los botones
        button_width = 21
        button_height = 1
        
        tk.Label(self.root, text="ID:", font=("Arial", 18), bg="#B0C4DE").pack(pady=5)
        self.entrada_id = tk.Entry(self.root, font=("Arial", 18))
        self.entrada_id.pack(pady=5)

        tk.Button(self.root, text="Consultar", command=self.realizar_consulta_id_proveedores, font=("Arial", 16), bg="#2196F3", fg="white", width=button_width, height=button_height).pack(pady=20)
        tk.Button(self.root, text="Regresar", command=self.pantalla_proveedores, font=("Arial", 16), bg="#607D8B", fg="white", width=button_width, height=button_height).pack(pady=10)

    def consulta_por_id_inventarios(self, tipo):
        """Muestra una ventana para consultar un registro por ID."""
        self.limpiar_pantalla()

        tk.Label(self.root, text=f"Consulta de {tipo.capitalize()} por ID producto", font=("Arial", 22, "bold"), bg="#B0C4DE").pack(pady=10)
        
        # Ancho y alto de los botones
        button_width = 21
        button_height = 1
        
        tk.Label(self.root, text="ID:", font=("Arial", 18), bg="#B0C4DE").pack(pady=5)
        self.entrada_id = tk.Entry(self.root, font=("Arial", 18))
        self.entrada_id.pack(pady=5)

        tk.Button(self.root, text="Consultar", command=self.realizar_consulta_id_inventario, font=("Arial", 16), bg="#2196F3", fg="white", width=button_width, height=button_height).pack(pady=20)
        tk.Button(self.root, text="Regresar", command=self.pantalla_inventarios, font=("Arial", 16), bg="#607D8B", fg="white", width=button_width, height=button_height).pack(pady=10)

    def consulta_por_id_ventas(self, tipo):
        """Muestra una ventana para consultar un registro por ID."""
        self.limpiar_pantalla()

        tk.Label(self.root, text=f"Consulta de {tipo.capitalize()} por ID clientes", font=("Arial", 22, "bold"), bg="#B0C4DE").pack(pady=10)
        
        # Ancho y alto de los botones
        button_width = 21
        button_height = 1
        
        tk.Label(self.root, text="ID:", font=("Arial", 18), bg="#B0C4DE").pack(pady=5)
        self.entrada_id = tk.Entry(self.root, font=("Arial", 18))
        self.entrada_id.pack(pady=5)

        tk.Button(self.root, text="Consultar", command=self.realizar_consulta_id_ventas, font=("Arial", 16), bg="#2196F3", fg="white", width=button_width, height=button_height).pack(pady=20)
        tk.Button(self.root, text="Regresar", command=self.pantalla_ventas, font=("Arial", 16), bg="#607D8B", fg="white", width=button_width, height=button_height).pack(pady=10)

    def consulta_por_fecha(self):
        """Muestra una ventana para consultar ventas por fecha."""
        self.limpiar_pantalla()

        tk.Label(self.root, text="Consulta de Ventas por Fecha", font=("Arial", 22, "bold"), bg="#B0C4DE").pack(pady=10)
        
        # Ancho y alto de los botones
        button_width = 21
        button_height = 1
        
        tk.Label(self.root, text="Fecha de Inicio (AAAA-MM-DD):", font=("Arial", 18), bg="#B0C4DE").pack(pady=5)
        entrada_fecha_inicio = tk.Entry(self.root, font=("Arial", 18))
        entrada_fecha_inicio.pack(pady=5)

        tk.Label(self.root, text="Fecha de Fin (AAAA-MM-DD):", font=("Arial", 18), bg="#B0C4DE").pack(pady=5)
        entrada_fecha_fin = tk.Entry(self.root, font=("Arial", 18))
        entrada_fecha_fin.pack(pady=5)

        tk.Button(self.root, text="Consultar", command=lambda: self.realizar_consulta_fecha(entrada_fecha_inicio.get(), entrada_fecha_fin.get()), font=("Arial", 16), bg="#2196F3", fg="white", width=button_width, height=button_height).pack(pady=20)
        tk.Button(self.root, text="Regresar", command=self.menu_principal, font=("Arial", 16), bg="#607D8B", fg="white", width=button_width, height=button_height).pack(pady=10)
    
    
    """/***************************************************************************
    FUNCIONES CONSULTAS
    ****************************************************************************/"""
    def consultar_usuarios(self):
        """Lógica para consultar usuarios."""
        self.limpiar_pantalla()
        tv = ttk.Treeview(self.root, columns = ('nivel','nombre','clave'))       
        tv.column('#0',width = 0)
        tv.column('nivel',width = 40,anchor=CENTER)
        tv.column('nombre',width = 150,anchor=CENTER)
        tv.column('clave',width = 150,anchor=CENTER)
        tv.heading('nivel', text='Nivel',anchor=CENTER)
        tv.heading('nombre', text='Nombre',anchor=CENTER)
        tv.heading('clave', text='Clave',anchor=CENTER)
        consultar = 'SELECT * FROM usuarios ;'
        cursor.execute(consultar)
        registro = cursor.fetchall()
        for linea in registro:
            tv.insert('',tk.END,values=linea)
        tv.pack()
        
        # Ancho y alto de los botones
        button_width = 21
        button_height = 1
        tk.Button(self.root, text="Regresar", command=self.pantalla_usuarios, font=("Arial", 16), bg="#607D8B", fg="white", width=button_width, height=button_height).pack(pady=10)

    def consultar_clientes(self):
        """Lógica para consultar clientes."""
        self.limpiar_pantalla()
        tv = ttk.Treeview(self.root, columns = ('id','nombre','direccion','telefono'))       
        tv.column('#0',width = 0)
        tv.column('id',width = 40,anchor=CENTER)
        tv.column('nombre',width = 80,anchor=CENTER)
        tv.column('direccion',width = 120,anchor=CENTER)
        tv.column('telefono',width = 100,anchor=CENTER)
        tv.heading('id', text='ID',anchor=CENTER)
        tv.heading('nombre', text='Nombre',anchor=CENTER)
        tv.heading('direccion', text='Direccion',anchor=CENTER)
        tv.heading('telefono', text='Telefono',anchor=CENTER)
        consultar = 'SELECT * FROM clientes ;'
        cursor.execute(consultar)
        registro = cursor.fetchall()
        for linea in registro:
            tv.insert('',tk.END,values=linea)
        tv.pack()
        
         # Ancho y alto de los botones
        button_width = 21
        button_height = 1
        tk.Button(self.root, text="Regresar", command=self.pantalla_clientes, font=("Arial", 16), bg="#607D8B", fg="white", width=button_width, height=button_height).pack(pady=10)

    def consultar_proveedores(self):
        """Lógica para consultar proveedores."""
        self.limpiar_pantalla()
        tv = ttk.Treeview(self.root, columns = ('id','codproducto','descripcion','costo','direccion','telefono'))       
        tv.column('#0',width = 0)
        tv.column('id',width = 40,anchor=CENTER)
        tv.column('codproducto',width = 80,anchor=CENTER)
        tv.column('descripcion',width = 120,anchor=CENTER)
        tv.column('costo',width = 100,anchor=CENTER)
        tv.column('direccion',width = 100,anchor=CENTER)
        tv.column('telefono',width = 100,anchor=CENTER)

        tv.heading('id', text='ID',anchor=CENTER)
        tv.heading('codproducto', text='Codproducto',anchor=CENTER)
        tv.heading('descripcion', text='Descripcion',anchor=CENTER)
        tv.heading('costo', text='Costo',anchor=CENTER)
        tv.heading('direccion', text='Direccion',anchor=CENTER)
        tv.heading('telefono', text='Telefono',anchor=CENTER)
        consultar = 'SELECT * FROM proveedores ;'
        cursor.execute(consultar)
        registro = cursor.fetchall()
        for linea in registro:
            tv.insert('',tk.END,values=linea)
        tv.pack()
        
         # Ancho y alto de los botones
        button_width = 21
        button_height = 1
        tk.Button(self.root, text="Regresar", command=self.pantalla_proveedores, font=("Arial", 16), bg="#607D8B", fg="white", width=button_width, height=button_height).pack(pady=20)

    def consultar_inventarios(self):
        self.limpiar_pantalla()
        tv = ttk.Treeview(self.root, columns = ('codproducto','cantidad','stockmin','costo /u'))       
        tv.column('#0',width = 0)
        tv.column('codproducto',width = 80,anchor=CENTER)
        tv.column('cantidad',width = 80,anchor=CENTER)
        tv.column('stockmin',width = 120,anchor=CENTER)
        tv.column('costo /u',width = 100,anchor=CENTER)
        tv.heading('codproducto', text='Codproducto',anchor=CENTER)
        tv.heading('cantidad', text='Cantidad',anchor=CENTER)
        tv.heading('stockmin', text='Stockmin',anchor=CENTER)
        tv.heading('costo /u', text='Costo /u',anchor=CENTER)
        consultar = 'SELECT * FROM inventarios ;'
        cursor.execute(consultar)
        registro = cursor.fetchall()
        for linea in registro:
            tv.insert('',tk.END,values=linea)
        tv.pack()
       
       
        # Ancho y alto de los botones
        button_width = 21
        button_height = 1
        tk.Button(self.root, text="Regresar", command=self.pantalla_inventarios, font=("Arial", 16), bg="#607D8B", fg="white", width=button_width, height=button_height).pack(pady=10)

    def consultar_ventas(self):
        """Lógica para consultar ventas."""
        self.limpiar_pantalla()
        tv = ttk.Treeview(self.root, columns = ('idclientes','codproducto','cantidad','descripcion','iva','subtotal','total'))       
        tv.column('#0',width = 0)
        tv.column('idclientes',width = 80,anchor=CENTER)
        tv.column('codproducto',width = 80,anchor=CENTER)
        tv.column('cantidad',width = 120,anchor=CENTER)
        tv.column('descripcion',width = 100,anchor=CENTER)
        tv.column('iva',width = 100,anchor=CENTER)
        tv.column('subtotal',width = 100,anchor=CENTER)
        tv.column('total',width = 100,anchor=CENTER)

        tv.heading('idclientes', text='Idclientes',anchor=CENTER)
        tv.heading('codproducto', text='Codproducto',anchor=CENTER)
        tv.heading('cantidad', text='Cantidad',anchor=CENTER)
        tv.heading('descripcion', text='descripcion',anchor=CENTER)
        tv.heading('iva', text='Iva',anchor=CENTER)
        tv.heading('subtotal', text='Subtotal',anchor=CENTER)
        tv.heading('total', text='Total',anchor=CENTER)
        consultar = 'SELECT * FROM ventas ;'
        cursor.execute(consultar)
        registro = cursor.fetchall()
        for linea in registro:
            tv.insert('',tk.END,values=linea)
        tv.pack()
        
         # Ancho y alto de los botones
        button_width = 21
        button_height = 1
        tk.Button(self.root, text="Regresar", command=self.pantalla_ventas, font=("Arial", 16), bg="#607D8B", fg="white", width=button_width, height=button_height).pack(pady=10)

    def realizar_consulta_id_usuarios(self):
        """Realiza la consulta por ID y muestra el resultado."""
        # Aquí debes conectar con la lógica de consulta por ID y mostrar el resultado
        
        tv = ttk.Treeview(self.root, columns = ('nivel','nombre','clave'))       
        tv.column('#0',width = 0)
        tv.column('nivel',width = 40,anchor=CENTER)
        tv.column('nombre',width = 150,anchor=CENTER)
        tv.column('clave',width = 150,anchor=CENTER)
        tv.heading('nivel', text='Nivel',anchor=CENTER)
        tv.heading('nombre', text='Nombre',anchor=CENTER)
        tv.heading('clave', text='Clave',anchor=CENTER)
        us = self.entrada_us.get()
        consultar = 'SELECT * FROM usuarios WHERE nivel = %s ;' % us
        cursor.execute(consultar)
        registro = cursor.fetchall()
        for linea in registro:
                tv.insert('',tk.END,values=linea)
        tv.pack()
        
    def realizar_consulta_id_cliente(self):
            """Realiza la consulta por ID y muestra el resultado."""
            # Aquí debes conectar con la lógica de consulta por ID y mostrar el resultado
            tv = ttk.Treeview(self.root, columns = ('id','nombre','direccion','telefono'))       
            tv.column('#0',width = 0)
            tv.column('id',width = 40,anchor=CENTER)
            tv.column('nombre',width = 80,anchor=CENTER)
            tv.column('direccion',width = 120,anchor=CENTER)
            tv.column('telefono',width = 100,anchor=CENTER)
            tv.heading('id', text='ID',anchor=CENTER)
            tv.heading('nombre', text='Nombre',anchor=CENTER)
            tv.heading('direccion', text='Direccion',anchor=CENTER)
            tv.heading('telefono', text='Telefono',anchor=CENTER)
            id = self.entrada_id.get()
            consultar = 'SELECT * FROM clientes WHERE idclientes = %s ;' % id
            cursor.execute(consultar)
            registro = cursor.fetchall()
            for linea in registro:
                tv.insert('',tk.END,values=linea)
            tv.pack()
           
    def realizar_consulta_id_proveedores(self):
            """Realiza la consulta por ID y muestra el resultado."""
            # Aquí debes conectar con la lógica de consulta por ID y mostrar el resultado
            tv = ttk.Treeview(self.root, columns = ('id','codproducto','descripcion','costo','direccion','telefono'))       
            tv.column('#0',width = 0)
            tv.column('id',width = 40,anchor=CENTER)
            tv.column('codproducto',width = 80,anchor=CENTER)
            tv.column('descripcion',width = 120,anchor=CENTER)
            tv.column('costo',width = 100,anchor=CENTER)
            tv.column('direccion',width = 100,anchor=CENTER)
            tv.column('telefono',width = 100,anchor=CENTER)

            tv.heading('id', text='ID',anchor=CENTER)
            tv.heading('codproducto', text='Codproducto',anchor=CENTER)
            tv.heading('descripcion', text='Descripcion',anchor=CENTER)
            tv.heading('costo', text='Costo',anchor=CENTER)
            tv.heading('direccion', text='Direccion',anchor=CENTER)
            tv.heading('telefono', text='Telefono',anchor=CENTER)    
            id = self.entrada_id.get()
            consultar = 'SELECT * FROM proveedores WHERE idproveedores = %s ;' % id
            cursor.execute(consultar)
            registro = cursor.fetchall()
            for linea in registro:
                tv.insert('',tk.END,values=linea)
            tv.pack()

    def realizar_consulta_id_inventario(self):
            """Realiza la consulta por ID y muestra el resultado."""
            # Aquí debes conectar con la lógica de consulta por ID y mostrar el resultado
            tv = ttk.Treeview(self.root, columns = ('codproducto','cantidad','stockmin','costo /u'))       
            tv.column('#0',width = 0)
            tv.column('codproducto',width = 80,anchor=CENTER)
            tv.column('cantidad',width = 80,anchor=CENTER)
            tv.column('stockmin',width = 120,anchor=CENTER)
            tv.column('costo /u',width = 100,anchor=CENTER)
            tv.heading('codproducto', text='Codproducto',anchor=CENTER)
            tv.heading('cantidad', text='Cantidad',anchor=CENTER)
            tv.heading('stockmin', text='Stockmin',anchor=CENTER)
            tv.heading('costo /u', text='Costo /u',anchor=CENTER)    
            id = self.entrada_id.get()
            consultar = 'SELECT * FROM inventarios WHERE codproducto = %s ;' % id
            cursor.execute(consultar)
            registro = cursor.fetchall()
            for linea in registro:
                tv.insert('',tk.END,values=linea)
            tv.pack()   

    def realizar_consulta_id_ventas(self):
            """Realiza la consulta por ID y muestra el resultado."""
            # Aquí debes conectar con la lógica de consulta por ID y mostrar el resultado
            tv = ttk.Treeview(self.root, columns = ('idclientes','codproducto','cantidad','descripcion','iva','subtotal','total'))       
            tv.column('#0',width = 0)
            tv.column('idclientes',width = 80,anchor=CENTER)
            tv.column('codproducto',width = 80,anchor=CENTER)
            tv.column('cantidad',width = 120,anchor=CENTER)
            tv.column('descripcion',width = 100,anchor=CENTER)
            tv.column('iva',width = 100,anchor=CENTER)
            tv.column('subtotal',width = 100,anchor=CENTER)
            tv.column('total',width = 100,anchor=CENTER)

            tv.heading('idclientes', text='Idclientes',anchor=CENTER)
            tv.heading('codproducto', text='Codproducto',anchor=CENTER)
            tv.heading('cantidad', text='Cantidad',anchor=CENTER)
            tv.heading('descripcion', text='descripcion',anchor=CENTER)
            tv.heading('iva', text='Iva',anchor=CENTER)
            tv.heading('subtotal', text='Subtotal',anchor=CENTER)
            tv.heading('total', text='Total',anchor=CENTER)   
            id = self.entrada_id.get()
            consultar = 'SELECT * FROM ventas WHERE idclientes = %s ;' % id
            cursor.execute(consultar)
            registro = cursor.fetchall()
            for linea in registro:
                tv.insert('',tk.END,values=linea)
            tv.pack() 
            
    def realizar_consulta_fecha(self, fecha_inicio, fecha_fin):
            """Realiza la consulta por fecha y muestra el resultado."""
            # Aquí debes conectar con la lógica de consulta por fecha y mostrar el resultado
            tv = ttk.Treeview(self.root, columns=('idclientes', 'codproducto', 'cantidad', 'descripcion', 'iva', 'subtotal', 'total', 'fecha'))
            tv.column('#0', width=0)
            tv.column('idclientes', width=80, anchor=CENTER)
            tv.column('codproducto', width=80, anchor=CENTER)
            tv.column('cantidad', width=120, anchor=CENTER)
            tv.column('descripcion', width=100, anchor=CENTER)
            tv.column('iva', width=100, anchor=CENTER)
            tv.column('subtotal', width=100, anchor=CENTER)
            tv.column('total', width=100, anchor=CENTER)
            tv.column('fecha', width=100, anchor=CENTER)

            tv.heading('idclientes', text='Idclientes', anchor=CENTER)
            tv.heading('codproducto', text='Codproducto', anchor=CENTER)
            tv.heading('cantidad', text='Cantidad', anchor=CENTER)
            tv.heading('descripcion', text='descripcion', anchor=CENTER)
            tv.heading('iva', text='Iva', anchor=CENTER)
            tv.heading('subtotal', text='Subtotal', anchor=CENTER)
            tv.heading('total', text='Total', anchor=CENTER)
            tv.heading('fecha', text='Fecha', anchor=CENTER)

            consultar = 'SELECT * FROM ventas WHERE fecha BETWEEN %s AND %s ;'
            cursor.execute(consultar, (fecha_inicio, fecha_fin))
            registros = cursor.fetchall()
            for linea in registros:
                tv.insert('', tk.END, values=linea)
            tv.pack()


    """/***************************************************************************
    PANTALLAS ELIMINAR
    ****************************************************************************/"""
    def eliminar_usuario(self):
        """Muestra la pantalla para eliminar un usuario."""
        self.limpiar_pantalla()

        tk.Label(self.root, text="Eliminar Usuario", font=("Arial", 22, "bold"), bg="#B0C4DE").pack(pady=20)

        
         # Ancho y alto de los botones
        button_width = 21
        button_height = 1
        
        tk.Label(self.root, text="Nombre del Usuario:", font=("Arial", 18), bg="#B0C4DE").pack(pady=5)
        self.entry_eliminar_usuario = tk.Entry(self.root, font=("Arial", 18))
        self.entry_eliminar_usuario.pack(pady=5)

        tk.Button(self.root, text="Eliminar", command=self.eliminar_usuario_confirmar, font=("Arial", 16), bg="#4CAF50", fg="white", width=button_width, height=button_height).pack(pady=20)
        tk.Button(self.root, text="Regresar", command=self.pantalla_usuarios, font=("Arial", 16), bg="#607D8B", fg="white", width=button_width, height=button_height).pack(pady=10)

    def eliminar_cliente(self):
        """Muestra la pantalla para eliminar un cliente."""
        self.limpiar_pantalla()

        tk.Label(self.root, text="Eliminar Cliente", font=("Arial", 22, "bold"), bg="#B0C4DE").pack(pady=20)
        
        # Ancho y alto de los botones
        button_width = 21
        button_height = 1
        
        tk.Label(self.root, text="ID Cliente:", font=("Arial", 18), bg="#B0C4DE").pack(pady=5)
        self.entry_eliminar_cliente = tk.Entry(self.root, font=("Arial", 18))
        self.entry_eliminar_cliente.pack(pady=5)

        tk.Button(self.root, text="Eliminar", command=self.eliminar_cliente_confirmar, font=("Arial", 16), bg="#4CAF50", fg="white", width=button_width, height=button_height).pack(pady=20)
        tk.Button(self.root, text="Regresar", command=self.pantalla_clientes, font=("Arial", 16), bg="#607D8B", fg="white", width=button_width, height=button_height).pack(pady=10)

    def eliminar_proveedor(self):
        """Muestra la pantalla para eliminar un proveedor."""
        self.limpiar_pantalla()

        tk.Label(self.root, text="Eliminar Proveedor", font=("Arial", 22, "bold"), bg="#B0C4DE").pack(pady=20)

         # Ancho y alto de los botones
        button_width = 21
        button_height = 1
        
        tk.Label(self.root, text="Código de Proveedor:", font=("Arial", 18), bg="#B0C4DE").pack(pady=5)
        self.entry_eliminar_proveedor = tk.Entry(self.root, font=("Arial", 18))
        self.entry_eliminar_proveedor.pack(pady=5)

        tk.Button(self.root, text="Eliminar", command=self.eliminar_proveedor_confirmar, font=("Arial", 16), bg="#4CAF50", fg="white", width=button_width, height=button_height).pack(pady=20)
        tk.Button(self.root, text="Regresar", command=self.pantalla_proveedores, font=("Arial", 16), bg="#607D8B", fg="white", width=button_width, height=button_height).pack(pady=10)

    def eliminar_inventario(self):
        """Muestra la pantalla para eliminar un inventario."""
        self.limpiar_pantalla()

        tk.Label(self.root, text="Eliminar Inventario", font=("Arial", 22, "bold"), bg="#B0C4DE").pack(pady=20)

         # Ancho y alto de los botones
        button_width = 21
        button_height = 1
        
        tk.Label(self.root, text="Código del Producto:", font=("Arial", 18), bg="#B0C4DE").pack(pady=5)
        self.entry_eliminar_inventario = tk.Entry(self.root, font=("Arial", 18))
        self.entry_eliminar_inventario.pack(pady=5)

        tk.Button(self.root, text="Eliminar", command=self.eliminar_inventario_confirmar, font=("Arial", 16), bg="#4CAF50", fg="white", width=button_width, height=button_height).pack(pady=20)
        tk.Button(self.root, text="Regresar", command=self.pantalla_inventarios, font=("Arial", 16), bg="#607D8B", fg="white", width=button_width, height=button_height).pack(pady=10)
    """/***************************************************************************
    FUNCIONES ELIMINAR 
    ****************************************************************************/"""
    def eliminar_usuario_confirmar(self):
        """Elimina un usuario luego de confirmar la acción."""
        usuario_eliminar = self.entry_eliminar_usuario.get()
        eliminar = ("DELETE FROM usuarios WHERE nombre = '{}';".format(usuario_eliminar))
        cursor.execute(eliminar)
        connection.commit()
        tk.Label(self.root, text="Usuario eliminado", font=("Arial", 16, "bold"), bg="#87CEEB").pack(pady=20)

    def eliminar_cliente_confirmar(self):
        """Elimina un usuario luego de confirmar la acción."""
        id_usuario = self.entry_eliminar_cliente.get()# Se obtiene el ID del cliente ingresado por el cliente
        eliminar = ("DELETE FROM clientes WHERE idclientes = {};".format(id_usuario))
        cursor.execute(eliminar)
        connection.commit()
        tk.Label(self.root, text="Cliente eliminado", font=("Arial", 16, "bold"), bg="#87CEEB").pack(pady=20)

    def eliminar_proveedor_confirmar(self):
        """Elimina un usuario luego de confirmar la acción."""
        id_usuario = self.entry_eliminar_proveedor.get() # Se obtiene el ID del proveedor
        eliminar = ("DELETE FROM proveedores WHERE idproveedores = {};".format(id_usuario))
        cursor.execute(eliminar)
        connection.commit()
        tk.Label(self.root, text="Proveedor eliminado", font=("Arial", 16, "bold"), bg="#87CEEB").pack(pady=20)

    def eliminar_inventario_confirmar(self):
        """Elimina un usuario luego de confirmar la acción."""
        id_usuario = self.entry_eliminar_inventario.get()# Se obtiene el ID del proveedor ingresado por el proveedor
        eliminar = ("DELETE FROM inventarios WHERE codproducto = {};".format(id_usuario))
        cursor.execute(eliminar)
        connection.commit()
        tk.Label(self.root, text="Inventario eliminado", font=("Arial", 16, "bold"), bg="#87CEEB").pack(pady=20)

    """/***************************************************************************
    PANTALLAS CREAR
    ****************************************************************************/"""

    def crear_usuario(self):
        """Muestra una ventana para ingresar los datos de un nuevo usuario."""
        self.limpiar_pantalla()

        tk.Label(self.root, text="Crear Nuevo Usuario", font=("Arial", 22, "bold"), bg="#B0C4DE").pack(pady=20)

        # Ancho y alto de los botones
        button_width = 21
        button_height = 1
        
        tk.Label(self.root, text="Usuario:", font=("Arial", 16), bg="#B0C4DE").pack(pady=5)
        self.entry_usuario = tk.Entry(self.root, font=("Arial", 16))
        self.entry_usuario.pack(pady=5)

        tk.Label(self.root, text="Contraseña:", font=("Arial", 16), bg="#B0C4DE").pack(pady=5)
        self.entry_contrasena = tk.Entry(self.root, show="*", font=("Arial", 16))
        self.entry_contrasena.pack(pady=5)

        tk.Label(self.root, text="Confirmar Contraseña:", font=("Arial", 16), bg="#B0C4DE").pack(pady=5)
        self.entry_confirmar_contrasena = tk.Entry(self.root, show="*", font=("Arial", 16))
        self.entry_confirmar_contrasena.pack(pady=5)

        # Nivel de usuario por defecto
        defecto_nivel_usuario = 3

        tk.Button(self.root, text="Crear Usuario", command=self.crear_usuario_confirmar, font=("Arial", 16), bg="#4CAF50", fg="white", width=button_width, height=button_height).pack(pady=20)
        tk.Button(self.root, text="Regresar", command=self.pantalla_usuarios, font=("Arial", 16), bg="#607D8B", fg="white", width=button_width, height=button_height).pack(pady=10)

        # Labels para mostrar informacion/errores
        self.mostrar_info = tk.Label(self.root, text="", font=("Arial", 12), bg="#B0C4DE", fg="black")
        self.mostrar_info.pack(pady=5)

        self.error_usuario = tk.Label(self.root, text="", font=("Arial", 12), bg="#B0C4DE", fg="red")
        self.error_usuario.pack(pady=5)

        self.error_contrasena = tk.Label(self.root, text="", font=("Arial", 12), bg="#B0C4DE", fg="red")
        self.error_contrasena.pack(pady=5)

        self.error_confirmar_contrasena = tk.Label(self.root, text="", font=("Arial", 12), bg="#B0C4DE", fg="red")
        self.error_confirmar_contrasena.pack(pady=5)

    def crear_cliente(self):
        """Muestra una ventana para ingresar los datos de un nuevo cliente."""
        self.limpiar_pantalla()

        tk.Label(self.root, text="Crear Nuevo Cliente", font=("Arial", 22, "bold"), bg="#B0C4DE").pack(pady=20)
        
        # Ancho y alto de los botones
        button_width = 21
        button_height = 1

        tk.Label(self.root, text="ID del Cliente:", font=("Arial", 16), bg="#B0C4DE").pack(pady=5)
        self.entry_id_cliente = tk.Entry(self.root, font=("Arial", 16))
        self.entry_id_cliente.pack(pady=5)

        tk.Label(self.root, text="Nombre:", font=("Arial", 16), bg="#B0C4DE").pack(pady=5)
        self.entry_nombre_cliente = tk.Entry(self.root, font=("Arial", 16))
        self.entry_nombre_cliente.pack(pady=5)

        tk.Label(self.root, text="Dirección:", font=("Arial", 16), bg="#B0C4DE").pack(pady=5)
        self.entry_direccion_cliente = tk.Entry(self.root, font=("Arial", 16))
        self.entry_direccion_cliente.pack(pady=5)

        tk.Label(self.root, text="Teléfono:", font=("Arial", 16), bg="#B0C4DE").pack(pady=5)
        self.entry_telefono_cliente = tk.Entry(self.root, font=("Arial", 16))
        self.entry_telefono_cliente.pack(pady=5)

        tk.Button(self.root, text="Crear Cliente", command=self.crear_cliente_confirmar, font=("Arial", 14), bg="#4CAF50", fg="white", width=button_width, height=button_height).pack(pady=20)
        tk.Button(self.root, text="Regresar", command=self.pantalla_clientes, font=("Arial", 14), bg="#607D8B", fg="white", width=button_width, height=button_height).pack(pady=10)
        
        # Labels para mostrar informacion/errores
        self.mostrar_info = tk.Label(self.root, text="", font=("Arial", 12), bg="#B0C4DE", fg="black")
        self.mostrar_info.pack(pady=5)

    def crear_proveedor(self):
        """Muestra una ventana para ingresar los datos de un nuevo proveedor."""
        self.limpiar_pantalla()

        tk.Label(self.root, text="Crear Nuevo Proveedor", font=("Arial", 22, "bold"), bg="#B0C4DE").pack(pady=20)
        
        # Ancho y alto de los botones
        button_width = 21
        button_height = 1

        tk.Label(self.root, text="idproveedores", font=("Arial", 14), bg="#B0C4DE").pack(pady=5)
        self.entry_idproveedores = tk.Entry(self.root, font=("Arial", 14))
        self.entry_idproveedores.pack(pady=5)

        tk.Label(self.root, text="Código del Producto:", font=("Arial", 14), bg="#B0C4DE").pack(pady=5)
        self.entry_codigo_proveedor = tk.Entry(self.root, font=("Arial", 14))
        self.entry_codigo_proveedor.pack(pady=5)

        tk.Label(self.root, text="Descripción del Producto:", font=("Arial", 14), bg="#B0C4DE").pack(pady=5)
        self.entry_descripcion_proveedor = tk.Entry(self.root, font=("Arial", 14))
        self.entry_descripcion_proveedor.pack(pady=5)

        tk.Label(self.root, text="Costo del Producto:", font=("Arial", 14), bg="#B0C4DE").pack(pady=5)
        self.entry_costo_proveedor = tk.Entry(self.root, font=("Arial", 14))
        self.entry_costo_proveedor.pack(pady=5)

        tk.Label(self.root, text="Dirección:", font=("Arial", 14), bg="#B0C4DE").pack(pady=5)
        self.entry_direccion_proveedor = tk.Entry(self.root, font=("Arial", 14))
        self.entry_direccion_proveedor.pack(pady=5)

        tk.Label(self.root, text="Teléfono:", font=("Arial", 14), bg="#B0C4DE").pack(pady=5)
        self.entry_telefono_proveedor = tk.Entry(self.root, font=("Arial", 14))
        self.entry_telefono_proveedor.pack(pady=5)

        tk.Button(self.root, text="Crear Proveedor", command=self.crear_proveedor_confirmar, font=("Arial", 14), bg="#4CAF50", fg="white", width=button_width, height=button_height).pack(pady=20)
        tk.Button(self.root, text="Regresar", command=self.pantalla_proveedores, font=("Arial", 14), bg="#607D8B", fg="white", width=button_width, height=button_height).pack(pady=10)
        
        # Labels para mostrar informacion/errores
        self.mostrar_info = tk.Label(self.root, text="", font=("Arial", 12), bg="#B0C4DE", fg="black")
        self.mostrar_info.pack(pady=5)
        
    def crear_inventario(self):
        """Muestra una ventana para ingresar los datos de un nuevo inventario."""
        self.limpiar_pantalla()

        tk.Label(self.root, text="Crear Nuevo Inventario", font=("Arial", 22, "bold"), bg="#B0C4DE").pack(pady=20)
        
        # Ancho y alto de los botones
        button_width = 21
        button_height = 1

        tk.Label(self.root, text="Código del Producto:", font=("Arial", 16), bg="#B0C4DE").pack(pady=5)
        self.entry_codigo_inventario = tk.Entry(self.root, font=("Arial", 16))
        self.entry_codigo_inventario.pack(pady=5)

        tk.Label(self.root, text="Cantidad:", font=("Arial", 16), bg="#B0C4DE").pack(pady=5)
        self.entry_cantidad_inventario = tk.Entry(self.root, font=("Arial", 16))
        self.entry_cantidad_inventario.pack(pady=5)

        tk.Label(self.root, text="Stock:", font=("Arial", 16), bg="#B0C4DE").pack(pady=5)
        self.entry_stock = tk.Entry(self.root, font=("Arial", 16))
        self.entry_stock.pack(pady=5)

        tk.Label(self.root, text="Costo /u:", font=("Arial", 16), bg="#B0C4DE").pack(pady=5)
        self.entry_costo_inventario = tk.Entry(self.root, font=("Arial", 16))
        self.entry_costo_inventario.pack(pady=5)

        # Opciones para el tipo de producto, esta opcion no esta en la base de datos, no la implementare
        """opciones_tipo_producto = ["Opción 1", "Opción 2", "Opción 3"]  # Aquí debes reemplazar con las opciones reales
        self.tipo_producto_seleccionado = tk.StringVar()
        self.tipo_producto_seleccionado.set(opciones_tipo_producto[0])  # Opción por defecto

        tk.Label(self.root, text="Tipo de Producto:", font=("Arial", 10), bg="#87CEEB").pack(pady=5)
        dropdown_tipo_producto = ttk.Combobox(self.root, textvariable=self.tipo_producto_seleccionado, values=opciones_tipo_producto, font=("Arial", 10))
        dropdown_tipo_producto.pack(pady=5)"""

        tk.Button(self.root, text="Crear Inventario", command=self.crear_inventario_confirmar, font=("Arial", 16), bg="#4CAF50", fg="white", width=button_width, height=button_height).pack(pady=20)
        tk.Button(self.root, text="Regresar", command=self.pantalla_inventarios, font=("Arial", 16), bg="#607D8B", fg="white", width=button_width, height=button_height).pack(pady=10) 
        
        # Labels para mostrar informacion/errores
        self.mostrar_info = tk.Label(self.root, text="", font=("Arial", 12), bg="#B0C4DE", fg="black")
        self.mostrar_info.pack(pady=5)
        
    def ingresar_venta(self):
        """Muestra una ventana para ingresar los datos de una nueva venta."""
        self.limpiar_pantalla()

        tk.Label(self.root, text="Crear Nueva Venta", font=("Arial", 22, "bold"), bg="#B0C4DE").pack(pady=20)

        # Ancho y alto de los botones
        button_width = 21
        button_height = 1
        
        tk.Label(self.root, text="ID del Cliente:", font=("Arial", 16), bg="#B0C4DE").pack(pady=5)
        self.entry_id_cliente_venta = tk.Entry(self.root, font=("Arial", 16))
        self.entry_id_cliente_venta.pack(pady=5)

        tk.Label(self.root, text="Código del Producto:", font=("Arial", 16), bg="#B0C4DE").pack(pady=5)
        self.entry_codigo_producto_venta = tk.Entry(self.root, font=("Arial", 16))
        self.entry_codigo_producto_venta.pack(pady=5)

        tk.Label(self.root, text="Cantidad de Producto:", font=("Arial", 16), bg="#B0C4DE").pack(pady=5)
        self.entry_cantidad_producto_venta = tk.Entry(self.root, font=("Arial", 16))
        self.entry_cantidad_producto_venta.pack(pady=5)

        tk.Button(self.root, text="Finalizar Venta", command=self.crear_venta_confirmar, font=("Arial", 16), bg="#4CAF50", fg="white", width=button_width, height=button_height).pack(pady=20)
        tk.Button(self.root, text="Regresar", command=self.pantalla_ventas, font=("Arial", 16), bg="#607D8B", fg="white", width=button_width, height=button_height).pack(pady=10)

        # Labels para mostrar informacion/errores
        self.mostrar_info = tk.Label(self.root, text="", font=("Arial", 12), bg="#B0C4DE", fg="black")
        self.mostrar_info.pack(pady=5)
        
    """/***************************************************************************
    FUNCIONES CREAR
    ****************************************************************************/"""

    def crear_usuario_confirmar(self):
        """Confirma la creación de un nuevo usuario."""
        usuario = self.entry_usuario.get()
        contrasena = self.entry_contrasena.get()
        confirmar_contrasena = self.entry_confirmar_contrasena.get()
        nivel_usuario = 3

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

        # Lógica para crear el usuario aquí
        # Ejemplo:
        insertar = "INSERT INTO public.usuarios(nivel, nombre, clave) VALUES (%s, %s, %s);"
        datos = (nivel_usuario,usuario,contrasena)
        cursor.execute(insertar, datos)
        connection.commit()
        self.mostrar_info.config(text="Usuario creado correctamente.")

    def crear_proveedor_confirmar(self):
        """Confirma la creación de un nuevo proveedor."""
        idproveedor = self.entry_idproveedores.get()
        codigo_producto = self.entry_codigo_proveedor.get()
        costo_producto = self.entry_costo_proveedor.get()
        descripcion_producto = self.entry_descripcion_proveedor.get()
        direccion = self.entry_direccion_proveedor.get()
        telefono = self.entry_telefono_proveedor.get()

        # Aquí puedes realizar la validación de los campos ingresados

        # Lógica para crear el proveedor aquí
        # Ejemplo:
        insertar = "INSERT INTO public.proveedores(idproveedores, codproducto, descripcion, costo, direccion, telefono) VALUES (%s, %s, %s, %s, %s, %s);"
        datos = (idproveedor,codigo_producto,descripcion_producto,costo_producto,direccion,telefono)
        cursor.execute(insertar, datos)
        connection.commit()
        self.mostrar_info.config(text="Proveedor creado correctamente.")

    def crear_cliente_confirmar(self):
        """Confirma la creación de un nuevo cliente."""
        id_cliente = self.entry_id_cliente.get()
        nombre = self.entry_nombre_cliente.get()
        direccion = self.entry_direccion_cliente.get()
        telefono = self.entry_telefono_cliente.get()

        # Aquí puedes realizar la validación de los campos ingresados

        # Lógica para crear el cliente aquí
        # Ejemplo:
        insertar = "INSERT INTO public.clientes(idclientes, nombre, direccion, telefono) VALUES (%s, %s, %s, %s);"
        datos = (id_cliente,nombre,direccion,telefono)
        cursor.execute(insertar, datos)
        connection.commit()
        self.mostrar_info.config(text="Cliente creado correctamente.")

    def crear_inventario_confirmar(self):
        """Confirma la creación de un nuevo inventario."""
        codigo_producto = self.entry_codigo_inventario.get()
        cantidad = self.entry_cantidad_inventario.get()
        stock = self.entry_stock.get()
        costo = self.entry_costo_inventario.get()

        # Aquí puedes realizar la validación de los campos ingresados

        # Lógica para crear el inventario aquí
        # Ejemplo:
        insertar = 'INSERT INTO public.inventarios(codproducto, cantidad, "stock min", "costo /u") VALUES (%s, %s, %s, %s);'
        datos = (codigo_producto,cantidad,stock,costo)
        cursor.execute(insertar, datos)
        connection.commit()
        self.mostrar_info.config(text="Inventario creado correctamente.")

    def crear_venta_confirmar(self):
        """Confirma la creación de una nueva venta."""
        id_cliente = self.entry_id_cliente_venta.get()
        codigo_producto = self.entry_codigo_producto_venta.get()
        cantidad_producto = self.entry_cantidad_producto_venta.get()
        cursor.execute('SELECT descripcion FROM proveedores WHERE codproducto = {};'.format(codigo_producto))
        descripcion = cursor.fetchall()
        cursor.execute('SELECT "costo /u" FROM inventarios WHERE codproducto = {}'.format(codigo_producto))
        costo = cursor.fetchone()
        cantidad_producto = int(cantidad_producto)
        descripcion = descripcion[0][0]
        costo = costo[0]
        subtotal = costo * cantidad_producto
        iva = costo* 0.19
        total = costo + iva

        # Aquí puedes realizar la validación de los campos ingresados

        # Lógica para crear la venta aquí
        # Ejemplo:
        insertar = 'INSERT INTO public.ventas(idclientes, codproducto, cantidad, descripcion, iva, subtotal, total) VALUES (%s, %s, %s, %s, %s, %s, %s);'
        datos = (id_cliente,codigo_producto,cantidad_producto,descripcion,iva,subtotal,total)
        cursor.execute(insertar, datos)
        connection.commit()
        self.mostrar_info.config(text="Venta creada correctamente.")
        
        """/***************************************************************************
    FUNCIONES ACTUALIZAR
    ****************************************************************************/"""

    def actualizar_usuario(self):
        self.limpiar_pantalla()

        tk.Label(self.root, text="Actualizar Usuario por su nombre", font=("Arial", 22, "bold"), bg="#B0C4DE").pack(pady=20)

         # Ancho y alto de los botones
        button_width = 21
        button_height = 1
        
        tk.Label(self.root, text="Usuario:", font=("Arial", 18), bg="#B0C4DE").pack(pady=5)
        self.entry_usuario = tk.Entry(self.root, font=("Arial", 16))
        self.entry_usuario.pack(pady=5)

        tk.Label(self.root, text="Contraseña:", font=("Arial", 18), bg="#B0C4DE").pack(pady=5)
        self.entry_contrasena = tk.Entry(self.root, show="*", font=("Arial", 16))
        self.entry_contrasena.pack(pady=5)

        tk.Label(self.root, text="Nivel:", font=("Arial", 18), bg="#B0C4DE").pack(pady=5)
        self.entry_nivel = tk.Entry(self.root, show="*", font=("Arial", 16))
        self.entry_nivel.pack(pady=5)

        tk.Button(self.root, text="Actualizar Usuario", command=self.actualizar_usuario_confirmar, font=("Arial", 18), bg="#4CAF50", fg="white", width=button_width, height=button_height).pack(pady=20)
        tk.Button(self.root, text="Regresar", command=self.pantalla_usuarios, font=("Arial", 18), bg="#607D8B", fg="white", width=button_width, height=button_height).pack(pady=10)
        
        self.mostrar_info = tk.Label(self.root, text="", font=("Arial", 12), bg="#B0C4DE", fg="black")
        self.mostrar_info.pack(pady=5)

    def actualizar_cliente(self):

        self.limpiar_pantalla()
        tk.Label(self.root, text="Actualizar Cliente por ID", font=("Arial", 22, "bold"), bg="#B0C4DE").pack(pady=20)
        
         # Ancho y alto de los botones
        button_width = 21
        button_height = 1

        tk.Label(self.root, text="ID del Cliente:", font=("Arial", 18), bg="#B0C4DE").pack(pady=5)
        self.entry_id_cliente = tk.Entry(self.root, font=("Arial", 16))
        self.entry_id_cliente.pack(pady=5)

        tk.Label(self.root, text="Nombre:", font=("Arial", 18), bg="#B0C4DE").pack(pady=5)
        self.entry_nombre_cliente = tk.Entry(self.root, font=("Arial", 16))
        self.entry_nombre_cliente.pack(pady=5)

        tk.Label(self.root, text="Dirección:", font=("Arial", 18), bg="#B0C4DE").pack(pady=5)
        self.entry_direccion_cliente = tk.Entry(self.root, font=("Arial", 16))
        self.entry_direccion_cliente.pack(pady=5)

        tk.Label(self.root, text="Teléfono:", font=("Arial", 18), bg="#B0C4DE").pack(pady=5)
        self.entry_telefono_cliente = tk.Entry(self.root, font=("Arial", 16))
        self.entry_telefono_cliente.pack(pady=5)

        tk.Button(self.root, text="Crear Cliente", command=self.actualizar_cliente_confirmar, font=("Arial", 18), bg="#4CAF50", fg="white", width=button_width, height=button_height).pack(pady=20)
        tk.Button(self.root, text="Regresar", command=self.pantalla_clientes, font=("Arial", 18), bg="#607D8B", fg="white", width=button_width, height=button_height).pack(pady=10)

        self.mostrar_info = tk.Label(self.root, text="", font=("Arial", 12), bg="#B0C4DE", fg="black")
        self.mostrar_info.pack(pady=5)
        
    def actualizar_proveedor(self):
        """Lógica para actualizar un proveedor."""
        self.limpiar_pantalla()

        tk.Label(self.root, text="Crear Nuevo Proveedor", font=("Arial", 22, "bold"), bg="#B0C4DE").pack(pady=20)
        
         # Ancho y alto de los botones
        button_width = 21
        button_height = 1

        tk.Label(self.root, text="idproveedores", font=("Arial", 18), bg="#B0C4DE").pack(pady=5)
        self.entry_idproveedores = tk.Entry(self.root, font=("Arial", 16))
        self.entry_idproveedores.pack(pady=5)

        tk.Label(self.root, text="Código del Producto:", font=("Arial", 18), bg="#B0C4DE").pack(pady=5)
        self.entry_codigo_proveedor = tk.Entry(self.root, font=("Arial", 16))
        self.entry_codigo_proveedor.pack(pady=5)

        tk.Label(self.root, text="Descripción del Producto:", font=("Arial", 18), bg="#B0C4DE").pack(pady=5)
        self.entry_descripcion_proveedor = tk.Entry(self.root, font=("Arial", 16))
        self.entry_descripcion_proveedor.pack(pady=5)

        tk.Label(self.root, text="Costo del Producto:", font=("Arial", 18), bg="#B0C4DE").pack(pady=5)
        self.entry_costo_proveedor = tk.Entry(self.root, font=("Arial", 16))
        self.entry_costo_proveedor.pack(pady=5)

        tk.Label(self.root, text="Dirección:", font=("Arial", 18), bg="#B0C4DE").pack(pady=5)
        self.entry_direccion_proveedor = tk.Entry(self.root, font=("Arial", 16))
        self.entry_direccion_proveedor.pack(pady=5)

        tk.Label(self.root, text="Teléfono:", font=("Arial", 18), bg="#B0C4DE").pack(pady=5)
        self.entry_telefono_proveedor = tk.Entry(self.root, font=("Arial", 16))
        self.entry_telefono_proveedor.pack(pady=5)

        tk.Button(self.root, text="Crear Proveedor", command=self.actualizar_proveedor_confirmar, font=("Arial", 18), bg="#4CAF50", fg="white", width=button_width, height=button_height).pack(pady=20)
        tk.Button(self.root, text="Regresar", command=self.pantalla_proveedores, font=("Arial", 18), bg="#607D8B", fg="white", width=button_width, height=button_height).pack(pady=10)

        self.mostrar_info = tk.Label(self.root, text="", font=("Arial", 12), bg="#B0C4DE", fg="black")
        self.mostrar_info.pack(pady=5)

    def actualizar_inventario(self):
        """Lógica para actualizar un inventario."""
        self.limpiar_pantalla()

        tk.Label(self.root, text="Actualizar inventario por cod Producto", font=("Arial", 22, "bold"), bg="#B0C4DE").pack(pady=20)
        
         # Ancho y alto de los botones
        button_width = 21
        button_height = 1

        tk.Label(self.root, text="Código del Producto:", font=("Arial", 18), bg="#B0C4DE").pack(pady=5)
        self.entry_codigo_inventario = tk.Entry(self.root, font=("Arial", 16))
        self.entry_codigo_inventario.pack(pady=5)

        tk.Label(self.root, text="Cantidad:", font=("Arial", 18), bg="#B0C4DE").pack(pady=5)
        self.entry_cantidad_inventario = tk.Entry(self.root, font=("Arial", 16))
        self.entry_cantidad_inventario.pack(pady=5)

        tk.Label(self.root, text="Stock:", font=("Arial", 18), bg="#B0C4DE").pack(pady=5)
        self.entry_stock = tk.Entry(self.root, font=("Arial", 16))
        self.entry_stock.pack(pady=5)

        tk.Label(self.root, text="Costo /u:", font=("Arial", 18), bg="#B0C4DE").pack(pady=5)
        self.entry_costo_inventario = tk.Entry(self.root, font=("Arial", 16))
        self.entry_costo_inventario.pack(pady=5)

        tk.Button(self.root, text="Crear Inventario", command=self.actualizar_inventario_confirmar, font=("Arial", 18), bg="#4CAF50", fg="white", width=button_width, height=button_height).pack(pady=20)
        tk.Button(self.root, text="Regresar", command=self.pantalla_inventarios, font=("Arial", 18), bg="#607D8B", fg="white", width=button_width, height=button_height).pack(pady=10) 
        
        # Labels para mostrar informacion/errores
        self.mostrar_info = tk.Label(self.root, text="", font=("Arial", 12), bg="#B0C4DE", fg="black")
        self.mostrar_info.pack(pady=5)

    def actualizar_usuario_confirmar(self):
        nivel = self.entry_nivel.get()
        usuario = self.entry_usuario.get()
        contrasena = self.entry_contrasena.get()
        
        insertar = "UPDATE public.usuarios SET nivel = %s, clave = %s WHERE nombre = %s;"
        datos = (nivel,contrasena,usuario)
        cursor.execute(insertar, datos)
        connection.commit()
        self.mostrar_info.config(text="Usuario actualizado correctamente.")
    
    def actualizar_cliente_confirmar(self):
        idcliente = self.entry_id_cliente.get()
        nombre = self.entry_nombre_cliente.get()
        direccion = self.entry_direccion_cliente.get()
        telefono = self.entry_telefono_cliente.get()
        
        insertar = "UPDATE public.clientes SET nombre = %s, direccion = %s, telefono = %s WHERE idclientes = %s;"
        datos = (nombre,direccion,telefono,idcliente)
        cursor.execute(insertar, datos)
        connection.commit()
        self.mostrar_info.config(text="Cliente actualizado correctamente.")

    def actualizar_proveedor_confirmar(self):
        idproveedores = self.entry_idproveedores.get()
        codproducto = self.entry_codigo_proveedor.get()
        descripcion = self.entry_descripcion_proveedor.get()
        costo = self.entry_costo_proveedor.get()
        direccion = self.entry_direccion_proveedor.get()
        telefono = self.entry_telefono_proveedor.get()
        
        insertar = "UPDATE public.proveedores SET codproducto= %s, descripcion= %s, costo= %s, direccion= %s, telefono=%s WHERE idproveedores= %s;"
        datos = (codproducto,descripcion,costo,direccion,telefono,idproveedores)
        cursor.execute(insertar, datos)
        connection.commit()
        self.mostrar_info.config(text="Proveedores actualizado correctamente.")

    def actualizar_inventario_confirmar(self):
        codproduto = self.entry_codigo_inventario.get()
        cantidad = self.entry_cantidad_inventario.get()
        stock = self.entry_stock.get()
        costo = self.entry_costo_inventario.get()
        
        insertar = 'UPDATE public.inventarios SET cantidad = %s, "stock min"= %s, "costo /u"= %s WHERE codproducto= %s;'
        datos = (cantidad,stock,costo,codproduto)
        cursor.execute(insertar, datos)
        connection.commit()
        self.mostrar_info.config(text="Inventarios actualizado correctamente.")

    def limpiar_pantalla(self):
        """Limpia todos los widgets de la pantalla."""
        for widget in self.root.winfo_children():
            widget.destroy()

    
if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()