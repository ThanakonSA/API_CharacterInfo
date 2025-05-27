// static/js/delete_set_items.js
window.addEventListener('DOMContentLoaded', () => {
  document.querySelectorAll('.btn-delete').forEach(btn => {
   btn.addEventListener('click', async () => {
     if (!confirm('ยืนยันการลบชุดนี้?')) return;
     const card  = btn.closest('.card');
     const docId = card.getAttribute('data-id');
     try {
       const res = await fetch(`/delete_set_items/${docId}`, { method: 'DELETE' });
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
