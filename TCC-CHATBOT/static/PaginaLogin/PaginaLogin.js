function toggleMode() {
    document.body.classList.toggle('light-mode');
    document.body.classList.toggle('dark-mode');
}

let texto = document.getElementById("texto-apresentacao-bem-vindo");
let tamanhoBase = parseFloat(window.getComputedStyle(texto).fontSize);

document.getElementById("increase-font").addEventListener("click", function () {
let tamanhoAtual = parseFloat(window.getComputedStyle(texto).fontSize);

let novoTamanho = tamanhoAtual * 1.1;

if (novoTamanho > 30) {
novoTamanho = 30
}

texto.style.fontSize = novoTamanho + "px";
});


document.getElementById("decrease-font").addEventListener("click", function () {
    let tamanhoAtual = parseFloat(window.getComputedStyle(texto).fontSize);
    if (tamanhoAtual > tamanhoBase * 1) { // Evita que fique muito pequeno
        texto.style.fontSize = (tamanhoAtual * 0.9) + "px"; // Diminui 10%
    }

    
}); 

function mostrarSenha() {
  const input = document.getElementById("senha");
  const icon = document.getElementById("toggleSenha");

  if (input.type === "password") {
    input.type = "text";
    icon.classList.add("fa-eye");
    icon.classList.remove("fa-eye-slash");
  } else {
    input.type = "password";
    icon.classList.add("fa-eye-slash");
    icon.classList.remove("fa-eye");

  }
}





document.addEventListener('DOMContentLoaded', function() {
    const textoDigitadoElement = document.getElementById('texto-apresentacao-bem-vindo');
    const texto = "Conheça a nova plataforma que vai alavancar sua oratória com a nova inteligência artificial Fala.i";
    let i = 0;

    function digitar() {
        if (i < texto.length) {
            textoDigitadoElement.textContent += texto.charAt(i);
            i++;
            setTimeout(digitar, 30); // Ajuste o tempo para controlar a velocidade da digitação
        } else {
            textoDigitadoElement.style.borderRight = 'none'; // Remove o cursor após a digitação
        }
    }

    digitar();
});