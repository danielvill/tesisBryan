// Validar lo que es la cedula 
function validarCedula(cedula) {
    // Verifica que tenga 10 caracteres y sea solo números
    if (cedula.length === 10 && Number.isInteger(+cedula)) {
        var digitos = cedula.split('').map(Number);
        var ultimoDigito = digitos.pop();
        var suma = digitos.reduce(function (acc, curr, i) {
            var valor = (i % 2 === 0) ? curr * 2 : curr;
            valor = (valor > 9) ? valor - 9 : valor;
            return acc + valor;
        }, 0);
        var digitoVerificador = 10 - (suma % 10);
        digitoVerificador = (digitoVerificador === 10) ? 0 : digitoVerificador;
        return ultimoDigito === digitoVerificador;
    } else {
        return false;
    }
}

document.querySelectorAll('form').forEach(function(form) {
    form.addEventListener('submit', function (e) {
        var cedula = form.querySelector('input[name="cedula"]').value;
        if (!validarCedula(cedula)) {
            Swal.fire({
                icon: 'error',
                title: 'Oops...',
                text: 'Cedula no valida'
            });
            e.preventDefault(); // Previene el envío del formulario
        }
    });
});


$(".eliminar").click(function (event) {
    event.preventDefault();
    var url = $(this).attr('href'); // Guarda la URL del enlace
    Swal.fire({
        title: '¿Estás seguro?',
        text: "¿Estás seguro de que quieres eliminar?",
        icon: 'warning',
        showCancelButton: true,
        confirmButtonColor: '#3085d6',
        cancelButtonColor: '#d33',
        confirmButtonText: 'Sí, eliminar!',
        cancelButtonText: 'No, cancelar!'
    }).then((result) => {
        if (result.isConfirmed) {
            window.location.href = url; // Navega a la URL del enlace
        }
    });
});



$(document).ready(function () {
    // Validar Correo
    function validarcorreos() {
        let usuarios = document.querySelectorAll('[data-nombre]');
        let regex = /^[\w-]+(\.[\w-]+)*@([\w-]+\.)+[a-zA-Z]{2,7}$/;

        for (let i = 0; i < usuarios.length; i++) {
            let correo = usuarios[i].querySelector('[name="correo"]').value;
            if (!regex.test(correo)) {
                Swal.fire({
                    icon: 'error',
                    title: 'Oops...',
                    text: 'Ingresa un correo valido'
                });
                return false;
            }
        }
    }

    // Llamar a la función de validación
    validarcorreos();
});
