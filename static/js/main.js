// Namespace based AJAX for cookie-based JWT
const fetchOpts = (method, body) => ({
  method,
  credentials: 'include',
  headers: { 'Content-Type': 'application/json' },
  body: body ? JSON.stringify(body) : undefined
});

document.addEventListener('DOMContentLoaded', () => {
  // Fetch and render todos
  async function loadTodos() {
    const res = await fetch('/api/todo/', fetchOpts('GET'));
    const data = await res.json();
    const tbody = document.getElementById('todoTableBody');
    tbody.innerHTML = '';
    data.forEach(t => {
      const tr = document.createElement('tr');
      tr.innerHTML = `
        <td><a href="/todos/${t.id}">${t.key}</a></td>
        <td>${t.title}</td>
        <td>${t.type}</td>
        <td>${t.status}</td>
        <td>${t.epic || '—'}</td>
        <td>${t.assignee || '—'}</td>`;
      tbody.appendChild(tr);
    });
  }

  // Load epics into modal select
  async function loadEpics() {
    const res = await fetch('/api/todo/epics', fetchOpts('GET'));
    const data = await res.json();
    const select = document.getElementById('epicSelect');
    select.innerHTML = '<option value="">None</option>' + data.map(e => `<option value="${e.id}">${e.key}</option>`).join('');
  }

  loadTodos(); loadEpics();

  // Show modal
  const newBtn = document.getElementById('newTodoBtn');
  const modal = new bootstrap.Modal(document.getElementById('todoModal'));
  newBtn.addEventListener('click', () => {
    document.getElementById('todoForm').reset();
    modal.show();
  });

  // Type change toggles parent_task
  document.getElementById('typeSelect').addEventListener('change', e => {
    const val = e.target.value;
    document.getElementById('parentTaskGroup').classList.toggle('d-none', val!=='sub-task');
    document.getElementById('epicSelectGroup').classList.toggle('d-none', val==='epic');
  });

  // Save
  document.getElementById('saveTodoBtn').addEventListener('click', async () => {
    const form = document.getElementById('todoForm');
    const obj = Object.fromEntries(new FormData(form));
    await fetch('/api/todo/', fetchOpts('POST', obj));
    modal.hide(); loadTodos();
  });
});