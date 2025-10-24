# 🚀 Guía de Despliegue - thumbnail.shortenqr.com:8088

## 📋 Pasos para Subir a GitHub

### 1. Crear Repositorio en GitHub
```bash
# Ve a https://github.com y crea un nuevo repositorio llamado "corta-imagen"
# O usa GitHub CLI:
gh repo create corta-imagen --public --description "Instagram Image Cropper with Gemini AI"
```

### 2. Subir Código a GitHub
```bash
# Agregar remote origin (reemplaza 'tu-usuario' con tu usuario de GitHub)
git remote add origin https://github.com/tu-usuario/corta-imagen.git

# Subir código
git branch -M main
git push -u origin main
```

## 🌐 Despliegue en thumbnail.shortenqr.com:8088

### Opción 1: Despliegue Manual (Recomendado)

#### 1. Conectar al Servidor
```bash
ssh usuario@thumbnail.shortenqr.com
```

#### 2. Ejecutar Script de Despliegue
```bash
# Descargar y ejecutar script de despliegue
curl -O https://raw.githubusercontent.com/tu-usuario/corta-imagen/main/deploy.sh
chmod +x deploy.sh
sudo ./deploy.sh
```

#### 3. Verificar Despliegue
```bash
# Verificar estado del servicio
sudo systemctl status instagram-cropper-api

# Ver logs
sudo journalctl -u instagram-cropper-api -f

# Probar API
curl http://localhost:8088/health
```

### Opción 2: Despliegue con Docker

#### 1. Instalar Docker en el Servidor
```bash
# Ubuntu/Debian
sudo apt update
sudo apt install docker.io docker-compose
sudo systemctl start docker
sudo systemctl enable docker
```

#### 2. Clonar Repositorio
```bash
git clone https://github.com/tu-usuario/corta-imagen.git
cd corta-imagen
```

#### 3. Ejecutar con Docker Compose
```bash
# Construir y ejecutar
docker-compose up -d --build

# Verificar estado
docker-compose ps
docker-compose logs -f
```

## 🔧 Configuración de Dominio

### 1. Configurar DNS
```
# En tu proveedor de DNS, agregar:
A     thumbnail.shortenqr.com    → IP_DEL_SERVIDOR
```

### 2. Configurar Nginx (si usas despliegue manual)
```bash
# El script deploy.sh ya configura Nginx automáticamente
# Verificar configuración:
sudo nginx -t
sudo systemctl reload nginx
```

### 3. Configurar SSL (Opcional)
```bash
# Instalar Certbot
sudo apt install certbot python3-certbot-nginx

# Obtener certificado SSL
sudo certbot --nginx -d thumbnail.shortenqr.com
```

## 📊 Monitoreo y Mantenimiento

### Comandos Útiles
```bash
# Ver estado del servicio
sudo systemctl status instagram-cropper-api

# Reiniciar servicio
sudo systemctl restart instagram-cropper-api

# Ver logs en tiempo real
sudo journalctl -u instagram-cropper-api -f

# Verificar puerto
sudo netstat -tlnp | grep 8088

# Probar API
curl http://thumbnail.shortenqr.com:8088/health
```

### Limpieza de Archivos
```bash
# El servicio limpia automáticamente archivos antiguos
# Para limpieza manual:
sudo find /var/www/instagram-cropper/outputs -name "*.jpg" -mtime +7 -delete
```

## 🔒 Seguridad

### Firewall
```bash
# Permitir solo puertos necesarios
sudo ufw allow 22/tcp    # SSH
sudo ufw allow 80/tcp    # HTTP
sudo ufw allow 443/tcp   # HTTPS (si usas SSL)
sudo ufw allow 8088/tcp  # API (opcional, solo si acceso directo)
sudo ufw enable
```

### Actualizaciones
```bash
# Actualizar aplicación
cd /var/www/instagram-cropper
sudo -u www-data git pull origin main
sudo systemctl restart instagram-cropper-api
```

## 📱 URLs de Acceso

Una vez desplegado, la API estará disponible en:

- **API Principal**: http://thumbnail.shortenqr.com:8088
- **Documentación**: http://thumbnail.shortenqr.com:8088/docs
- **ReDoc**: http://thumbnail.shortenqr.com:8088/redoc
- **Health Check**: http://thumbnail.shortenqr.com:8088/health

## 🧪 Pruebas Post-Despliegue

```bash
# Probar endpoint de salud
curl http://thumbnail.shortenqr.com:8088/health

# Probar análisis de imagen
curl -X POST "http://thumbnail.shortenqr.com:8088/analyze-url" \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://picsum.photos/1200/800",
    "api_key": "tu_api_key_gemini",
    "output_filename": "test.jpg"
  }'
```

## 🆘 Solución de Problemas

### Servicio no inicia
```bash
# Ver logs detallados
sudo journalctl -u instagram-cropper-api -n 50

# Verificar dependencias
sudo -u www-data /var/www/instagram-cropper/venv/bin/python -c "import fastapi"
```

### Puerto ocupado
```bash
# Ver qué usa el puerto 8088
sudo lsof -i :8088

# Cambiar puerto en /etc/systemd/system/instagram-cropper-api.service
```

### Problemas de permisos
```bash
# Corregir permisos
sudo chown -R www-data:www-data /var/www/instagram-cropper
sudo chmod +x /var/www/instagram-cropper/venv/bin/uvicorn
```

---

**¡Tu API estará lista para procesar imágenes en thumbnail.shortenqr.com:8088!** 🚀✨
