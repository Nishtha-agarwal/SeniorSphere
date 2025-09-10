<template>
  <div class="d-flex vh-100">
    <!-- Sidebar -->
    <aside
      :class="['bg-dark text-white p-3 d-flex flex-column', sidebarCollapsed ? 'd-none d-md-flex' : '']"
      style="width: 220px;"
    >
      <div class="d-flex justify-content-between mb-4">
        <button @click="login" class="btn btn-outline-light btn-sm">←</button>
        <button @click="goForward" class="btn btn-outline-light btn-sm">→</button>
        <button @click="reload" class="btn btn-outline-light btn-sm">⟳</button>
      </div>
      <ul class="nav flex-column">
        <li class="nav-item mb-2">
          <button class="btn btn-outline-light w-100 text-start" @click="setView('reports')">View Reports</button>
        </li>
        <li class="nav-item mb-2">
          <button class="btn btn-outline-light w-100 text-start" @click="setView('home')">Home</button>
        </li>
      </ul>
    </aside>

    <!-- Main Content -->
    <main class="flex-grow-1 d-flex flex-column bg-light">
      <!-- Header -->
      <header class="bg-white border-bottom d-flex justify-content-between align-items-center p-3 shadow-sm">
        <div class="d-flex align-items-center">
          <button class="btn btn-outline-dark d-md-none me-2" @click="toggleSidebar">☰</button>
          <img src="@/assets/logo.jpeg" alt="Logo" width="32" height="32" class="me-2" />
          <h5 class="mb-0 text-dark">SeniorSphere</h5>
        </div>
        <button class="btn btn-danger" @click="logout">Logout</button>
      </header>

      <div class="p-4">
        <h2 class="mb-3">Family Dashboard</h2>

        <div v-if="currentView === 'reports'">
          <h4>Reports of Monitored Relatives</h4>
          <div class="row">
            <div v-for="report in reports" :key="report.id" class="col-md-4 mb-3">
              <div
                class="card bg-info text-white"
                style="cursor: pointer;"
                @click="selectReport(report)"
              >
                <div class="card-body">
                  <h5 class="card-title">{{ report.name }}</h5>
                  <p class="card-text">Click to view details</p>
                </div>
              </div>
            </div>
          </div>

          <!-- Floating Report Card -->
          <div v-if="selectedReport" class="position-fixed top-0 start-0 w-100 h-100 bg-dark bg-opacity-50 d-flex justify-content-center align-items-center" style="z-index: 1050;">
            <div class="card shadow-lg" style="width: 400px;">
              <div class="card-header d-flex justify-content-between align-items-center">
                <h5 class="mb-0">{{ selectedReport.name }}</h5>
                <button class="btn btn-close" @click="selectedReport = null"></button>
              </div>
              <div class="card-body">
                <p><strong>Summary:</strong> {{ selectedReport.summary }}</p>
                <p><strong>Last Checkup:</strong> {{ selectedReport.lastCheckup }}</p>
              </div>
            </div>
          </div>
        </div>

        <div v-if="currentView === 'home'">
          <h4>Welcome to your Family Dashboard</h4>
          <p class="text-muted">Use the sidebar to view health reports of your relatives.</p>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()

//const goBack = () => window.history.back()
const goForward = () => window.history.forward()
const reload = () => location.reload()
const logout = () => router.push('/')
const login = () => router.push('/login')

const sidebarCollapsed = ref(false)
const toggleSidebar = () => {
  sidebarCollapsed.value = !sidebarCollapsed.value
}

const currentView = ref('home')
const setView = (view) => {
  currentView.value = view
  selectedReport.value = null
}

const reports = ref([
  { id: 1, name: 'Ramesh Kumar', summary: 'All vitals normal.', lastCheckup: '2025-06-20' },
  { id: 2, name: 'Sushila Devi', summary: 'Blood pressure elevated.', lastCheckup: '2025-06-19' },
  { id: 3, name: 'Meena Singh', summary: 'Scheduled physiotherapy session.', lastCheckup: '2025-06-18' }
])

const selectedReport = ref(null)
const selectReport = (report) => {
  selectedReport.value = report
}
</script>