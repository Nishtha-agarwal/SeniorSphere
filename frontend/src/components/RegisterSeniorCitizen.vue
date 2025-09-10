<template>
  <div :class="['homepage', { dark: isDarkTheme }]">
    <Toast />

    <!-- Navbar -->
    <nav class="navbar navbar-expand-md fixed-top glass-navbar">
      <div class="container">
        <span class="navbar-brand fw-bold fs-3 text-white typewriter-text">SeniorSphere</span>

        <!-- Toggle Button -->
        <button
          class="navbar-toggler text-white border-0"
          type="button"
          @click="isNavOpen = !isNavOpen"
          aria-label="Toggle navigation"
        >
          <i class="bi bi-list fs-1"></i>
        </button>

        <!-- Mobile Menu -->
        <transition name="fade">
          <div
            v-if="isNavOpen"
            class="w-100 mt-2 bg-dark rounded-bottom shadow-lg d-md-none"
            style="position: absolute; top: 60px; left: 0; z-index: 998;"
          >
            <ul class="navbar-nav text-center py-2">
              <li class="nav-item my-1">
                <a class="nav-link text-white fw-semibold" href="/" @click="isNavOpen = false">Home</a>
              </li>
              <li class="nav-item my-1">
                <a class="nav-link text-white fw-semibold" href="#" data-bs-toggle="modal" data-bs-target="#aboutModal" @click="isNavOpen = false">About</a>
              </li>
              <li class="nav-item my-1">
                <a class="nav-link text-white fw-semibold" href="#" data-bs-toggle="modal" data-bs-target="#contactModal" @click="isNavOpen = false">Contact</a>
              </li>
              <li class="nav-item my-1">
                <a class="nav-link text-white fw-semibold" href="#" @click.prevent="toggleTheme">Comfort View</a>
              </li>
            </ul>
          </div>
        </transition>

        <!-- Desktop Menu -->
        <div class="collapse navbar-collapse justify-content-end d-none d-md-flex">
          <ul class="navbar-nav">
            <li class="nav-item mx-2">
              <a class="nav-link text-white fw-semibold" href="/">Home</a>
            </li>
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

    <!-- Registration Form -->
    <div class="form-scroll-container">
      <div class="container d-flex justify-content-center align-items-start pt-4">
        <div class="glass-form p-4 rounded-4 shadow-lg" style="width: 100%; max-width: 600px">
          <h2 class="text-center mb-1 fw-bold">Register as Senior Citizen</h2>
          <p class="text-center text-white mb-4">Create your SeniorSphere account</p>

          <form @submit.prevent="submitForm">
            <!-- Full Name -->
            <div class="mb-3">
              <input type="text" class="form-control" v-model="fullName" placeholder="Enter your name" required />
            </div>

            <!-- Age & Password -->
            <div class="row">
              <div class="col-md-6 mb-3">
                <input type="number" class="form-control" v-model="age" placeholder="Enter your age" min="0" required />
              </div>
              <div class="col-md-6 mb-3 position-relative">
                <input :type="showPassword ? 'text' : 'password'" class="form-control pe-5" :value="password" placeholder="Password (4-10 digits)" @input="validatePassword" maxlength="10" required />
                <i :class="showPassword ? 'bi bi-eye-slash-fill' : 'bi bi-eye-fill'" class="position-absolute" style="right: 25px; top: 50%; transform: translateY(-50%); cursor: pointer; color: #aaa;" @click="togglePasswordVisibility"></i>
                <div v-if="passwordError" class="text-danger mt-1">{{ passwordError }}</div>
              </div>
            </div>

            <!-- Contact -->
            <div class="mb-3">
              <input type="tel" class="form-control" v-model="contact" placeholder="Your Mobile Number" maxlength="10" @input="validateContact" required />
            </div>

            <!-- Languages -->
            <div class="mb-3">
              <MultiSelect v-model="languages" :options="languageOptions" filter multiple chips placeholder="Select languages" class="w-100" />
            </div>
            <div v-if="languages.includes('Other')" class="mb-3">
              <input type="text" class="form-control" v-model="otherLanguage" placeholder="Other Language" />
            </div>

            <!-- PIN, City & State -->
            <div class="mb-3">
              <input type="text" class="form-control" v-model="pincode" maxlength="6" placeholder="Enter PIN Code" @input="handlePinInput" required />
            </div>
            <div class="row">
              <div class="col-md-6 mb-3">
                <input type="text" class="form-control" v-model="city" placeholder="City (auto-filled)" readonly />
              </div>
              <div class="col-md-6 mb-3">
                <input type="text" class="form-control" v-model="state" placeholder="State (auto-filled)" readonly />
              </div>
            </div>

            <!-- Emergency Contact -->
            <div class="mb-3">
              <input type="text" class="form-control" v-model="emergencyContactName" placeholder="Emergency Contact Name" required />
            </div>
            <div class="mb-3">
              <input type="tel" class="form-control" v-model="emergencyContact" placeholder="Emergency Contact Number" maxlength="10" @input="validateEmergencyContact" required />
            </div>
            <div class="mb-3">
                <input type="email" class="form-control" v-model="emergencyEmail" placeholder="EmergencyEmail Address" required />
            </div>

            <button type="submit" class="btn btn-primary w-100">Register</button>
            <p class="text-center mt-3">
              Already have an account? <a href="/login" class="text-primary">Log in</a>
            </p>
          </form>
        </div>
      </div>
    </div>

    <!-- Modals -->
    <div class="modal fade" id="aboutModal" tabindex="-1">
      <div class="modal-dialog modal-dialog-centered">
        <div class="modal-content rounded-4 p-3">
          <div class="modal-header">
            <h5 class="modal-title">About SeniorSphere</h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
          </div>
          <div class="modal-body">
            SeniorSphere is designed to support elderly individuals through friendly, safe technology.
          </div>
        </div>
      </div>
    </div>

    <div class="modal fade" id="contactModal" tabindex="-1">
      <div class="modal-dialog modal-dialog-centered">
        <div class="modal-content rounded-4 p-3">
          <div class="modal-header">
            <h5 class="modal-title">Contact Us</h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
          </div>
          <div class="modal-body">
            📞 contact: +91-123-456-7890<br />
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
import MultiSelect from 'primevue/multiselect';

export default {
  components: { Toast, MultiSelect },
  data() {
    return {
      fullName: '',
      age: '',
      password: '',
      showPassword: false,
      passwordError: '',
      languages: [],
      otherLanguage: '',
      contact: '',
      pincode: '',
      city: '',
      state: '',
      emergencyContact: '',
      emergencyContactName: '',
      emergencyEmail: '',
      isDarkTheme: false,
      isNavOpen: false,
      languageOptions: ['English', 'Hindi', 'Tamil', 'Bengali', 'Telugu', 'Other'],
    };
  },
  methods: {
    toggleTheme() {
      this.isDarkTheme = !this.isDarkTheme;
      this.isNavOpen = false;
    },
    togglePasswordVisibility() {
      this.showPassword = !this.showPassword;
    },
    validatePassword(event) {
      const value = event.target.value;
      if (/^\d*$/.test(value)) {
        this.password = value;
        
      } else {
        event.target.value = this.password;
      }
    },
    
    validateContact(event) {
      this.contact = event.target.value.replace(/\D/g, '');
    },
    validateEmergencyContact(event) {
      this.emergencyContact = event.target.value.replace(/\D/g, '');
    },
    handlePinInput() {
      if (this.pincode.length === 6) {
        fetch(`https://api.postalpincode.in/pincode/${this.pincode}`)
          .then(res => res.json())
          .then(data => {
            if (data[0].Status === "Success") {
              const postOffice = data[0].PostOffice[0];
              this.city = postOffice.District;
              this.state = postOffice.State;
            } else {
              this.city = '';
              this.state = '';
              this.$toast.add({ severity: 'warn', summary: 'Invalid PIN', detail: 'Could not fetch city/state', life: 3000 });
            }
          })
          .catch(() => {
            this.city = '';
            this.state = '';
            this.$toast.add({ severity: 'error', summary: 'Error', detail: 'Failed to fetch from PIN API', life: 3000 });
          });
      }
    },
    async submitForm() {
      if (this.password.length < 4 || this.password.length > 10) {
        return this.$toast.add({ severity: 'warn', summary: 'Invalid Password', detail: 'Password is too small.', life: 3000 });
        
      }
      if (this.contact.length !== 10) {
        return this.$toast.add({ severity: 'warn', summary: 'Invalid Mobile', detail: 'Incorrect Mobile Number Entered.', life: 3000 });
      }
      if (this.emergencyContact.length !== 10) {
        return this.$toast.add({ severity: 'warn', summary: 'Invalid Mobile', detail: 'Incorrect Emergency Mobile Number Entered.', life: 3000 });
      }

      const finalLanguages = [...this.languages];
      if (finalLanguages.includes('Other') && this.otherLanguage) {
        finalLanguages.splice(finalLanguages.indexOf('Other'), 1, this.otherLanguage);
      }

      const formData = {
        fullName: this.fullName,
        age: this.age,
        password: this.password,
        languages: JSON.stringify(finalLanguages),
        pinCode: this.pincode,
        city: this.city,
        state: this.state,
        contact: this.contact,
        emergencyContactName: this.emergencyContactName,
        emergencyContact: this.emergencyContact,
        emergencyEmail: this.emergencyEmail
      };

      try {
        const response = await fetch("http://127.0.0.1:5000/api/register/senior", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(formData)
        });

        const data = await response.json();
        if (response.ok) {
          this.$toast.add({ severity: 'success', summary: 'Success', detail: 'Registration successful!', life: 4000 });
          this.resetForm();
        } else {
          this.$toast.add({ severity: 'error', summary: 'Error', detail: data.error || 'Registration failed', life: 4000 });
        }
      } catch (err) {
        this.$toast.add({ severity: 'error', summary: 'Error', detail: 'Server error occurred.', life: 4000 });
      }
    },
    resetForm() {
      this.fullName = '';
      this.age = '';
      this.password = '';
      this.languages = [];
      this.otherLanguage = '';
      this.contact = '';
      this.pincode = '';
      this.city = '';
      this.state = '';
      this.emergencyContact = '';
      this.emergencyContactName = '';
    }
  }
};
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Quicksand:wght@400;600;700&display=swap');
@import url('https://cdn.jsdelivr.net/npm/bootstrap-icons@1.10.5/font/bootstrap-icons.css');

.homepage {
  display: flex;
  flex-direction: column;
  height: 100vh;
  overflow: hidden;
  font-family: 'Quicksand', sans-serif;
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
.form-scroll-container {
  flex: 1;
  overflow-y: auto;
  padding-top: 80px;
}
.glass-form {
  background: rgba(255, 255, 255, 0.12);
  backdrop-filter: blur(18px);
  border: 1px solid rgba(255, 255, 255, 0.3);
  color: white;
  margin-bottom: 2rem;
}
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
.dark {
  background: linear-gradient(135deg, #1c1c1c, #2d2d2d);
}
.dark .glass-form,
.dark .glass-navbar {
  background: rgba(0, 0, 0, 0.25);
  color: #fff;
}
.dark .modal-content {
  background-color: #2a2a2a;
  color: #fff;
}
.fade-enter-active, .fade-leave-active {
  transition: all 0.3s ease;
}
.fade-enter-from, .fade-leave-to {
  opacity: 0;
  transform: translateY(-10px);
}

</style>
