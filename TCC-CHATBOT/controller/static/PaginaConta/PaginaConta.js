let posicaoAtual = 0; // 0 = container1, 1 = container2, 2 = container3

function moverGaleria(direcao) {
  const container1 = document.getElementById('container1');
  const container2 = document.getElementById('container2');
  const container3 = document.getElementById('container3');
  const container4 = document.getElementById('container4');

  if (direcao === 'direita' && posicaoAtual < 3) {
    posicaoAtual++;
  } else if (direcao === 'esquerda' && posicaoAtual > 0) {
    posicaoAtual--;
  }

  // Aplicando transformação de acordo com a posição atual
  if (posicaoAtual === 0) {
    container1.style.transform = 'translateX(0px) scale(1)';
    container2.style.transform = 'translateX(0px) scale(1)';
    container3.style.transform = 'translateX(0px) scale(1)';
    container4.style.transform = 'translateX(0px) scale(1)';
  } else if (posicaoAtual === 1) {
    container1.style.transform = 'translateX(-560px) scale(0.8)';
    container2.style.transform = 'translateX(-700px) scale(1.24)';
    container3.style.transform = 'translateX(-700px) scale(1)';
    container4.style.transform = 'translateX(-700px) scale(1)';
  } else if (posicaoAtual === 2) {
    container1.style.transform = 'translateX(-1120px) scale(0.8)';
    container2.style.transform = 'translateX(-1400px) scale(1)';
    container3.style.transform = 'translateX(-1400px) scale(1.24)';
    container4.style.transform = 'translateX(-1400px) scale(1)';
  } else if (posicaoAtual === 3) {
    container1.style.transform = 'translateX(-1680px) scale(0.8)';
    container2.style.transform = 'translateX(-2100px) scale(1)';
    container3.style.transform = 'translateX(-2100px) scale(1)';
    container4.style.transform = 'translateX(-2100px) scale(1.24)';
  }
}