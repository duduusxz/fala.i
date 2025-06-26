const dicas = document.querySelectorAll('.container-nova-senha');

  dicas.forEach(dica => {
    dica.addEventListener('mouseenter', () => {
      document.body.classList.add('blur-ativa');
      dica.style.zIndex = "9999"; // traz a dica para frente
    });

    dica.addEventListener('mouseleave', () => {
      document.body.classList.remove('blur-ativa');
      dica.style.zIndex = ""; // reseta o z-index
    });
  });

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