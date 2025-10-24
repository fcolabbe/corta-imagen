#!/usr/bin/env bash

# Script para iniciar la API de Instagram Image Cropper
echo "🚀 Iniciando Instagram Image Cropper API..."

# Verificar si Python está instalado
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 no está instalado. Por favor instala Python 3 primero."
    exit 1
fi

echo "✅ Python 3 encontrado"

# Instalar dependencias si es necesario
echo "📦 Verificando dependencias..."
pip install -r requirements.txt

# Configurar API key si está disponible
if [ -n "$GEMINI_API_KEY" ]; then
    echo "🔑 API key de Gemini configurada desde variable de entorno"
else
    echo "⚠️  Variable GEMINI_API_KEY no configurada"
    echo "   Los usuarios deberán proporcionar su API key en cada request"
fi

echo ""
echo "🌐 Iniciando servidor API..."
echo "📖 Documentación disponible en: http://localhost:8000/docs"
echo "🔧 Interfaz alternativa en: http://localhost:8000/redoc"
echo ""
echo "📋 Endpoints disponibles:"
echo "   POST /analyze-url     - Procesar imagen desde URL"
echo "   POST /analyze-file    - Procesar imagen desde archivo"
echo "   GET  /download/{file} - Descargar imagen procesada"
echo "   GET  /health          - Verificar estado de la API"
echo "   GET  /models          - Información de modelos"
echo "   GET  /rules           - Reglas de corte"
echo ""

# Iniciar la API
python3 api.py
