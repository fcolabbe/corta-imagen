#!/usr/bin/env python3
"""
Interfaz gráfica simple para la aplicación de corte de imágenes para Instagram
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import threading
import os
from main import ImageProcessor

class InstagramCropGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Cortador de Imágenes para Instagram con Gemini AI")
        self.root.geometry("600x500")
        
        # Variables
        self.api_key = tk.StringVar()
        self.image_url = tk.StringVar()
        self.output_path = tk.StringVar()
        self.processor = None
        
        self.setup_ui()
        
    def setup_ui(self):
        """Configurar la interfaz de usuario"""
        # Frame principal
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configurar grid
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        
        # Título
        title_label = ttk.Label(main_frame, text="🖼️ Cortador de Imágenes para Instagram", 
                               font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        # API Key
        ttk.Label(main_frame, text="API Key de Gemini:").grid(row=1, column=0, sticky=tk.W, pady=5)
        api_key_entry = ttk.Entry(main_frame, textvariable=self.api_key, show="*", width=50)
        api_key_entry.grid(row=1, column=1, sticky=(tk.W, tk.E), pady=5)
        
        # URL de imagen
        ttk.Label(main_frame, text="URL de la imagen:").grid(row=2, column=0, sticky=tk.W, pady=5)
        url_entry = ttk.Entry(main_frame, textvariable=self.image_url, width=50)
        url_entry.grid(row=2, column=1, sticky=(tk.W, tk.E), pady=5)
        
        # Ruta de salida
        ttk.Label(main_frame, text="Archivo de salida:").grid(row=3, column=0, sticky=tk.W, pady=5)
        output_frame = ttk.Frame(main_frame)
        output_frame.grid(row=3, column=1, sticky=(tk.W, tk.E), pady=5)
        output_frame.columnconfigure(0, weight=1)
        
        output_entry = ttk.Entry(output_frame, textvariable=self.output_path, width=40)
        output_entry.grid(row=0, column=0, sticky=(tk.W, tk.E))
        
        browse_btn = ttk.Button(output_frame, text="Examinar", command=self.browse_output)
        browse_btn.grid(row=0, column=1, padx=(5, 0))
        
        # Botón de procesar
        process_btn = ttk.Button(main_frame, text="🚀 Procesar Imagen", 
                                command=self.process_image_threaded)
        process_btn.grid(row=4, column=0, columnspan=2, pady=20)
        
        # Área de log
        ttk.Label(main_frame, text="Log de procesamiento:").grid(row=5, column=0, sticky=tk.W, pady=(10, 5))
        
        self.log_text = scrolledtext.ScrolledText(main_frame, height=15, width=70)
        self.log_text.grid(row=6, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=5)
        
        # Barra de progreso
        self.progress = ttk.Progressbar(main_frame, mode='indeterminate')
        self.progress.grid(row=7, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        
        # Configurar peso de filas
        main_frame.rowconfigure(6, weight=1)
        
        # Cargar API key desde variable de entorno si existe
        if os.getenv("GEMINI_API_KEY"):
            self.api_key.set(os.getenv("GEMINI_API_KEY"))
    
    def browse_output(self):
        """Abrir diálogo para seleccionar archivo de salida"""
        filename = filedialog.asksaveasfilename(
            defaultextension=".jpg",
            filetypes=[("JPEG files", "*.jpg"), ("PNG files", "*.png"), ("All files", "*.*")]
        )
        if filename:
            self.output_path.set(filename)
    
    def log_message(self, message):
        """Agregar mensaje al log"""
        self.log_text.insert(tk.END, f"{message}\n")
        self.log_text.see(tk.END)
        self.root.update_idletasks()
    
    def process_image_threaded(self):
        """Procesar imagen en un hilo separado"""
        if not self.api_key.get():
            messagebox.showerror("Error", "Por favor ingresa tu API key de Gemini")
            return
        
        if not self.image_url.get():
            messagebox.showerror("Error", "Por favor ingresa la URL de la imagen")
            return
        
        # Iniciar procesamiento en hilo separado
        thread = threading.Thread(target=self.process_image)
        thread.daemon = True
        thread.start()
    
    def process_image(self):
        """Procesar la imagen"""
        try:
            self.progress.start()
            self.log_text.delete(1.0, tk.END)
            
            self.log_message("🚀 Iniciando procesamiento...")
            
            # Crear procesador
            self.processor = ImageProcessor(self.api_key.get())
            
            # Procesar imagen
            output_file = self.processor.process_image(
                self.image_url.get(), 
                self.output_path.get() if self.output_path.get() else None
            )
            
            self.log_message(f"✅ ¡Procesamiento completado!")
            self.log_message(f"📁 Archivo guardado: {output_file}")
            self.log_message(f"📱 Lista para Instagram!")
            
            # Mostrar mensaje de éxito
            self.root.after(0, lambda: messagebox.showinfo(
                "Éxito", 
                f"¡Imagen procesada exitosamente!\n\nArchivo guardado en:\n{output_file}"
            ))
            
        except Exception as e:
            error_msg = f"❌ Error: {str(e)}"
            self.log_message(error_msg)
            self.root.after(0, lambda: messagebox.showerror("Error", str(e)))
        
        finally:
            self.progress.stop()

def main():
    """Función principal para la GUI"""
    root = tk.Tk()
    app = InstagramCropGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
