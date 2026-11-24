(() => {
  const root = document.documentElement;
  const toggle = document.getElementById("themeToggle");
  const icon = document.getElementById("themeIcon");
  const text = document.getElementById("themeText");
  const saved = localStorage.getItem("gadgetrent-theme");
  if (saved === "light" || saved === "dark") root.dataset.theme = saved;
  function updateThemeButton() {
    const light = root.dataset.theme === "light";
    if (icon) icon.textContent = light ? "☾" : "☼";
    if (text) text.textContent = light ? "Dark mode" : "Light mode";
  }
  updateThemeButton();
  if (toggle) toggle.addEventListener("click", () => {
    root.dataset.theme = root.dataset.theme === "dark" ? "light" : "dark";
    localStorage.setItem("gadgetrent-theme", root.dataset.theme);
    updateThemeButton();
  });
  const menu = document.getElementById("menuToggle");
  const sidebar = document.getElementById("sidebar");
  if (menu && sidebar) menu.addEventListener("click", () => sidebar.classList.toggle("open"));
})();