"use strict";

/* ============ tiny helpers ============ */
const $ = (sel, el = document) => el.querySelector(sel);
const el = (tag, cls, html) => {
  const n = document.createElement(tag);
  if (cls) n.className = cls;
  if (html != null) n.innerHTML = html;
  return n;
};
const esc = (s) => String(s == null ? "" : s)
  .replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
const enc = (p) => p.split("/").map(encodeURIComponent).join("/");

async function loadJSON(name) {
  const r = await fetch(`data/${name}`);
  if (!r.ok) throw new Error(`load ${name} failed: ${r.status}`);
  return r.json();
}

/* ============ global state ============ */
const DB = {};                 // loaded json
const state = { selected: [] }; // shared order selection across pages

/* ============ toast ============ */
function toast(msg) {
  const wrap = $("#toasts");
  const t = el("div", "toast", esc(msg));
  wrap.appendChild(t);
  setTimeout(() => { t.style.opacity = "0"; t.style.transition = "opacity .3s"; }, 2000);
  setTimeout(() => t.remove(), 2400);
}

/* ============ modal ============ */
function openModal(html) {
  $("#modal").innerHTML = html;
  $("#modal-mask").classList.add("show");
}
function closeModal() { $("#modal-mask").classList.remove("show"); }
$("#modal-mask").addEventListener("click", (e) => {
  if (e.target === $("#modal-mask")) closeModal();
});

/* ============ patient banner ============ */
function renderPatientBanner() {
  const p = DB.patient;
  $("#patient-banner").innerHTML = `
    <div class="patient-card">
      <h3>👤 ${esc(p.name)}　<span style="opacity:.85;font-weight:500;font-size:1rem">${esc(p.gender)} · ${esc(p.age)}岁</span></h3>
      <div class="patient-info">
        <div class="pi-item"><span class="pi-label">门诊号</span><span class="pi-value">${esc(p.patient_id)}</span></div>
        <div class="pi-item"><span class="pi-label">就诊科室</span><span class="pi-value">${esc(p.department)}</span></div>
        <div class="pi-item"><span class="pi-label">就诊类型</span><span class="pi-value">${esc(p.visit_type)}</span></div>
        <div class="pi-item"><span class="pi-label">就诊日期</span><span class="pi-value">${esc(p.visit_date)}</span></div>
      </div>
      <div class="patient-cc">
        <span class="pi-label">主诉</span>
        <span class="cc">${esc(p.chief_complaint)}</span>
      </div>
    </div>`;
}

/* ============ page 1: 问诊 ============ */
function page1() {
  const v = $("#view");
  v.innerHTML = "";
  v.appendChild(el("h2", "page-title", "🩺 问诊"));

  // status panel
  v.appendChild(el("div", "status-panel",
    `<div class="rec"><span class="recording-dot"></span> 实时录音中…</div>
     <div class="searching">AI 检索相似病例中</div>`));

  // dialogue summary
  v.appendChild(el("div", "subheader", "对话摘要"));
  v.appendChild(el("div", "caption", "以下内容完全引用自原句要点"));
  const box = el("div", "card");
  DB.transcript.slice(-5).forEach((m) => {
    box.appendChild(el("div", "dialogue-line",
      `<b style="color:${m.role === "医生" ? "#028090" : "#764ba2"}">${esc(m.role)}</b>　${esc(m.text)}`));
  });
  v.appendChild(box);

  v.appendChild(el("hr", "divider"));

  // similar cases
  v.appendChild(el("div", "subheader", "🔗 相似病例"));
  DB.similar_cases.forEach((c) => v.appendChild(caseCard(c)));
}

function caseCard(c) {
  const card = el("div", "card");
  card.style.marginBottom = "1rem";
  card.appendChild(el("div", "case-head",
    `<span>${esc(c.patient_name)}　${esc(c.gender)} · ${esc(c.age)}　${esc(c.department)}</span>
     <span class="sim-badge">相似度 ${Math.round((c.similarity || 0) * 100)}%</span>`));
  const rows = [
    ["主诉", c.chief_complaint], ["现病史", c.history_present], ["既往史", c.history_past],
    ["中医四诊", c.tcm_diagnosis_info], ["体格检查", c.physical_exam], ["生命体征", c.vital_signs],
    ["西医诊断", c.western_diagnosis], ["中医诊断", c.tcm_diagnosis], ["辅助检查", c.auxiliary_exam],
    ["药品处方", c.prescription], ["建议", c.advice], ["治疗效果", c.treatment_effect],
    ["相似点", c.similar_points], ["不同点", c.different_points],
  ];
  rows.forEach(([k, val]) => {
    if (!val) return;
    card.appendChild(el("div", "case-row",
      `<div class="lbl">${esc(k)}</div><div class="val">${esc(val)}</div>`));
  });
  return card;
}

/* ============ page 2: 开检查 ============ */
function page2() {
  const v = $("#view");
  v.innerHTML = "";
  v.appendChild(el("h2", "page-title", "📝 开检查"));

  const search = el("input", "search");
  search.placeholder = "输入关键词快速查找检查项目…";
  v.appendChild(search);
  v.appendChild(el("div", "", "<div style='height:.8rem'></div>"));

  const listWrap = el("div", "");
  v.appendChild(listWrap);

  const renderList = () => {
    const q = search.value.trim();
    let orders = [...DB.orders_ranked].sort((a, b) => (a.order || 999) - (b.order || 999));
    if (q) orders = orders.filter((o) => (o.order_name || "").includes(q));
    listWrap.innerHTML = "";
    if (!orders.length) { listWrap.appendChild(el("div", "info-box", "未找到匹配的检查项目")); return; }
    listWrap.appendChild(el("div", "h3", `检查项目列表 (${orders.length})`));
    const grid = el("div", "grid-2");
    orders.forEach((o) => {
      const name = o.order_name || "";
      const row = el("label", "order-item");
      const checked = state.selected.includes(name) ? "checked" : "";
      row.innerHTML =
        `<input type="checkbox" ${checked} />
         <div class="oname">${esc(name)}<div class="oreason">${esc(o.reason || "")}</div></div>
         <span class="pill ${esc(o.priority)}">${esc(o.priority)}</span>`;
      const cb = $("input", row);
      cb.addEventListener("change", () => {
        if (cb.checked && !state.selected.includes(name)) state.selected.push(name);
        else if (!cb.checked) state.selected = state.selected.filter((x) => x !== name);
      });
      grid.appendChild(row);
    });
    listWrap.appendChild(grid);
  };
  search.addEventListener("input", renderList);
  renderList();

  v.appendChild(el("hr", "divider"));
  const submit = el("button", "btn primary", "提交检查申请");
  submit.addEventListener("click", () => {
    if (!state.selected.length) { toast("⚠️ 请至少选择一项检查项目"); return; }
    showOrderWarnings();
  });
  v.appendChild(submit);
}

function showOrderWarnings() {
  const rules = DB.order_check_rules;
  const selected = state.selected;
  const patientText = DB.transcript.filter((m) => m.role === "病人").map((m) => m.text).join(" ");

  // conflicts
  const conflicts = [];
  (rules.conflicts || []).forEach((c) => {
    const inGroup = (c.items || []).filter((it) => selected.includes(it));
    if (inGroup.length >= 2) conflicts.push({ group: c.group, items: inGroup });
  });
  // missing
  let missing = [];
  (rules.missing_checks || []).forEach((m) => {
    if (!selected.includes(m.missing_item) &&
        (m.symptom_keywords || []).some((kw) => patientText.includes(kw))) {
      missing.push({ item: m.missing_item, priority: m.priority });
    }
  });
  const order = { "高": 1, "中": 2, "低": 3 };
  missing.sort((a, b) => (order[a.priority] || 4) - (order[b.priority] || 4));

  const hasIssues = conflicts.length || missing.length;
  let html = `<h3>🤖 AI 检查提醒</h3>`;
  if (hasIssues) {
    html += `<div class="h4">请您再次确认！</div>`;
    if (conflicts.length) {
      html += `<div class="h4">⚠️ 检查项目可能冲突</div>`;
      conflicts.forEach((c) => {
        html += `<div class="card" style="margin-bottom:.6rem"><b>${esc(c.group)}</b><br>
          <span style="color:var(--muted)">冲突项目：${esc(c.items.join("、"))}</span></div>`;
      });
    }
    if (missing.length) {
      html += `<div class="h4">🔍 可能遗漏的检查</div>`;
      const color = { "高": "var(--red)", "中": "var(--orange)", "低": "var(--muted)" };
      missing.forEach((m) => {
        html += `<div class="card" style="margin-bottom:.6rem">
          <b style="color:${color[m.priority] || "#333"}">${esc(m.item)}</b>
          <span class="pill ${esc(m.priority)}" style="margin-left:.5rem">${esc(m.priority)}</span></div>`;
      });
    }
    html += `<hr class="divider">
      <div class="grid-2">
        <button class="btn primary" id="m-go">继续提交</button>
        <button class="btn" id="m-back">返回调整</button>
      </div>`;
  } else {
    html += `<div class="success-box">✓ 未发现需要特别提醒的事项</div>
      <hr class="divider"><button class="btn primary" id="m-go">确认提交</button>`;
  }
  openModal(html);
  const go = $("#m-go");
  if (go) go.addEventListener("click", () => {
    toast("✓ 检查单已提交");
    state.selected = [];
    closeModal();
    page2();
  });
  const back = $("#m-back");
  if (back) back.addEventListener("click", closeModal);
}

/* ============ page 3: 检查结果 ============ */
function page3() {
  const v = $("#view");
  v.innerHTML = "";
  v.appendChild(el("h2", "page-title", "📊 检查结果"));
  v.appendChild(el("div", "subheader", "异常指标"));

  const imgDir = "data/";
  const grid = el("div", "grid-2");

  const col1 = el("div", "");
  col1.appendChild(el("div", "h3", "嗜酸小板数目"));
  col1.appendChild(el("img", "result-img"))
    .setAttribute("src", imgDir + enc("Screenshot 2026-02-01 at 11.28.11.webp"));
  col1.appendChild(el("div", "ref-box",
    `<b>医学参考</b>
     <p><b>正常参考范围</b>：30–350 cells/µL 或 0.04–0.4 × 10⁹/L</p>
     <p><b>当前值</b>：338.0 ×10⁹/L</p>
     <p class="rs">临床意义：嗜酸性粒细胞升高常提示过敏反应，在过敏性鼻炎患者中较为常见。该数值接近正常上限，结合其他指标（如嗜酸性粒细胞比例）综合判断过敏严重程度。</p>
     <p class="rs">参考来源：Cleveland Clinic, WebMD, Medical News Today</p>`));
  grid.appendChild(col1);

  const col2 = el("div", "");
  col2.appendChild(el("div", "h3", "嗜酸板压积"));
  col2.appendChild(el("img", "result-img"))
    .setAttribute("src", imgDir + enc("Screenshot 2026-02-01 at 11.28.19.webp"));
  col2.appendChild(el("div", "ref-box",
    `<b>医学参考</b>
     <p><b>正常参考范围</b>：0.0–6.0%（占白细胞总数的百分比）</p>
     <p><b>当前值</b>：32.00%</p>
     <p class="rs">临床意义：嗜酸性粒细胞比例显著升高强烈提示活跃的过敏性炎症反应。研究表明，该指标升高与过敏性鼻炎的严重程度呈正相关。高比例嗜酸性粒细胞常见于哮喘、过敏性鼻炎、特应性皮炎等过敏性疾病。</p>
     <p class="rs">参考来源：NIH, Healthline, Cleveland Clinic</p>`));
  grid.appendChild(col2);
  v.appendChild(grid);

  v.appendChild(el("hr", "divider"));
  v.appendChild(el("div", "subheader", "原始检查报告"));
  const orig = el("img", "result-img");
  orig.setAttribute("src", imgDir + enc("Screenshot 2026-02-01 at 11.27.59.webp"));
  v.appendChild(orig);
}

/* ============ page 4: 电子病历 ============ */
function firstPatient(pred) {
  for (const m of DB.transcript) if (m.role === "病人" && pred(m.text)) return m.text;
  return "";
}
function buildRecord() {
  const p = DB.patient;
  const t = DB.transcript;
  const chief = firstPatient((x) => x.length > 5 && !x.includes("没有"));
  const present = t.filter((m) => m.role === "病人").map((m) => m.text).join("\n");
  // past history
  let past = "既往体健，否认药敏史";
  for (let i = 0; i < t.length; i++) {
    if (t[i].role === "医生" && /以前|过敏|既往/.test(t[i].text)) {
      const nx = t[i + 1];
      if (nx && nx.role === "病人" && nx.text.trim()) {
        past = nx.text.includes("没有") ? "既往体健，否认药敏史" : nx.text.trim();
      }
      break;
    }
  }
  const physical = "鼻黏膜苍白，双侧下鼻甲肿大，总鼻道可见清水样鼻涕。";
  const vital = "收缩压:120mmHg、舒张压:78mmHg";
  const aux = state.selected.length ? state.selected.join("、") : "过敏原检测、血常规";
  const advice = "避开过敏原，不适随诊。";
  const header =
    `姓名:${p.name}                         性别:${p.gender}                     ` +
    `年龄:${p.age}岁                    门诊号:${p.patient_id} 就诊科室:${p.department}`;
  return [
    header,
    `主诉:         ${chief}`,
    `现病史:       ${present}`,
    `既往史:       ${past}`,
    `体格检查:     ${physical}`,
    `生命体征:     ${vital}`,
    `辅助检查:     ${aux}`,
    `建议:         ${advice}`,
  ].join("\n") + "\n";
}

function page4() {
  const v = $("#view");
  v.innerHTML = "";
  v.appendChild(el("h2", "page-title", "📄 电子病历"));

  const split = el("div", "split");

  // left
  const left = el("div", "");
  left.appendChild(el("div", "subheader", "门诊病历"));
  const ta = el("textarea", "ta");
  ta.value = buildRecord();
  ta.rows = ta.value.split("\n").length + 2;
  ta.style.minHeight = "440px";
  left.appendChild(ta);
  const row = el("div", "btn-row");
  const bCopy = el("button", "btn", "📋 复制病历");
  const bPrint = el("button", "btn", "🖨️ 打印病历");
  const bDown = el("button", "btn", "📥 导出病历");
  bCopy.addEventListener("click", async () => {
    try { await navigator.clipboard.writeText(ta.value); toast("✓ 已复制"); }
    catch { ta.select(); document.execCommand("copy"); toast("✓ 已复制"); }
  });
  bPrint.addEventListener("click", () => {
    const w = window.open("", "_blank");
    w.document.write(`<pre style="font-family:monospace;white-space:pre-wrap;padding:24px">${esc(ta.value)}</pre>`);
    w.document.close(); w.print();
  });
  bDown.addEventListener("click", () => {
    const blob = new Blob([ta.value], { type: "text/markdown" });
    const a = el("a"); a.href = URL.createObjectURL(blob);
    a.download = "medical_record.md"; a.click(); URL.revokeObjectURL(a.href);
    toast("✓ 已导出");
  });
  row.appendChild(bCopy); row.appendChild(bPrint); row.appendChild(bDown);
  left.appendChild(row);
  split.appendChild(left);

  // right
  const right = el("div", "");
  right.appendChild(el("div", "subheader", "🔍 辅助参考"));
  const p = DB.patient;
  right.appendChild(el("div", "card",
    `<b>患者：${esc(p.name)} (${esc(p.gender)})</b><br>
     <span class="caption">年龄：${esc(p.age)}岁 | ID：${esc(p.patient_id)}</span>`));
  right.appendChild(el("div", "h3", "💬 对话原文"));
  const dta = el("textarea", "ta");
  dta.disabled = true;
  dta.style.minHeight = "200px";
  dta.value = DB.transcript.map((m) => m.text).join("\n\n");
  right.appendChild(dta);

  right.appendChild(el("div", "h3", "💡 关键线索"));
  const findings = [];
  (DB.sidebar_support.key_tests || []).forEach((x) => findings.push(x));
  (DB.abnormal_summary.abnormal_items || []).forEach((it) => findings.push(`${it.name}: ${it.value}`));
  const uniq = [...new Set(findings)].slice(0, 6);
  if (uniq.length) uniq.forEach((f) => right.appendChild(el("div", "info-box", esc(f))));
  else right.appendChild(el("div", "caption", "暂无关键线索"));

  split.appendChild(right);
  v.appendChild(split);
}

/* ============ router / nav ============ */
const PAGES = [
  { id: "consult", label: "问诊",   ico: "🩺", step: "01", render: page1 },
  { id: "order",   label: "开检查", ico: "📝", step: "02", render: page2 },
  { id: "result",  label: "查结果", ico: "📊", step: "03", render: page3 },
  { id: "record",  label: "写病历", ico: "📄", step: "04", render: page4 },
];

function buildNav() {
  const nav = $("#nav");
  nav.innerHTML = "";
  PAGES.forEach((p) => {
    const item = el("div", "nav-item");
    item.dataset.id = p.id;
    item.innerHTML = `<span class="ico">${p.ico}</span><span class="lbl">${p.label}</span><span class="nav-step">${p.step}</span>`;
    item.addEventListener("click", () => { location.hash = p.id; });
    nav.appendChild(item);
  });
}

function route() {
  const id = (location.hash || "#consult").slice(1);
  const page = PAGES.find((p) => p.id === id) || PAGES[0];
  document.querySelectorAll(".nav-item").forEach((n) =>
    n.classList.toggle("active", n.dataset.id === page.id));
  page.render();
  window.scrollTo(0, 0);
}
window.addEventListener("hashchange", route);

/* ============ boot ============ */
(async function boot() {
  try {
    const [patient, transcript, similar_cases, orders_ranked, order_check_rules, sidebar_support, abnormal_summary] =
      await Promise.all([
        loadJSON("patient.json"), loadJSON("transcript.json"), loadJSON("similar_cases.json"),
        loadJSON("orders_ranked.json"), loadJSON("order_check_rules.json"),
        loadJSON("sidebar_support.json"), loadJSON("abnormal_summary.json"),
      ]);
    Object.assign(DB, { patient, transcript, similar_cases, orders_ranked, order_check_rules, sidebar_support, abnormal_summary });
    renderPatientBanner();
    buildNav();
    route();
  } catch (e) {
    $("#view").innerHTML = `<div class="warn-box">加载数据失败：${esc(e.message)}</div>`;
  }
})();
