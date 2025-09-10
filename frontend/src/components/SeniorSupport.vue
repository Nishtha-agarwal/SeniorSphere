<template>
  <div class="d-flex vh-100">
    <!-- Sidebar -->
    <aside
      class="bg-dark text-white p-3 d-flex flex-column position-fixed top-0 start-0 h-100"
      :class="{ 'd-none': !sidebarOpen && isMobile, 'd-block': sidebarOpen || !isMobile }"
      style="width: 220px; z-index: 1040;"
    >
      <div class="d-flex justify-content-between mb-4 mt-5">
        <button @click="goBack" class="btn btn-outline-light btn-sm">←</button>
        <button @click="goForward" class="btn btn-outline-light btn-sm">→</button>
        <button @click="reload" class="btn btn-outline-light btn-sm">⟳</button>
      </div>
      <ul class="nav flex-column">
        <li class="nav-item mb-2">
          <a href="/dashboard" class="btn btn-outline-light w-100 text-start">Dashboard</a>
        </li>
        <li class="nav-item mb-2">
          <a href="/profile" class="btn btn-outline-light w-100 text-start">Profile</a>
        </li>
        <li class="nav-item mb-2">
          <a href="/support" class="btn btn-outline-light w-100 text-start">Support</a>
        </li>
        <li class="nav-item mb-2">
          <a href="/resources" class="btn btn-outline-light w-100 text-start">Resources</a>
        </li>
      </ul>
    </aside>

    <!-- Content wrapper -->
    <div
      class="flex-grow-1 d-flex flex-column overflow-auto"
      :class="{ 'ms-0': isMobile && !sidebarOpen, 'ms-220': !isMobile || sidebarOpen }"
    >
      <!-- Header -->
      <header class="bg-white border-bottom d-flex justify-content-between align-items-center p-3 shadow-sm sticky-top">
        <div class="d-flex align-items-center">
          <button class="btn btn-outline-dark d-md-none me-2" @click="toggleSidebar">☰</button>
          <img src="@/assets/logo.jpeg" alt="Logo" width="32" height="32" class="me-2" />
          <h5 class="mb-0 text-dark">SeniorSphere</h5>
        </div>
        <button class="btn btn-danger" @click="logout">Logout</button>
      </header>

      <!-- Support Content -->
      <main class="p-4">
        <h3 class="mb-3">Support</h3>

        <div class="card p-3 mb-3">
          <h5>24/7 App Helpline</h5>
          <p>If you're facing any issues, please contact our round-the-clock support team.</p>
          <button class="btn btn-primary">Call Now</button>
        </div>

        <div class="card p-3">
          <h5>Contact Caretaker</h5>
          <p><strong>Caretaker:</strong> {{ caretakerName }}</p>
          <p><strong>Phone:</strong> {{ caretakerPhone }}</p>
          <button class="btn btn-outline-secondary">Message</button>
        </div>
      </main>
    </div>
  </div>
</template>

<script setup>
import axios from 'axios'
import { onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()

const goBack = () => window.history.back()
const goForward = () => window.history.forward()
const reload = () => location.reload()
const logout = () => {
  localStorage.removeItem('token')
  router.push('/')
}

const sidebarOpen = ref(true)
const isMobile = ref(false)

const caretakerName = ref('')
const caretakerPhone = ref('')

const toggleSidebar = () => {
  sidebarOpen.value = !sidebarOpen.value
}

const checkScreen = () => {
  isMobile.value = window.innerWidth < 768
  if (isMobile.value) sidebarOpen.value = false
}

function authHeader() {
  const token = localStorage.getItem('accessToken')
  return { headers: { Authorization: `Bearer ${token}` } }
}

const fetchCaretakerDetails = async () => {
  try {
    const res = await axios.get('http://localhost:5000/api/senior/dashboard', authHeader())
    caretakerName.value = res.data.caretaker || 'Not Assigned'
    caretakerPhone.value = res.data.caretakerContact || 'Not Available'
  } catch (err) {
    console.error('Error fetching caretaker details:', err)
  }
}

onMounted(() => {
  checkScreen()
  window.addEventListener('resize', checkScreen)
  fetchCaretakerDetails()
})
</script>


<style scoped>
.ms-220 {
  margin-left: 220px;
}
</style>
