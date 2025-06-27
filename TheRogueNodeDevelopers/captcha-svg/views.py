import random
import string
import svgwrite


# Función para generar colores aleatorios en formato hexadecimal
def random_color():
    return f"#{random.randint(0, 0xFFFFFF):06x}"


def generate_random_string(length=6):
    """Generar una cadena aleatoria de letras y números."""
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))



def generate_captcha_svg(request):

    width = 200  # Ancho de la imagen
    height = 80  # Altura de la imagen
    num_elements = 100  # Número de líneas y puntos a dibujar
    characterSize = "40px";
    characterSize2 = 20;
    # Generar un nuevo texto de captcha aleatorio
    captcha_text = generate_random_string()

    # Guardar el texto del captcha en la sesión para validación
    request.session['captcha_text'] = captcha_text

    # Crear el archivo SVG utilizando svgwrite
    dwg = svgwrite.Drawing(size=("200px", "80px"))

    # Definir un fondo blanco para el captcha
    dwg.add(dwg.rect(insert=(0, 0), size=("100%", "100%"), fill="#121212"))
    # Agregar líneas aleatorias
    for _ in range(num_elements):
        x1, y1 = random.randint(0, width), random.randint(0, height)
        x2, y2 = random.randint(0, width), random.randint(0, height)
        color = random_color()
        dwg.add(dwg.line(start=(x1, y1), end=(x2, y2), stroke=color, stroke_width=random.randint(1, 3)))

    # Agregar puntos aleatorios
    for _ in range(num_elements // 2):
        x, y = random.randint(0, width), random.randint(0, height)
        color = random_color()
        dwg.add(dwg.circle(center=(x, y), r=random.randint(1, 5), fill=color))
    

    initposX = 20;
    count = 0;
    # Agregar el texto del captcha al SVG con algunas configuraciones
    #dwg.add(dwg.text(captcha_text, insert=(20, 50), font_size="40px", fill="black", font_family="Arial"))
    for character in captcha_text:
        count+=1;
        initposX+=characterSize2;
        initposY=50;
        dwg.add(dwg.text(character,
            insert=(initposX,initposY),
            stroke=random_color(),
            fill_opacity = 0.6,
            fill= random_color(),
            stroke_width=2,
            font_size=characterSize,
            font_weight="bold",
            font_family="Courier New")
        )
        if(count%3 == 0):
            dwg.add(dwg.text("c",
                insert=(initposX,initposY),
                stroke_width=2,
                stroke_opacity = 0.0,
                fill_opacity = 0.0,
                font_size='40px',
                font_weight="bold",
                font_family="Courier New")
            )
    # Retornar el SVG como respuesta HTTP
    response = HttpResponse(content_type="image/svg+xml")
    dwg.write(response)
    return response

