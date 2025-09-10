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

      <div class="container mt-4">
        <h2 class="text-center mb-4">Caretaker Statistics</h2>

        <div class="row">
          <!-- Assigned Seniors -->
          <div class="col-md-3">
            <div class="card text-center shadow-sm">
              <div class="card-body">
                <h5 class="card-title">Assigned Seniors</h5>
                <p class="card-text display-4">{{ stats.assigned_seniors }}</p>
              </div>
            </div>
          </div>

          <!-- SOS Alerts -->
          <div class="col-md-3">
            <div class="card text-center shadow-sm">
              <div class="card-body">
                <h5 class="card-title">SOS Alerts</h5>
                <p class="card-text display-4">{{ stats.sos_alerts }}</p>
              </div>
            </div>
          </div>

          <!-- Emergency Alerts -->
          <div class="col-md-3">
            <div class="card text-center shadow-sm">
              <div class="card-body">
                <h5 class="card-title">Emergency Alerts</h5>
                <p class="card-text display-4">{{ stats.emergency_alerts }}</p>
              </div>
            </div>
          </div>

          <!-- Tasks Created -->
          <div class="col-md-3">
            <div class="card text-center shadow-sm">
              <div class="card-body">
                <h5 class="card-title">Tasks Created</h5>
                <p class="card-text display-4">{{ stats.tasks_created }}</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';

const router = useRouter();
const sidebarCollapsed = ref(false);
const stats = ref({
  assigned_seniors: 0,
  sos_alerts: 0,
  emergency_alerts: 0,
  tasks_created: 0,
});

const goBack = () => window.history.back();
const goForward = () => window.history.forward();
const reload = () => location.reload();
const logout = () => {
  localStorage.clear();
  router.push('/login');
};

const toggleSidebar = () => {
  sidebarCollapsed.value = !sidebarCollapsed.value;
};

const fetchStats = async () => {
  const token = localStorage.getItem('accessToken');
  const headers = { Authorization: `Bearer ${token}` };

  try {
    const res = await fetch('http://127.0.0.1:5000/api/caretaker/stats', { headers });
    if (!res.ok) {
      console.error('Failed to fetch stats:', res.statusText);
      return;
    }

    stats.value = await res.json();
  } catch (err) {
    console.error('Error fetching stats:', err);
  }
};

onMounted(fetchStats);
</script>