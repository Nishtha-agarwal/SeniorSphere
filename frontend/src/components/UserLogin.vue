<template>
  <div :class="['homepage', { dark: isDarkTheme }]">
    <Toast />

    <!-- Navbar -->
    <nav class="navbar navbar-expand-md fixed-top glass-navbar">
      <div class="container">
        <span class="navbar-brand fw-bold fs-3 text-white typewriter-text">SeniorSphere</span>

        <button
          class="navbar-toggler text-white border-0"
          type="button"
          @click="isNavOpen = !isNavOpen"
          aria-label="Toggle navigation"
        >
          <i class="bi bi-list fs-1"></i>
        </button>

        <!-- Mobile Nav -->
        <transition name="fade">
          <div
            v-if="isNavOpen"
            class="dropdown-nav bg-dark rounded-bottom shadow-lg mt-2 w-100 text-center d-md-none"
          >
            <ul class="navbar-nav py-2">
              <li class="nav-item my-1">
                <a href="#" class="nav-link text-white fw-semibold" data-bs-toggle="modal" data-bs-target="#aboutModal" @click="isNavOpen = false">About</a>
              </li>
              <li class="nav-item my-1">
                <a href="#" class="nav-link text-white fw-semibold" data-bs-toggle="modal" data-bs-target="#contactModal" @click="isNavOpen = false">Contact</a>
              </li>
              <li class="nav-item my-1">
                <a href="#" class="nav-link text-white fw-semibold" @click.prevent="() => { toggleTheme(); isNavOpen = false; }">Comfort View</a>
              </li>
            </ul>
          </div>
        </transition>

        <!-- Desktop Nav -->
        <div class="collapse navbar-collapse justify-content-end d-none d-md-flex">
          <ul class="navbar-nav">
            <li class="nav-item mx-2">
              <a href="#" class="nav-link text-white fw-semibold" data-bs-toggle="modal" data-bs-target="#aboutModal">About</a>
            </li>
            <li class="nav-item mx-2">
              <a href="#" class="nav-link text-white fw-semibold" data-bs-toggle="modal" data-bs-target="#contactModal">Contact</a>
            </li>
            <li class="nav-item mx-2">
              <a href="#" class="nav-link text-white fw-semibold" @click.prevent="toggleTheme">Comfort View</a>
            </li>
          </ul>
        </div>
      </div>
    </nav>

    <!-- Auth Section -->
    <div class="hero-section d-flex justify-content-center align-items-center">
      <div class="auth-card p-4">
        <!-- Tabs -->
        <ul class="nav nav-tabs mb-4">
          <li class="nav-item">
            <a href="#" class="nav-link" :class="{ active: activeTab === 'login' }" @click.prevent="activeTab = 'login'">Login</a>
          </li>
          <li class="nav-item">
            <a href="#" class="nav-link" :class="{ active: activeTab === 'register' }" @click.prevent="activeTab = 'register'">Register</a>
          </li>
        </ul>

        <!-- Login Form -->
        <div v-if="activeTab === 'login'">
          <h4 class="mb-3 fw-bold">Login</h4>
          <form @submit.prevent="loginUser">
            <div class="mb-3">
              <label class="form-label">Mobile Number</label>
              <input v-model="phone" @input="onlyDigits('phone')" maxlength="10" required type="text" class="form-control rounded-3" placeholder="Enter mobile number" />
            </div>

            <div class="mb-3">
              <label class="form-label">Password</label>
              <div class="input-group">
                <input :type="showPassword ? 'text' : 'password'" v-model="password" @input="onlyDigits('password')" maxlength="10" required class="form-control rounded-start-3" placeholder="Enter your password" />
                <button type="button" class="pin-eye-btn rounded-end-3" @click="showPassword = !showPassword">
                  <i :class="showPassword ? 'bi bi-eye-slash' : 'bi bi-eye'"></i>
                </button>
              </div>
            </div>

            <div class="mb-3 text-end">
              <a href="#" class="small text-info text-decoration-none" @click.prevent="resendPassword">Forgot Password?</a>
            </div>

            <button type="submit" class="btn btn-primary w-100 rounded-3 py-2">Login</button>
          </form>
          <p class="text-center text-muted mt-3 small">Or register a new account</p>
        </div>

        <!-- Register Role Selection -->
        <div v-else>
          <h4 class="mb-4 fw-bold">Choose your role</h4>
          <div class="d-grid gap-3">
            <div class="role-card p-3 rounded-4 d-flex align-items-center justify-content-between">
              <div>
                <h5 class="mb-1 fw-bold">I am a Caretaker</h5>
                <p class="small mb-2">Support seniors, manage health, and provide daily assistance.</p>
                <button class="btn btn-filled" @click="goToRegister('caretaker')">Register as Caretaker</button>
              </div>
              <div class="circle-indicator bg-info"></div>
            </div>

            <div class="role-card p-3 rounded-4 d-flex align-items-center justify-content-between">
              <div>
                <h5 class="mb-1 fw-bold">I am a Senior Citizen</h5>
                <p class="small mb-2">Monitor your health, routines, and connect with caretakers.</p>
                <button class="btn btn-filled" @click="goToRegister('senior')">Register as Senior Citizen</button>
              </div>
              <div class="circle-indicator bg-info"></div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- About Modal -->
    <div class="modal fade" id="aboutModal" tabindex="-1">
      <div class="modal-dialog modal-dialog-centered">
        <div class="modal-content rounded-4">
          <div class="modal-header">
            <h5 class="modal-title">About SeniorSphere</h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
          </div>
          <div class="modal-body text-start">
            SeniorSphere helps senior citizens with a safer, simpler digital life through intuitive technology and care-centered design.
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
            <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
          </div>
          <div class="modal-body text-start">
            📞 Phone: +91-123-456-7890<br />
            📧 Email: support@seniorsphere.in<br />
            📍 Address: 123 Elder Care Lane, New Delhi, India
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import Toast from 'primevue/toast';

export default {
  name: "LoginPage",
  components: { Toast },
  data() {
    return {
      phone: '',
      password: '',
      showPassword: false,
      isDarkTheme: false,
      isNavOpen: false,
      activeTab: 'login',
    };
  },
  methods: {
    toggleTheme() {
      this.isDarkTheme = !this.isDarkTheme;
    },
    onlyDigits(field) {
      this[field] = this[field].replace(/\D/g, '');
    },
    resendPassword() {
      this.$toast.add({
        severity: 'info',
        summary: 'Password Reset',
        detail: 'Your Password is Sent to your Registered Mobile Number.',
        life: 3000
      });
    },
    goToRegister(role) {
      const routes = {
        caretaker: '/Register/Caretaker',
        senior: '/Register/SeniorCitizen'
      };
      this.$router.push(routes[role] || '/');
    },
    async loginUser() {
  if (this.phone.length !== 10) {
    return this.$toast.add({
      severity: 'warn',
      summary: 'Invalid Mobile',
      detail: 'Incorrect Mobile Number Entered.',
      life: 3000
    });
  }

  if (this.password.length < 4 || this.password.length > 10) {
    return this.$toast.add({
      severity: 'warn',
      summary: 'Invalid Password',
      detail: 'Incorrect password Entered.',
      life: 3000
    });
  }

  try {
    const res = await fetch("http://127.0.0.1:5000/api/login", {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ contact: this.phone, password: this.password })
    });

    const data = await res.json();
    if (!res.ok) throw new Error(data.error);
    if (data.isVerified === 0) {
      this.$toast.add({
        severity: 'warn',
        summary: 'Account Not Verified',
        detail: 'Your account is not verified yet.',
        life: 3000
      });
      return this.$router.push('/login'); // Redirect to the login page
    }
    if (data.isVerified === 2) {
      this.$toast.add({
        severity: 'error',
        summary: 'Application Rejected',
        detail: 'Your application has been rejected. Contact Support.',
        life: 3000
      });
      return this.$router.push('/login'); // Redirect to the login page
    }
    if (data.isBlocked === true) {
      this.$toast.add({
        severity: 'error',
        summary: 'Account Blocked',
        detail: 'Your account has been blocked due to poor reputation. Contact Support.',
        life: 3000
      });
      return this.$router.push('/login'); // Redirect to the login page
    }

    localStorage.setItem('accessToken', data.access_token);
    localStorage.setItem('role', data.role);

    const roleRoute = {
      'SENIOR_CITIZEN': '/dashboard',
      'CARETAKER': '/caretaker_dash'
    };

    this.$router.push(roleRoute[data.role] || '/admin');
  } catch (err) {
    this.$toast.add({
      severity: 'error',
      summary: 'Login Failed',
      detail: err.message || 'Check your connection.',
      life: 3000
    });
  }
}
  }
};
</script>


<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Quicksand:wght@400;600;700&display=swap');
@import url('https://cdn.jsdelivr.net/npm/bootstrap-icons@1.10.5/font/bootstrap-icons.css');

.homepage {
  font-family: 'Quicksand', sans-serif;
  min-height: 100vh;
  background: url("@/assets/senior-bg.jpg") no-repeat center center fixed;
  background-size: cover;
}

.glass-navbar {
  background-color: rgba(255, 255, 255, 0.05);
  backdrop-filter: blur(8px);
  height: 60px;
  z-index: 999;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.typewriter-text {
  animation: typing 3s steps(30, end), blink-caret 0.75s step-end infinite;
  white-space: nowrap;
  overflow: hidden;
  border-right: 3px solid white;
}
@keyframes typing {
  from { width: 0; }
  to { width: 14ch; }
}
@keyframes blink-caret {
  0%, 100% { border-color: transparent; }
  50% { border-color: rgba(255, 255, 255, 0); }
}

.hero-section {
  height: 100vh;
  padding-top: 80px;
}

.auth-card {
  max-width: 400px;
  width: 100%;
  background: rgba(255, 255, 255, 0.2);
  backdrop-filter: blur(15px);
  border-radius: 20px;
  padding: 2rem;
  color: #000;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
}

.auth-card input {
  background-color: #f8f8f8;
  border: none;
}

.modal-content {
  font-family: 'Quicksand', sans-serif;
  padding: 1.5rem;
  border-radius: 1rem;
  background-color: #fff;
}

.dark {
  background: linear-gradient(135deg, #1c1c1c, #2d2d2d);
  color: white;
}
.dark .glass-navbar { background-color: rgba(0, 0, 0, 0.5); }
.dark .modal-content, .dark .auth-card { background-color: #2a2a2a; color: white; }
.dark .auth-card input { background-color: #444; color: white; }

.nav-tabs .nav-link {
  background: transparent;
  border: none;
  color: #fff;
  font-weight: 600;
  position: relative;
  padding-bottom: 10px;
}
.nav-tabs .nav-link.active {
  color: #00d4ff;
  font-weight: 700;
}
.nav-tabs .nav-link.active::after {
  content: "";
  position: absolute;
  bottom: 0; left: 0;
  width: 100%; height: 3px;
  background-color: #00d4ff;
  border-radius: 2px;
}

.pin-eye-btn {
  background-color: rgba(255, 255, 255, 0.15);
  border: none;
  backdrop-filter: blur(6px);
  padding: 0.5rem 0.75rem;
}
.pin-eye-btn:hover {
  background-color: rgba(255, 255, 255, 0.25);
  box-shadow: 0 0 6px rgba(0, 212, 255, 0.4);
}
.pin-eye-btn i { color: white; font-size: 1.1rem; }

.role-card {
  background-color: hsla(0, 0%, 100%, 0.05);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.1);
  transition: transform 0.2s;
}
.role-card:hover {
  transform: scale(1.02);
  box-shadow: 0 0 8px rgb(0, 213, 255);
}

.btn-filled {
  background-color: #0d6efd;
  color: white;
  border: none;
  transition: background-color 0.3s ease;
}
.btn-filled:hover {
  background-color: #dc3545;
}

.fade-enter-active, .fade-leave-active {
  transition: all 0.3s ease;
}
.fade-enter-from, .fade-leave-to {
  opacity: 0;
  transform: translateY(-10px);
}

</style>
