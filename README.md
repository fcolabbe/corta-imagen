# Instagram Image Cropper

Una aplicación inteligente que descarga imágenes desde URLs, las analiza con Google Gemini AI y las corta automáticamente para formato Instagram, manteniendo el contenido esencial de la imagen.

## ✨ Características

- **Descarga automática** de imágenes desde URLs
- **Análisis inteligente** con Google Gemini AI para detectar contenido esencial
- **Corte automático** para formato cuadrado de Instagram (1080x1080)
- **Detección especial** de imágenes divididas en dos partes
- **Selección inteligente** del lado más importante en imágenes fusionadas
- **API REST** profesional con FastAPI
- **Interfaz gráfica** fácil de usar
- **Interfaz de línea de comandos** para automatización

## 🚀 Instalación

1. **Clona el repositorio:**
```bash
git clone https://github.com/tu-usuario/corta-imagen.git
cd corta-imagen
```

2. **Instala las dependencias:**
```bash
pip install -r requirements.txt
```

3. **Obtén tu API key de Google Gemini:**
   - Ve a [Google AI Studio](https://makersuite.google.com/app/apikey)
   - Crea una nueva API key
   - Copia la clave

## 📖 Uso

### Interfaz Gráfica (Recomendado)

```bash
python gui.py
```

### Línea de Comandos

```bash
# Uso básico
python main.py "https://ejemplo.com/imagen.jpg"

# Con archivo de salida específico
python main.py "https://ejemplo.com/imagen.jpg" -o "mi_imagen_instagram.jpg"

# Con API key específica
python main.py "https://ejemplo.com/imagen.jpg" -k "tu_api_key_aqui"

# Modo verbose para más información
python main.py "https://ejemplo.com/imagen.jpg" -v
```

### API REST

```bash
# Iniciar la API
./start_api.sh

# La API estará disponible en http://localhost:8000
# Documentación: http://localhost:8000/docs
```

## 🧠 Cómo Funciona

1. **Descarga**: La aplicación descarga la imagen desde la URL proporcionada
2. **Análisis**: Gemini AI analiza la imagen para detectar:
   - Contenido principal
   - Elementos importantes en los bordes
   - **Imágenes divididas en dos partes** (caso especial)
   - Cuál lado es más importante cuando hay dos fotos fusionadas
   - Punto focal principal
   - Texto visible
3. **Cálculo**: Se calcula el área de corte óptima basada en el análisis
4. **Corte**: La imagen se corta manteniendo el contenido esencial
5. **Redimensionado**: Se ajusta al formato cuadrado de Instagram (1080x1080)

## 🎯 Casos Especiales

### Imágenes Divididas en Dos Partes

Cuando la aplicación detecta que una imagen contiene dos fotos fusionadas:

- **Análisis automático**: Gemini determina cuál lado contiene el contenido más importante
- **Corte inteligente**: Se enfoca en el lado más relevante
- **Preservación**: Mantiene la integridad visual del contenido principal

### Reglas de Prioridad para Dípticos

| Escenario | Comportamiento |
|-----------|----------------|
| Solo lado izquierdo tiene personas | ✅ Siempre elige izquierda |
| Solo lado derecho tiene personas | ✅ Siempre elige derecha |
| Ambos lados tienen personas | ✅ Siempre elige izquierda |
| Ningún lado tiene personas | ✅ Elige el más visualmente interesante |

## 📁 Estructura del Proyecto

```
corta-imagen/
├── main.py              # Aplicación principal (CLI)
├── gui.py               # Interfaz gráfica
├── api.py               # API REST con FastAPI
├── requirements.txt     # Dependencias
├── start_api.sh         # Script para iniciar API
├── test_api.py          # Cliente de prueba
├── install.sh           # Script de instalación
├── setup_api.sh         # Configuración de API key
├── ejemplos.sh          # Ejemplos de uso
├── prompt_n8n_modificado.txt # Prompt para n8n
├── README.md            # Este archivo
└── API_README.md        # Documentación de la API
```

## 🔧 Dependencias

- `requests`: Para descargar imágenes
- `Pillow`: Para procesamiento de imágenes
- `google-generativeai`: Para análisis con Gemini AI
- `fastapi`: Para la API REST
- `uvicorn`: Servidor ASGI para FastAPI
- `python-multipart`: Para manejo de archivos
- `tkinter`: Para la interfaz gráfica (incluido con Python)

## 🌐 API REST

La aplicación incluye una API REST completa con FastAPI:

- **Documentación automática**: http://localhost:8000/docs
- **Endpoints**: `/analyze-url`, `/analyze-file`, `/download`, `/health`
- **Formato de respuesta**: JSON estructurado con análisis completo
- **Coordenadas de corte**: Formato PIL estándar

Ver `API_README.md` para documentación completa de la API.

## ⚠️ Limitaciones

- Requiere conexión a internet para descargar imágenes y usar Gemini AI
- Las imágenes muy grandes pueden tardar más en procesarse
- El análisis de Gemini puede variar según la complejidad de la imagen

## 🤝 Contribuciones

¡Las contribuciones son bienvenidas! Si encuentras bugs o tienes ideas para mejorar la aplicación, no dudes en crear un issue o pull request.

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo LICENSE para más detalles.

---

**¡Disfruta creando contenido perfecto para Instagram! 📱✨**