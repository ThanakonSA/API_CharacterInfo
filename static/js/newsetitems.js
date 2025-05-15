window.addEventListener('DOMContentLoaded', () => {
  // เปลี่ยนรูปฮีโร่เมื่อเลือกใน Dropdown
  const heroSelect = document.getElementById('heroSelect');
  const heroImg    = document.getElementById('selectedHeroIcon');
  heroSelect.addEventListener('change', () => {
    heroImg.src = heroSelect.selectedOptions[0].dataset.icon;
  });

  // เปลี่ยนรูปไอเทมแต่ละช่องเมื่อเลือก
  document.querySelectorAll('.item-slot').forEach(slot => {
    const selectEl = slot.querySelector('.itemSelect');
    const imgEl    = slot.querySelector('.selectedItemIcon');
    selectEl.addEventListener('change', () => {
      imgEl.src = selectEl.selectedOptions[0].dataset.icon;
    });
  });
});
