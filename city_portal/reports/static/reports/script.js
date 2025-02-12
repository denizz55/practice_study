
function toggleMenu() {
document.querySelector('nav').classList.toggle('menu-open');
}

function handleKey(event) {
if (event.key === "Enter" || event.key === " ") {
 toggleMenu();
}
}
