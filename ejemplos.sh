# Ejemplo de uso de la aplicación

# Configurar API key (opcional si ya está en variables de entorno)
export GEMINI_API_KEY="tu_api_key_de_gemini_aqui"

# Ejemplo 1: Uso básico con interfaz gráfica
python gui.py

# Ejemplo 2: Uso desde línea de comandos
python main.py "https://ejemplo.com/imagen.jpg"

# Ejemplo 3: Con archivo de salida específico
python main.py "https://ejemplo.com/imagen.jpg" -o "mi_imagen_instagram.jpg"

# Ejemplo 4: Con API key específica
python main.py "https://ejemplo.com/imagen.jpg" -k "tu_api_key_aqui"

# Ejemplo 5: Modo verbose para más información
python main.py "https://ejemplo.com/imagen.jpg" -v

# Ejemplo 6: URL de imagen real para probar
python main.py "https://picsum.photos/1200/800" -o "ejemplo_instagram.jpg"
