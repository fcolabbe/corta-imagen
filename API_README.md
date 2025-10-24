# 🚀 Instagram Image Cropper API

API REST profesional para cortar imágenes automáticamente para Instagram usando Gemini AI.

## 📋 Características

- **Análisis inteligente** con Gemini AI
- **Detección automática** de dípticos
- **Reglas de prioridad** para personas
- **Corte preciso** para formato Instagram (1080x1080)
- **API REST** con FastAPI
- **Documentación automática** con Swagger
- **Soporte** para URLs y archivos

## 🚀 Instalación

1. **Instalar dependencias:**
```bash
pip install -r requirements.txt
```

2. **Configurar API key (opcional):**
```bash
export GEMINI_API_KEY="tu_api_key_aqui"
```

3. **Iniciar la API:**
```bash
./start_api.sh
```

## 📖 Documentación

Una vez iniciada la API, la documentación estará disponible en:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 🔗 Endpoints

### **POST /analyze-url**
Analizar y cortar imagen desde URL.

**Request Body:**
```json
{
  "url": "https://ejemplo.com/imagen.jpg",
  "api_key": "tu_api_key_gemini",
  "output_filename": "mi_imagen.jpg"
}
```

**Response:**
```json
{
  "success": true,
  "message": "Imagen procesada exitosamente",
  "analysis": {
    "contenido_principal": "Descripción del contenido",
    "imagen_dividida": true,
    "personas_izquierda": true,
    "personas_derecha": false,
    "lado_importante": "izquierda"
  },
  "crop_coordinates": {
    "left": 0,
    "top": 16,
    "right": 600,
    "bottom": 616
  },
  "output_file": "mi_imagen.jpg",
  "processing_time": 12.5
}
```

### **POST /analyze-file**
Analizar y cortar imagen desde archivo subido.

**Form Data:**
- `file`: Archivo de imagen
- `api_key`: API key de Gemini
- `output_filename`: Nombre opcional del archivo de salida

### **GET /download/{filename}**
Descargar imagen procesada.

### **GET /health**
Verificar estado de la API.

### **GET /models**
Información sobre modelos disponibles.

### **GET /rules**
Reglas de corte implementadas.

## 🎯 Reglas de Prioridad

| Escenario | Comportamiento |
|-----------|----------------|
| Solo lado izquierdo tiene personas | ✅ Siempre elige izquierda |
| Solo lado derecho tiene personas | ✅ Siempre elige derecha |
| Ambos lados tienen personas | ✅ Siempre elige izquierda |
| Ningún lado tiene personas | ✅ Elige el más visualmente interesante |

## 📊 Ejemplos de Uso

### **cURL**
```bash
# Analizar desde URL
curl -X POST "http://localhost:8000/analyze-url" \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://ejemplo.com/imagen.jpg",
    "api_key": "tu_api_key",
    "output_filename": "resultado.jpg"
  }'

# Descargar imagen
curl -O "http://localhost:8000/download/resultado.jpg"
```

### **Python**
```python
import requests

# Analizar imagen
response = requests.post("http://localhost:8000/analyze-url", json={
    "url": "https://ejemplo.com/imagen.jpg",
    "api_key": "tu_api_key",
    "output_filename": "resultado.jpg"
})

result = response.json()
print(f"Archivo procesado: {result['output_file']}")
print(f"Coordenadas de corte: {result['crop_coordinates']}")

# Descargar imagen
download_response = requests.get(f"http://localhost:8000/download/{result['output_file']}")
with open("imagen_final.jpg", "wb") as f:
    f.write(download_response.content)
```

### **JavaScript**
```javascript
// Analizar imagen
const response = await fetch('http://localhost:8000/analyze-url', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    url: 'https://ejemplo.com/imagen.jpg',
    api_key: 'tu_api_key',
    output_filename: 'resultado.jpg'
  })
});

const result = await response.json();
console.log('Archivo procesado:', result.output_file);
console.log('Coordenadas:', result.crop_coordinates);
```

## 🧪 Pruebas

Ejecutar cliente de prueba:
```bash
python3 test_api.py
```

## 🔧 Configuración

### **Variables de Entorno**
- `GEMINI_API_KEY`: API key de Google Gemini (opcional)

### **Puerto**
- Puerto por defecto: 8000
- Cambiar en `api.py`: `uvicorn.run(..., port=8000)`

## 📱 Formato de Salida

- **Dimensiones**: 1080x1080 píxeles
- **Formato**: JPEG
- **Calidad**: 95%
- **Proporción**: 1:1 (cuadrado)

## 🚨 Manejo de Errores

La API devuelve códigos de estado HTTP estándar:
- `200`: Éxito
- `400`: Error en la solicitud
- `404`: Archivo no encontrado
- `500`: Error interno del servidor

## 🔒 Seguridad

- La API key se pasa en cada request
- No se almacenan API keys en el servidor
- CORS habilitado para desarrollo
- Validación de tipos con Pydantic

---

**¡Tu API está lista para procesar imágenes inteligentemente para Instagram!** 📱✨
