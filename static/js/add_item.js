// แสดง preview icon
const iconInput = document.querySelector('input[name="Icon_Item"]');
const iconPreview = document.getElementById('preview-icon-item');
iconInput.addEventListener("change", () => {
  const file = iconInput.files[0];
  if (file) {
    iconPreview.src = URL.createObjectURL(file);
  }
});

// AJAX submit
document.getElementById("form-add-item")
  .addEventListener("submit", async function(e) {
    e.preventDefault();
    const form = e.target;
    const fd = new FormData(form);

    // แปลงค่าทุก field เป็น string (ยกเว้นไฟล์)
    for (let [k, v] of fd.entries()) {
      if (!(v instanceof File)) {
        fd.set(k, String(v));
      }
    }

    const res = await fetch("/add_item", {
      method: "POST",
      body: fd
    });

    if (res.ok) {
      alert("เพิ่มไอเทมสำเร็จ 🎉");
      form.reset();
      iconPreview.src = "/static/icons/default_item.png";
    } else {
      const err = await res.json().catch(() => null);
      alert("เกิดข้อผิดพลาด: " + (err?.detail || res.statusText));
    }
  });