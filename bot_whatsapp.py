from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

def iniciar_whatsapp():
    try:
        # Configurar el navegador con opciones adicionales
        options = webdriver.ChromeOptions()
        options.add_experimental_option("detach", True)
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-gpu')
        options.add_argument('--window-size=1920,1080')
        
        try:
            # Usar la versión más reciente de ChromeDriver
            print("Obteniendo la versión más reciente de ChromeDriver...")
            service = Service(ChromeDriverManager().install())
            print("¡ChromeDriver instalado correctamente!")
            
        except Exception as e:
            print(f"Error al instalar ChromeDriver: {str(e)}")
            print("\nVamos a intentar con la versión más reciente...")
            try:
                service = Service(ChromeDriverManager().install())
                print("¡Versión más reciente de ChromeDriver instalada correctamente!")
            except Exception as e2:
                print(f"Error con la versión más reciente: {str(e2)}")
                print("\nPor favor, descarga manualmente ChromeDriver:")
                print("1. Ve a: https://chromedriver.chromium.org/downloads")
                print("2. Descarga la versión 114.0.5735.90")
                print("3. Extrae el archivo y copia 'chromedriver.exe' a esta carpeta:")
                print("   C:\\Users\\VICTOR\\Desktop\\BOTwhatzap\\")
                print("\nPresiona Enter después de completar estos pasos...")
                input()
                service = Service('chromedriver.exe')
        
        # Iniciar el navegador
        driver = webdriver.Chrome(service=service, options=options)
        driver.get("https://web.whatsapp.com/")
        
        print("Por favor, escanea el código QR de WhatsApp Web...")
        # Esperar a que el usuario escanee el código QR
        input("Después de escanear el código QR, presiona Enter para continuar...")
        return driver
        
    except Exception as e:
        print(f"Error al iniciar el navegador: {str(e)}")
        print("\nSolución de problemas:")
        print("1. Asegúrate de tener Google Chrome instalado")
        print("2. Si usas Windows, asegúrate de tener los permisos necesarios")
        print("3. Intenta ejecutar el script como administrador")
        print("4. Verifica tu conexión a internet")
        input("Presiona Enter para salir...")
        exit()

def encontrar_cuadro_mensaje(driver):
    """
    Función para encontrar el cuadro de mensaje de WhatsApp Web.
    Devuelve el elemento del cuadro de mensaje si se encuentra, o None en caso contrario.
    """
    # Lista de estrategias para encontrar el cuadro de mensaje
    estrategias = [
        # Estrategia 1: Buscar por atributos específicos
        {
            'selector': '//div[@role="textbox"][@title="Escribe un mensaje" or @title="Type a message"]',
            'descripcion': 'Buscando por role=textbox y título...'
        },
        # Estrategia 2: Buscar en el footer del chat
        {
            'selector': '//footer//div[@contenteditable="true"]',
            'descripcion': 'Buscando en el footer del chat...'
        },
        # Estrategia 3: Buscar por clase específica
        {
            'selector': '//div[contains(@class, "_3Uu1_")]//div[@contenteditable="true"]',
            'descripcion': 'Buscando por clase _3Uu1_...'
        },
        # Estrategia 4: Buscar por data-tab
        {
            'selector': '//div[@contenteditable="true"][@data-tab="10"]',
            'descripcion': 'Buscando por data-tab="10"...'
        },
        # Estrategia 5: Usar JavaScript para encontrar el elemento
        {
            'javascript': """
                var elements = document.querySelectorAll('div[contenteditable="true"]');
                for (var i = 0; i < elements.length; i++) {
                    var style = window.getComputedStyle(elements[i]);
                    if (style.display !== 'none' && style.visibility !== 'hidden' && elements[i].offsetParent !== null) {
                        elements[i].focus();
                        return elements[i];
                    }
                }
                return null;
            """,
            'descripcion': 'Buscando con JavaScript...',
            'es_js': True
        }
    ]
    
    # Intentar cada estrategia
    for estrategia in estrategias:
        try:
            print(estrategia['descripcion'])
            
            if 'es_js' in estrategia and estrategia['es_js']:
                # Usar JavaScript para encontrar el elemento
                elemento = driver.execute_script(estrategia['javascript'])
                if elemento:
                    # Si se encontró con JS, devolver el elemento
                    return elemento
            else:
                # Usar el selector XPath
                elemento = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.XPATH, estrategia['selector']))
                )
                if elemento:
                    # Hacer clic para asegurar el foco
                    elemento.click()
                    time.sleep(0.0001)
                    return elemento
                    
        except Exception as e:
            print(f"  - No se pudo encontrar con esta estrategia: {str(e)}")
            continue
    
    print("No se pudo encontrar el cuadro de mensaje con ninguna estrategia.")
    return None

def enviar_mensajes(numero, mensajes):
    print("\n=== Iniciando el envío de mensajes ===")
    driver = iniciar_whatsapp()
    
    try:
        print(f"\nAbriendo chat con el número: {numero}")
        url = f"https://web.whatsapp.com/send?phone={numero}"
        driver.get(url)
        
        print("Esperando a que cargue la página de chat...")
        time.sleep(10)  # Tiempo para que cargue la página
        
        print("Buscando el cuadro de mensaje...")
        input_box = encontrar_cuadro_mensaje(driver)
        
        if not input_box:
            print("No se pudo encontrar el cuadro de mensaje. Tomando captura de pantalla...")
            driver.save_screenshot('error_whatsapp.png')
            print("Se ha guardado una captura de pantalla como 'error_whatsapp.png'")
            raise Exception("No se pudo encontrar el cuadro de mensaje en WhatsApp Web")
        
        # Enviar cada mensaje
        for i, mensaje in enumerate(mensajes, 1):
            try:
                print(f"\nEnviando mensaje {i} de {len(mensajes)}...")
                
                # Asegurarse de que el cuadro de mensaje esté listo
                input_box = encontrar_cuadro_mensaje(driver)
                if not input_box:
                    raise Exception("No se pudo encontrar el cuadro de mensaje")
                
                # Hacer clic en el cuadro de texto para asegurar que está enfocado
                input_box.click()
                time.sleep(0.01)
                
                # Limpiar cualquier texto existente
                input_box.clear()
                time.sleep(0.01)
                
                # Escribir todo el mensaje de una vez (máxima velocidad)
                input_box.send_keys(mensaje)
                time.sleep(0.05)  # Mínima pausa para asegurar el envío
                
                # Intentar enviar el mensaje (usar Enter o el botón de enviar)
                try:
                    # Intentar con Enter
                    input_box.send_keys(Keys.RETURN)
                    print("  Mensaje enviado con Enter")
                except Exception as e:
                    print(f"  - No se pudo enviar con Enter. Error: {str(e)}")
                    
                    # Si falla, intentar con el botón de enviar
                    try:
                        send_button = WebDriverWait(driver, 5).until(
                            EC.element_to_be_clickable((By.XPATH, '//span[@data-icon="send"]'))
                        )
                        send_button.click()
                        print("  Mensaje enviado con el botón de enviar")
                    except Exception as e2:
                        print(f"  - No se pudo enviar con el botón. Error: {str(e2)}")
                        
                        # Si todo falla, intentar con JavaScript
                        try:
                            driver.execute_script("""
                                var elements = document.querySelectorAll('span[data-icon="send"]');
                                if (elements.length > 0) {
                                    elements[0].click();
                                    return true;
                                }
                                return false;
                            """)
                            print("  Mensaje enviado con JavaScript")
                        except Exception as e3:
                            print(f"  - No se pudo enviar con JavaScript. Error: {str(e3)}")
                            raise Exception("No se pudo enviar el mensaje con ningún método")
                
                # Esperar un momento entre mensajes
                time.sleep(0.01)
                
            except Exception as e:
                print(f"Error al enviar el mensaje {i}: {str(e)}")
                print("Reintentando en 2 segundos...")
                time.sleep(0.5)  # Tiempo mínimo de espera antes de reintentar
                continue
        
        print("\n=== Proceso completado ===")
        print("¡Mensajes enviados exitosamente!")
        
    except Exception as e:
        print("\n=== Ocurrió un error crítico ===")
        print(f"Tipo de error: {type(e).__name__}")
        print(f"Mensaje: {str(e)}")
        print("\nPosibles soluciones:")
        print("1. Verifica la conexión a internet")
        print("2. Asegúrate de que el número sea válido y tenga WhatsApp")
        print("3. Intenta nuevamente")
    
    finally:
        print("\nEl navegador se cerrará en 30 segundos...")
        time.sleep(30)
        try:
            driver.quit()
            print("Navegador cerrado.")
        except:
            print("No se pudo cerrar el navegador correctamente.")

if __name__ == "__main__":
    # Ejemplo de uso
    numero = input("Ingresa el número de teléfono con código de país (ej. 521234567890): ")
    cantidad = int(input("¿Cuántos mensajes quieres enviar?: "))
    
    mensajes = []
    print("Escribe el mensaje que quieres enviar (presiona Enter después de cada mensaje, escribe 'listo' para terminar):")
    
    while len(mensajes) < cantidad:
        mensaje = input(f"Mensaje {len(mensajes) + 1}: ")
        if mensaje.lower() == 'listo':
            break
        mensajes.append(mensaje)
    
    # Si no se ingresaron mensajes, usar uno por defecto
    if not mensajes:
        mensajes = ["Hola, este es un mensaje de prueba."] * cantidad
    
    # Asegurarse de que haya la cantidad correcta de mensajes
    if len(mensajes) < cantidad:
        mensajes = mensajes * (cantidad // len(mensajes) + 1)
        mensajes = mensajes[:cantidad]
    
    enviar_mensajes(numero, mensajes)
