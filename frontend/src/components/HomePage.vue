<template>
  <div :class="['homepage', { dark: isDarkTheme }]">
    <!-- Navbar -->
    <nav class="navbar navbar-expand-md fixed-top glass-navbar">
      <div class="container">
        <span class="navbar-brand fw-bold fs-3 text-white typewriter-text">SeniorSphere</span>

        <!-- Toggle Button for Mobile -->
        <button
          class="navbar-toggler text-white border-0"
          type="button"
          @click="isNavOpen = !isNavOpen"
          aria-label="Toggle navigation"
        >
          <i class="bi bi-list fs-1"></i>
        </button>

        <!-- Mobile Dropdown -->
        <transition name="fade">
          <div
            v-if="isNavOpen"
            class="dropdown-nav bg-dark rounded-bottom shadow-lg mt-2 w-100 text-center d-md-none"
          >
            <ul class="navbar-nav py-2">
              <li class="nav-item my-1">
                <a class="nav-link text-white fw-semibold" href="#" data-bs-toggle="modal" data-bs-target="#aboutModal" @click="isNavOpen = false">About</a>
              </li>
              <li class="nav-item my-1">
                <a class="nav-link text-white fw-semibold" href="#" data-bs-toggle="modal" data-bs-target="#contactModal" @click="isNavOpen = false">Contact</a>
              </li>
              <li class="nav-item my-1">
                <a class="nav-link text-white fw-semibold" href="#" @click.prevent="() => { toggleTheme(); isNavOpen = false; }">Comfort View</a>
              </li>
            </ul>
          </div>
        </transition>

        <!-- Desktop Menu -->
        <div class="collapse navbar-collapse justify-content-end d-none d-md-flex">
          <ul class="navbar-nav">
            <li class="nav-item mx-2">
              <a class="nav-link text-white fw-semibold" href="#" data-bs-toggle="modal" data-bs-target="#aboutModal">About</a>
            </li>
            <li class="nav-item mx-2">
              <a class="nav-link text-white fw-semibold" href="#" data-bs-toggle="modal" data-bs-target="#contactModal">Contact</a>
            </li>
            <li class="nav-item mx-2">
              <a class="nav-link text-white fw-semibold" href="#" @click.prevent="toggleTheme">Comfort View</a>
            </li>
          </ul>
        </div>
      </div>
    </nav>

    <!-- Hero Section -->
    <div class="hero-section d-flex flex-column justify-content-center align-items-center">
      <img src="@/assets/logo.jpeg" alt="SeniorSphere Logo" class="logo mb-3" />
      <h1 class="display-4 fw-bold text-white glow-text">Welcome to SeniorSphere</h1>
      <p class="lead text-white mt-1 glow-text text-center">
        Help Us Build a Better Digital Companion for Seniors.<br />
        Connect, care, and support those who matter the most.
      </p>

      <div class="arrow-down my-3">
        <i class="bi bi-arrow-down-circle-fill text-white"></i>
      </div>

      <router-link to="/login" class="btn btn-lg btn-primary mt-1 px-5 py-3 shadow rounded-pill">
        Let's Get Connected
      </router-link>
    </div>

    <!-- About Modal -->
    <div class="modal fade" id="aboutModal" tabindex="-1">
      <div class="modal-dialog modal-dialog-centered">
        <div class="modal-content rounded-4">
          <div class="modal-header">
            <h5 class="modal-title">About SeniorSphere</h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
          </div>
          <div class="modal-body text-start">
            SeniorSphere supports elderly individuals with simple, friendly technology that makes digital life safer and warmer.
          </div>
        </div>
      </div>
    </div>

    <!-- Contact Modal -->
    <div class="modal fade" id="contactModal" tabindex="-1">
      <div class="modal-dialog modal-dialog-centered">
        <div class="modal-content rounded-4">
          <div class="modal-header">
            <h5 class="modal-title">Contact Us</h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
          </div>
          <div class="modal-body text-start">
            📞 Phone: +91-123-456-7890<br />
            📧 Email: support@seniorsphere.in<br />
            📍 Address: 123 Elder Care Lane, New Delhi, India
          </div>
        </div>
      </div>
    </div>

    <!-- Footer -->
    <footer class="text-white text-center py-3 small-footer">
      © {{ new Date().getFullYear() }} SeniorSphere. All Rights Reserved.
    </footer>
  </div>
</template>

<script>
export default {
  name: "HomePage",
  data() {
    return {
      isDarkTheme: false,
      isNavOpen: false,
    };
  },
  methods: {
    toggleTheme() {
      this.isDarkTheme = !this.isDarkTheme;
    },
  },
};
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Quicksand:wght@400;600;700&display=swap');
@import url('https://cdn.jsdelivr.net/npm/bootstrap-icons@1.10.5/font/bootstrap-icons.css');

/* Layout Base */
.homepage {
  font-family: 'Quicksand', sans-serif;
  min-height: 100vh;
  background: url("@/assets/senior-bg.jpg") no-repeat center center fixed;
  background-size: cover;
  position: relative;
  overflow-x: hidden;
}

/* Navbar */
.glass-navbar {
  background-color: rgba(255, 255, 255, 0.05);
  backdrop-filter: blur(8px);
  height: 60px;
  z-index: 999;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

/* Typing Effect */
.typewriter-text {
  animation: typing 3s steps(30, end), blink-caret 0.75s step-end infinite;
  white-space: nowrap;
  overflow: hidden;
  border-right: 3px solid white;
  color: white;
}
@keyframes typing {
  from { width: 0; }
  to { width: 14ch; }
}
@keyframes blink-caret {
  0%, 100% { border-color: transparent; }
  50% { border-color: rgba(255, 255, 255, 0); }
}

/* Hero Section */
.hero-section {
  height: 100vh;
  padding-top: 70px;
  padding-bottom: 3rem;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  text-align: center;
}
.logo {
  max-width: 90px;
  border-radius: 50%;
  opacity: 0.96;
  box-shadow: 0 0 12px rgba(255, 255, 255, 0.25);
}
.glow-text {
  text-shadow: 1px 1px 5px rgba(0, 0, 0, 0.7);
}

/* Arrow Animation */
.arrow-down i {
  font-size: 2.5rem;
  animation: blink 1.5s infinite;
}
@keyframes blink {
  0%, 100% { opacity: 0.2; transform: translateY(0); }
  50% { opacity: 1; transform: translateY(5px); }
}

/* Button */
.btn-primary {
  background-color: #007bff;
  border: none;
  transition: 0.3s ease;
}
.btn-primary:hover {
  background-color: #a93030;
}

/* Modal */
.modal-content {
  font-family: 'Quicksand', sans-serif;
  padding: 1.5rem;
  border-radius: 1rem;
  background-color: #fff;
  box-shadow: 0 0 15px rgba(0, 0, 0, 0.15);
}

/* Footer */
.small-footer {
  font-size: 0.85rem;
  background-color: transparent;
  margin-top: auto;
}

/* Dark Theme */
.dark {
  background: linear-gradient(135deg, #1c1c1c, #2d2d2d);
  background-attachment: fixed;
  background-size: cover;
  color: white;
}
.dark .glow-text {
  text-shadow: 1px 1px 6px rgba(255, 255, 255, 0.6);
}
.dark .glass-navbar {
  background-color: rgba(0, 0, 0, 0.5);
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}
.dark .modal-content {
  background-color: #2a2a2a;
  color: #fff;
}

/* Transition */
.fade-enter-active, .fade-leave-active {
  transition: all 0.3s ease;
}
.fade-enter-from, .fade-leave-to {
  opacity: 0;
  transform: translateY(-10px);
}

</style>
