const API_BASE = "http://localhost:8000";

// Состояние приложения
let currentUser = null;

// DOM элементы
const authScreen = document.getElementById('auth-screen');
const workspace = document.getElementById('workspace');
const phoneInput = document.getElementById('phone-input');
const codeInput = document.getElementById('code-input');
const codeInputContainer = document.getElementById('code-input-container');
const authMsg = document.getElementById('auth-msg');
const tasksGrid = document.getElementById('tasks-grid');
const btnRequestCode = document.getElementById('btn-request-code');
const btnVerifyCode = document.getElementById('btn-verify-code');
const btnAddTask = document.getElementById('btn-add-task');

// Инициализация
document.addEventListener('DOMContentLoaded', () => {
    btnRequestCode.addEventListener('click', requestAuthCode);
    btnVerifyCode.addEventListener('click', verifyAuthCode);
    btnAddTask.addEventListener('click', () => {
        // В реальности откроется модалка, сейчас пока просто алерт
        alert("Функция добавления через веб-интерфейс будет доступна в следующей версии");
    });
});

async function requestAuthCode() {
    const phone = phoneInput.value;
    if (!phone) {
        authMsg.innerText = "Введите номер телефона";
        return;
    }

    try {
        const response = await fetch(`${API_BASE}/auth/request`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ phone })
        });
        const data = await response.json();
        
        if (response.ok) {
            codeInputContainer.classList.remove('hidden');
            authMsg.innerText = "Код отправлен!";
            authMsg.classList.replace('text-red-500', 'text-green-500');
        } else {
            authMsg.innerText = data.message || "Ошибка";
        }
    } catch (e) {
        authMsg.innerText = "Ошибка соединения с сервером";
    }
}

async function verifyAuthCode() {
    const phone = phoneInput.value;
    const code = codeInput.value;

    try {
        const response = await fetch(`${API_BASE}/auth/verify`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ phone, code })
        });
        const data = await response.json();

        if (response.ok) {
            currentUser = data.user_id;
            showWorkspace();
        } else {
            authMsg.innerText = data.message || "Неверный код";
            authMsg.classList.replace('text-green-500', 'text-red-500');
        }
    } catch (e) {
        authMsg.innerText = "Ошибка соединения с сервером";
    }
}

function showWorkspace() {
    authScreen.classList.add('hidden');
    workspace.classList.remove('hidden');
    fetchTasks();
}

async function fetchTasks() {
    try {
        const response = await fetch(`${API_BASE}/tasks`);
        const tasks = await response.json();
        renderTasks(tasks);
    } catch (e) {
        console.error("Ошибка загрузки задач", e);
    }
}

function renderTasks(tasks) {
    tasksGrid.innerHTML = '';
    if (tasks.length === 0) {
        tasksGrid.innerHTML = '<p class="col-span-full text-center text-gray-500 p-10">Задач пока нет. Добавьте первую через Telegram!</p>';
        return;
    }

    tasks.forEach(task => {
        const card = document.createElement('div');
        card.className = "task-card bg-white p-6 rounded-xl shadow-md border hover:border-blue-400";
        card.innerHTML = `
            <div class="flex justify-between items-start mb-2">
                <h3 class="font-bold text-lg">${task.title}</h3>
                <span class="text-xs bg-blue-100 text-blue-800 px-2 py-1 rounded">${new Date(task.due_date).toLocaleDateString()}</span>
            </div>
            <p class="text-gray-600 text-sm mb-4">${task.description || ''}</p>
            <div class="flex items-center">
                <input type="checkbox" ${task.is_completed ? 'checked' : ''} class="mr-2">
                <span class="text-sm text-gray-500">Выполнено</span>
            </div>
        `;
        tasksGrid.appendChild(card);
    });
}
