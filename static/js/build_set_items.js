window.addEventListener("DOMContentLoaded", () => {
  // —– Hero —–
  const heroSel  = document.getElementById("heroSelect");
  const heroIcon = document.getElementById("heroIcon");
  const heroName = document.getElementById("heroName");

  heroSel.addEventListener("change", () => {
    const opt = heroSel.selectedOptions[0];
    heroIcon.src      = opt.dataset.icon;
    heroName.value    = opt.text;
  });

  // —– Items —–
  for (let i = 1; i <= 6; i++) {
    const sel = document.getElementById(`itemSelect${i}`);
    const ic  = document.getElementById(`itemIcon${i}`);
    sel.addEventListener("change", () => {
      const cur = sel.selectedOptions[0];
      ic.src = cur.dataset.icon || "";
    });
  }
});
