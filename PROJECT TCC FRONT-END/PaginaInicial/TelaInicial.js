document.addEventListener("DOMContentLoaded", function() {
    const textElement = document.getElementById("text");
    const textContent = "Aprimore sua comunicação e fale com confiança! Descubra técnicas eficazes para melhorar sua oralidade e se destacar em qualquer situação!";
    let index = 0;

    function typeWriter() {
        if (index < textContent.length) {
            textElement.textContent = textContent.substring(0, index + 1); 
            index++;
            setTimeout(typeWriter, 50); 
        }
    }

    typeWriter(); 
});

// Funções para aumentar e diminuir o tamanho da fonte
function increaseFontSize() {
    let elements = document.querySelectorAll('body, .titulo, .comecando, .texto, #textinho');
    elements.forEach(function(element) {
        let currentSize = window.getComputedStyle(element).fontSize;
        currentSize = parseFloat(currentSize);
        element.style.fontSize = (currentSize * 1.1) + 'px'; // Aumenta em 10%
    });
}

function decreaseFontSize() {
    let elements = document.querySelectorAll('body, .titulo, .comecando, .texto, #textinho');
    elements.forEach(function(element) {
        let currentSize = window.getComputedStyle(element).fontSize;
        currentSize = parseFloat(currentSize);
        element.style.fontSize = (currentSize * 0.9) + 'px'; // Diminui em 10%
    });
}0