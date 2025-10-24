#!/usr/bin/env bash

# Script de despliegue para producción en thumbnail.shortenqr.com:8088
# Ejecutar en el servidor de producción

echo "🚀 Desplegando Instagram Image Cropper en thumbnail.shortenqr.com:8088"

# Variables de configuración
APP_NAME="instagram-cropper"
APP_DIR="/var/www/$APP_NAME"
SERVICE_NAME="instagram-cropper-api"
USER="www-data"
GROUP="www-data"

# Crear directorio de la aplicación
echo "📁 Creando directorio de la aplicación..."
sudo mkdir -p $APP_DIR
sudo chown $USER:$GROUP $APP_DIR

# Clonar o actualizar el repositorio
echo "📥 Clonando/actualizando código..."
if [ -d "$APP_DIR/.git" ]; then
    cd $APP_DIR
    sudo -u $USER git pull origin main
else
    sudo -u $USER git clone https://github.com/tu-usuario/corta-imagen.git $APP_DIR
fi

# Crear entorno virtual
echo "🐍 Configurando entorno virtual..."
cd $APP_DIR
sudo -u $USER python3 -m venv venv
sudo -u $USER ./venv/bin/pip install -r requirements.txt

# Crear directorios necesarios
echo "📂 Creando directorios..."
sudo mkdir -p /var/log/$APP_NAME
sudo mkdir -p /var/www/$APP_NAME/outputs
sudo mkdir -p /tmp/$APP_NAME
sudo chown -R $USER:$GROUP /var/log/$APP_NAME
sudo chown -R $USER:$GROUP /var/www/$APP_NAME/outputs
sudo chown -R $USER:$GROUP /tmp/$APP_NAME

# Crear archivo de configuración de producción
echo "⚙️ Configurando variables de entorno..."
sudo -u $USER cp production.env .env

# Crear servicio systemd
echo "🔧 Configurando servicio systemd..."
sudo tee /etc/systemd/system/$SERVICE_NAME.service > /dev/null <<EOF
[Unit]
Description=Instagram Image Cropper API
After=network.target

[Service]
Type=exec
User=$USER
Group=$GROUP
WorkingDirectory=$APP_DIR
Environment=PATH=$APP_DIR/venv/bin
ExecStart=$APP_DIR/venv/bin/uvicorn api:app --host 0.0.0.0 --port 8088 --workers 4
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

# Recargar systemd y habilitar servicio
echo "🔄 Configurando servicio..."
sudo systemctl daemon-reload
sudo systemctl enable $SERVICE_NAME
sudo systemctl start $SERVICE_NAME

# Configurar Nginx (opcional, para proxy reverso)
echo "🌐 Configurando Nginx..."
sudo tee /etc/nginx/sites-available/$APP_NAME > /dev/null <<EOF
server {
    listen 80;
    server_name thumbnail.shortenqr.com;

    location / {
        proxy_pass http://127.0.0.1:8088;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
        
        # Configuración para archivos grandes
        client_max_body_size 10M;
        proxy_read_timeout 300s;
        proxy_connect_timeout 75s;
    }
}
EOF

# Habilitar sitio en Nginx
sudo ln -sf /etc/nginx/sites-available/$APP_NAME /etc/nginx/sites-enabled/
sudo nginx -t && sudo systemctl reload nginx

# Configurar firewall (si es necesario)
echo "🔥 Configurando firewall..."
sudo ufw allow 8088/tcp comment "Instagram Cropper API"

# Verificar estado del servicio
echo "✅ Verificando despliegue..."
sleep 5
sudo systemctl status $SERVICE_NAME --no-pager

echo ""
echo "🎉 ¡Despliegue completado!"
echo "📖 API disponible en: http://thumbnail.shortenqr.com:8088"
echo "📚 Documentación: http://thumbnail.shortenqr.com:8088/docs"
echo "🔧 Estado del servicio: sudo systemctl status $SERVICE_NAME"
echo "📋 Logs: sudo journalctl -u $SERVICE_NAME -f"
