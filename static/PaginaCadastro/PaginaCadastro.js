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

// Funcionalidades existentes
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

function mostrarSenha() {
  const input = document.getElementById("senha")
  const icon = document.getElementById("toggleSenha")
  if (input.type === "password") {
    input.type = "text"
    icon.classList.add("fa-eye")
    icon.classList.remove("fa-eye-slash")
  } else {
    input.type = "password"
    icon.classList.add("fa-eye-slash")
    icon.classList.remove("fa-eye")
  }
}

document.addEventListener("DOMContentLoaded", () => {
  // Inicializa o gerenciador de tema
  new ThemeManager()

  // Animação de digitação
  const textoDigitadoElement = document.getElementById("texto-apresentacao-bem-vindo")
  const textoCompleto =
    "Conheça a nova plataforma que vai alavancar sua oratória com a nova inteligência artificial Fala.i"
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
})