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

// Função para adicionar mensagem do usuário
function adicionarMensagemUsuario(texto) {
  const mensagemDiv = document.createElement("div")
  mensagemDiv.className = "mensagem-usuario"
  mensagemDiv.innerHTML = `
    <div class="conteudo-mensagem">
      <p>${texto}</p>
    </div>
    <div class="avatar-usuario">
      <i class="fas fa-user"></i>
    </div>
  `
  mensagensChat.appendChild(mensagemDiv)

  // Scroll para baixo
  chatContainer.scrollTop = chatContainer.scrollHeight
}

// Função para adicionar mensagem de carregamento
function adicionarMensagemCarregando() {
  const mensagemDiv = document.createElement("div")
  mensagemDiv.className = "mensagem-bot mensagem-carregando"
  mensagemDiv.id = "mensagem-carregando"
  mensagemDiv.innerHTML = `
    <div class="avatar-bot">
      <img src="{{ url_for('static', filename='img/logo.png') }}" alt="Fala.i" width="30">
    </div>
    <div class="conteudo-mensagem">
      <strong>Fala.i:</strong>
      <div class="typing-indicator">
        <span></span>
        <span></span>
        <span></span>
      </div>
    </div>
  `
  mensagensChat.appendChild(mensagemDiv)

  // Scroll para baixo
  chatContainer.scrollTop = chatContainer.scrollHeight
}

// Função para remover mensagem de carregamento
function removerMensagemCarregando() {
  const mensagemCarregando = document.getElementById("mensagem-carregando")
  if (mensagemCarregando) {
    mensagemCarregando.remove()
  }
}

// Função para adicionar resposta do bot
function adicionarRespostaBot(resposta) {
  const mensagemDiv = document.createElement("div")
  mensagemDiv.className = "mensagem-bot"
  mensagemDiv.innerHTML = `
    <div class="avatar-bot">
      <img src="{{ url_for('static', filename='img/logo.png') }}" alt="Fala.i" width="30">
    </div>
    <div class="conteudo-mensagem">
      <strong>Fala.i:</strong>
      <p>${resposta}</p>
    </div>
  `
  mensagensChat.appendChild(mensagemDiv)

  // Scroll para baixo
  chatContainer.scrollTop = chatContainer.scrollHeight
}

// Interceptar envio do formulário
form.addEventListener("submit", async (e) => {
  e.preventDefault()

  const pergunta = textarea.value.trim()
  if (!pergunta) return

  // Adicionar mensagem do usuário
  adicionarMensagemUsuario(pergunta)

  // Adicionar indicador de carregamento
  adicionarMensagemCarregando()

  // Limpar textarea
  textarea.value = ""

  // Desabilitar botão de envio
  const btnEnviar = document.getElementById("btn-enviar")
  btnEnviar.disabled = true

  try {
    // Enviar para o servidor
    const formData = new FormData()
    formData.append("pergunta", pergunta)

    const response = await fetch("/resposta", {
      method: "POST",
      body: formData,
    })

    if (response.ok) {
      const data = await response.text()

      // Extrair a resposta do HTML retornado (você pode ajustar isso conforme sua implementação)
      const parser = new DOMParser()
      const doc = parser.parseFromString(data, "text/html")
      const respostaElement = doc.querySelector(".resposta-animada p")
      const respostaTexto = respostaElement ? respostaElement.textContent : "Desculpe, ocorreu um erro."

      // Remover indicador de carregamento
      removerMensagemCarregando()

      // Adicionar resposta do bot
      adicionarRespostaBot(respostaTexto)
    } else {
      removerMensagemCarregando()
      adicionarRespostaBot("Desculpe, ocorreu um erro ao processar sua mensagem.")
    }
  } catch (error) {
    console.error("Erro:", error)
    removerMensagemCarregando()
    adicionarRespostaBot("Desculpe, ocorreu um erro de conexão.")
  } finally {
    // Reabilitar botão de envio
    btnEnviar.disabled = false
  }
})

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
  new ThemeManager()
})