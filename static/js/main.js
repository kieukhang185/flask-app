const fetchOpts = (method, body) => ({
  method,
  credentials: 'include',
  headers: { 'Content-Type': 'application/json' },
  body: body ? JSON.stringify(body) : undefined
});

// Fetch all users once and build a map of id->username
async function loadUsers() {
  const res = await fetch('/api/user/', fetchOpts('GET'));
  if (!res.ok) {
    console.error('Failed to load users:', res.status);
    return {};
  }
  const users = await res.json();
  const map = {};
  users.forEach(u => {
    map[u.id] = u.username || u.email || u.id;
  });
  return map;
}

document.addEventListener('DOMContentLoaded', async () => {
  // Load user map before rendering ToDos
  const usersMap = await loadUsers();

  // ——— Load and render all ToDos ———
  async function loadTodos() {
    const res = await fetch('/api/todo/', fetchOpts('GET'));
    if (!res.ok) {
      console.error('Failed to load todos:', res.status);
      return;
    }
    const todos = await res.json();
    const tbody = document.getElementById('todoTableBody');
    tbody.innerHTML = '';
    todos.forEach(t => {
      // Use username from map, fallback to raw id or dash
      const assigneeDisplay = t.assignee ? (usersMap[t.assignee] || t.assignee) : '—';
      const reporterDisplay = t.reporter ? (usersMap[t.reporter] || t.reporter) : '—';

      const tr = document.createElement('tr');
      tr.innerHTML = `
        <td><a href="/todos/${t.id}">${t.key}</a></td>
        <td>${t.title}</td>
        <td>${t.type}</td>
        <td>${t.status}</td>
        <td>${t.epic || '—'}</td>
        <td>${assigneeDisplay}</td>
        <td>${reporterDisplay}</td>
        <td>
          <button class="btn btn-sm btn-outline-primary assign-btn" data-id="${t.id}">
            Assign to Me
          </button>
        </td>
      `;
      tbody.appendChild(tr);
    });
  }

  // ——— Load Epics into the modal’s Epic dropdown ———
  async function loadEpics() {
    const res = await fetch('/api/todo/epics', fetchOpts('GET'));
    if (!res.ok) {
      console.error('Failed to load epics:', res.status);
      return;
    }
    const epics = await res.json();
    const select = document.getElementById('epicSelect');
    select.innerHTML =
      '<option value="">None</option>' +
      epics.map(e => `<option value="${e.id}">${e.key}</option>`).join('');
  }

  // ——— Load Tasks for Sub-Task parent dropdown ———
  async function loadParentTasks() {
    const res = await fetch('/api/todo/', fetchOpts('GET'));
    if (!res.ok) {
      console.error('Failed to load tasks:', res.status);
      return;
    }
    const todos = await res.json();
    const tasks = todos.filter(t => t.type === 'task');
    const select = document.getElementById('parentTaskSelect');
    select.innerHTML =
      '<option value="">Select Task</option>' +
      tasks.map(t => `<option value="${t.id}">${t.key}</option>`).join('');
  }

  // Initial loads
  await loadTodos();
  loadEpics();
  loadParentTasks();

  // ——— Modal setup ———
  const todoModalEl = document.getElementById('todoModal');
  const todoModal = new bootstrap.Modal(todoModalEl);
  document.getElementById('newTodoBtn').addEventListener('click', () => {
    document.getElementById('todoForm').reset();
    document.getElementById('parentTaskGroup').classList.add('d-none');
    document.getElementById('epicSelectGroup').classList.remove('d-none');
    todoModal.show();
  });

  // Toggle fields when Type changes
  document.getElementById('typeSelect').addEventListener('change', e => {
    const type = e.target.value;
    document.getElementById('parentTaskGroup').classList.toggle('d-none', type !== 'sub-task');
    document.getElementById('epicSelectGroup').classList.toggle('d-none', type === 'epic');
  });

  // ——— Save a new ToDo ———
  document.getElementById('saveTodoBtn').addEventListener('click', async () => {
    const form = document.getElementById('todoForm');
    const payload = Object.fromEntries(new FormData(form));
    const res = await fetch('/api/todo/', fetchOpts('POST', payload));
    if (res.ok) {
      todoModal.hide();
      await loadTodos();
      loadParentTasks();
      loadEpics();
    } else {
      console.error('Failed to save ToDo:', res.status);
    }
  });

  // ——— Delegate Assign-to-Me button clicks ———
  document.getElementById('todoTableBody').addEventListener('click', async (e) => {
    if (e.target.classList.contains('assign-btn')) {
      const id = e.target.dataset.id;
      const res = await fetch(`/api/todo/${id}/assign`, fetchOpts('POST'));
      if (res.ok) {
        const updated = await res.json();
        // Update assignee cell in-place
        const row = e.target.closest('tr');
        row.children[5].textContent = usersMap[updated.assignee] || updated.assignee || '—';
        e.target.disabled = true;
      } else {
        console.error('Failed to assign ToDo:', res.status);
      }
    }
  });
});
