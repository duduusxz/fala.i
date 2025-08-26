function abrirmenu() {
  const menu = document.getElementById("menu")
  menu.classList.toggle("ativo")
}

const menuContainer = document.querySelector(".menu-container")
const menu = document.getElementById("menu")
const addButton = document.querySelector(".add")

menuContainer.addEventListener("mouseenter", () => {
  menu.classList.add("ativo")
})

menuContainer.addEventListener("mouseleave", () => {
  menu.classList.remove("ativo")
})

addButton.addEventListener("mouseenter", () => {
  menu.classList.add("ativo")
})

addButton.addEventListener("mouseleave", () => {
  menu.classList.remove("ativo")
})

const textarea = document.getElementById("pergunta")
const form = document.getElementById("form")
const chatContainer = document.getElementById("chat-container")
const mensagensChat = document.getElementById("mensagens-chat")


textarea.addEventListener("keydown", (event) => {
  if (event.key === "Enter" && !event.shiftKey) {
    event.preventDefault()
    form.dispatchEvent(new Event("submit"))
  }
})

function toggleMobileMenu() {
  const navMenu = document.getElementById("nav-menu")
  navMenu.classList.toggle("mobile-active")
}

// Gerenciamento do Modo Escuro - SISTEMA UNIFICADO (IGUAL À PÁGINA INICIAL)
class ThemeManager {
  constructor() {
    this.init()
  }

  init() {
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
  new ThemeManager();
  // Inicializa animações de fade-in
  observeElements();
});

// Animação de fade-in
function observeElements() {
  const observer = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          entry.target.classList.add("fade-animate");
        }
      });
    },
    {
      threshold: 0.1,
    }
  );
  const fadeElements = document.querySelectorAll(".fade-in");
  fadeElements.forEach((element) => {
    observer.observe(element);
  });
}

//audio chatbot

async function enviarMensagem(mensagem) {
    if (!mensagem.trim()) return;

    // mostra mensagem do usuário no chat (ajusta pra sua função real)
    adicionarMensagemUsuario(mensagem);

    const res = await fetch("/resposta", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: mensagem })
    });

    const data = await res.json();
    adicionarMensagemBot(data.resposta); // idem
}

// Reconhecimento de voz
let recognition = null;

function iniciarReconhecimento() {
    recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
    recognition.lang = "pt-BR";
    recognition.continuous = false;
    recognition.interimResults = false;
    recognition.start();

    recognition.onresult = function(event) {
        const texto = event.results[0][0].transcript;
        enviarMensagem(texto);
    };

    recognition.onerror = (event) => console.error("Erro:", event.error);
}

function pararReconhecimento() {
    if (recognition) {
        recognition.stop();
        recognition = null;
    }
}
