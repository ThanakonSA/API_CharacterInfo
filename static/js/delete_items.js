window.addEventListener('DOMContentLoaded', () => {
  document.querySelectorAll('.btn-delete').forEach(btn => {
    btn.addEventListener('click', async () => {
      if (!confirm('ยืนยันการลบไอเทมนี้?')) return;
      const card = btn.closest('.card');
      const itemId = card.getAttribute('data-item-id');
      try {
        const res = await fetch(`/delete_items/${itemId}`, { method: 'DELETE' });
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