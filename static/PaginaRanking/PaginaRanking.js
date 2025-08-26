// Gerenciamento do Modo Escuro (igual ao da tela de login)
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

// Inicialização quando a página carregar
document.addEventListener("DOMContentLoaded", () => {
  // Inicializa o gerenciador de tema
  new ThemeManager()
  // Inicializa animações de fade-in
  observeElements()
})

// Animação de fade-in
function observeElements() {
  const observer = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          entry.target.classList.add("fade-animate")
        }
      })
    },
    {
      threshold: 0.1,
    },
  )
  const fadeElements = document.querySelectorAll(".fade-in")
  fadeElements.forEach((element) => {
    observer.observe(element)
  })
}