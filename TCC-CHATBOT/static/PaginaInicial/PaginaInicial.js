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

var onda1 = document.getElementById('onda1')
var onda2 = document.getElementById('onda2')
var onda3 = document.getElementById('onda3')
var onda4 = document.getElementById('onda4')
var onda5 = document.getElementById('onda5')
var onda6 = document.getElementById('onda6')
var onda7 = document.getElementById('onda7')
var onda8 = document.getElementById('onda8')

window.addEventListener('scroll', function(){
  var rolagemPos = this.window.scrollY

  onda1.style.backgroundPositionX = 600 + rolagemPos * 1.5 + 'px'
  onda2.style.backgroundPositionX = 400 + rolagemPos * -1.5 + 'px'
  onda3.style.backgroundPositionX = 200 + rolagemPos * 0.5 + 'px'
  onda4.style.backgroundPositionX = 100 + rolagemPos * -0.5 + 'px'
  onda5.style.backgroundPositionX = 100 + rolagemPos * 1.5 + 'px'
  onda6.style.backgroundPositionX = 100 + rolagemPos * -1.5 + 'px'
  onda7.style.backgroundPositionX = 100 + rolagemPos * 0.5 + 'px'
  onda8.style.backgroundPositionX = 100 + rolagemPos * -0.5 + 'px'
})