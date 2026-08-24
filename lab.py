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
                    