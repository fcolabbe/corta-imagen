#!/bin/bash

# Script simple para actualizar solo api.py en producción
echo "🚀 Actualizando api.py en producción..."

# Configuración
SERVER="thumbnail.shortenqr.com"
API_DIR="/var/www/instagram-cropper"

echo "📁 Copiando api.py actualizado..."
scp -o StrictHostKeyChecking=no api.py root@$SERVER:$API_DIR/

echo "🔄 Reiniciando servicio API..."
ssh -o StrictHostKeyChecking=no root@$SERVER << 'EOF'
cd /var/www/instagram-cropper
docker-compose restart api
sleep 3
docker-compose logs --tail=10 api
EOF

echo "✅ Actualización completada!"
echo ""
echo "🧪 Prueba la nueva funcionalidad:"
echo "curl -X POST 'http://thumbnail.shortenqr.com:8088/analyze-url' \\"
echo "  -H 'Content-Type: application/json' \\"
echo "  -d '{\"url\": \"https://ejemplo.com/imagen.jpg\", \"api_key\": \"TU_API_KEY\"}'"
