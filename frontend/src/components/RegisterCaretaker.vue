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

    <!-- Form Section -->
    <div class="form-scroll-container">
      <div class="container d-flex justify-content-center align-items-start pt-4">
        <div class="glass-form p-4 rounded-4 shadow-lg" style="width: 100%; max-width: 600px">
          <h2 class="text-center mb-1 fw-bold">Register as Caretaker</h2>
          <p class="text-center text-white mb-4">Create your caretaker account to support seniors and connect with families.</p>

          <form @submit.prevent="submitForm">
            <div class="row">
              <div class="col-md-6 mb-3">
                <input type="text" class="form-control" v-model="fullName" placeholder="Full Name" required />
              </div>
              <div class="col-md-6 mb-3">
                <input type="text" class="form-control" v-model="age" placeholder="Age (in years)" maxlength="2" @input="validateAge" required />
              </div>
            </div>

            <div class="row">
              <div class="col-md-6 mb-3">
                <input type="email" class="form-control" v-model="email" placeholder="Email Address" required />
              </div>
              <div class="col-md-6 mb-3">
                <input type="tel" class="form-control" v-model="contact" placeholder="Contact Number" maxlength="10" @input="validateContact" required />
              </div>
              <div class="col-md-6 mb-3 position-relative">
                <input :type="showPassword ? 'text' : 'password'" class="form-control pe-5" :value="password" placeholder="Password (4-10 digits)" @input="validatePassword" maxlength="10" required />
                <i :class="showPassword ? 'bi bi-eye-slash-fill' : 'bi bi-eye-fill'" class="position-absolute" style="right: 25px; top: 50%; transform: translateY(-50%); cursor: pointer; color: #aaa;" @click="togglePasswordVisibility"></i>
                <div v-if="passwordError" class="text-danger mt-1">{{ passwordError }}</div>
              </div>
              <div class="col-md-6 mb-3">
                <MultiSelect v-model="languages" :options="languageOptions" filter multiple chips placeholder="Select languages" class="w-100" />
              </div>
              <div v-if="languages.includes('Other')" class="col-md-6 mb-3">
                <input type="text" class="form-control" v-model="otherLanguage" placeholder="Other Language" />
              </div>
            </div>

            <div class="mb-3">
              <MultiSelect v-model="qualifications" :options="qualificationOptions" filter multiple chips placeholder="Select qualifications" class="w-100" />
            </div>

            <div v-if="qualifications.includes('Other')" class="mb-3">
              <input type="text" class="form-control" v-model="otherQualification" placeholder="Other Qualification" />
            </div>

            <div class="mb-3">
              <textarea class="form-control" rows="4" v-model="about" placeholder="About You (brief experience/specialization and motivation)"></textarea>
            </div>

            <div class="mb-3">
              <label class="form-label text-white">Upload your resume (PDF/Doc)</label>
              <input type="file" class="form-control" @change="handleFileUpload" required />
            </div>

            <button type="submit" class="btn btn-danger w-100">Register</button>
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
            📞 +91-123-456-7890<br />
            📧 support@seniorsphere.in<br />
            📍 123 Elder Care Lane, New Delhi, India
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
  data() {
    return {
      fullName: '',
      age: '',
      email: '',
      contact: '',
      password: '',
      about: '',
      languages: [],
      qualifications: [],
      otherLanguage: '',
      otherQualification: '',
      resumeFile: null,
      showPassword: false,
      passwordError: '',
      isDarkTheme: false,
      isNavOpen: false,
      languageOptions: ['English', 'Hindi', 'Tamil', 'Bengali', 'Telugu', 'Other'],
      qualificationOptions: ['B.Sc Nursing', 'Diploma', '12th Pass', 'ANM', 'GNM', 'Other']
      
    };
  },
  components: {
    Toast,
    MultiSelect
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
    const value = event.target.value.replace(/\D/g, ''); // Removes all non-digits
    this.contact = value;
  },
    
    handleFileUpload(e) {
      this.resumeFile = e.target.files[0];
    },
    async submitForm() {
      if (this.password.length < 4 || this.password.length > 10) {
        return this.$toast.add({ severity: 'warn', summary: 'Invalid Password', detail: 'Password is too small.', life: 3000 });
        
      }
      if (this.contact.length !== 10) {
        return this.$toast.add({ severity: 'warn', summary: 'Invalid Mobile', detail: 'Incorrect Mobile Number Entered.', life: 3000 });
      }

      const formData = new FormData();
      formData.append('fullName', this.fullName);
      formData.append('age', this.age);
      formData.append('email', this.email);
      formData.append('contact', this.contact);
      formData.append('password', this.password);
      formData.append('about', this.about);

      const finalLanguages = [...this.languages];
      if (finalLanguages.includes('Other') && this.otherLanguage) {
        finalLanguages.splice(finalLanguages.indexOf('Other'), 1, this.otherLanguage);
      }
      formData.append('languages', JSON.stringify(finalLanguages));

      const finalQualifications = [...this.qualifications];
      if (finalQualifications.includes('Other') && this.otherQualification) {
        finalQualifications.splice(finalQualifications.indexOf('Other'), 1, this.otherQualification);
      }
      formData.append('qualifications', JSON.stringify(finalQualifications));

      if (this.resumeFile) {
        formData.append('resume', this.resumeFile);
      }

      try {
        const response = await fetch("http://127.0.0.1:5000/api/register/caretaker", {
          method: 'POST',
          body: formData
        });
        const data = await response.json();

        if (response.ok) {
          this.$toast.add({ severity: 'success', summary: 'Success', detail: 'Registration sent to admin.', life: 4000 });
          this.resetForm();
        } else {
          this.$toast.add({ severity: 'error', summary: 'Error', detail: data.error || 'Failed to register.', life: 4000 });
        }
      } catch (error) {
        this.$toast.add({ severity: 'error', summary: 'Error', detail: 'Unexpected error occurred.', life: 4000 });
      }
    },
    resetForm() {
      this.fullName = '';
      this.email = '';
      this.age = '';
      this.contact = '';
      this.password = '';
      this.about = '';
      this.languages = [];
      this.qualifications = [];
      this.otherLanguage = '';
      this.otherQualification = '';
      this.resumeFile = null;
      
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
