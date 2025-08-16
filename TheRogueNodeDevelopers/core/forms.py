from django import forms
from .models import Information
from pagedown.widgets import PagedownWidget


class InformationForm(forms.ModelForm):
    """
    Formulario para crear o editar instancias del modelo :class:`core.models.Information`.

    Este formulario utiliza widgets personalizados para mejorar la experiencia
    del usuario en el ingreso de datos.

    Attributes
    ----------
    Meta.model : Information
        Modelo asociado al formulario.
    Meta.fields : list
        Lista de campos que se incluyen en el formulario.
    Meta.widgets : dict
        Diccionario que especifica los widgets a utilizar para cada campo.

    Example
    -------
    .. code-block:: python

        # Crear formulario vacío
        form = InformationForm()

        # Crear formulario con datos POST
        form = InformationForm(data={
            'title': 'Documento de prueba',
            'content': 'Contenido en markdown',
            'is_public': True
        })
        if form.is_valid():
            form.save()
    """

    class Meta:
        """
        Metadatos del formulario ``InformationForm``.

        Define el modelo de referencia, los campos a mostrar en el formulario
        y los widgets personalizados para la representación de dichos campos.

        Attributes
        ----------
        model : Information
            Modelo ``Information`` definido en ``models.py``.
        fields : list
            Campos incluidos en el formulario: ``title``, ``content`` y ``is_public``.
        widgets : dict
            Diccionario de widgets personalizados:
                - ``content`` usa un ``Textarea`` con 5 filas.
                - ``title`` usa un ``TextInput`` estilizado.
                - ``is_public`` usa un ``CheckboxInput``.
        """
        model = Information
        fields = ['title', 'content', 'is_public']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 5, 'class': 'form-control'}),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'is_public': forms.CheckboxInput(),
        }
