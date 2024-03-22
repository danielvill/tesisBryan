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

// Filtro para visualizar la edicion
$(document).ready(function () {
    $("#filtro").on("keyup", function () {
        var value = $(this).val().toLowerCase();
        $("tbody[data-nombre]").filter(function () {
            $(this).parent().toggle($(this).data("nombre").toLowerCase().indexOf(value) > -1)
        });
    });
});