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





// Limitar cedula
function limitarEntrada() {
    let x = document.getElementById("miInput");
    if (x.value.length > 10) {
        x.value = x.value.slice(0, 10);
    }
}
