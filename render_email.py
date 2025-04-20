from mjml import mjml2html
from jinja2 import Environment, FileSystemLoader
import os
import smtplib
import base64
import mimetypes
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Credenciales y configuración SMTP (¡Usa variables de entorno o un gestor de secretos en producción!)
GMAIL_SERVER = os.getenv('GMAIL_SERVER')
GMAIL_PORT = os.getenv('GMAIL_PORT')
GMAIL_SENDER_EMAIL = os.getenv('GMAIL_SENDER_EMAIL')
GMAIL_APP_PASSWORD = os.getenv('GMAIL_APP_PASSWORD')
EMAIL_RECEIVER = os.getenv('EMAIL_RECEIVER')


def attach_image(msg, image_path, content_id):
    """
    Adjunta una imagen al mensaje con el Content-ID especificado.
    
    Args:
        msg: Objeto MIMEMultipart al que adjuntar la imagen
        image_path: Ruta al archivo de imagen
        content_id: Identificador para referenciar la imagen en el HTML (sin los brackets)
    
    Returns:
        bool: True si se adjuntó correctamente, False si hubo un error
    """
    try:
        with open(image_path, 'rb') as img:
            # Determinar el tipo MIME
            mime_type, _ = mimetypes.guess_type(image_path)
            if not mime_type:
                # Si no se puede determinar, intentar basado en la extensión
                ext = os.path.splitext(image_path)[1].lower()
                if ext == '.png':
                    mime_type = 'image/png'
                elif ext in ['.jpg', '.jpeg']:
                    mime_type = 'image/jpeg'
                elif ext == '.gif':
                    mime_type = 'image/gif'
                else:
                    mime_type = 'application/octet-stream'
            
            # Crear la parte de la imagen
            mime_subtype = mime_type.split('/')[1] if '/' in mime_type else 'png'
            mime_img = MIMEImage(img.read(), _subtype=mime_subtype)
            
            # Añadir headers necesarios
            mime_img.add_header('Content-ID', f'<{content_id}>')
            mime_img.add_header('Content-Disposition', 'inline', filename=os.path.basename(image_path))
            
            # Adjuntar al mensaje
            msg.attach(mime_img)
            return True
    except FileNotFoundError:
        print(f"Error: No se encontró el archivo de imagen {image_path}")
        return False
    except Exception as e:
        print(f"Error al adjuntar la imagen {image_path}: {e}")
        return False

def send_email_with_images(recipient_email, subject, html_content, images=None):
    """
    Envía un correo electrónico HTML con imágenes adjuntas usando CID.
    
    Args:
        recipient_email: Email del destinatario
        subject: Asunto del correo
        html_content: Contenido HTML del correo
        images: Diccionario con CID como clave y ruta de la imagen como valor
               Ejemplo: {'logo': 'img/logo.png', 'banner': 'img/banner.jpg'}
    
    Returns:
        bool: True si el envío fue exitoso, False en caso contrario
    """
    # Crear mensaje
    msg = MIMEMultipart('related')  # Usamos 'related' para imágenes CID
    msg['Subject'] = subject
    msg['From'] = GMAIL_SENDER_EMAIL
    msg['To'] = recipient_email
    
    # Crear la parte HTML
    html_part = MIMEText(html_content, 'html')
    msg.attach(html_part)
    
    # Adjuntar imágenes con Content-ID
    if images:
        for cid, img_path in images.items():
            attach_image(msg, img_path, cid)
    
    try:
        # Conectar al servidor SMTP
        server = smtplib.SMTP(GMAIL_SERVER, GMAIL_PORT)
        server.ehlo()
        server.starttls()
        server.ehlo()
        server.login(GMAIL_SENDER_EMAIL, GMAIL_APP_PASSWORD)
        
        # Enviar correo (spliteamos múltiples destinatarios si es necesario)
        recipients_list = [email.strip() for email in recipient_email.split(',')]
        server.sendmail(GMAIL_SENDER_EMAIL, recipients_list, msg.as_string())
        server.quit()
        print(f"Correo enviado exitosamente a {recipient_email}")
        return True
    except smtplib.SMTPAuthenticationError:
        print("Error de autenticación SMTP. Verifica el correo y la contraseña de aplicación.")
        return False
    except Exception as e:
        print(f"Error al enviar el correo: {e}")
        return False

def render_and_send_email(template_file, context, recipient, subject, images):
    """
    Renderiza una plantilla MJML, la compila a HTML y envía el correo.
    
    Args:
        template_file: Nombre del archivo de plantilla MJML
        context: Diccionario con los datos para la plantilla
        recipient: Email del destinatario
        subject: Asunto del correo
        images: Diccionario con CID como clave y ruta de la imagen como valor
    """
    # 1. Configurar Jinja2
    template_dir = os.path.dirname(__file__)
    env = Environment(loader=FileSystemLoader(template_dir))
    template = env.get_template(template_file)
    
    # 2. Renderizar la plantilla MJML con los datos
    rendered_mjml = template.render(context)
    
    # 3. Compilar el MJML renderizado a HTML
    try:
        html_output = mjml2html(rendered_mjml)
        
        # 4. Guardar HTML (opcional)
        output_file = f"output_{template_file.replace('.mjml', '.html')}"
        with open(output_file, 'w') as f:
            f.write(html_output)
        print(f"HTML guardado en '{output_file}'")
        
        # 5. Enviar el correo con las imágenes adjuntas
        if html_output:
            send_email_with_images(recipient, subject, html_output, images)
        else:
            print("No se envió el correo porque falló la compilación MJML.")
            
    except Exception as e:
        print(f"Error al compilar MJML a HTML: {e}")
        print("\n--- Rendered MJML (compilation failed) ---")
        print(rendered_mjml)

# --- Flujo Principal ---
if __name__ == "__main__":
    # Datos para las plantillas
    contexto = {
        'nombre_cliente': 'Carlos Pérez',
        'link_servicios': 'https://ejemplo.com/lavanderia-servicios'
    }
    
    # Definir destinatario
    recipient = EMAIL_RECEIVER
    
    # ---------------------------------------------------
    # Ejemplo 1: Plantilla Original (email_template.mjml)
    # ---------------------------------------------------
    # print("\n=== Enviando correo con la plantilla original ===")
    
    # # Configurar imágenes para la plantilla original
    # images_original = {
    #     'logo': 'img/image.png',
    #     'banner': 'img/image.png'
    # }
    
    # # Renderizar y enviar la plantilla original
    # render_and_send_email(
    #     template_file='email_template.mjml',
    #     context=contexto,
    #     recipient=recipient,
    #     subject="¡Bienvenido a TuLavanderia! (Plantilla Original)",
    #     images=images_original
    # )
    
    # ---------------------------------------------------
    # Ejemplo 2: Segunda Plantilla (email_template_lavanderia.mjml)
    # ---------------------------------------------------
    print("\n=== Enviando correo con la segunda plantilla ===")
    
    # Configurar imágenes para la segunda plantilla
    images_lavanderia = {
        'logo-banner': 'img/image.png',  # Banner de cabecera
        'icon-lavanderia': 'img/image.png'  # Icono para la sección central
    }
    
    # Renderizar y enviar la segunda plantilla
    # render_and_send_email(
    #     template_file='email_template_lavanderia.mjml',
    #     context=contexto,
    #     recipient=recipient,
    #     subject="¡Bienvenido a TuLavanderia! (Segunda Plantilla)",
    #     images=images_lavanderia
    # )
    
    # # ---------------------------------------------------
    # # Ejemplo 3: Plantilla Premium (email_template_premium.mjml)
    # # ---------------------------------------------------
    print("\n=== Enviando correo con la plantilla premium ===")
    
    # Configurar imágenes para la plantilla premium
    images_premium = {
        'logo-premium': 'img/image.png',
        'header-top': 'img/image.png',
        'header-bottom': 'img/image.png',
        'premium-image1': 'img/image.png',
        'premium-image2': 'img/image.png',
        'mapa-ubicacion': 'img/image.png'
    }
    
    # Contexto extendido para la plantilla premium
    contexto_premium = contexto.copy()
    contexto_premium.update({
        'codigo_descuento': 'PREMIUM25',
        'porcentaje_descuento': '25%'
    })
    
    # Renderizar y enviar la plantilla premium
    render_and_send_email(
        template_file='email_template_premium.mjml',
        context=contexto_premium,
        recipient=recipient,
        subject="Nuevos servicios premium en TuLavanderia - 25% de descuento",
        images=images_premium
    )
