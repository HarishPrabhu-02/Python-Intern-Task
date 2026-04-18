const API_URL = "http://127.0.0.1:8000";

// --- UI Toggle ---
function checkAuth() {
    const token = localStorage.getItem("token");
    if (token) {
        document.getElementById("auth-section").style.display = "none";
        document.getElementById("task-section").style.display = "block";
        fetchTasks();
    } else {
        document.getElementById("auth-section").style.display = "block";
        document.getElementById("task-section").style.display = "none";
    }
}

// --- Authentication ---
async function register() {
    const username = document.getElementById("username").value;
    const password = document.getElementById("password").value;
    
    const response = await fetch(`${API_URL}/auth/register`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ username, password })
    });

    if (response.ok) {
        document.getElementById("auth-message").innerText = "Registered! Now click Login.";
        document.getElementById("auth-message").style.color = "green";
    } else {
        const error = await response.json();
        document.getElementById("auth-message").innerText = error.detail || "Registration failed";
    }
}

async function login() {
    const username = document.getElementById("username").value;
    const password = document.getElementById("password").value;
    
    // OAuth2 expects URL Encoded form data, not JSON!
    const formData = new URLSearchParams();
    formData.append("username", username);
    formData.append("password", password);

    const response = await fetch(`${API_URL}/auth/login`, {
        method: "POST",
        headers: { "Content-Type": "application/x-www-form-urlencoded" },
        body: formData
    });

    if (response.ok) {
        const data = await response.json();
        localStorage.setItem("token", data.access_token); // Save the JWT!
        checkAuth();
    } else {
        document.getElementById("auth-message").innerText = "Invalid credentials";
    }
}

function logout() {
    localStorage.removeItem("token");
    checkAuth();
}

// --- Tasks ---
// --- Tasks ---
async function fetchTasks() {
    const token = localStorage.getItem("token");
    const response = await fetch(`${API_URL}/tasks/`, {
        headers: { "Authorization": `Bearer ${token}` }
    });
    
    if (response.ok) {
        const tasks = await response.json();
        const list = document.getElementById("task-list");
        list.innerHTML = "";
        tasks.forEach(task => {
            // Added a checkbox and a dynamic strikethrough style if completed
            list.innerHTML += `
                <li style="text-decoration: ${task.completed ? 'line-through' : 'none'}; color: ${task.completed ? 'gray' : 'black'};">
                    <div style="display: flex; align-items: center; gap: 10px;">
                        <input type="checkbox" ${task.completed ? 'checked' : ''} onchange="toggleTask(${task.id}, ${task.completed})">
                        ${task.title}
                    </div>
                    <button onclick="deleteTask(${task.id})" style="background: red; padding: 5px;">X</button>
                </li>
            `;
        });
    } else if (response.status === 401) {
        logout(); // Token expired
    }
}

// NEW FUNCTION: Sends the PUT request to update completion status
async function toggleTask(id, currentStatus) {
    const token = localStorage.getItem("token");
    await fetch(`${API_URL}/tasks/${id}`, {
        method: "PUT",
        headers: { 
            "Content-Type": "application/json",
            "Authorization": `Bearer ${token}` 
        },
        // We send the opposite of the current status to toggle it
        body: JSON.stringify({ completed: !currentStatus }) 
    });
    fetchTasks(); // Refresh the list to show the updated strikethrough
}

async function createTask() {
    const title = document.getElementById("new-task-title").value;
    if (!title) return;

    const token = localStorage.getItem("token");
    await fetch(`${API_URL}/tasks/`, {
        method: "POST",
        headers: { 
            "Content-Type": "application/json",
            "Authorization": `Bearer ${token}`
        },
        body: JSON.stringify({ title, description: "A test task" })
    });

    document.getElementById("new-task-title").value = "";
    fetchTasks();
}

async function deleteTask(id) {
    const token = localStorage.getItem("token");
    await fetch(`${API_URL}/tasks/${id}`, {
        method: "DELETE",
        headers: { "Authorization": `Bearer ${token}` }
    });
    fetchTasks();
}

// Initialize
checkAuth();