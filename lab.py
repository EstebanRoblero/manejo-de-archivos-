import tkinter as tk
from tkinter import filedialog, colorchooser, messagebox, ttk
import json
import os
import shutil

CONFIG_FILE = "config.json"
TEMP_FILE = "temp_config.json"
BAK_FILE = "config.bak"

DEFAULT_CONFIG = {
    "nombre_usuario": "Estudiante",
    "tema": "claro",
    "idioma": "es-Es",
    "tamano_fuente": 12,
    "color_menu": "#e0e0e0",
    "color_letra": "#000000",
    "color_fondo": "#ffffff",
    "foto_perfil": ""
}


class ConfigMananger:

    @staticmethod
    def load_config():
        if not os.path.exists(CONFIG_FILE):
            return DEFAULT_CONFIG

        try:
            with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)

                return {**DEFAULT_CONFIG, **data}

        except json.JSONDecodeError:
            messagebox.showerror(
                "Archivo corrupto",
                "El archivo de configuración está corrupto. "
                "Los valores se usarán por defecto."
            )
            return DEFAULT_CONFIG.copy()

        except PermissionError:
            messagebox.showerror(
                "Sin permisos",
                "No hay permisos de lectura. "
                "Se usarán los valores por defecto."
            )
            return DEFAULT_CONFIG.copy()

        except Exception as e:
            messagebox.showerror(
                "Error desconocido",
                f"Error al leer: {e}"
            )
            return DEFAULT_CONFIG.copy()

    @staticmethod
    def save_config(config_data):
        try:

            # Aquí hay respaldo (backup)
            if os.path.exists(CONFIG_FILE):
                shutil.copy2(CONFIG_FILE, BAK_FILE)

            # Escritura segura en archivo temporal
            with open(TEMP_FILE, 'w', encoding='utf-8') as f:
                json.dump(
                    config_data,
                    f,
                    ensure_ascii=False,
                    indent=4
                )

            # Reemplazo atómico
            os.replace(TEMP_FILE, CONFIG_FILE)

            messagebox.showinfo(
                "Éxito",
                "La configuración se ha guardado correctamente."
            )

        except PermissionError:
            messagebox.showerror(
                "Sin permisos",
                "No tiene permiso de escritura en este directorio."
            )

        except Exception as e:
            messagebox.showerror(
                "Error",
                f"Error al guardar la configuración: {e}"
            )
            return False

class SettingsWindow(tk.TopLevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.title("Configuracion")
        self.geometry("400x500")

        self.config_data = parent.config_data.copy()

        self.create_widgets()

    def create_widgets(self):
        #nombre de usuario
        tk.Label(self, text="Nombre de Usuario: ").pacK(anchor="w", padx=10, pady=2)
        self.ent_usuario = tk.Entry(self)
        self.ent_usuario.insert(0, self.config_data.get("nombre_usuario", ""))
        self.ent_usuario.pack(fill="x", padx=10, pady=2)

        #tema
        tk.Label(self, text="Tema: ").pack(anchor="w", padx=10, pady=2)
        self.cb_tema = ttk.Combobox(
            self, values = ["claro", "oscuro"], state="readonly",
        )
        self.cb_tema.set(self.config_data.get("tema", "claro"))
        self.cb_tema.pack(fill="x", padx=10, pady=2)

        #idioma




class App(tk.Tk):

    def __init__(self):
        super().__init__()

        self.title("App de gestión de archivos")
        self.geometry("400x300")

        self.config_data = ConfigMananger.load_config()

        self.create_menu()
        self.apply_config()

    def create_menu(self):
        menubar = tk.Menu(self)

        # Menú de simulaciones
        file_menu = tk.Menu(menubar, tearoff=0)

        file_menu.add_command(
            label="Nuevo (Simulado)"
        )

        menubar.add_cascade(
            label="Archivo",
            menu=file_menu
        )

        edit_menu = tk.Menu(menubar, tearoff=0)

        menubar.add_cascade(
            label="Edición",
            menu=edit_menu
        )

        view_menu = tk.Menu(menubar, tearoff=0)

        menubar.add_cascade(
            label="Ver",
            menu=view_menu
        )

        # Menú Settings
        setting_menu = tk.Menu(menubar, tearoff=0)

        setting_menu.add_command(
            label="Configuración...",
            command=self.open_setting
        )

        menubar.add_cascade(
            label="Settings",
            menu=setting_menu
        )

        self.config(menu=menubar)

    def apply_config(self):

        bg_color = (
            "#333333"
            if self.config_data["tema"] == "oscuro"
            else "#ffffff"
        )

        self.configure(bg=bg_color)

        for widget in self.winfo_children():
            if isinstance(widget, tk.Label):
                widget.destroy()

        lbl = tk.Label(
            self,
            text=f"Hola, ¿qué tal {self.config_data['nombre_usuario']}?",
            bg=bg_color,
            fg=self.config_data["color_letra"],
            font=("Arial", self.config_data["tamano_fuente"])
        )

        lbl.pack(pady=50)

    def open_setting(self):
        settingsWindow(self)


app = App()
app.mainloop()