#!/bin/bash

# Script para probar la API actualizada en producción
# Uso: ./test_production_api.sh

echo "🧪 Probando API actualizada en producción..."

BASE_URL="http://thumbnail.shortenqr.com:8088"
API_KEY="AIzaSyCiQgx31nbA6f6nCrGksIfPn6EmcOkH9pw"
TEST_IMAGE="https://media.biobiochile.cl/wp-content/uploads/2025/10/dahbia-benkired-caso.png"
OUTPUT_FILE="test_urls_production.jpg"

echo "1️⃣ Verificando health check..."
curl -s -X GET "$BASE_URL/health" | python3 -m json.tool
echo ""

echo "2️⃣ Probando análisis con URLs públicas..."
RESPONSE=$(curl -s -X POST "$BASE_URL/analyze-url" \
  -H "Content-Type: application/json" \
  -d "{
    \"url\": \"$TEST_IMAGE\",
    \"api_key\": \"$API_KEY\",
    \"output_filename\": \"$OUTPUT_FILE\"
  }")

echo "$RESPONSE" | python3 -m json.tool
echo ""

echo "3️⃣ Extrayendo URLs de la respuesta..."
DOWNLOAD_URL=$(echo "$RESPONSE" | python3 -c "import sys, json; data=json.load(sys.stdin); print(data.get('download_url', 'No encontrado'))")
VIEW_URL=$(echo "$RESPONSE" | python3 -c "import sys, json; data=json.load(sys.stdin); print(data.get('view_url', 'No encontrado'))")

echo "📥 Download URL: $DOWNLOAD_URL"
echo "👁️  View URL: $VIEW_URL"
echo ""

echo "4️⃣ Probando descarga..."
curl -I "$DOWNLOAD_URL"
echo ""

echo "5️⃣ Probando visualización..."
curl -I "$VIEW_URL"
echo ""

echo "6️⃣ Verificando información de modelos..."
curl -s -X GET "$BASE_URL/models" | python3 -m json.tool
echo ""

echo "7️⃣ Verificando reglas de corte..."
curl -s -X GET "$BASE_URL/rules" | python3 -m json.tool
echo ""

echo "✅ Pruebas completadas!"
echo ""
echo "🌐 URLs disponibles:"
echo "   • API Principal: $BASE_URL/"
echo "   • Documentación: $BASE_URL/docs"
echo "   • Health Check: $BASE_URL/health"
echo "   • Descargar imagen: $DOWNLOAD_URL"
echo "   • Ver imagen: $VIEW_URL"
