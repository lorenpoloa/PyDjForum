import markdown
from django import template
from django.utils.safestring import mark_safe
from django.template.defaultfilters import stringfilter
from bleach import clean

register = template.Library()

@register.filter(name='markdown')
@stringfilter
def markdown_format(text):
        # Lista de tags y atributos permitidos
    ALLOWED_TAGS = [
        'a', 'abbr', 'acronym', 'b', 'blockquote', 'code', 'em',
        'i', 'li', 'ol', 'strong', 'ul', 'p', 'br', 'pre',
        'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'hr',
        'table', 'thead', 'tbody', 'tr', 'th', 'td',
        'img', 'div', 'span'
    ]
    
    ALLOWED_ATTRIBUTES = {
        'a': ['href', 'title', 'target', 'rel'],
        'img': ['src', 'alt', 'width', 'height'],
        '*': ['class', 'id'],
    }

    # Extensiones opcionales (puedes personalizar)
    MARKDOWN_EXTENSIONS = [
        'fenced_code',          # Bloques de código cercados
        'codehilite',           # Resaltado de sintaxis
        'tables',               # Tablas
        'nl2br',               # Saltos de línea automáticos
        'sane_lists',          # Listas más intuitivas
    ]
    
    # Configuración adicional para codehilite
    extension_configs = {
        'codehilite': {
            'linenums': True,   # Números de línea
            'css_class': 'codehilite',
        }
    }

    html = markdown.markdown(text, extensions=MARKDOWN_EXTENSIONS)
    cleaned_html = clean(html, tags=ALLOWED_TAGS, attributes=ALLOWED_ATTRIBUTES)
    

    
    
    return mark_safe(
        markdown.markdown(
            text,
            extensions=MARKDOWN_EXTENSIONS,
            extension_configs=extension_configs,
            output_format='html5'
        )
    )