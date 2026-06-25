// API Configuration
const API_BASE_URL = 'http://127.0.0.1:5000/api';

// State Management
let todos = [];
let currentFilter = 'all';

// DOM Elements
const todoTitleInput = document.getElementById('todoTitle');
const todoDescriptionInput = document.getElementById('todoDescription');
const addBtn = document.getElementById('addBtn');
const todoList = document.getElementById('todoList');
const emptyState = document.getElementById('emptyState');
const filterBtns = document.querySelectorAll('.filter-btn');
const totalCount = document.getElementById('totalCount');
const activeCount = document.getElementById('activeCount');
const completedCount = document.getElementById('completedCount');
const toast = document.getElementById('toast');

// Initialize App
document.addEventListener('DOMContentLoaded', () => {
    loadTodos();
    setupEventListeners();
});

// Event Listeners
function setupEventListeners() {
    // Add todo button
    addBtn.addEventListener('click', handleAddTodo);
    
    // Enter key in title input
    todoTitleInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            handleAddTodo();
        }
    });
    
    // Filter buttons
    filterBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            currentFilter = btn.dataset.filter;
            filterBtns.forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            renderTodos();
        });
    });
}

// API Functions
async function loadTodos() {
    try {
        showLoading();
        const response = await fetch(`${API_BASE_URL}/todos`);
        
        if (!response.ok) {
            throw new Error('Failed to load todos');
        }
        
        todos = await response.json();
        renderTodos();
        updateStats();
    } catch (error) {
        console.error('Error loading todos:', error);
        showToast('Failed to load todos', 'error');
    } finally {
        hideLoading();
    }
}

async function createTodo(title, description) {
    try {
        const response = await fetch(`${API_BASE_URL}/todos`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                title: title,
                description: description
            })
        });
        
        if (!response.ok) {
            throw new Error('Failed to create todo');
        }
        
        const newTodo = await response.json();
        todos.unshift(newTodo);
        renderTodos();
        updateStats();
        showToast('Todo added successfully!', 'success');
        
        return newTodo;
    } catch (error) {
        console.error('Error creating todo:', error);
        showToast('Failed to add todo', 'error');
        throw error;
    }
}

async function updateTodo(id, updates) {
    try {
        const response = await fetch(`${API_BASE_URL}/todos/${id}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(updates)
        });
        
        if (!response.ok) {
            throw new Error('Failed to update todo');
        }
        
        const updatedTodo = await response.json();
        const index = todos.findIndex(t => t.id === id);
        if (index !== -1) {
            todos[index] = updatedTodo;
        }
        renderTodos();
        updateStats();
        
        return updatedTodo;
    } catch (error) {
        console.error('Error updating todo:', error);
        showToast('Failed to update todo', 'error');
        throw error;
    }
}

async function deleteTodo(id) {
    try {
        const response = await fetch(`${API_BASE_URL}/todos/${id}`, {
            method: 'DELETE'
        });
        
        if (!response.ok) {
            throw new Error('Failed to delete todo');
        }
        
        todos = todos.filter(t => t.id !== id);
        renderTodos();
        updateStats();
        showToast('Todo deleted successfully!', 'success');
    } catch (error) {
        console.error('Error deleting todo:', error);
        showToast('Failed to delete todo', 'error');
        throw error;
    }
}

// UI Functions
function handleAddTodo() {
    const title = todoTitleInput.value.trim();
    const description = todoDescriptionInput.value.trim();
    
    if (!title) {
        showToast('Please enter a todo title', 'error');
        todoTitleInput.focus();
        return;
    }
    
    createTodo(title, description).then(() => {
        todoTitleInput.value = '';
        todoDescriptionInput.value = '';
        todoTitleInput.focus();
    });
}

function renderTodos() {
    const filteredTodos = getFilteredTodos();
    
    if (filteredTodos.length === 0) {
        todoList.innerHTML = '';
        emptyState.classList.remove('hidden');
        return;
    }
    
    emptyState.classList.add('hidden');
    
    todoList.innerHTML = filteredTodos.map(todo => createTodoElement(todo)).join('');
    
    // Attach event listeners to dynamically created elements
    filteredTodos.forEach(todo => {
        const todoElement = document.querySelector(`[data-id="${todo.id}"]`);
        if (todoElement) {
            const checkbox = todoElement.querySelector('.todo-checkbox');
            const deleteBtn = todoElement.querySelector('.delete-btn');
            
            checkbox.addEventListener('change', () => handleToggleComplete(todo.id, checkbox.checked));
            deleteBtn.addEventListener('click', () => handleDeleteTodo(todo.id));
        }
    });
}

function createTodoElement(todo) {
    const createdDate = new Date(todo.created_at).toLocaleDateString('en-US', {
        month: 'short',
        day: 'numeric',
        year: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
    });
    
    return `
        <div class="todo-item ${todo.completed ? 'completed' : ''}" data-id="${todo.id}">
            <div class="todo-header">
                <input 
                    type="checkbox" 
                    class="todo-checkbox" 
                    ${todo.completed ? 'checked' : ''}
                >
                <div class="todo-content">
                    <div class="todo-title">${escapeHtml(todo.title)}</div>
                    ${todo.description ? `<div class="todo-description">${escapeHtml(todo.description)}</div>` : ''}
                    <div class="todo-meta">Created: ${createdDate}</div>
                </div>
                <div class="todo-actions">
                    <button class="todo-btn delete-btn" title="Delete">🗑️</button>
                </div>
            </div>
        </div>
    `;
}

function getFilteredTodos() {
    switch (currentFilter) {
        case 'active':
            return todos.filter(t => !t.completed);
        case 'completed':
            return todos.filter(t => t.completed);
        default:
            return todos;
    }
}

function handleToggleComplete(id, completed) {
    updateTodo(id, { completed });
}

function handleDeleteTodo(id) {
    if (confirm('Are you sure you want to delete this todo?')) {
        deleteTodo(id);
    }
}

function updateStats() {
    const total = todos.length;
    const active = todos.filter(t => !t.completed).length;
    const completed = todos.filter(t => t.completed).length;
    
    totalCount.textContent = total;
    activeCount.textContent = active;
    completedCount.textContent = completed;
}

function showToast(message, type = 'success') {
    toast.textContent = message;
    toast.className = `toast ${type} show`;
    
    setTimeout(() => {
        toast.classList.remove('show');
    }, 3000);
}

function showLoading() {
    todoList.innerHTML = '<div class="loading">Loading todos</div>';
    emptyState.classList.add('hidden');
}

function hideLoading() {
    const loadingElement = todoList.querySelector('.loading');
    if (loadingElement) {
        loadingElement.remove();
    }
}

function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

// Error Handling
window.addEventListener('unhandledrejection', (event) => {
    console.error('Unhandled promise rejection:', event.reason);
    showToast('An unexpected error occurred', 'error');
});

// Service Worker Registration (Optional - for PWA)
if ('serviceWorker' in navigator) {
    window.addEventListener('load', () => {
        // Uncomment to enable service worker
        // navigator.serviceWorker.register('/sw.js')
        //     .then(registration => console.log('SW registered:', registration))
        //     .catch(error => console.log('SW registration failed:', error));
    });
}

// Made with Bob
