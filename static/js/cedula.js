function limitarEntrada() {
    let x = document.getElementById("miInput");
    if (x.value.length > 10) {
      x.value = x.value.slice(0,10);
    }
  }