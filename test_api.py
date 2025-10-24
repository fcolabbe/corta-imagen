#!/usr/bin/env python3
"""
Cliente de ejemplo para probar la API de Instagram Image Cropper
"""

import requests
import json
import time

# Configuración de la API
API_BASE_URL = "http://localhost:8000"
API_KEY = "AIzaSyCiQgx31nbA6f6nCrGksIfPn6EmcOkH9pw"  # Tu API key

def test_health():
    """Probar endpoint de salud"""
    print("🔍 Probando endpoint de salud...")
    response = requests.get(f"{API_BASE_URL}/health")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    print()

def test_analyze_url():
    """Probar análisis desde URL"""
    print("🔍 Probando análisis desde URL...")
    
    url = "https://media.biobiochile.cl/wp-content/uploads/2025/10/acusacion-constitucional-diego-pardow.png"
    
    payload = {
        "url": url,
        "api_key": API_KEY,
        "output_filename": "test_api_pardow.jpg"
    }
    
    response = requests.post(f"{API_BASE_URL}/analyze-url", json=payload)
    
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        result = response.json()
        print(f"Success: {result['success']}")
        print(f"Message: {result['message']}")
        print(f"Processing time: {result['processing_time']}s")
        print(f"Output file: {result['output_file']}")
        print(f"Crop coordinates: {result['crop_coordinates']}")
        print(f"Analysis: {json.dumps(result['analysis'], indent=2)}")
    else:
        print(f"Error: {response.text}")
    print()

def test_get_models():
    """Probar endpoint de modelos"""
    print("🔍 Probando endpoint de modelos...")
    response = requests.get(f"{API_BASE_URL}/models")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    print()

def test_get_rules():
    """Probar endpoint de reglas"""
    print("🔍 Probando endpoint de reglas...")
    response = requests.get(f"{API_BASE_URL}/rules")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    print()

def test_download():
    """Probar descarga de imagen"""
    print("🔍 Probando descarga de imagen...")
    response = requests.get(f"{API_BASE_URL}/download/test_api_pardow.jpg")
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        print(f"Content-Type: {response.headers.get('content-type')}")
        print(f"Content-Length: {len(response.content)} bytes")
        # Guardar imagen
        with open("downloaded_image.jpg", "wb") as f:
            f.write(response.content)
        print("✅ Imagen descargada como 'downloaded_image.jpg'")
    else:
        print(f"Error: {response.text}")
    print()

if __name__ == "__main__":
    print("🚀 Cliente de prueba para Instagram Image Cropper API")
    print("=" * 60)
    
    try:
        # Probar endpoints
        test_health()
        test_get_models()
        test_get_rules()
        test_analyze_url()
        test_download()
        
        print("✅ Todas las pruebas completadas")
        
    except requests.exceptions.ConnectionError:
        print("❌ Error: No se puede conectar a la API")
        print("   Asegúrate de que la API esté ejecutándose en http://localhost:8000")
        print("   Ejecuta: ./start_api.sh")
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
