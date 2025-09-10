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

      <!-- Main Content -->
      <main class="p-4">
        <h3 class="mb-3">Health Resources</h3>

        <ul class="nav nav-tabs mb-3">
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
          <div
            v-for="article in articles"
            :key="article.id"
            class="card p-3 mb-3"
          >
            <h5>{{ article.title }}</h5>
            <p class="text-muted">{{ article.summary }}</p>
            <a
              :href="article.link"
              target="_blank"
              rel="noopener noreferrer"
              class="btn btn-outline-primary btn-sm"
            >
              Read More
            </a>
          </div>
        </div>

        <div v-else>
          <div
            v-for="video in videos"
            :key="video.id"
            class="card p-3 mb-3"
          >
            <h5>{{ video.title }}</h5>
            <p class="text-muted">{{ video.description }}</p>
            <a
              :href="video.link"
              target="_blank"
              rel="noopener noreferrer"
              class="btn btn-outline-success btn-sm"
            >
              Watch
            </a>
          </div>
        </div>
      </main>
    </div>
  </div>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()

const goBack = () => window.history.back()
const goForward = () => window.history.forward()
const reload = () => location.reload()
const logout = () => router.push('/')

const activeTab = ref('articles')
const sidebarOpen = ref(true)
const isMobile = ref(false)

const toggleSidebar = () => {
  sidebarOpen.value = !sidebarOpen.value
}

const checkScreen = () => {
  isMobile.value = window.innerWidth < 768
  if (isMobile.value) sidebarOpen.value = false
}

onMounted(() => {
  checkScreen()
  window.addEventListener('resize', checkScreen)
})

const articles = [
  {
    id: 1,
    title: 'Tips to Stay Active After 70',
    summary: 'Gentle routines and walking habits that promote mobility.',
    link: 'https://www.nia.nih.gov/health/exercise-and-physical-activity/tips-getting-and-staying-active-you-age',
  },
  {
    id: 2,
    title: 'Managing Diabetes',
    summary: 'Best foods and habits to control blood sugar levels.',
    link: 'https://www.cdc.gov/diabetes/managing/index.html',
  },
  {
    id: 3,
    title: 'Heart Health for Seniors',
    summary: 'How to keep your heart strong and active.',
    link: 'https://www.heart.org/en/health-topics/consumer-healthcare/what-is-cardiovascular-disease',
  },
]

const videos = [
  {
    id: 1,
    title: 'Morning Yoga for Seniors',
    description: 'Follow this 15-minute routine for flexibility.',
    link: 'https://www.youtube.com/watch?v=kFhG-ZzLNN4',
  },
  {
    id: 2,
    title: 'Healthy Breakfast Tips',
    description: 'Easy meal planning for energy and wellness.',
    link: 'https://www.youtube.com/watch?v=Zl9lOTB-9Dk',
  },
  {
    id: 3,
    title: 'Breathing Exercises',
    description: 'Relaxation and lung-strengthening techniques.',
    link: 'https://www.youtube.com/watch?v=8vkYJf8DOsc',
  },
]
</script>

<style scoped>
.ms-220 {
  margin-left: 220px;
}
</style>
