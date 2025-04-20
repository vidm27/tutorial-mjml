# Ejemplo de Plantillas de Correo con MJML y Jinja2

Este proyecto demuestra cómo crear plantillas de correo electrónico HTML responsivas utilizando MJML y cómo personalizarlas con parámetros dinámicos usando Jinja2.

## Características

- Creación de plantillas de correo con MJML (responsive por defecto)
- Personalización de plantillas con parámetros usando Jinja2
- Renderizado de plantillas a HTML
- Manejo automático de rutas de imágenes para correcta visualización en correos
- Soporte para imágenes incrustadas como CID (Content-ID) para visualización en clientes de correo
- Envío de correos electrónicos con el contenido HTML generado
- Múltiples diseños de plantillas para diferentes casos de uso (estándar, lavandería, premium)
- Configuración mediante variables de entorno (.env)

## Requisitos

- Python 3.6+
- Paquetes de Python:
  - mjml (`pip install mjml`)
  - jinja2 (`pip install jinja2`)
  - python-dotenv (`pip install python-dotenv`)

## Estructura del Proyecto

- `email_template.mjml`: Plantilla de correo básica en formato MJML con variables Jinja2
- `email_template_lavanderia.mjml`: Plantilla especializada para un servicio de lavandería
- `email_template_premium.mjml`: Plantilla con diseño premium y más elementos visuales
- `render_email.py`: Funciones para renderizar plantillas y enviar correos
- `output_email_template.html`: HTML generado a partir de la plantilla básica
- `output_email_template_lavanderia.html`: HTML generado a partir de la plantilla de lavandería
- `output_email_template_premium.html`: HTML generado a partir de la plantilla premium
- `img/`: Directorio para imágenes utilizadas en las plantillas
- `pyproject.toml`: Configuración de dependencias del proyecto
- `.env`: Archivo para configuración de variables de entorno (no incluido en el repositorio)

## Configuración de Variables de Entorno

Crea un archivo `.env` en la raíz del proyecto con las siguientes variables:

```
GMAIL_SERVER=smtp.gmail.com
GMAIL_PORT=587
GMAIL_SENDER_EMAIL=tu_correo@gmail.com
GMAIL_APP_PASSWORD=tu_contraseña_o_clave_de_aplicación
EMAIL_RECEIVER=destinatario@ejemplo.com
```

## Uso Básico

### 1. Renderizar y Enviar una Plantilla

El proyecto incluye la función `render_and_send_email` que realiza todo el proceso:

```python
from render_email import render_and_send_email

# Datos para personalizar la plantilla
contexto = {
    'nombre_cliente': 'Ana García',
    'link_servicios': 'https://ejemplo.com/servicios'
}

# Configurar imágenes para la plantilla
images = {
    'logo': 'img/logo.png',
    'banner': 'img/banner.jpg'
}

# Renderizar y enviar la plantilla
render_and_send_email(
    template_file='email_template.mjml',
    context=contexto,
    recipient='destinatario@ejemplo.com',
    subject='Bienvenido a Nuestro Servicio',
    images=images
)
```

### 2. Enviar un Correo con Imágenes CID (Content-ID)

Para enviar imágenes que se visualizan correctamente en clientes de correo:

```python
from render_email import send_email_with_images

# Configurar imágenes con sus CID
imagenes = {
    'logo': 'img/logo.png',  # Se referencia en el HTML como <img src="cid:logo">
    'banner': 'img/banner.jpg'
}

# Enviar el correo con las imágenes adjuntas
send_email_with_images(
    recipient_email="destinatario@ejemplo.com",
    subject="Bienvenido a Nuestro Servicio",
    html_content=html_content,
    images=imagenes
)
```

## Personalización de Plantillas

### Variables en la Plantilla MJML

En el archivo MJML, puedes incluir variables de Jinja2 usando la sintaxis `{{ nombre_variable }}`:

```html
<mj-text>
  ¡Hola {{ nombre_cliente }}! Gracias por registrarte.
</mj-text>

<mj-button href="{{ link_servicios }}">
  Ver Nuestros Servicios
</mj-button>
```

### Pasar Variables a la Plantilla

Cuando llamas a la función `render_and_send_email`, pasa un diccionario con los valores para las variables:

```python
contexto = {
    'nombre_cliente': 'Juan Pérez',
    'link_servicios': 'https://miservicio.com/ofertas-especiales'
}
```

### Plantillas Disponibles

#### 1. Plantilla Básica (email_template.mjml)

Plantilla simple con un diseño básico para correos generales.

#### 2. Plantilla de Lavandería (email_template_lavanderia.mjml)

Diseño específico para un servicio de lavandería, con secciones para promociones y servicios.

#### 3. Plantilla Premium (email_template_premium.mjml)

Diseño avanzado con múltiples secciones, imágenes destacadas y promociones. Incluye variables adicionales como:

```python
contexto_premium = {
    'nombre_cliente': 'Juan Pérez',
    'link_servicios': 'https://miservicio.com/ofertas-especiales',
    'codigo_descuento': 'PREMIUM25',
    'porcentaje_descuento': '25%'
}
```

### Manejo de Imágenes en Correos Electrónicos

Un problema común al enviar correos HTML es que las imágenes no se muestran correctamente porque los clientes de correo no tienen acceso a las rutas de imágenes.

#### Uso de Imágenes CID (Content-ID)

El proyecto utiliza el enfoque CID para adjuntar imágenes que se muestran correctamente en clientes de correo:

1. En la plantilla HTML, referenciar las imágenes con `cid:`:

```html
<img src="cid:logo" alt="Logo">
```

2. Al enviar el correo, proporcionar un diccionario con los CID y rutas de las imágenes:

```python
imagenes = {
    'logo': 'img/logo.png',
    'banner': 'img/banner.jpg'
}
```

La función `send_email_with_images` se encargará de adjuntar las imágenes con los Content-ID correctos.

## Ejecutar el Proyecto

Para ejecutar el proyecto y enviar correos, simplemente ejecuta el archivo `render_email.py`:

```bash
python render_email.py
```

El script por defecto enviará la plantilla premium al destinatario configurado en el archivo `.env`.

## Notas para Gmail

Si utilizas Gmail para enviar correos, necesitarás:

1. Habilitar la verificación en dos pasos para tu cuenta de Google
2. Crear una "contraseña de aplicación" específica para la aplicación
3. Usar esa contraseña en la variable `GMAIL_APP_PASSWORD`

Más información: https://support.google.com/accounts/answer/185833

## Recursos Adicionales

- [Documentación de MJML](https://mjml.io/documentation/)
- [Documentación de Jinja2](https://jinja.palletsprojects.com/)
- [Documentación de python-dotenv](https://pypi.org/project/python-dotenv/)
