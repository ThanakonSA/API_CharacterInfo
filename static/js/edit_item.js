const itemListEl = document.getElementById('itemList');
const formFieldsEl = document.getElementById('formFields');
const editBtn = document.getElementById('editBtn');
const saveBtn = document.getElementById('saveBtn');
const cancelBtn = document.getElementById('cancelBtn');
const formNote = document.getElementById('formNote');
const iconPreview = document.getElementById('iconPreview');
let items = window.items || [];
let selectedItem = null;
let isEditing = false;

// ฟิลด์ที่ต้องการแสดงในฟอร์ม (แก้ไขให้ตรงกับ collection จริง)
const itemFields = [
    "Item_ID", "ItemName", "Type_Item", "Passive", "Price",
    "Physical_Attack", "Magic_Power", "HP", "HP_Regen", "Mana", "Mana_Regen",
    "Physical_Defense", "Magic_Defense", "Lifesteal%", "Spell_Vamp%",
    "Hybrid_Lifesteal%", "Cooldown_Reduction%", "Attack_Speed%", "Adaptive_Attack", "Adaptive_Attack%", 
    "Physical_Penetration", "Physical_Penetration%", "Magic_Penetration", "Magic_Penetration%", 
    "Critical_Chance%", "Critical_Damage%", "Critical_Damage_Reduction%", "Movement_Speed", "Movement_Speed%", 
    "Slow_Reduction%", "Healing_Effect%"
];

// แสดงรายชื่อไอเทมด้านซ้าย
function renderItemList() {
    itemListEl.innerHTML = '';
    items.forEach((item, idx) => {
        const li = document.createElement('li');
        li.className = 'item-item' + (selectedItem && selectedItem.Item_ID === item.Item_ID ? ' selected' : '');
        li.onclick = () => selectItem(idx);
        li.innerHTML = `
            <img class="item-img" src="${item.Icon_Item || '/static/icons/default_item.png'}" alt="">
            <div class="item-name">${item.ItemName || ''}</div>
        `;
        itemListEl.appendChild(li);
    });
}

// เลือกไอเทม
function selectItem(idx) {
    selectedItem = items[idx];
    isEditing = false;
    renderItemList();
    renderForm(selectedItem);
    editBtn.style.display = '';
    saveBtn.style.display = 'none';
    cancelBtn.style.display = 'none';
    formNote.innerHTML = 'ข้อมูลในฟอร์มนี้ดึงจาก MongoDB collection itemsInfos';
    iconPreview.src = selectedItem.Icon_Item || '/static/icons/default_item.png';
}

// แสดงฟอร์ม
function renderForm(item) {
    let html = '';
    for (let i = 0; i < itemFields.length; i += 5) {
        html += '<div class="form-row">';
        for (let j = i; j < i + 5 && j < itemFields.length; j++) {
            const field = itemFields[j];
            html += `
                <div class="form-group">
                    <label>${field}</label>
                    <input name="${field}" value="${item[field] || ''}" ${isEditing ? '' : 'readonly'}>
                </div>
            `;
        }
        html += '</div>';
    }
    formFieldsEl.innerHTML = html;
}

// เปิดโหมดแก้ไข
editBtn.addEventListener('click', () => {
    isEditing = true;
    renderForm(selectedItem);
    editBtn.style.display = 'none';
    saveBtn.style.display = '';
    cancelBtn.style.display = '';
    formNote.innerHTML = 'กด SAVE เพื่อบันทึก กด CANCEL เพื่อยกเลิก';
});

// ยกเลิกการแก้ไข
cancelBtn.addEventListener('click', () => {
    isEditing = false;
    renderForm(selectedItem);
    editBtn.style.display = '';
    saveBtn.style.display = 'none';
    cancelBtn.style.display = 'none';
    formNote.innerHTML = 'ยกเลิกการแก้ไขแล้ว';
});

// กด SAVE
document.getElementById('editItemForm').onsubmit = async function(e) {
    e.preventDefault();
    if (!isEditing) return;
    const formData = new FormData(e.target);
    const data = {};
    itemFields.forEach(f => data[f] = formData.get(f));
    // ส่ง PUT ไป backend (คุณต้องสร้าง API สำหรับอัปเดต)
    const res = await fetch(`/items/${selectedItem.Item_ID}`, {
        method: 'PUT',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify(data)
    });
    if (res.ok) {
        Object.assign(selectedItem, data);
        isEditing = false;
        renderForm(selectedItem);
        editBtn.style.display = '';
        saveBtn.style.display = 'none';
        cancelBtn.style.display = 'none';
        formNote.innerHTML = 'บันทึกสำเร็จ!';
    } else {
        formNote.innerHTML = 'เกิดข้อผิดพลาดในการบันทึก';
    }
};

// เริ่มต้น
if (items.length > 0) {
    renderItemList();
    selectItem(0);
}