// Intersection Observer para fade in
document.addEventListener("DOMContentLoaded", () => {
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
      rootMargin: "-50px",
    },
  )
  // Observar todos os elementos com classe fade-in
  const fadeElements = document.querySelectorAll(".fade-in")
  fadeElements.forEach((el) => observer.observe(el))
})

// Função para toggle do menu mobile
function toggleMobileMenu() {
  const menu = document.getElementById("nav-menu")
  menu.classList.toggle("active")
}

// Fechar menu mobile ao clicar em um link
document.addEventListener("DOMContentLoaded", () => {
  const menuLinks = document.querySelectorAll(".nav-menu a")
  const menu = document.getElementById("nav-menu")
  menuLinks.forEach((link) => {
    link.addEventListener("click", () => {
      menu.classList.remove("active")
    })
  })
})

// Fechar menu mobile ao clicar fora dele
document.addEventListener("click", (event) => {
  const menu = document.getElementById("nav-menu")
  const toggle = document.querySelector(".mobile-menu-toggle")
  if (!menu.contains(event.target) && !toggle.contains(event.target)) {
    menu.classList.remove("active")
  }
})

// Gerenciamento do Modo Escuro - SISTEMA UNIFICADO
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

// Inicialização quando a página carregar
document.addEventListener("DOMContentLoaded", () => {
  // Inicializa o gerenciador de tema
  new ThemeManager()
  // Inicializa animações de fade-in
  observeElements()
})