const dicas = document.querySelectorAll('.dica');

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