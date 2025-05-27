window.addEventListener('DOMContentLoaded', () => {
  const form       = document.getElementById('build-set-form');
  const heroSelect = document.getElementById('hero_id');
  const heroImg    = document.getElementById('hero_icon_img');
  const heroNameIn = document.getElementById('hero_name');
  const heroIconIn = document.getElementById('hero_icon');

  // เมื่อเปลี่ยนฮีโร่ → อัปเดตรูป + hidden
  function updateHero() {
    const opt = heroSelect.options[heroSelect.selectedIndex];
    heroImg.src      = opt.dataset.icon;
    heroNameIn.value = opt.dataset.name;
    heroIconIn.value = opt.dataset.icon;
  }
  updateHero();
  heroSelect.addEventListener('change', updateHero);
  heroSelect.dispatchEvent(new Event('change'));  // เรียกครั้งแรก

  // วนทำซ้ำสำหรับไอเท็ม 1–6
  for (let i = 1; i <= 6; i++) {
    const sel = document.getElementById(`item${i}`);
    const img = document.getElementById(`item${i}_img`);
    const hid = document.getElementById(`item${i}_icon`);
    sel.addEventListener('change', () => {
      const o = sel.options[sel.selectedIndex];
      img.src = o.dataset.icon;
      hid.value = o.dataset.icon;
    });
    sel.dispatchEvent(new Event('change'));
  }

  // เมื่อกด submit → ส่ง JSON ด้วย fetch
  form.addEventListener('submit', async (e) => {
    e.preventDefault();
    const fd = new FormData(form);

    // สร้าง payload
    const payload = {
      hero_id:   fd.get('hero_id'),
      hero_name: fd.get('hero_name'),
      hero_icon: fd.get('hero_icon'),
      items: []
    };
    for (let i = 1; i <= 6; i++) {
      const id = fd.get(`item${i}`);
      if (id) {
        payload.items.push({
          iteminfo: {
            item_id: id,
            icon:    fd.get(`item${i}_icon`)
          }
        });
      }
    }

    // POST ไป backend
    const res = await fetch('/build_set_items', {
      method:  'POST',
      headers: { 'Content-Type': 'application/json' },
      body:    JSON.stringify(payload)
    });
    const data = await res.json();
    if (res.ok) {
      alert(`บันทึกสำเร็จ: ชุดที่ ${data.set}`);
      location.reload();
    } else {
      alert(`Error: ${data.detail || JSON.stringify(data)}`);
    }
  });
});
