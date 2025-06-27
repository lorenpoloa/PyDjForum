function refresh_captcha(){
    fetch(captchaUrl)
    .then(response => response.text())
    .then(data => {
        // Insertar el nuevo SVG en el contenedor
        document.getElementById('captcha-img-container').innerHTML = data;
    })
    .catch(error => console.log('Error al refrescar el captcha:', error));

}

function asign_refresh_button(){
    document.getElementById('refresh-captcha').addEventListener('click', refresh_captcha);
}

window.addEventListener("load", asign_refresh_button);

window.addEventListener("load", refresh_captcha);
