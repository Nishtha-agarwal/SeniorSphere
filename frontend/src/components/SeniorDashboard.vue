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

    <!-- Content Container with header and main -->
    <div
      class="flex-grow-1 d-flex flex-column overflow-auto"
      :class="{ 'ms-0': isMobile && !sidebarOpen, 'ms-220': !isMobile || sidebarOpen }"
    >
      <!-- Header (moved inside the scrollable container) -->
      <header class="bg-white border-bottom d-flex justify-content-between align-items-center p-3 shadow-sm sticky-top">
        <div class="d-flex align-items-center">
          <button class="btn btn-outline-dark d-md-none me-2" @click="toggleSidebar">☰</button>
          <img :src="logo" alt="Logo" width="32" height="32" class="me-2" />
          <h5 class="mb-0 text-dark">SeniorSphere</h5>
        </div>
        <button class="btn btn-danger" @click="logout">Logout</button>
      </header>

      <!-- Main Content -->
      <main class="p-4">
        <h4 class="mb-4 text-center">Health Status</h4>

        <div class="card p-3 mb-4">
          <div class="d-flex justify-content-between align-items-center">
            <div>
              <h5 class="text-success">ONTRACK</h5>
              <p class="mb-0 text-muted">
                {{ profile.condition ? profile.condition : 'No medical conditions recorded' }}
              </p>
            </div>
            <div>
              <button class="btn btn-outline-secondary me-2" @click="raiseQuery">Raise Query</button>
              <button class="btn btn-danger" @click="sendSOS">SOS Alert</button>
            </div>
          </div>
        </div>


        <h5>Daily Routine</h5>
        <table class="table table-bordered mb-4">
          <thead>
            <tr>
              <th>Time</th>
              <th>Task</th>
              <th>Caretaker</th>
              <th>Status</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="activity in routine" :key="activity.taskId">
              <td>{{ activity.time }}</td>
              <td>{{ activity.task }}</td>
              <td>{{ activity.caretaker }}</td>
              <td>
                <span
                  class="badge"
                  :class="{
                    'bg-success': activity.status === 'completed',
                    'bg-warning text-dark': activity.status === 'upcoming',
                    'bg-danger': activity.status === 'missed'
                  }"
                >
                  {{ activity.status }}
                </span>
              </td>
              <td>
                <button
                  v-if="activity.status !== 'completed'"
                  class="btn btn-sm btn-success"
                  @click="markCompleted(activity.taskId)"
                >
                  ✅ Complete
                </button>
              </td>
            </tr>
          </tbody>
        </table>

        <div class="row">
          <!-- Health Resources -->
          <div class="col-md-6 mb-4">
            <h5>Health Resources</h5>
            <ul class="nav nav-tabs mb-2">
              <li class="nav-item">
                <button
                  class="nav-link"
                  :class="{ active: activeTab === 'articles' }"
                  @click="activeTab = 'articles'"
                 >
                  Articles
                </button>
              </li>
              <li class="nav-item">
                <button
                  class="nav-link"
                  :class="{ active: activeTab === 'videos' }"
                  @click="activeTab = 'videos'"
                >
                  Videos
                </button>
              </li>
            </ul>

            <div v-if="activeTab === 'articles'">
              <div v-for="article in articles" :key="article.id" class="card p-3 mb-2">
                <h6>{{ article.title }}</h6>
                <p class="mb-1">{{ article.summary }}</p>
                <button onclick="window.location.href='{{ article.link }}';" class="btn btn-outline-primary btn-sm">Read</button>
              </div>
            </div>
            <div v-else>
              <div v-for="video in videos" :key="video.id" class="card p-3 mb-2">
                <h6>{{ video.title }}</h6>
                <p class="mb-1">{{ video.description }}</p>
                <button onclick="window.location.href='{{ video.link }}';" class="btn btn-outline-success btn-sm">Watch</button>
              </div>
            </div>
          </div>

          <!-- Caretaker Info -->
          <div class="col-md-6 mb-4">
            <h5>Caretaker & Support</h5>
            <div class="d-flex align-items-center">
              <img
                src="https://cdn-icons-png.flaticon.com/512/194/194935.png"
                alt="Caretaker"
                width="40"
                height="40"
                class="me-3"
              />
              <div>
                <strong>{{ profile.caretaker || 'No caretaker assigned' }}</strong><br />
                <small class="text-muted">Caretaker</small>
              </div>
            </div>
          </div>
        </div>
      </main>
    </div>
  </div>
</template>

<script setup>
import logo from '@/assets/logo.jpeg'
import { onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const sidebarOpen = ref(true)
const isMobile = ref(false)

const profile = ref({})
const routine = ref([])
const queries = ref([])

const activeTab = ref('articles')
const articles = ref([])
const videos = ref([])

const toggleSidebar = () => { sidebarOpen.value = !sidebarOpen.value }
const checkScreen = () => {
  isMobile.value = window.innerWidth < 768
  if (isMobile.value) sidebarOpen.value = false
}
const goBack = () => window.history.back()
const goForward = () => window.history.forward()
const reload = () => location.reload()
const logout = () => { localStorage.clear(); router.push('/login') }

function authHeader() {
  const token = localStorage.getItem('accessToken')
  return { Authorization: `Bearer ${token}` }
}

// API Calls with fetch
const fetchProfile = async () => {
  try {
    const res = await fetch('http://localhost:5000/api/senior/dashboard', {
      headers: authHeader()
    })
    profile.value = await res.json()
  } catch (err) {
    console.error(err)
  }
}

const fetchRoutine = async () => {
  try {
    const res = await fetch('http://localhost:5000/api/senior/routine', {
      headers: authHeader()
    })
    routine.value = await res.json()
  } catch (err) {
    console.error(err)
  }
}

const fetchQueries = async () => {
  try {
    const res = await fetch('http://localhost:5000/api/senior/query', {
      headers: authHeader()
    })
    queries.value = await res.json()
  } catch (err) {
    console.error(err)
  }
}

const sendSOS = async () => {
  try {
    await fetch('http://localhost:5000/api/senior/sos', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        ...authHeader()
      }
    })
    alert('SOS alert sent successfully!')
  } catch (err) {
    console.error(err)
  }
}

const raiseQuery = async () => {
  const message = prompt('Enter your query:')
  if (!message) return
  try {
    await fetch('http://localhost:5000/api/senior/query', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        ...authHeader()
      },
      body: JSON.stringify({ message })
    })
    alert('Query raised successfully!')
    fetchQueries()
  } catch (err) {
    console.error(err)
  }
}

const markCompleted = async (taskId) => {
  console.log('Marking task as completed:', taskId)
  try {
    await fetch('http://localhost:5000/api/senior/routine', {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
        ...authHeader()
      },
      body: JSON.stringify({ taskId })
    })
    alert('Task marked as completed')
    fetchRoutine() // 🔄 refresh list
  } catch (err) {
    console.error(err)
  }
}

onMounted(() => {
  checkScreen()
  window.addEventListener('resize', checkScreen)
  fetchProfile()
  fetchRoutine()
  // fetchQueries()

  // Static for now, could also be fetched from API
  articles.value = [
    { id: 1, title: 'Tips to Stay Active After 70', summary: 'Gentle routines and walking habits that promote mobility.', link: 'https://www.nia.nih.gov/health/exercise-and-physical-activity/tips-getting-and-staying-active-you-age' },
    { id: 2, title: 'Managing Diabetes', summary: 'Best foods and habits to control blood sugar levels.', link:'https://www.healthline.com/nutrition/foods-to-lower-blood-sugar' }
  ]
  videos.value = [
    { id: 1, title: 'Morning Yoga for Seniors', description: 'Follow this 15-minute routine for flexibility.' },
    { id: 2, title: 'Healthy Breakfast Tips', description: 'Easy meal planning for energy and wellness.' }
  ]
})

</script>


<style scoped>
.ms-220 {
  margin-left: 220px;
}

table td {
  vertical-align: middle;
}
</style>