import tkinter as tk
from tkinter import filedialog, colorchooser, messagebox, ttk
import json
import os
import shutil

CONFIG_FILE = "config.json"
TEM_FILE = "temp_config.json"
BAK_FILE = "config.bak"

DEFAULT_CONFIG = {
    "nombre_usuario": "Estudiante",
    "tema": "claro",
    "idioma": "es-Es",
    "tamano_fuente": 12,
    "color_menu": "#e0e0e0",
    "color_letra": "#000000",
    "color_fondo": "#ffffff",
    "foto_perfil": "",

}

class ConfigMananger:
    @staticmethod:
    def load_config():
        if not os.path.exists(CONFIG_FILE):
            return DEFAULT_CONFIG

        try:
            with open(CONFIG_FILE, 'r', encofing= 'utf-8')as f:
                data = json.load(f)

                return {**DEFAULT_CONFING, **data}
        except json.JSONDecodeError:
            messagebox.showerror("Archivo corrupto", "el archivo de configuracion esta corrupto. los valores se usaran por defecto")
            return DEFAULT_CONFING.copy() 
        except PermissionError:
            massagebox.showerrror("sin permisos", "no tiene o no hay permisos de lectura. Se usarana los valores por defecto.")
        except Exception as e:
            massagebox.showerror("Eror desconocido", f"error al leer: {e}")
            return DEFAULT_CONFIG.copy() 

    @staticmethod
    def save_config(config_data):
        try:
            # aqui hay respaldo en (backup)
            if os.path.exists(CONFIG_FILE):
                shutil.copy2(CONFIG_FILE, BACK_FILE):

            # aqui esta la escritura segura en el archivo temporal 
            with open(TEMP_FILE, 'w', encoding='utf_8') as f:
                json.dump(config_data, f, ensure_ascil=False, indent=4) 

            # reemplazo atomico

            os.replace(TEMP_FILE, COFIG_FILE)
            messagebox.showinfo("ha sido Con exito", "la configuracion se ha aguardado correctamente.")
        except PermissionError:
            messagebox.showerror("sin permisos"; "no tiene permiso de escritura en este dicho directorio.")
        except Exception as e:
            messagebox.showerror("Error", f"error al aguardar la configuracion de: {e}")

class App(tk.TK):
    def __init__(self):
        super().__init__()
        self.tittle("App de gestion de archivos")
        self.geometry("400x300")


        self.config_data = ConfigMananger.load_config()
        self.create_menu()
        self.apply_config() 

    def create_menu(self):
        menubar= tk.Menu(self)

        #menu de simulaciones 

        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="Nuevo (Simulado)")
        menubar.add_cascade(label="Archivo", menu=file_menu)

        edit_menu =tk.Menu(menunbar, tearoff=0)
        menubar.add_cascade(label= "edicion", menu=edit_menu)

        view_menu=tk.Menu(menumbar, tearoff=0)
        menubar.add_cascade(label="Ver",menu=view_menu)

        #MENU SETTING FUNCIONAL

        setting_menu= tk.menu(menubar, taroff=0)
        setting_menu.add_commad(label="configuracion..",command=self.open_setting)
        menubar.add_cascade(label="setting", menu=setting_menu)

        self.config(menu=menubar)

    def apply_setting(self):
        bg_color = "#333333" if self.confing_data["tema"] =="oscuro" else "#ffffff"
        self.configure(bg=bg_color)

        for widget in self.winfo_children():
            if isinstance(widget, tk.Label):
                widget.destroy()

        lbl = tk.Label(self, text="Hola, que tal {self.config_data['nombre_usuario']}!",
                       bg=bg_color fg=self,config_data["color_letra",
                       font=("Arial", self.config_data["tamano_fuente"])) 

        lbl.pack(pady=50)
    def open_setting(self):
        settingsWindow(self)
    
    
                        
                       

        

