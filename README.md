# 🤖 Bot de WhatsApp Automatizado

Un bot de WhatsApp desarrollado en Python que permite el envío automatizado de mensajes a través de WhatsApp Web.

## 🚀 Características

- Envío masivo de mensajes a múltiples contactos
- Soporte para mensajes largos
- Interfaz de línea de comandos fácil de usar
- Configuración personalizable de tiempos de espera
- Múltiples métodos de envío (Enter, botón de enviar, JavaScript)
- Detección inteligente del cuadro de mensaje
- Manejo de errores robusto

## 📋 Requisitos

- Python 3.7 o superior
- Navegador Chrome o Edge instalado
- Conexión a Internet estable
- Cuenta de WhatsApp activa

## 🛠 Instalación

1. Clona el repositorio:
   ```bash
   git clone https://github.com/tuusuario/bot-whatsapp.git
   cd bot-whatsapp
   ```

2. Crea un entorno virtual (recomendado):
   ```bash
   python -m venv venv
   venv\Scripts\activate  # Windows
   source venv/bin/activate  # Linux/Mac
   ```

3. Instala las dependencias:
   ```bash
   pip install -r requirements.txt
   ```

## 🚦 Uso

1. Ejecuta el script principal:
   ```bash
   python bot_whatsapp.py
   ```

2. Sigue las instrucciones en pantalla para:
   - Ingresar el número de teléfono (con código de país, sin espacios ni caracteres especiales)
   - Ingresar los mensajes a enviar (pueden ser múltiples)

3. Escanea el código QR con tu teléfono cuando se solicite

4. ¡Listo! El bot comenzará a enviar los mensajes automáticamente.

## ⚙️ Configuración

Puedes ajustar los tiempos de espera en el archivo `bot_whatsapp.py` modificando las variables de tiempo en la función `enviar_mensajes`.

## ⚠️ Advertencia

- Este bot es solo para uso educativo y de pruebas.
- El uso excesivo puede resultar en la restricción temporal de tu cuenta de WhatsApp.
- No nos hacemos responsables del mal uso de esta herramienta.

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo [LICENSE](LICENSE) para más detalles.

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Por favor, abre un issue primero para discutir los cambios que te gustaría hacer.

## 📧 Contacto

¿Preguntas o sugerencias? ¡Siéntete libre de contactarme!
