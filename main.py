#!/usr/bin/env python3
"""
Aplicación para cortar imágenes automáticamente para Instagram usando Gemini AI
Analiza imágenes y las corta manteniendo el contenido esencial
"""

import os
import sys
import argparse
import requests
from PIL import Image, ImageOps
import google.generativeai as genai
from io import BytesIO
import json
from typing import Tuple, Dict, Any
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class ImageProcessor:
    def __init__(self, api_key: str):
        """Inicializar el procesador de imágenes con la API key de Gemini"""
        self.api_key = api_key
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-2.5-flash')
        
    def load_image(self, source: str) -> Image.Image:
        """Cargar imagen desde URL o archivo local"""
        try:
            if source.startswith(('http://', 'https://')):
                # Descargar desde URL
                logger.info(f"Descargando imagen desde: {source}")
                response = requests.get(source, timeout=30)
                response.raise_for_status()
                
                image = Image.open(BytesIO(response.content))
                logger.info(f"Imagen descargada: {image.size[0]}x{image.size[1]} píxeles")
            else:
                # Cargar archivo local
                logger.info(f"Cargando imagen local: {source}")
                image = Image.open(source)
                logger.info(f"Imagen cargada: {image.size[0]}x{image.size[1]} píxeles")
            
            return image
        except Exception as e:
            logger.error(f"Error al cargar imagen: {e}")
            raise
    
    def analyze_image_with_gemini(self, image: Image.Image) -> Dict[str, Any]:
        """Analizar imagen con Gemini para detectar contenido esencial"""
        try:
            # Convertir imagen a bytes para Gemini
            img_byte_arr = BytesIO()
            image.save(img_byte_arr, format='JPEG', quality=85)
            img_byte_arr = img_byte_arr.getvalue()
            
            prompt = """
            Analiza esta imagen y proporciona información detallada en formato JSON:
            
            1. ¿Cuál es el contenido principal de la imagen?
            2. ¿Hay elementos importantes en los bordes que no deben cortarse?
            3. ¿La imagen parece estar dividida en dos partes distintas (como dos fotos fusionadas o un díptico)?
            4. Si está dividida, analiza cada lado por separado:
               - Lado izquierdo: ¿qué contiene? ¿hay personas visibles?
               - Lado derecho: ¿qué contiene? ¿hay personas visibles?
               - ¿Cuál lado tiene personas?
               - ¿Cuál lado tiene más contenido visual interesante o importante?
               - ¿Cuál lado tiene mejor composición para Instagram?
            5. ¿Cuál es el punto focal principal de la imagen?
            6. ¿Hay texto visible que debe mantenerse?
            
            REGLAS DE PRIORIDAD PARA DÍPTICOS:
            - Si solo UN lado tiene personas: SIEMPRE elige ese lado
            - Si AMBOS lados tienen personas: SIEMPRE elige el lado izquierdo
            - Si NINGÚN lado tiene personas: elige el más visualmente interesante
            
            IMPORTANTE: Si la imagen está dividida, NO cortes por la mitad. Elige UN lado completo (izquierda o derecha) que sea más interesante para Instagram.
            
            Responde SOLO en formato JSON válido con estas claves:
            {
                "contenido_principal": "descripción",
                "elementos_bordes": "descripción de elementos en bordes",
                "imagen_dividida": true/false,
                "lado_izquierdo": "descripción del contenido del lado izquierdo",
                "lado_derecho": "descripción del contenido del lado derecho",
                "personas_izquierda": true/false,
                "personas_derecha": true/false,
                "lado_importante": "izquierda/derecha/centro",
                "razon_lado_elegido": "explicación de por qué se eligió ese lado",
                "punto_focal": "descripción del punto focal",
                "texto_visible": "texto encontrado o 'ninguno'",
                "recomendacion_corte": "descripción específica de cómo cortar"
            }
            """
            
            logger.info("Analizando imagen con Gemini...")
            response = self.model.generate_content([prompt, {"mime_type": "image/jpeg", "data": img_byte_arr}])
            
            # Extraer JSON de la respuesta
            response_text = response.text.strip()
            if response_text.startswith('```json'):
                response_text = response_text[7:-3]
            elif response_text.startswith('```'):
                response_text = response_text[3:-3]
            
            analysis = json.loads(response_text)
            logger.info("Análisis completado")
            return analysis
            
        except Exception as e:
            logger.error(f"Error al analizar imagen con Gemini: {e}")
            # Análisis por defecto si falla Gemini
            return {
                "contenido_principal": "imagen general",
                "elementos_bordes": "no detectados",
                "imagen_dividida": False,
                "lado_izquierdo": "no aplicable",
                "lado_derecho": "no aplicable",
                "personas_izquierda": False,
                "personas_derecha": False,
                "lado_importante": "centro",
                "razon_lado_elegido": "imagen no dividida",
                "punto_focal": "centro de la imagen",
                "texto_visible": "ninguno",
                "recomendacion_corte": "corte centrado"
            }
    
    def calculate_crop_area(self, image: Image.Image, analysis: Dict[str, Any]) -> Tuple[int, int, int, int]:
        """Calcular área de corte basada en el análisis"""
        width, height = image.size
        target_ratio = 1.0  # Instagram square format
        
        logger.info(f"Dimensiones originales: {width}x{height}")
        
        # Si la imagen está dividida, aplicar reglas de prioridad
        if analysis.get("imagen_dividida", False):
            lado_importante = analysis.get("lado_importante", "centro")
            razon = analysis.get("razon_lado_elegido", "no especificada")
            personas_izq = analysis.get("personas_izquierda", False)
            personas_der = analysis.get("personas_derecha", False)
            
            logger.info(f"Imagen dividida detectada, lado importante: {lado_importante}")
            logger.info(f"Personas izquierda: {personas_izq}, Personas derecha: {personas_der}")
            logger.info(f"Razón de elección: {razon}")
            
            # Aplicar reglas de prioridad para personas
            if personas_izq and not personas_der:
                lado_importante = "izquierda"
                logger.info("REGLA APLICADA: Solo lado izquierdo tiene personas - eligiendo izquierda")
            elif personas_der and not personas_izq:
                lado_importante = "derecha"
                logger.info("REGLA APLICADA: Solo lado derecho tiene personas - eligiendo derecha")
            elif personas_izq and personas_der:
                lado_importante = "izquierda"
                logger.info("REGLA APLICADA: Ambos lados tienen personas - eligiendo izquierda por defecto")
            
            if lado_importante == "izquierda":
                # Enfocar completamente en el lado izquierdo
                crop_width = min(width // 2, height)  # Usar solo la mitad izquierda
                crop_height = crop_width
                left = 0
                top = (height - crop_height) // 2
                right = crop_width
                bottom = top + crop_height
                logger.info("Corte aplicado: Lado izquierdo completo")
                
            elif lado_importante == "derecha":
                # Enfocar completamente en el lado derecho
                crop_width = min(width // 2, height)  # Usar solo la mitad derecha
                crop_height = crop_width
                left = width - crop_width
                top = (height - crop_height) // 2
                right = width
                bottom = top + crop_height
                logger.info("Corte aplicado: Lado derecho completo")
                
            else:  # centro
                # Corte centrado normal
                crop_size = min(width, height)
                left = (width - crop_size) // 2
                top = (height - crop_size) // 2
                right = left + crop_size
                bottom = top + crop_size
                logger.info("Corte aplicado: Centrado")
        else:
            # Corte centrado normal
            crop_size = min(width, height)
            left = (width - crop_size) // 2
            top = (height - crop_size) // 2
            right = left + crop_size
            bottom = top + crop_size
            logger.info("Corte aplicado: Centrado (imagen no dividida)")
        
        logger.info(f"Área de corte calculada: ({left}, {top}, {right}, {bottom})")
        return (left, top, right, bottom)
    
    def crop_image(self, image: Image.Image, crop_area: Tuple[int, int, int, int]) -> Image.Image:
        """Cortar imagen según el área calculada"""
        left, top, right, bottom = crop_area
        cropped = image.crop((left, top, right, bottom))
        
        # Redimensionar a tamaño estándar de Instagram si es necesario
        target_size = (1080, 1080)  # Tamaño recomendado para Instagram
        if cropped.size != target_size:
            cropped = cropped.resize(target_size, Image.Resampling.LANCZOS)
        
        logger.info(f"Imagen cortada a: {cropped.size[0]}x{cropped.size[1]} píxeles")
        return cropped
    
    def process_image(self, source: str, output_path: str = None) -> str:
        """Procesar imagen completa: cargar, analizar y cortar"""
        try:
            # Cargar imagen (URL o archivo local)
            image = self.load_image(source)
            
            # Analizar con Gemini
            analysis = self.analyze_image_with_gemini(image)
            logger.info(f"Análisis: {analysis}")
            
            # Calcular área de corte
            crop_area = self.calculate_crop_area(image, analysis)
            
            # Guardar datos para la API
            self._last_analysis = analysis
            self._last_crop_coordinates = {
                "left": crop_area[0],
                "top": crop_area[1], 
                "right": crop_area[2],
                "bottom": crop_area[3]
            }
            
            # Cortar imagen
            cropped_image = self.crop_image(image, crop_area)
            
            # Guardar imagen procesada
            if output_path is None:
                output_path = f"instagram_crop_{hash(source) % 10000}.jpg"
            
            cropped_image.save(output_path, "JPEG", quality=95)
            logger.info(f"Imagen guardada en: {output_path}")
            
            return output_path
            
        except Exception as e:
            logger.error(f"Error al procesar imagen: {e}")
            raise

def main():
    """Función principal"""
    parser = argparse.ArgumentParser(description="Cortar imágenes para Instagram usando Gemini AI")
    parser.add_argument("source", help="URL de la imagen o ruta del archivo local a procesar")
    parser.add_argument("-o", "--output", help="Ruta de salida para la imagen procesada")
    parser.add_argument("-k", "--api-key", help="API key de Google Gemini", 
                       default=os.getenv("GEMINI_API_KEY"))
    parser.add_argument("-v", "--verbose", action="store_true", help="Mostrar información detallada")
    
    args = parser.parse_args()
    
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    if not args.api_key:
        print("Error: Se requiere una API key de Gemini. Usa -k o configura GEMINI_API_KEY")
        sys.exit(1)
    
    try:
        processor = ImageProcessor(args.api_key)
        output_file = processor.process_image(args.source, args.output)
        
        print(f"\n✅ ¡Imagen procesada exitosamente!")
        print(f"📁 Archivo guardado: {output_file}")
        print(f"📱 Lista para Instagram: {output_file}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
