// Array para armazenar as tarefas (agora vindas do banco)
let tarefas = [];

// Gerenciamento do Modo Escuro (igual ao da tela de login)
class ThemeManager {
  constructor() {
    this.init();
  }

  init() {
    const currentTheme =
      document.documentElement.getAttribute("data-theme") || "light";
    this.updateToggleIcon(currentTheme);
    this.setupToggleButton();
  }

  setTheme(theme) {
    document.documentElement.setAttribute("data-theme", theme);
    localStorage.setItem("theme", theme);
    this.updateToggleIcon(theme);
  }

  updateToggleIcon(theme) {
    const icon = document.getElementById("theme-icon");
    if (icon) {
      icon.className = theme === "dark" ? "fas fa-sun" : "fas fa-moon";
    }
  }

  toggleTheme() {
    const currentTheme = document.documentElement.getAttribute("data-theme");
    const newTheme = currentTheme === "dark" ? "light" : "dark";
    this.setTheme(newTheme);
  }

  setupToggleButton() {
    const toggleButton = document.getElementById("toggle-dark-mode");
    if (toggleButton) {
      toggleButton.addEventListener("click", () => {
        this.toggleTheme();
      });
    }
  }
}

function abrirModal() {
  const modal = document.getElementById("modal-overlay");
  modal.classList.add("show");
  document.body.style.overflow = "hidden";
}

function fecharModal() {
  const modal = document.getElementById("modal-overlay");
  modal.classList.remove("show");
  document.body.style.overflow = "auto";
  document.getElementById("form-tarefa").reset();
}

document.getElementById("modal-overlay").addEventListener("click", function (e) {
  if (e.target === this) fecharModal();
});

document.getElementById("form-tarefa").addEventListener("submit", async (e) => {
  e.preventDefault();

  const nomeTarefa = document.getElementById("nome-tarefa").value;
  const descricaoTarefa = document.getElementById("descricao-tarefa").value;
  const dataHora = document.getElementById("data-tarefa").value;

  if (!nomeTarefa || !dataHora) {
    mostrarMensagem("Preencha todos os campos obrigatórios!", "erro");
    return;
  }

  const [dataTarefa, horarioTarefa] = dataHora.split("T");

  try {
    const response = await fetch("/tarefas", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        titulo: nomeTarefa,
        descricao: descricaoTarefa,
        data_tarefa: dataTarefa,
        horario_tarefa: horarioTarefa,
      }),
    });

    const resultado = await response.json();

    if (response.ok) {
      mostrarMensagem("Tarefa adicionada com sucesso!", "sucesso");
      fecharModal();
      document.getElementById("form-tarefa").reset();
      // aqui pode chamar atualizarListaTarefas() se quiser exibir
    } else {
      mostrarMensagem(resultado.erro || "Erro ao salvar tarefa!", "erro");
    }
  } catch (erro) {
    console.error("Erro:", erro);
    mostrarMensagem("Erro ao conectar com o servidor!", "erro");
  }
});


async function salvarTarefaNoBanco(tarefa) {
  try {
    await fetch("http://localhost:5000/tarefas", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        titulo: tarefa.nome,
        descricao: tarefa.descricao,
        data_tarefa: tarefa.data,
        horario_tarefa: tarefa.horario
      }),
    });

    mostrarMensagem("Tarefa salva com sucesso no banco!", "sucesso");
    carregarTarefasDoBanco();
    fecharModal();
  } catch (error) {
    console.error("Erro ao salvar tarefa:", error);
    mostrarMensagem("Erro ao salvar tarefa no banco.", "erro");
  }
}

async function carregarTarefasDoBanco() {
  try {
    const resposta = await fetch("http://localhost:5000/tarefas");
    const dados = await resposta.json();
    tarefas = dados.map(t => ({
      nome: t.titulo,
      descricao: t.descricao,
      data: t.data_tarefa,
      horario: t.horario_tarefa
    }));
    atualizarListaTarefas();
  } catch (error) {
    console.error("Erro ao carregar tarefas:", error);
    mostrarMensagem("Erro ao carregar tarefas do banco.", "erro");
  }
}

async function atualizarListaTarefas() {
  const listaTarefas = document.getElementById("lista-tarefas");

  try {
    console.log("Chamando /tarefas para buscar do banco...");
    const response = await fetch("/tarefas");
    const dados = await response.json();

    if (!Array.isArray(dados) || dados.length === 0) {
      listaTarefas.innerHTML = "<p>Nenhuma tarefa cadastrada.</p>";
      return;
    }

    let html = "";
    dados.forEach((tarefa) => {
      const dataHoraFormatada = formatarData(`${tarefa.data_tarefa}T${tarefa.horario_tarefa}`);
      html += `
        <div class="tarefa-item">
          <h4>${tarefa.titulo}</h4>
          <div class="data">${dataHoraFormatada}</div>
          ${
            tarefa.descricao
              ? `<div class="descricao">${tarefa.descricao}</div>`
              : ""
          }
        </div>
      `;
    });

    listaTarefas.innerHTML = html;

  } catch (erro) {
    console.error("Erro ao buscar tarefas:", erro);
    listaTarefas.innerHTML = "<p>Erro ao carregar tarefas do banco.</p>";
  }
}

// Atualiza a lista assim que a página carregar
document.addEventListener("DOMContentLoaded", () => {
  new ThemeManager();
  observeElements();
  atualizarListaTarefas(); // <- ESSA LINHA É O QUE FAZ BUSCAR DO BANCO
});



function formatarData(dataString, horarioString) {
  if (!dataString) return "Data não informada";
  try {
    const data = new Date(`${dataString}T${horarioString || "00:00:00"}`);
    return data.toLocaleString("pt-BR", {
      day: "2-digit",
      month: "2-digit",
      year: "numeric",
      hour: "2-digit",
      minute: "2-digit",
    });
  } catch (error) {
    return dataString;
  }
}

function mostrarMensagem(texto, tipo) {
  const mensagem = document.createElement("div");
  mensagem.className = `mensagem ${tipo}`;
  mensagem.textContent = texto;
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
  `;

  if (tipo === "sucesso") mensagem.style.backgroundColor = "#10b981";
  else if (tipo === "erro") mensagem.style.backgroundColor = "#ef4444";

  document.body.appendChild(mensagem);

  setTimeout(() => {
    mensagem.style.animation = "slideOutRight 0.3s ease-out";
    setTimeout(() => document.body.removeChild(mensagem), 300);
  }, 3000);
}

const style = document.createElement("style");
style.textContent = `
  @keyframes slideInRight {
    from { transform: translateX(100%); opacity: 0; }
    to { transform: translateX(0); opacity: 1; }
  }
  @keyframes slideOutRight {
    from { transform: translateX(0); opacity: 1; }
    to { transform: translateX(100%); opacity: 0; }
  }
`;
document.head.appendChild(style);

document.addEventListener("keydown", (e) => {
  if (e.key === "Escape") fecharModal();
});

document.addEventListener("DOMContentLoaded", () => {
  new ThemeManager();
  observeElements();
  carregarTarefasDoBanco();
});

function observeElements() {
  const observer = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          entry.target.classList.add("fade-animate");
        }
      });
    },
    { threshold: 0.1 }
  );
  const fadeElements = document.querySelectorAll(".fade-in");
  fadeElements.forEach((element) => observer.observe(element));
}
