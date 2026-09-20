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
        tk.Label(self, text="Idioma: ").pack(anchor="w", padx=10, pady=2)
        self.cb_idioma = ttk.Combobox(
            self, values = ["Español ES", "English EN"], state="readonly",
        )

        self.cb_idioma.set(self.config_data.get("Idioma", "Español ES"))
        self.cb_idioma.pack(fill="x", padx=10, pady=2)

        #tamaño de la fuente
        self.sp_fuente = tk.Spinbox(self, from_=8, to=32)
        self.sp_fuente.delete(0, "end")
        self.sp_fuente.insert(0, self.config_data.get("Tamaño de la fuente", 12))
        self.sp_fuente.pack(fill="x", padx=10, pady=2)

        #color del menu
        btn_col_menu = tk.Button(
            self, text="Color de la barra de menu", command=self.pick_color_menu
        )
        btn_col_menu.pack(fill="x", padx=10, pady=2)

        #color de letra
        btn_color_letra = tk.Button(
            self, text="Color de la fuente", command=self.pick_color_letra
        )
        btn_color_letra.pack(fill="x", padx=10, pady=2)

        #boton foto de perfil
        btn_foto = tk.Button(
            self, text="Seleccione su foto de perfil", command=self.pick_foto
        )
        btn_foto.pack(fill="x", padx=10, pady=2)

        self.lbl_foto = tk.Label(self, text=self.config_data.get("foto_perfil", ""))
        self.lbl_foto.pack(padx=10, pady=2)

        #guardar
        btn_guardar = tk.Button(
            self, text="Guardar Configuración", command=self.save
        )
        btn_guardar.pack(pady=15)

    def pick_color_menu(self):
        color = colorchooser.askcolor(title="Seleccionar color de menú")
        if color[1]:
            self.config_data["color_menu"] = color[1]

    def pick_color_letra(self):
        color = colorchooser.askcolor(title="Seleccionar color de letra")
        if color[1]:
            self.config_data["color_letra"] = color[1]

    def pick_foto(self):
        filename = filedialog.askopenfilename(
            title="Seleccionar imagen",
            filetypes=[("Archivos de imagen", "*.png *.jpg *.jpeg *.gif *.bmp")],
        )
        if filename:
            self.config_data["foto_perfil"] = filename
            self.lbl_foto.config(text=filename)

    def save(self):
        try:
            self.config_data["nombre_usuario"] = self.ent_usuario.get()
            self.config_data["tema"] = self.cb_tema.get()
            self.config_data["idioma"] = self.cb_idioma.get()
            self.config_data["tamano_fuente"] = int(self.sp_fuente.get())

            if ConfigManager.save_config(self.config_data):
                self.parent.config_data = self.config_data
                self.parent.apply_config()
                self.destroy()
        except ValueError:
            messagebox.showerror(
                "Error", "El tamaño de fuente debe ser un número entero."
            )

    class App(tk.Tk):

        def __init__(self):
            super().__init__()

            self.title("App de gestión de archivos")
            self.geometry("400x300")

            self.config_data = ConfigManager.load_config()

            self.create_menu()
            self.apply_config()

        def create_menu(self):
            self.menubar = tk.Menu(self)

            file_menu = tk.Menu(self.menubar, tearoff=0)
            file_menu.add_command(label="Nuevo (Simulado)")
            self.menubar.add_cascade(label="Archivo", menu=file_menu)

            edit_menu = tk.Menu(self.menubar, tearoff=0)
            self.menubar.add_cascade(label="Edición", menu=edit_menu)

            view_menu = tk.Menu(self.menubar, tearoff=0)
            self.menubar.add_cascade(label="Ver", menu=view_menu)

            setting_menu = tk.Menu(self.menubar, tearoff=0)
            setting_menu.add_command(
                label="Configuración...", command=self.open_setting
            )
            self.menubar.add_cascade(label="Settings", menu=setting_menu)

            self.config(menu=self.menubar)

        def apply_config(self):
            bg_color = (
                "#333333" if self.config_data.get("tema") == "oscuro" else "#ffffff"
            )
            self.configure(bg=bg_color)

            if "color_menu" in self.config_data:
                self.menubar.config(bg=self.config_data["color_menu"])

            for widget in self.winfo_children():
                if isinstance(widget, tk.Label):
                    widget.destroy()

            lbl = tk.Label(
                self,
                text=f"Hola, ¿qué tal {self.config_data.get('nombre_usuario')}?",
                bg=bg_color,
                fg=self.config_data.get("color_letra", "#000000"),
                font=("Arial", self.config_data.get("tamano_fuente", 12)),
            )

            lbl.pack(pady=50)

        def open_setting(self):
            SettingsWindow(self)

    if __name__ == "__main__":
        app = App()
        app.mainloop()