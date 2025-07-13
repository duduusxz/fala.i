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

        

let posicaoAtual = 0;

function moverContainer(direcao) {
    const containerLogin = document.getElementById('container-login');
    const containerCadastro = document.getElementById('container-cadastro');

    if (direcao === 'direita' && posicaoAtual < 1) {
        posicaoAtual++;
    } else if (direcao === 'esquerda' && posicaoAtual > -1) {
        posicaoAtual--;
    }

    if (posicaoAtual === 0) {
        containerLogin.style.transform = 'translateX(0) translateY(-50%)';
        containerCadastro.style.transform = 'translateX(0) translateY(-50%)';
    } else if (posicaoAtual === 1) {
        containerLogin.style.transform = 'translateX(200%) translateY(-50%)';
        containerCadastro.style.transform = 'translateX(-140%) translateY(-50%) scale(1.10)';
    }
}

function moverContainer2(direcao) {
    const containerLogin = document.getElementById('container-login');
    const senhaEsquecida = document.getElementById('senha-esquecida');

    if (direcao === 'direita' && posicaoAtual < 1) {
        posicaoAtual++;
    } else if (direcao === 'esquerda' && posicaoAtual > -1) {
        posicaoAtual--;
    }

    if (posicaoAtual === 0) {
        containerLogin.style.transform = 'translateX(0) translateY(-50%)';
        senhaEsquecida.style.transform = 'translateX(0) translateY(-50%)';
    } else if (posicaoAtual === 1) {
        containerLogin.style.transform = 'translateX(200%) translateY(-50%)';
        senhaEsquecida.style.transform = 'translateX(-140%) translateY(-55%) scale(1.10)';
    }
}

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