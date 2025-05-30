window.addEventListener('DOMContentLoaded', () => {
  document.querySelectorAll('.btn-delete').forEach(btn => {
    btn.addEventListener('click', async () => {
      if (!confirm('ยืนยันการลบฮีโร่นี้?')) return;
      const card = btn.closest('.card');
      const heroId = card.getAttribute('data-hero-id');
      try {
        const res = await fetch(`/delete_heroes/${heroId}`, { method: 'DELETE' });
        if (!res.ok) {
          const err = await res.json();
          alert(`ลบไม่สำเร็จ: ${err.detail || err}`);
        } else {
          card.remove();
        }
      } catch (e) {
        alert('เกิดข้อผิดพลาด: ' + e.message);
      }
    });
  });
});