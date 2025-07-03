// Array para armazenar as tarefas
let tarefas = []

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

// Função para abrir o modal
function abrirModal() {
  const modal = document.getElementById("modal-overlay")
  modal.classList.add("show")
  document.body.style.overflow = "hidden" // Impede scroll da página
}

// Função para fechar o modal
function fecharModal() {
  const modal = document.getElementById("modal-overlay")
  modal.classList.remove("show")
  document.body.style.overflow = "auto" // Restaura scroll da página

  // Limpar formulário
  document.getElementById("form-tarefa").reset()
}

// Função para fechar modal clicando fora dele
document.getElementById("modal-overlay").addEventListener("click", function (e) {
  if (e.target === this) {
    fecharModal()
  }
})

// Função para adicionar tarefa (sem validação de data)
document.getElementById("form-tarefa").addEventListener("submit", (e) => {
  e.preventDefault()

  const nomeTarefa = document.getElementById("nome-tarefa").value
  const dataTarefa = document.getElementById("data-tarefa").value
  const descricaoTarefa = document.getElementById("descricao-tarefa").value

  // Criar objeto da tarefa sem validação de data
  const novaTarefa = {
    id: Date.now(),
    nome: nomeTarefa,
    data: dataTarefa,
    descricao: descricaoTarefa,
  }

  // Adicionar à lista de tarefas
  tarefas.push(novaTarefa)
  salvarTarefas() // Salvar no localStorage
  atualizarListaTarefas()
  fecharModal()
  mostrarMensagem("Tarefa adicionada com sucesso!", "sucesso")
})

// Função para atualizar a lista de tarefas na tela (ordenada por data)
function atualizarListaTarefas() {
  const listaTarefas = document.getElementById("lista-tarefas")

  if (tarefas.length === 0) {
    listaTarefas.innerHTML = ""
    return
  }

  // Ordenar tarefas por data
  const tarefasOrdenadas = [...tarefas].sort((a, b) => {
    // Se uma tarefa não tem data, coloca no final
    if (!a.data && !b.data) return 0
    if (!a.data) return 1
    if (!b.data) return -1

    // Comparar as datas
    const dataA = new Date(a.data)
    const dataB = new Date(b.data)

    return dataA - dataB
  })

  let html = ""
  tarefasOrdenadas.forEach((tarefa) => {
    const dataFormatada = formatarData(tarefa.data)
    html += `
            <div class="tarefa-item">
                <h4>${tarefa.nome}</h4>
                <div class="data">${dataFormatada}</div>
                ${tarefa.descricao ? `<div class="descricao">${tarefa.descricao}</div>` : ""}
            </div>
        `
  })

  listaTarefas.innerHTML = html
}

// Função para formatar data (sem erro para data inválida)
function formatarData(dataString) {
  if (!dataString) return "Data não informada"

  try {
    const data = new Date(dataString)
    const opcoes = {
      day: "2-digit",
      month: "2-digit",
      year: "numeric",
      hour: "2-digit",
      minute: "2-digit",
    }
    return data.toLocaleDateString("pt-BR", opcoes)
  } catch (error) {
    return dataString // Retorna a data original se não conseguir formatar
  }
}

// Função para mostrar mensagens (opcional)
function mostrarMensagem(texto, tipo) {
  // Criar elemento da mensagem
  const mensagem = document.createElement("div")
  mensagem.className = `mensagem ${tipo}`
  mensagem.textContent = texto
  mensagem.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        padding: 15px 20px;
        border-radius: 8px;
        color: white;
        font-weight: bold;
        z-index: 1001;
        animation: slideInRight 0.3s ease-out;
    `

  if (tipo === "sucesso") {
    mensagem.style.backgroundColor = "#10b981"
  } else if (tipo === "erro") {
    mensagem.style.backgroundColor = "#ef4444"
  }

  document.body.appendChild(mensagem)

  // Remover mensagem após 3 segundos
  setTimeout(() => {
    mensagem.style.animation = "slideOutRight 0.3s ease-out"
    setTimeout(() => {
      document.body.removeChild(mensagem)
    }, 300)
  }, 3000)
}

// Adicionar estilos para as animações das mensagens
const style = document.createElement("style")
style.textContent = `
    @keyframes slideInRight {
        from {
            transform: translateX(100%);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }
    
    @keyframes slideOutRight {
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

// Fechar modal com tecla ESC
document.addEventListener("keydown", (e) => {
  if (e.key === "Escape") {
    fecharModal()
  }
})

// Inicialização quando a página carregar
document.addEventListener("DOMContentLoaded", () => {
  // Inicializa o gerenciador de tema
  new ThemeManager()

  // Carregar tarefas
  const tarefasSalvas = localStorage.getItem("tarefas")
  if (tarefasSalvas) {
    tarefas = JSON.parse(tarefasSalvas)
    atualizarListaTarefas()
  }
})

// Salvar tarefas no localStorage sempre que a lista for atualizada
function salvarTarefas() {
  localStorage.setItem("tarefas", JSON.stringify(tarefas))
}
