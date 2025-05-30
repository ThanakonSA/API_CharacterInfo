// static/edit_heroes.js

const heroSelect = document.getElementById('heroSelect');
const heroSidebar = document.getElementById('heroSidebar');
const formFields = document.getElementById('formFields');
const form = document.getElementById('heroForm');
const editBtn = document.getElementById('editBtn');
const saveBtn = document.getElementById('saveBtn');
const cancelBtn = document.getElementById('cancelBtn');

let heroes = window.heroes || [];
let currentHero = null;
let originalData = {};

const fields = [
  "Hero_ID", "HeroName", "Role", "Specialty", "Lane_Recc",
  "Basic_attack_type", "Price_Battle_Points", "Price_Diamonds", "Price_hero_fragments", "Price_Tickets",
  "Price_lucky_gem", "PassiveName", "PassiveDetail", "Skill_1_Name", "Skill_1_Detail",
  "Skill_2_Name", "Skill_2_Detail", "Skill_3_Name", "Skill_3_Detail",
  "Skill_4_Name", "Skill_4_Detail", "Swap_Skill_1_Name", "Swap_Skill_1_Detail",
  "Swap_Skill_2_Name", "Swap_Skill_2_Detail", "Swap_Skill_3_Name", "Swap_Skill_3_Detail",
  "Durability", "Offense", "Control_effects", "Difficulty", "HP", "HP_Regen",
  "Armor_HP", "Mana", "Mana_Regen", "Energy", "Energy_Regen",
  "Physical_Attack", "Magic_Power", "Physical_Defense", "Magic_Defense",
  "Attack_Speed", "Attack_Speed_Ratio%", "Critical_Chance%", "Critical_Damage%", 
  "Movement_Speed", "Basic_Attack_Range"
];

// สร้าง sidebar แสดงฮีโร่
function renderSidebar(selectedId) {
  heroSidebar.innerHTML = "";
  heroes.forEach(hero => {
    const div = document.createElement("div");
    div.className = "sidebar-hero" + (hero.Hero_ID === selectedId ? " selected" : "");
    div.innerHTML = `
      <div class="arrow" style="display:${hero.Hero_ID === selectedId ? 'block' : 'none'};">
        <svg width="40" height="40"><polygon points="0,20 30,5 30,35" fill="#4ed0ff"/></svg>
      </div>
      <img class="hero-img" src="${hero.icon ? hero.icon : '/static/icons/default.png'}" alt="">
      <div class="hero-name">${hero.HeroName ? hero.HeroName : ''}</div>
    `;
    div.onclick = () => selectHero(hero.Hero_ID);
    heroSidebar.appendChild(div);
  });
}

// โหลดข้อมูลฮีโร่ทั้งหมด
async function loadHeroes() {
  const res = await fetch("/heroesmain");
  heroes = await res.json();
  if (heroes.length > 0) {
    renderSidebar(heroes[0].Hero_ID);
    await selectHero(heroes[0].Hero_ID);
  }
}

// เลือกฮีโร่และโหลดข้อมูลมาแสดงในฟอร์ม
async function selectHero(idx) {
    selectedHero = heroes[idx];
    isEditing = false;
    renderHeroList();
    renderForm(selectedHero);
    editBtn.style.display = '';
    saveBtn.style.display = 'none';
    cancelBtn.style.display = 'none';
    formNote.innerHTML = 'ข้อความในฟอร์มนี้ดึงข้อมูลใน mongodb มาแสดงโดยใช้ Hero_ID เป็นตัวตั้ง';
    // แสดงไอคอน
    document.getElementById('heroIconPreview').src = selectedHero.icon || '/static/icons/default.png';
}

// แสดงข้อมูลในฟอร์ม
function renderForm(data) {
  formFields.innerHTML = "";
  let row;
  Object.keys(data).forEach((key, idx) => {
    if (["icon", "Imagehero"].includes(key)) return; // ไม่ต้องแสดง path รูปในฟอร์ม
    if (idx % 5 === 0) {
      row = document.createElement("div");
      row.className = "form-row";
      formFields.appendChild(row);
    }
    const group = document.createElement("div");
    group.className = "form-group";
    const label = document.createElement("label");
    label.textContent = key;
    const input = document.createElement("input");
    input.type = "text";
    input.name = key;
    input.value = data[key] || "";
    input.disabled = true;
    group.appendChild(label);
    group.appendChild(input);
    row.appendChild(group);
  });
}

function toggleEditMode(editMode) {
  const inputs = formFields.querySelectorAll("input");
  inputs.forEach(input => input.disabled = !editMode || input.name === "Hero_ID");
  editBtn.style.display = editMode ? "none" : "inline";
  saveBtn.style.display = editMode ? "inline" : "none";
  cancelBtn.style.display = editMode ? "inline" : "none";
}

editBtn.addEventListener("click", () => {
  toggleEditMode(true);
});

cancelBtn.addEventListener("click", () => {
  renderForm(originalData);
  toggleEditMode(false);
});

saveBtn.addEventListener("click", async (e) => {
  e.preventDefault();
  const inputs = formFields.querySelectorAll("input");
  const data = {};
  inputs.forEach(input => data[input.name] = input.value);
  const res = await fetch(`/edit_heroes?id=${data["Hero_ID"]}`, {
    method: "PUT",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data)
  });
  if (res.ok) {
    alert("บันทึกเรียบร้อย");
    toggleEditMode(false);
    originalData = JSON.parse(JSON.stringify(data));
  } else {
    alert("เกิดข้อผิดพลาด");
  }
});

// เรียกครั้งแรก
if (heroes.length > 0) {
  renderSidebar(heroes[0].Hero_ID);
  selectHero(heroes[0].Hero_ID);
}
