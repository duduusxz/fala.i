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

// Efeito de blur no hover do container
const containers = document.querySelectorAll(".container-nova-senha")
containers.forEach((container) => {
  container.addEventListener("mouseenter", () => {
    document.body.classList.add("blur-ativa")
    container.style.zIndex = "9999"
  })

  container.addEventListener("mouseleave", () => {
    document.body.classList.remove("blur-ativa")
    container.style.zIndex = ""
  })
})

// Controles de fonte (adaptado para funcionar sem o elemento específico)
document.getElementById("increase-font").addEventListener("click", () => {
  const elementos = document.querySelectorAll("h3, label, p, input, button")
  elementos.forEach((elemento) => {
    const tamanhoAtual = Number.parseFloat(window.getComputedStyle(elemento).fontSize)
    let novoTamanho = tamanhoAtual * 1.1
    if (novoTamanho > 30) {
      novoTamanho = 30
    }
    elemento.style.fontSize = novoTamanho + "px"
  })
})

document.getElementById("decrease-font").addEventListener("click", () => {
  const elementos = document.querySelectorAll("h3, label, p, input, button")
  elementos.forEach((elemento) => {
    const tamanhoAtual = Number.parseFloat(window.getComputedStyle(elemento).fontSize)
    const tamanhoBase = 16 // tamanho base em px
    if (tamanhoAtual > tamanhoBase) {
      elemento.style.fontSize = tamanhoAtual * 0.9 + "px"
    }
  })
})

document.addEventListener("DOMContentLoaded", () => {
  // Inicializa o gerenciador de tema
  new ThemeManager()
})