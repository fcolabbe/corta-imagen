#!/bin/bash

# Script para actualizar la API en producción con URLs públicas
# Uso: ./update_production.sh

echo "🚀 Actualizando API de Instagram Image Cropper en producción..."

# Configuración
SERVER="thumbnail.shortenqr.com"
API_DIR="/var/www/instagram-cropper"
SERVICE_NAME="instagram-cropper-api"

echo "📡 Conectando al servidor de producción..."

# Crear directorio si no existe
ssh root@$SERVER "mkdir -p $API_DIR"

# Copiar archivos actualizados
echo "📁 Copiando archivos actualizados..."
scp api.py root@$SERVER:$API_DIR/
scp requirements.txt root@$SERVER:$API_DIR/
scp Dockerfile root@$SERVER:$API_DIR/
scp docker-compose.yml root@$SERVER:$API_DIR/
scp nginx.conf root@$SERVER:$API_DIR/

# Reiniciar servicios en producción
echo "🔄 Reiniciando servicios..."
ssh root@$SERVER << 'EOF'
cd /var/www/instagram-cropper

# Detener servicios actuales
docker-compose down

# Reconstruir y levantar servicios
docker-compose up --build -d

# Verificar que los servicios estén funcionando
sleep 5
docker-compose ps

# Verificar logs
echo "📋 Últimos logs del servicio:"
docker-compose logs --tail=20 api
EOF

echo "✅ Actualización completada!"
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
