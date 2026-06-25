/**
 * Todo Application - Frontend JavaScript
 * 
 * This file demonstrates literate coding principles by providing detailed
 * explanations of how the code works. Each function includes comprehensive
 * comments that explain not just WHAT the code does, but WHY and HOW.
 * 
 * Key Concepts Demonstrated:
 * - Async/await for cleaner asynchronous code
 * - Fetch API for HTTP requests
 * - DOM manipulation
 * - Error handling
 * - Event listeners
 * - State management
 */

// ============================================================================
// CONFIGURATION
// ============================================================================

/**
 * API Base URL
 * 
 * This constant defines where our Flask backend is running.
 * In production, this would be an environment variable or config file.
 * For development, we use localhost:5000 (Flask's default port).
 */
const API_URL = 'http://localhost:5000/api/todos';

/**
 * Application State
 * 
 * We maintain a simple state object to track the current todos.
 * This helps us avoid unnecessary API calls and provides a single
 * source of truth for our application data.
 */
let appState = {
    todos: [],
    isLoading: false,
    error: null
};


// ============================================================================
// INITIALIZATION
// ============================================================================

/**
 * Initialize the application when the DOM is fully loaded
 * 
 * We use DOMContentLoaded event to ensure all HTML elements are available
 * before we try to manipulate them. This is a best practice that prevents
 * errors from trying to access elements that don't exist yet.
 */
document.addEventListener('DOMContentLoaded', () => {
    console.log('🚀 Todo App initialized');
    
    // Set up event listeners
    setupEventListeners();
    
    // Load initial data
    fetchTodos();
});


// ============================================================================
// EVENT LISTENERS
// ============================================================================

/**
 * Set up all event listeners for the application
 * 
 * Centralizing event listener setup makes it easier to manage and debug.
 * We attach listeners to the form submission event to handle todo creation.
 */
function setupEventListeners() {
    const form = document.getElementById('todo-form');
    
    /**
     * Form submission handler
     * 
     * We prevent the default form submission behavior (which would reload
     * the page) and instead handle it with JavaScript to create a smooth
     * single-page application experience.
     */
    form.addEventListener('submit', async (event) => {
        event.preventDefault();
        
        // Get form values
        const title = document.getElementById('todo-title').value.trim();
        const description = document.getElementById('todo-description').value.trim();
        
        // Validate input
        if (!title) {
            showError('Please enter a todo title');
            return;
        }
        
        // Create the todo
        await createTodo(title, description);
    });
}


// ============================================================================
// API FUNCTIONS
// ============================================================================

/**
 * Fetch all todos from the backend API
 * 
 * This function demonstrates the async/await pattern for handling promises.
 * Async/await makes asynchronous code look and behave more like synchronous
 * code, which is easier to read and understand.
 * 
 * The try/catch block handles any errors that might occur during the fetch
 * operation, such as network errors or server errors.
 * 
 * @returns {Promise<void>}
 */
async function fetchTodos() {
    try {
        // Update UI to show loading state
        setLoadingState(true);
        
        /**
         * Fetch API call
         * 
         * The fetch() function returns a Promise that resolves to the Response
         * object representing the response to the request. We use await to
         * pause execution until the promise resolves.
         */
        const response = await fetch(API_URL);
        
        /**
         * Error handling
         * 
         * Even if the fetch succeeds, the server might return an error status
         * (like 404 or 500). We check response.ok to ensure we got a success
         * status code (200-299).
         */
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        /**
         * Parse JSON response
         * 
         * The response.json() method also returns a Promise, so we await it.
         * This parses the JSON string into a JavaScript object/array.
         */
        const todos = await response.json();
        
        // Update application state
        appState.todos = todos;
        appState.error = null;
        
        // Update the UI with the fetched todos
        displayTodos(todos);
        
        console.log(`✅ Loaded ${todos.length} todos`);
        
    } catch (error) {
        /**
         * Error handling
         * 
         * If anything goes wrong (network error, parsing error, etc.),
         * we catch the error here and display it to the user.
         */
        console.error('❌ Error fetching todos:', error);
        appState.error = error.message;
        showErrorState('Failed to load todos. Please check if the backend is running.');
    } finally {
        /**
         * Finally block
         * 
         * This code runs whether the try block succeeds or fails.
         * It's perfect for cleanup operations like hiding loading indicators.
         */
        setLoadingState(false);
    }
}

/**
 * Create a new todo item
 * 
 * This function demonstrates how to make a POST request with JSON data.
 * We need to specify the HTTP method, headers, and body for the request.
 * 
 * @param {string} title - The todo title
 * @param {string} description - The todo description
 * @returns {Promise<void>}
 */
async function createTodo(title, description) {
    try {
        /**
         * POST request with JSON body
         * 
         * We use the fetch API with additional options:
         * - method: 'POST' specifies this is a POST request
         * - headers: tells the server we're sending JSON
         * - body: the actual data, converted to JSON string
         */
        const response = await fetch(API_URL, {
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
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const newTodo = await response.json();
        
        console.log('✅ Todo created:', newTodo);
        
        // Clear the form
        clearForm();
        
        // Refresh the todo list
        await fetchTodos();
        
    } catch (error) {
        console.error('❌ Error creating todo:', error);
        showError('Failed to create todo. Please try again.');
    }
}

/**
 * Toggle todo completion status
 * 
 * This function updates a todo's completed status by making a PUT request.
 * 
 * @param {number} todoId - The ID of the todo to update
 * @param {boolean} completed - The new completion status
 * @returns {Promise<void>}
 */
async function toggleTodo(todoId, completed) {
    try {
        const response = await fetch(`${API_URL}/${todoId}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                completed: !completed
            })
        });
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        console.log(`✅ Todo ${todoId} toggled`);
        
        // Refresh the todo list
        await fetchTodos();
        
    } catch (error) {
        console.error('❌ Error toggling todo:', error);
        showError('Failed to update todo. Please try again.');
    }
}

/**
 * Delete a todo item
 * 
 * This function removes a todo by making a DELETE request.
 * We ask for confirmation before deleting to prevent accidental deletions.
 * 
 * @param {number} todoId - The ID of the todo to delete
 * @returns {Promise<void>}
 */
async function deleteTodo(todoId) {
    /**
     * User confirmation
     * 
     * The confirm() function shows a browser dialog asking the user
     * to confirm the action. This is a simple way to prevent accidental
     * deletions, though a custom modal would be more user-friendly.
     */
    if (!confirm('Are you sure you want to delete this todo?')) {
        return;
    }
    
    try {
        const response = await fetch(`${API_URL}/${todoId}`, {
            method: 'DELETE'
        });
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        console.log(`✅ Todo ${todoId} deleted`);
        
        // Refresh the todo list
        await fetchTodos();
        
    } catch (error) {
        console.error('❌ Error deleting todo:', error);
        showError('Failed to delete todo. Please try again.');
    }
}


// ============================================================================
// UI FUNCTIONS
// ============================================================================

/**
 * Display todos in the UI
 * 
 * This function takes an array of todos and renders them as HTML elements.
 * We use template literals (backticks) to create HTML strings, which is
 * cleaner than concatenating strings with +.
 * 
 * @param {Array} todos - Array of todo objects
 */
function displayTodos(todos) {
    const todosList = document.getElementById('todos-list');
    const emptyState = document.getElementById('empty-state');
    const todoCount = document.getElementById('todo-count');
    
    // Update todo count
    const count = todos.length;
    todoCount.textContent = `${count} ${count === 1 ? 'todo' : 'todos'}`;
    
    /**
     * Handle empty state
     * 
     * If there are no todos, we show a friendly empty state message
     * instead of just showing nothing.
     */
    if (todos.length === 0) {
        todosList.innerHTML = '';
        emptyState.style.display = 'block';
        return;
    }
    
    // Hide empty state
    emptyState.style.display = 'none';
    
    /**
     * Render todos
     * 
     * We use Array.map() to transform each todo object into an HTML string,
     * then join them together. This is more efficient than concatenating
     * strings in a loop.
     */
    todosList.innerHTML = todos.map(todo => createTodoHTML(todo)).join('');
    
    /**
     * Attach event listeners to buttons
     * 
     * Since we're creating new DOM elements, we need to attach event
     * listeners to them. We use event delegation by attaching listeners
     * to the parent element and checking which button was clicked.
     */
    todosList.querySelectorAll('.btn-success').forEach(button => {
        button.addEventListener('click', () => {
            const todoId = parseInt(button.dataset.id);
            const completed = button.dataset.completed === 'true';
            toggleTodo(todoId, completed);
        });
    });
    
    todosList.querySelectorAll('.btn-danger').forEach(button => {
        button.addEventListener('click', () => {
            const todoId = parseInt(button.dataset.id);
            deleteTodo(todoId);
        });
    });
}

/**
 * Create HTML for a single todo item
 * 
 * This function generates the HTML structure for a todo item.
 * We use template literals for cleaner, more readable HTML generation.
 * 
 * @param {Object} todo - Todo object
 * @returns {string} HTML string
 */
function createTodoHTML(todo) {
    /**
     * Format date
     * 
     * We convert the ISO date string to a more readable format.
     * The Date object provides methods for formatting dates.
     */
    const date = new Date(todo.created_at);
    const formattedDate = date.toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
    });
    
    /**
     * Conditional classes
     * 
     * We add the 'completed' class if the todo is completed,
     * which applies different styling (like strikethrough text).
     */
    const completedClass = todo.completed ? 'completed' : '';
    const buttonText = todo.completed ? '↩️ Undo' : '✓ Complete';
    
    /**
     * Template literal
     * 
     * Template literals (backticks) allow us to write multi-line strings
     * and embed expressions using ${expression} syntax. This makes HTML
     * generation much more readable than string concatenation.
     */
    return `
        <div class="todo-item ${completedClass}">
            <div class="todo-header">
                <h3 class="todo-title">${escapeHtml(todo.title)}</h3>
            </div>
            ${todo.description ? `<p class="todo-description">${escapeHtml(todo.description)}</p>` : ''}
            <div class="todo-meta">
                <span class="todo-date">📅 ${formattedDate}</span>
                <div class="todo-actions">
                    <button 
                        class="btn btn-success" 
                        data-id="${todo.id}"
                        data-completed="${todo.completed}"
                    >
                        ${buttonText}
                    </button>
                    <button 
                        class="btn btn-danger" 
                        data-id="${todo.id}"
                    >
                        🗑️ Delete
                    </button>
                </div>
            </div>
        </div>
    `;
}

/**
 * Escape HTML to prevent XSS attacks
 * 
 * This is a security function that prevents Cross-Site Scripting (XSS)
 * attacks by converting special HTML characters to their entity equivalents.
 * 
 * For example: < becomes < and > becomes >
 * This prevents user input from being interpreted as HTML/JavaScript.
 * 
 * @param {string} text - Text to escape
 * @returns {string} Escaped text
 */
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

/**
 * Set loading state
 * 
 * Shows or hides the loading indicator based on the loading state.
 * 
 * @param {boolean} isLoading - Whether the app is loading
 */
function setLoadingState(isLoading) {
    const loading = document.getElementById('loading');
    const todosList = document.getElementById('todos-list');
    
    appState.isLoading = isLoading;
    
    if (isLoading) {
        loading.style.display = 'block';
        todosList.style.display = 'none';
    } else {
        loading.style.display = 'none';
        todosList.style.display = 'block';
    }
}

/**
 * Show error state
 * 
 * Displays an error message to the user when something goes wrong.
 * 
 * @param {string} message - Error message to display
 */
function showErrorState(message) {
    const errorState = document.getElementById('error-state');
    const errorMessage = document.getElementById('error-message');
    const todosList = document.getElementById('todos-list');
    const emptyState = document.getElementById('empty-state');
    
    errorMessage.textContent = message;
    errorState.style.display = 'block';
    todosList.style.display = 'none';
    emptyState.style.display = 'none';
}

/**
 * Show temporary error message
 * 
 * Displays a temporary error message using the browser's alert.
 * In a production app, you'd want to use a more sophisticated
 * notification system (like a toast or snackbar).
 * 
 * @param {string} message - Error message
 */
function showError(message) {
    alert(message);
}

/**
 * Clear the todo form
 * 
 * Resets the form fields after successfully creating a todo.
 * This provides good user feedback and prepares the form for the next entry.
 */
function clearForm() {
    document.getElementById('todo-title').value = '';
    document.getElementById('todo-description').value = '';
    
    // Focus back on the title input for quick entry of next todo
    document.getElementById('todo-title').focus();
}


// ============================================================================
// UTILITY FUNCTIONS
// ============================================================================

/**
 * Log application state (for debugging)
 * 
 * This function is useful during development to inspect the current state.
 * You can call it from the browser console: logState()
 */
function logState() {
    console.log('📊 Current App State:', appState);
}

// Make logState available globally for debugging
window.logState = logState;

/**
 * Export functions for testing (if needed)
 * 
 * In a real application with a build system, you might export these
 * functions for unit testing. For now, they're just available globally.
 */
if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        fetchTodos,
        createTodo,
        toggleTodo,
        deleteTodo,
        escapeHtml
    };
}

console.log('📝 Todo App JavaScript loaded successfully!');

// Made with Bob
