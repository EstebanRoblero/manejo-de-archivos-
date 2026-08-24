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