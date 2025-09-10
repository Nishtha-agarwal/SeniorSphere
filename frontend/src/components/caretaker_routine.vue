<template>
  <div class="d-flex vh-100">
    <!-- Sidebar -->
    <aside :class="['bg-dark text-white p-3 d-flex flex-column', sidebarCollapsed ? 'd-none d-md-flex' : '']" style="width: 220px;">
      <div class="d-flex justify-content-between mb-4">
        <button @click="goBack" class="btn btn-outline-light btn-sm">←</button>
        <button @click="goForward" class="btn btn-outline-light btn-sm">→</button>
        <button @click="reload" class="btn btn-outline-light btn-sm">⟳</button>
      </div>
      <ul class="nav flex-column">
        <li class="nav-item mb-2">
          <router-link to="/caretaker_dash" class="btn btn-outline-light w-100 text-start">Dashboard</router-link>
        </li>
        <li class="nav-item mb-2">
          <router-link to="/caretaker_routine" class="btn btn-outline-light w-100 text-start">Daily Routine</router-link>
        </li>
        <li class="nav-item mb-2">
          <router-link to="/caretaker_profile" class="btn btn-outline-light w-100 text-start">Profile</router-link>
        </li>
        <li class="nav-item mb-2">
          <router-link to="/caretaker_stats" class="btn btn-outline-light w-100 text-start">Statistics</router-link>
        </li>
      </ul>
    </aside>

    <!-- Main Content -->
    <main class="flex-grow-1 d-flex flex-column bg-light overflow-auto">
      <header class="bg-white border-bottom d-flex justify-content-between align-items-center p-3 shadow-sm">
        <div class="d-flex align-items-center">
          <button class="btn btn-outline-dark d-md-none me-2" @click="toggleSidebar">☰</button>
          <img src="../assets/logo.jpeg" alt="Logo" width="32" height="32" class="me-2" />
          <h2 class="m-0 text-dark">SeniorSphere</h2>
        </div>
        <button class="btn btn-danger" @click="logout">Logout</button>
      </header>

      <!-- Routine Form -->
      <div class="p-6 max-w-5xl mx-auto">
        <h2 class="text-2xl font-bold mb-4">Daily Routine</h2>
        <div class="grid grid-cols-1 gap-4 mb-4 max-w-xl">
          <div>
            <label class="block text-sm font-medium mb-1">Task Name</label>
            <input v-model="form.taskName" type="text" placeholder="e.g. Medicine, Walk" class="p-2 border rounded w-full" />
          </div>
          <div>
            <label class="block text-sm font-medium mb-1">Details</label>
            <input v-model="form.details" type="text" placeholder="Details" class="p-2 border rounded w-full" />
          </div>
          <div>
            <label class="block text-sm font-medium mb-1">Time</label>
            <input v-model="form.duration" type="datetime-local" class="p-2 border rounded w-full" />
          </div>
          <div>
            <label class="block text-sm font-medium mb-1">Assign To</label>
            <select v-model="form.senior" class="p-2 border rounded w-full">
              <option disabled value="">Select a Senior</option>
              <option v-for="senior in seniors" :key="senior.id" :value="senior.id">
                {{ senior.name }} ({{ senior.city }})
              </option>
            </select>
          </div>
        </div>

        <div class="mb-6">
          <button @click="saveTask" class="bg-blue-600 text-white px-6 py-2 rounded hover:bg-blue-700">
            {{ editingIndex !== null ? 'Save Changes' : 'Add Task' }}
          </button>
        </div>

        <!-- Tasks Table -->
        <table class="w-full border table-auto mt-3">
          <thead class="bg-gray-100">
            <tr>
              <th class="px-4 py-2 border">Task Name</th>
              <th class="px-4 py-2 border">Details</th>
              <th class="px-4 py-2 border">Time</th>
              <th class="px-4 py-2 border">Senior</th>
              <th class="px-4 py-2 border">Status</th>
              <th class="px-4 py-2 border">Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(task, index) in tasks" :key="task.id">
              <td class="px-4 py-2 border">{{ task.taskName }}</td>
              <td class="px-4 py-2 border">{{ task.details }}</td>
              <td class="px-4 py-2 border">{{ formatTime(task.duration) }}</td>
              <td class="px-4 py-2 border">{{ task.senior.name }} ({{ task.senior.city }})</td>
              <td class="px-4 py-2 border">{{ task.status }}</td>
              <td class="px-4 py-2 border">
                <button @click="editTask(index)" class="text-blue-600 hover:underline mr-2">Edit</button>
                <button @click="deleteTask(index)" class="text-red-600 hover:underline">Delete</button>
              </td>
            </tr>
            <tr v-if="tasks.length === 0">
              <td colspan="6" class="text-center py-4 text-gray-500">No tasks assigned yet.</td>
            </tr>
          </tbody>
        </table>
      </div>
    </main>
  </div>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const sidebarCollapsed = ref(false)
const toggleSidebar = () => sidebarCollapsed.value = !sidebarCollapsed.value

const goBack = () => window.history.back()
const goForward = () => window.history.forward()
const reload = () => location.reload()
const logout = () => router.push('/')

const form = ref({ taskName: '', details: '', duration: '', senior: '' })
const editingIndex = ref(null)
const tasks = ref([])
const seniors = ref([])

const saveTask = async () => {
  if (!form.value.taskName || !form.value.senior) {
    alert('Please fill Task Name and assign a Senior.');
    return;
  }

  try {
    const token = localStorage.getItem("accessToken");
    const headers = { Authorization: `Bearer ${token}`, "Content-Type": "application/json" };

    let url = "http://127.0.0.1:5000/api/caretaker/routine";
    let method = "POST";

    if (editingIndex.value !== null) {
      // Edit task
      url = `http://127.0.0.1:5000/api/caretaker/tasks/${tasks.value[editingIndex.value].id}`;
      method = "PUT";
    }

    const res = await fetch(url, {
      method,
      headers,
      body: JSON.stringify({
        task_name: form.value.taskName,
        details: form.value.details,
        duration: form.value.duration,
        senior_id: form.value.senior,
        status: form.value.status || "Pending",
      }),
    });

    if (!res.ok) {
      const error = await res.json();
      alert(error.error || "Failed to save task");
      return;
    }

    const data = await res.json();
    alert(data.message);

    if (editingIndex.value !== null) {
      // Update the task in the local list
      tasks.value[editingIndex.value] = {
        ...tasks.value[editingIndex.value],
        taskName: form.value.taskName,
        details: form.value.details,
        duration: form.value.duration,
        status: form.value.status || "Pending",
        senior: seniors.value.find(s => s.id === form.value.senior),
      };
    } else {
      // Add the task to the local list
      tasks.value.push({
        id: data.id, // Assuming the backend returns the task ID
        taskName: form.value.taskName,
        details: form.value.details,
        duration: form.value.duration,
        status: "Pending",
        senior: seniors.value.find(s => s.id === form.value.senior),
      });
    }

    resetForm();
  } catch (err) {
    console.error(err);
    alert("An error occurred while saving the task.");
  }
};

const deleteTask = async (index) => {
  const task = tasks.value[index];

  if (!confirm(`Are you sure you want to delete the task "${task.taskName}"?`)) {
    return;
  }

  try {
    const token = localStorage.getItem("accessToken");
    const headers = { Authorization: `Bearer ${token}` };

    const res = await fetch(`http://127.0.0.1:5000/api/caretaker/tasks/${task.id}`, {
      method: "DELETE",
      headers,
    });

    if (!res.ok) {
      const error = await res.json();
      alert(error.error || "Failed to delete task");
      return;
    }

    alert("Task deleted successfully");
    tasks.value.splice(index, 1);
  } catch (err) {
    console.error(err);
    alert("An error occurred while deleting the task.");
  }
};

const editTask = (index) => {
  const task = tasks.value[index];
  form.value = {
    taskName: task.taskName,
    details: task.details,
    duration: task.duration,
    senior: task.senior.id,
    status: task.status,
  };
  editingIndex.value = index;
};

const resetForm = () => {
  form.value = { taskName: '', details: '', duration: '', senior: '' };
  editingIndex.value = null;
};

function formatTime(timeStr) {
  if (!timeStr) return ""
  const parts = timeStr.split("T")
  if (parts.length < 2) return timeStr

  const timePart = parts[1].slice(0,5)
  return timePart
}


onMounted(async () => {
  const token = localStorage.getItem("accessToken");
  const headers = { Authorization: `Bearer ${token}` };

  try {
    // Fetch seniors
    const seniorsRes = await fetch("http://127.0.0.1:5000/api/caretaker/dashboard", { headers });
    if (!seniorsRes.ok) {
      console.error("Failed to fetch seniors:", seniorsRes.statusText);
      seniors.value = [];
    } else {
      const seniorsData = await seniorsRes.json();
      seniors.value = Array.isArray(seniorsData) ? seniorsData : [];
    }

    // Fetch tasks
    const tasksRes = await fetch("http://127.0.0.1:5000/api/caretaker/tasks", { headers });
    if (!tasksRes.ok) {
      console.error("Failed to fetch tasks:", tasksRes.statusText);
      tasks.value = [];
    } else {
      const tasksData = await tasksRes.json();
      tasks.value = Array.isArray(tasksData) ? tasksData : [];
    }
  } catch (err) {
    console.error("Error fetching data:", err);
    seniors.value = [];
    tasks.value = [];
  }
});
</script>

<style scoped>
html, body, #app {
  margin: 0;
  padding: 0;
  height: 100%;
  width: 100%;
}

.main-content {
  flex-grow: 1;
  overflow-y: auto;
  background-color: #fff;
}

.sidebar1 a {
  padding: 10px 20px;
  display: block;
  color: #ccc;
  text-decoration: none;
}

.sidebar1 a.router-link-active {
  background-color: #495057;
  color: #fff;
  font-weight: bold;
}

.sidebar1 a:hover {
  background-color: #6c757d;
  color: white;
}

input, select {
  width: 100%;
}

.text-decoration-line-through {
  text-decoration: line-through;
  color: gray;
}
</style>
