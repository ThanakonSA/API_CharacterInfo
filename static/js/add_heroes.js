function setupPreview(inputName, imgId) {
  const inp = document.querySelector(`input[name="${inputName}"]`);
  const img = document.getElementById(imgId);
  inp.addEventListener("change", () => {
    const file = inp.files[0];
    if (file) {
      img.src = URL.createObjectURL(file);
    }
  });
}

[
  ["iconhero",        "preview-iconhero"],
  ["imagehero",       "preview-imagehero"],
  ["passive_icon",    "preview-passive"],
  ["skill_1_icon",    "preview-s1"],
  ["skill_2_icon",    "preview-s2"],
  ["skill_3_icon",    "preview-s3"],
  ["skill_4_icon",    "preview-s4"],
  ["swap_skill_1_icon","preview-sw1"],
  ["swap_skill_2_icon","preview-sw2"],
  ["swap_skill_3_icon","preview-sw3"],
].forEach(([field, imgId]) => setupPreview(field, imgId));

// AJAX submit
document.getElementById("form-add-hero")
  .addEventListener("submit", async function(e) {
    e.preventDefault();
    const form = e.target;
    const fd = new FormData(form);

    const res = await fetch("/add_heroes", {
      method: "POST",
      body: fd
    });

    if (res.ok) {
      alert("เพิ่มฮีโร่สำเร็จ 🎉");
      form.reset();
      document.querySelectorAll(".preview-img").forEach(img => img.src = "");
    } else {
      const err = await res.json().catch(() => null);
      alert("เกิดข้อผิดพลาด: " + (err?.detail || res.statusText));
    }
  });
