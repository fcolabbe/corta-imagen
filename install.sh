#!/usr/bin/env bash

# Script de instalación para Cortador de Imágenes Instagram
echo "🖼️ Instalando Cortador de Imágenes para Instagram..."

# Verificar si Python está instalado
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 no está instalado. Por favor instala Python 3 primero."
    exit 1
fi

echo "✅ Python 3 encontrado"

# Crear entorno virtual
echo "📦 Creando entorno virtual..."
python3 -m venv venv

# Activar entorno virtual
echo "🔧 Activando entorno virtual..."
source venv/bin/activate

# Instalar dependencias
echo "📚 Instalando dependencias..."
pip install -r requirements.txt

echo ""
echo "🎉 ¡Instalación completada!"
echo ""
echo "📖 Para usar la aplicación:"
echo "1. Activa el entorno virtual: source venv/bin/activate"
echo "2. Ejecuta la interfaz gráfica: python gui.py"
echo "3. O usa la línea de comandos: python main.py <URL_IMAGEN>"
echo ""
echo "🔑 No olvides configurar tu API key de Gemini:"
echo "   export GEMINI_API_KEY='tu_api_key_aqui'"
echo ""
echo "📚 Lee el README.md para más información"
