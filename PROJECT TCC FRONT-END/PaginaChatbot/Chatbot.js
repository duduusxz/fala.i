function abrirmenu() {
    const menu = document.getElementById("menu");
    menu.classList.toggle("ativo");
}

const menuContainer = document.querySelector(".menu-container");
const menu = document.getElementById("menu");
const addButton = document.querySelector(".add");

menuContainer.addEventListener("mouseenter", () => {
    menu.classList.add("ativo");
});

menuContainer.addEventListener("mouseleave", () => {
    menu.classList.remove("ativo");
});

addButton.addEventListener("mouseenter", () => {
    menu.classList.add("ativo");
});

addButton.addEventListener("mouseleave", () => {
    menu.classList.remove("ativo");
});