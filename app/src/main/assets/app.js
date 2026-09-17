(() => {
  const DATA = window.BO4_DATA;
  const ORDER = window.BO4_ORDER;
  const $ = (id) => document.getElementById(id);
  const esc = (s='') => String(s).replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));

  const STORAGE_KEY = 'bo4-guide-v06-state';
  const NOTE_KEY = 'bo4-guide-v06-notes';
  let state = { map:'alpha', step:0, done:{} };
  let notes = {};

  function safeLoad() {
    try {
      const s = JSON.parse(localStorage.getItem(STORAGE_KEY) || '{}');
      if (s && DATA[s.map]) state.map = s.map;
      if (Number.isInteger(s.step)) state.step = s.step;
      if (s.done && typeof s.done === 'object') state.done = s.done;
      notes = JSON.parse(localStorage.getItem(NOTE_KEY) || '{}') || {};
    } catch (_) {}
    ORDER.forEach(k => {
      if (!Array.isArray(state.done[k])) state.done[k] = [];
    });
    clampStep();
  }

  function save() {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(state));
  }
  function saveNotes() {
    localStorage.setItem(NOTE_KEY, JSON.stringify(notes));
  }
  function clampStep() {
    const len = DATA[state.map].steps.length;
    state.step = Math.max(0, Math.min(Number(state.step) || 0, len - 1));
  }
  function isDone(map, i) { return state.done[map].includes(i); }
  function setDone(map, i, val) {
    const set = new Set(state.done[map]);
    val ? set.add(i) : set.delete(i);
    state.done[map] = [...set].sort((a,b)=>a-b);
  }

  function selectMap(k) {
    state.map = k;
    state.step = 0;
    clampStep();
    save();
    render();
    window.scrollTo({top:0, behavior:'smooth'});
  }
  function selectStep(i) {
    state.step = i;
    clampStep();
    save();
    renderStep();
    renderFlow();
    renderProgress();
    window.scrollTo({top:0, behavior:'smooth'});
  }

  function renderTabs() {
    const host = $('mapTabs');
    host.innerHTML = '';
    ORDER.forEach(k => {
      const b = document.createElement('button');
      b.type = 'button';
      b.className = 'tab' + (k === state.map ? ' active' : '');
      b.textContent = DATA[k].name;
      b.addEventListener('click', () => selectMap(k));
      host.appendChild(b);
    });
  }

  function renderHeader() {
    const m = DATA[state.map];
    $('mapName').textContent = m.name;
    $('mapMeta').textContent = `${m.quest} · ${m.difficulty} · ${m.time}`;
    $('source').textContent = `步骤核对：${m.source}`;
    const req = $('requirements');
    req.innerHTML = m.requirements.map(x => `<li>${esc(x)}</li>`).join('');
  }

  function renderProgress() {
    const m = DATA[state.map];
    const complete = state.done[state.map].length;
    $('progressText').textContent = `${complete} / ${m.steps.length} 已完成`;
    $('progressBar').style.width = `${Math.round(complete / m.steps.length * 100)}%`;
  }

  function renderStep() {
    const m = DATA[state.map];
    const s = m.steps[state.step];
    $('stepNo').textContent = `第 ${state.step + 1} / ${m.steps.length} 步`;
    $('stepTitle').textContent = s.title;
    $('stepPlace').textContent = `地点：${s.place}`;
    $('stepAction').textContent = s.action;
    $('stepSuccess').textContent = s.success;
    $('stepTips').textContent = s.tips || '—';
    $('prevBtn').disabled = state.step === 0;
    $('nextBtn').textContent = state.step === m.steps.length - 1 ? '标记完成' : '完成这一步 →';
    $('doneBtn').textContent = isDone(state.map, state.step) ? '✓ 已完成（点此取消）' : '标记当前步骤完成';
    $('doneBtn').classList.toggle('done-active', isDone(state.map, state.step));
  }

  function renderFlow() {
    const host = $('flow');
    host.innerHTML = '';
    DATA[state.map].steps.forEach((s, i) => {
      const row = document.createElement('button');
      row.type = 'button';
      row.className = 'flow-row' + (i === state.step ? ' current' : '') + (isDone(state.map, i) ? ' done' : '');
      const mark = isDone(state.map, i) ? '✓' : String(i + 1);
      row.innerHTML = `<span class="flow-num">${mark}</span><span class="flow-copy"><b>${esc(s.title)}</b><small>${esc(s.place)}</small></span>`;
      row.addEventListener('click', () => selectStep(i));
      host.appendChild(row);
    });
  }

  function renderNotes() {
    $('notes').value = notes[state.map] || '';
  }

  function renderSearch() {
    const q = $('search').value.trim().toLowerCase();
    const box = $('searchResults');
    box.innerHTML = '';
    if (!q) { box.hidden = true; return; }
    const hits = [];
    ORDER.forEach(k => DATA[k].steps.forEach((s,i) => {
      const hay = `${DATA[k].name} ${DATA[k].english} ${s.title} ${s.place} ${s.action} ${s.tips}`.toLowerCase();
      if (hay.includes(q)) hits.push({k,i,s});
    }));
    box.hidden = false;
    if (!hits.length) {
      box.innerHTML = '<div class="search-empty">没搜到。可试：电视、时钟、蓝石、盾牌、图腾、强化机。</div>';
      return;
    }
    hits.slice(0, 30).forEach(h => {
      const b = document.createElement('button');
      b.type = 'button';
      b.className = 'search-hit';
      b.innerHTML = `<b>${esc(DATA[h.k].name)} · ${esc(h.s.title)}</b><small>${esc(h.s.place)}</small>`;
      b.addEventListener('click', () => {
        state.map = h.k; state.step = h.i; save(); $('search').value = ''; render(); box.hidden = true;
      });
      box.appendChild(b);
    });
  }

  function render() {
    clampStep();
    renderTabs();
    renderHeader();
    renderProgress();
    renderStep();
    renderFlow();
    renderNotes();
  }

  $('prevBtn').addEventListener('click', () => { if (state.step > 0) selectStep(state.step - 1); });
  $('nextBtn').addEventListener('click', () => {
    setDone(state.map, state.step, true);
    if (state.step < DATA[state.map].steps.length - 1) state.step++;
    save(); render(); window.scrollTo({top:0, behavior:'smooth'});
  });
  $('doneBtn').addEventListener('click', () => {
    setDone(state.map, state.step, !isDone(state.map, state.step));
    save(); renderStep(); renderFlow(); renderProgress();
  });
  $('resetBtn').addEventListener('click', () => {
    if (confirm(`清空“${DATA[state.map].name}”的完成进度？记事不会删除。`)) {
      state.done[state.map] = []; state.step = 0; save(); render();
    }
  });
  $('notes').addEventListener('input', (e) => {
    notes[state.map] = e.target.value; saveNotes();
    $('noteStatus').textContent = '已保存';
    clearTimeout(window.__noteTimer);
    window.__noteTimer = setTimeout(() => $('noteStatus').textContent = '自动保存', 900);
  });
  $('search').addEventListener('input', renderSearch);
  $('searchClear').addEventListener('click', () => { $('search').value=''; renderSearch(); $('search').focus(); });

  safeLoad();
  render();
})();