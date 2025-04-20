# Ejemplo de Plantillas de Correo con MJML y Jinja2

Este proyecto demuestra cómo crear plantillas de correo electrónico HTML responsivas utilizando MJML y cómo personalizarlas con parámetros dinámicos usando Jinja2.

## Características

- Creación de plantillas de correo con MJML (responsive por defecto)
- Personalización de plantillas con parámetros usando Jinja2
- Renderizado de plantillas a HTML
- Manejo automático de rutas de imágenes para correcta visualización en correos
- Soporte para imágenes incrustadas como base64 directamente en el HTML
- Envío de correos electrónicos con el contenido HTML generado

## Requisitos

- Python 3.6+
- Paquetes de Python:
  - mjml (`pip install mjml`)
  - jinja2 (`pip install jinja2`)

## Estructura del Proyecto

- `email_template.mjml`: Plantilla de correo en formato MJML con variables Jinja2
- `email_template_base64.mjml`: Plantilla de correo que usa imágenes incrustadas como base64
- `render_email.py`: Funciones para renderizar plantillas y enviar correos
- `ejemplo_uso.py`: Ejemplos de uso de las funciones
- `enviar_correo_base64.py`: Script para enviar correos con imágenes base64
- `ejemplo_correo_base64.py`: Ejemplo completo de envío de correo con imágenes base64 y demostración de codificación
- `img/`: Directorio para imágenes utilizadas en las plantillas

## Uso Básico

### 1. Renderizar una Plantilla

```python
from render_email import render_email_template

# Datos para personalizar la plantilla
contexto = {
    'nombre_cliente': 'Ana García',
    'link_servicios': 'https://ejemplo.com/servicios'
}

# Definir una URL base para las imágenes (importante para que se muestren correctamente)
base_url = "https://midominio.com/assets/"

# Renderizar la plantilla y obtener HTML
html_output = render_email_template('email_template.mjml', contexto, base_url)

# Guardar el HTML generado (opcional)
with open('email_output.html', 'w') as f:
    f.write(html_output)
```

### 2. Enviar un Correo con la Plantilla Renderizada

```python
from render_email import render_email_template, send_email

# Datos para personalizar la plantilla
contexto = {
    'nombre_cliente': 'Ana García',
    'link_servicios': 'https://ejemplo.com/servicios'
}

# Definir una URL base para las imágenes (importante para que se muestren correctamente)
base_url = "https://midominio.com/assets/"

# Renderizar la plantilla
html_output = render_email_template('email_template.mjml', contexto, base_url)

# Enviar el correo
send_email(
    recipient_email="destinatario@ejemplo.com",
    subject="Bienvenido a Nuestro Servicio",
    html_content=html_output,
    sender_email="tu_correo@gmail.com",
    smtp_password="tu_contraseña_o_clave_de_aplicación",
    smtp_server="smtp.gmail.com",
    smtp_port=587
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

Cuando llamas a la función `render_email_template`, pasa un diccionario con los valores para las variables:

```python
contexto = {
    'nombre_cliente': 'Juan Pérez',
    'link_servicios': 'https://miservicio.com/ofertas-especiales'
}

html_output = render_email_template('email_template.mjml', contexto)
```

### Manejo de Imágenes en Correos Electrónicos

Un problema común al enviar correos HTML es que las imágenes con rutas relativas (como `img/logo.png`) no se muestran correctamente porque los clientes de correo no tienen acceso al sistema de archivos local.

#### Opción 1: Usar URLs absolutas

La función `render_email_template` acepta un parámetro `base_url` que convierte automáticamente las rutas relativas de imágenes a URLs absolutas:

```python
# Usar una URL base donde están alojadas tus imágenes (recomendado para producción)
base_url = "https://midominio.com/assets/"
html_output = render_email_template('email_template.mjml', contexto, base_url)

# O usar la ruta absoluta local (útil para pruebas)
html_output = render_email_template('email_template.mjml', contexto)
```

Para que las imágenes se muestren correctamente en los correos enviados:

1. Sube tus imágenes a un servidor web accesible públicamente
2. Especifica la URL base de ese servidor al llamar a `render_email_template`
3. En la plantilla MJML, usa rutas relativas para las imágenes (ej: `img/logo.png`)

#### Opción 2: Usar imágenes incrustadas como base64

Otra opción es incrustar las imágenes directamente en el HTML como datos base64. Esto tiene la ventaja de que las imágenes siempre se mostrarán correctamente, incluso sin conexión a internet, pero aumenta el tamaño del correo.

Para usar imágenes base64:

1. En la plantilla MJML, usa la etiqueta `<mj-raw>` con una imagen que tenga una URL de datos base64:

```html
<mj-raw>
  <div style="text-align: center; margin-bottom: 20px;">
    <img src="data:image/png;base64,{{ logo_base64 }}" alt="Logo" style="width: 100px; height: auto;">
  </div>
</mj-raw>
```

2. Al llamar a `render_email_template`, proporciona un diccionario con las rutas de las imágenes a codificar:

```python
from render_email import render_email_template, encode_image_to_base64

# Datos para personalizar la plantilla
contexto = {
    'nombre_cliente': 'Juan Pérez',
    'link_servicios': 'https://ejemplo.com/servicios'
}

# Rutas de las imágenes a codificar en base64
imagenes_base64 = {
    'logo_base64': 'img/logo.png',
    'banner_base64': 'img/banner.jpg'
}

# Renderizar la plantilla con las imágenes en base64
html_output = render_email_template(
    'email_template_base64.mjml', 
    contexto,
    base64_images=imagenes_base64
)
```

La función `render_email_template` se encargará de leer las imágenes, codificarlas en base64 y pasarlas a la plantilla.

## Ejemplos

### Ejemplos de Uso Básico

Consulta el archivo `ejemplo_uso.py` para ver ejemplos completos de cómo:

1. Crear un correo de bienvenida personalizado
2. Crear un correo promocional con diferentes parámetros
3. Crear un correo con imágenes incrustadas como base64
4. Guardar el HTML generado
5. Enviar el correo electrónico

### Enviar Correo con Imágenes Base64

#### Opción 1: Script básico

Para enviar directamente un correo con imágenes codificadas en base64, puedes usar el script `enviar_correo_base64.py`:

```bash
python enviar_correo_base64.py
```

Este script:
1. Carga una plantilla MJML que usa imágenes base64
2. Codifica automáticamente las imágenes especificadas
3. Renderiza la plantilla con los datos proporcionados
4. Guarda el HTML generado en un archivo
5. Envía el correo electrónico

#### Opción 2: Ejemplo completo con demostración

Para un ejemplo más completo que incluye una demostración de cómo funciona la codificación base64, puedes usar el script `ejemplo_correo_base64.py`:

```bash
python ejemplo_correo_base64.py
```

Este script ofrece:
1. Una demostración de cómo se codifica una imagen en base64
2. Visualización de los primeros caracteres del string base64 generado
3. Un ejemplo de cómo se usaría la imagen base64 en HTML
4. Guardado del string base64 completo en un archivo de texto
5. Un ejemplo completo de envío de correo con imágenes base64
6. Instrucciones detalladas para personalizar el ejemplo

Es ideal para entender paso a paso cómo funciona la codificación base64 de imágenes y cómo se integra en correos electrónicos.

#### Configuración para envío de correos

Antes de ejecutar cualquiera de los scripts, asegúrate de modificar los siguientes valores:
- `recipient_email`: Correo del destinatario
- `sender_email`: Tu correo electrónico
- `smtp_password`: Tu contraseña o clave de aplicación

```python
enviado = send_email(
    recipient_email="destinatario@ejemplo.com",  # Reemplaza con el correo del destinatario real
    subject="¡Bienvenido a TuLavanderia con imágenes Base64!",
    html_content=html_resultado,
    sender_email="tu_correo@gmail.com",  # Reemplaza con tu correo
    smtp_password="tu_contraseña_segura"  # Reemplaza con tu contraseña o clave de aplicación
)
```

## Notas para Gmail

Si utilizas Gmail para enviar correos, necesitarás:

1. Habilitar el acceso de aplicaciones menos seguras, o
2. Usar una "contraseña de aplicación" (recomendado)

Más información: https://support.google.com/accounts/answer/185833

## Recursos Adicionales

- [Documentación de MJML](https://mjml.io/documentation/)
- [Documentación de Jinja2](https://jinja.palletsprojects.com/)
