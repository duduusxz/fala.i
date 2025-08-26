// Gerenciamento do Modo Escuro
class ThemeManager {
  constructor() {
    this.init()
  }

  init() {
    // O tema já foi aplicado pelo script inline no head
    // Aqui apenas configuramos o botão e atualizamos o ícone
    const currentTheme = document.documentElement.getAttribute("data-theme") || "light"
    this.updateToggleIcon(currentTheme)
    this.setupToggleButton()
  }

  setTheme(theme) {
    document.documentElement.setAttribute("data-theme", theme)
    localStorage.setItem("theme", theme)
    this.updateToggleIcon(theme)
  }

  updateToggleIcon(theme) {
    const icon = document.getElementById("theme-icon")
    if (icon) {
      if (theme === "dark") {
        icon.className = "fas fa-sun"
      } else {
        icon.className = "fas fa-moon"
      }
    }
  }

  toggleTheme() {
    const currentTheme = document.documentElement.getAttribute("data-theme")
    const newTheme = currentTheme === "dark" ? "light" : "dark"
    this.setTheme(newTheme)
  }

  setupToggleButton() {
    const toggleButton = document.getElementById("toggle-dark-mode")
    if (toggleButton) {
      toggleButton.addEventListener("click", () => {
        this.toggleTheme()
      })
    }
  }
}

// Funcionalidades de acessibilidade - controle de fonte
const texto = document.getElementById("texto-apresentacao-bem-vindo")
const tamanhoBase = Number.parseFloat(window.getComputedStyle(texto).fontSize)

document.getElementById("increase-font").addEventListener("click", () => {
  const tamanhoAtual = Number.parseFloat(window.getComputedStyle(texto).fontSize)
  let novoTamanho = tamanhoAtual * 1.1
  if (novoTamanho > 30) {
    novoTamanho = 30
  }
  texto.style.fontSize = novoTamanho + "px"
})

document.getElementById("decrease-font").addEventListener("click", () => {
  const tamanhoAtual = Number.parseFloat(window.getComputedStyle(texto).fontSize)
  if (tamanhoAtual > tamanhoBase * 1) {
    texto.style.fontSize = tamanhoAtual * 0.9 + "px"
  }
})

// Auto-hide flash messages
function autoHideFlashMessages() {
  const flashMessages = document.querySelectorAll('.flash-message')
  flashMessages.forEach((message, index) => {
    setTimeout(() => {
      message.style.animation = 'slideOut 0.3s ease forwards'
      setTimeout(() => {
        message.remove()
      }, 300)
    }, 3000 + (index * 500)) // Escalonamento para múltiplas mensagens
  })
}

// Adicionar animação de saída para flash messages
const style = document.createElement('style')
style.textContent = `
  @keyframes slideOut {
    from {
      transform: translateX(0);
      opacity: 1;
    }
    to {
      transform: translateX(100%);
      opacity: 0;
    }
  }
`
document.head.appendChild(style)

document.addEventListener("DOMContentLoaded", () => {
  // Inicializa o gerenciador de tema
  new ThemeManager()
  
  // Auto-hide flash messages
  autoHideFlashMessages()
  
  // Animação de digitação
  const textoDigitadoElement = document.getElementById("texto-apresentacao-bem-vindo")
  const textoCompleto = "Esqueceu sua senha? Não se preocupe! Digite seu e-mail e RM para receber um link de redefinição."
  let i = 0
  
  function digitar() {
    if (i < textoCompleto.length) {
      textoDigitadoElement.textContent += textoCompleto.charAt(i)
      i++
      setTimeout(digitar, 30)
    } else {
      textoDigitadoElement.style.borderRight = "none"
    }
  }
  
  digitar()
  
  // Validação do formulário
  const form = document.querySelector('form')
  if (form) {
    form.addEventListener('submit', function(e) {
      const email = form.querySelector('input[name="email"]').value
      const rm = form.querySelector('input[name="rm"]').value
      
      if (!email || !rm) {
        e.preventDefault()
        alert('Por favor, preencha todos os campos.')
        return false
      }
      
      if (rm.length !== 5) {
        e.preventDefault()
        alert('O RM deve ter exatamente 5 dígitos.')
        return false
      }
      
      // Feedback visual durante o envio
      const submitButton = form.querySelector('button[type="submit"]')
      submitButton.textContent = 'Enviando...'
      submitButton.disabled = true
    })
  }
})

// Detectar mudanças na preferência do sistema
window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', (e) => {
  // Só muda automaticamente se não houver preferência salva
  if (!localStorage.getItem('theme')) {
    const newTheme = e.matches ? 'dark' : 'light'
    document.documentElement.setAttribute('data-theme', newTheme)
    
    const themeManager = new ThemeManager()
    themeManager.updateToggleIcon(newTheme)
  }
})
