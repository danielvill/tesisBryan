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
            alert('La cédula ingresada no es válida');
            e.preventDefault(); // Previene el envío del formulario
        }
    });
});


// Este es oara preguntar de la edicion y eliminacion
$(document).ready(function () {
    $(".eliminar").click(function (event) {
        if (!confirm("¿Estás seguro de que quieres eliminar?")) {
            event.preventDefault();
        }
    });
});

// Filtro para visualizar la edicion
$(document).ready(function () {
    $("#filtro").on("keyup", function () {
        var value = $(this).val().toLowerCase();
        $("tbody[data-nombre]").filter(function () {
            $(this).parent().toggle($(this).data("nombre").toLowerCase().indexOf(value) > -1)
        });
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
                alert('Por favor, ingresa un correo válido para el usuario ' + usuarios[i].getAttribute('data-nombre'));
                return false;
            }
        }
    }

    // Llamar a la función de validación
    validarcorreos();
});
