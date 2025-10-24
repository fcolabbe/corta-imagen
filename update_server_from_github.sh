#!/bin/bash

# Script para actualizar el servidor desde GitHub
# Uso: ./update_server_from_github.sh

echo "🚀 Actualizando servidor desde GitHub..."

# Configuración
SERVER="thumbnail.shortenqr.com"
REPO_URL="https://github.com/fcolabbe/corta-imagen.git"
API_DIR="/var/www/instagram-cropper"

echo "📡 Conectando al servidor de producción..."

# Actualizar desde GitHub
ssh -o StrictHostKeyChecking=no root@$SERVER << EOF
echo "📁 Actualizando código desde GitHub..."
cd $API_DIR

# Hacer backup del api.py actual
cp api.py api.py.backup.\$(date +%Y%m%d_%H%M%S)

# Actualizar desde GitHub
git pull origin main

echo "🔄 Reiniciando servicio API..."
docker-compose restart api

echo "⏳ Esperando que el servicio se inicie..."
sleep 5

echo "📋 Verificando estado del servicio..."
docker-compose ps

echo "📋 Últimos logs del servicio:"
docker-compose logs --tail=15 api

echo "✅ Actualización completada!"
EOF

echo ""
echo "🌐 URLs disponibles:"
echo "   • API Principal: http://thumbnail.shortenqr.com:8088/"
echo "   • Documentación: http://thumbnail.shortenqr.com:8088/docs"
echo "   • Health Check: http://thumbnail.shortenqr.com:8088/health"
echo ""
echo "📱 Nuevas funcionalidades:"
echo "   • download_url: Enlace para descargar imagen"
echo "   • view_url: Enlace para ver imagen en navegador"
echo ""
echo "🧪 Prueba la nueva funcionalidad:"
echo "curl -X POST 'http://thumbnail.shortenqr.com:8088/analyze-url' \\"
echo "  -H 'Content-Type: application/json' \\"
echo "  -d '{\"url\": \"https://ejemplo.com/imagen.jpg\", \"api_key\": \"TU_API_KEY\"}'"
