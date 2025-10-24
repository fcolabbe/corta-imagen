#!/usr/bin/env python3
"""
API REST para el servicio de corte de imágenes para Instagram
Usando FastAPI para crear endpoints profesionales
"""

from fastapi import FastAPI, HTTPException, UploadFile, File, Form
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, HttpUrl
from typing import Optional, Dict, Any
import uvicorn
import os
import tempfile
import logging
from main import ImageProcessor

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Crear aplicación FastAPI
app = FastAPI(
    title="Instagram Image Cropper API",
    description="API para cortar imágenes automáticamente para Instagram usando Gemini AI",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Modelos Pydantic
class ImageAnalysisRequest(BaseModel):
    url: HttpUrl
    api_key: str
    output_filename: Optional[str] = None

class ImageAnalysisResponse(BaseModel):
    success: bool
    message: str
    analysis: Optional[Dict[str, Any]] = None
    crop_coordinates: Optional[Dict[str, int]] = None
    output_file: Optional[str] = None
    processing_time: Optional[float] = None

class HealthResponse(BaseModel):
    status: str
    version: str
    gemini_model: str

# Variable global para el procesador
processor = None

@app.on_event("startup")
async def startup_event():
    """Inicializar el procesador al arrancar la API"""
    global processor
    logger.info("🚀 Iniciando Instagram Image Cropper API...")

@app.get("/", response_model=HealthResponse)
async def root():
    """Endpoint de salud de la API"""
    return HealthResponse(
        status="healthy",
        version="1.0.0",
        gemini_model="gemini-2.5-flash"
    )

@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Endpoint de verificación de salud"""
    return HealthResponse(
        status="healthy",
        version="1.0.0",
        gemini_model="gemini-2.5-flash"
    )

@app.post("/analyze-url", response_model=ImageAnalysisResponse)
async def analyze_image_from_url(request: ImageAnalysisRequest):
    """
    Analizar y cortar imagen desde URL
    
    - **url**: URL de la imagen a procesar
    - **api_key**: API key de Google Gemini
    - **output_filename**: Nombre opcional para el archivo de salida
    """
    try:
        import time
        start_time = time.time()
        
        # Crear procesador con la API key
        global processor
        processor = ImageProcessor(request.api_key)
        
        # Procesar imagen
        output_file = processor.process_image(
            str(request.url), 
            request.output_filename
        )
        
        processing_time = time.time() - start_time
        
        # Obtener análisis del último procesamiento
        analysis = getattr(processor, '_last_analysis', {})
        crop_coords = getattr(processor, '_last_crop_coordinates', {})
        
        return ImageAnalysisResponse(
            success=True,
            message="Imagen procesada exitosamente",
            analysis=analysis,
            crop_coordinates=crop_coords,
            output_file=output_file,
            processing_time=round(processing_time, 2)
        )
        
    except Exception as e:
        logger.error(f"Error procesando imagen: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Error procesando imagen: {str(e)}"
        )

@app.post("/analyze-file", response_model=ImageAnalysisResponse)
async def analyze_image_from_file(
    file: UploadFile = File(...),
    api_key: str = Form(...),
    output_filename: Optional[str] = Form(None)
):
    """
    Analizar y cortar imagen desde archivo subido
    
    - **file**: Archivo de imagen a procesar
    - **api_key**: API key de Google Gemini
    - **output_filename**: Nombre opcional para el archivo de salida
    """
    try:
        import time
        start_time = time.time()
        
        # Guardar archivo temporalmente
        with tempfile.NamedTemporaryFile(delete=False, suffix=f".{file.filename.split('.')[-1]}") as temp_file:
            content = await file.read()
            temp_file.write(content)
            temp_file_path = temp_file.name
        
        # Crear procesador
        global processor
        processor = ImageProcessor(api_key)
        
        # Procesar imagen
        output_file = processor.process_image(
            temp_file_path,
            output_filename
        )
        
        processing_time = time.time() - start_time
        
        # Limpiar archivo temporal
        os.unlink(temp_file_path)
        
        # Obtener análisis del último procesamiento
        analysis = getattr(processor, '_last_analysis', {})
        crop_coords = getattr(processor, '_last_crop_coordinates', {})
        
        return ImageAnalysisResponse(
            success=True,
            message="Imagen procesada exitosamente",
            analysis=analysis,
            crop_coordinates=crop_coords,
            output_file=output_file,
            processing_time=round(processing_time, 2)
        )
        
    except Exception as e:
        logger.error(f"Error procesando archivo: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Error procesando archivo: {str(e)}"
        )

@app.get("/download/{filename}")
async def download_image(filename: str):
    """Descargar imagen procesada"""
    file_path = filename
    if os.path.exists(file_path):
        return FileResponse(
            file_path,
            media_type="image/jpeg",
            filename=filename
        )
    else:
        raise HTTPException(
            status_code=404,
            detail="Archivo no encontrado"
        )

@app.get("/models")
async def get_available_models():
    """Obtener información sobre modelos disponibles"""
    return {
        "current_model": "gemini-2.5-flash",
        "model_type": "multimodal",
        "capabilities": [
            "image_analysis",
            "person_detection", 
            "diptych_detection",
            "smart_cropping",
            "json_output"
        ],
        "supported_formats": ["jpg", "jpeg", "png", "webp"],
        "max_image_size": "10MB"
    }

@app.get("/rules")
async def get_cropping_rules():
    """Obtener reglas de corte implementadas"""
    return {
        "priority_rules": {
            "single_person_left": "Siempre elige el lado izquierdo si solo tiene personas",
            "single_person_right": "Siempre elige el lado derecho si solo tiene personas", 
            "both_sides_persons": "Siempre elige el lado izquierdo si ambos tienen personas",
            "no_persons": "Elige el lado más visualmente interesante"
        },
        "output_format": {
            "aspect_ratio": "1:1 (cuadrado)",
            "dimensions": "1080x1080 pixels",
            "quality": "95% JPEG"
        },
        "coordinate_format": "PIL standard (left, top, right, bottom)"
    }

if __name__ == "__main__":
    uvicorn.run(
        "api:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
