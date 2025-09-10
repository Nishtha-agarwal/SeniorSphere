<template>
  <div class="d-flex vh-100">
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
        <h2 class="text-center mb-4">Caretaker Profile</h2>

        <!-- Caretaker Details Card -->
        <div class="card p-4 shadow-sm mb-4">
          <h4 class="mb-3">Caretaker Details</h4>
          <p><strong>Name:</strong> {{ caretaker.name }}</p>
          <p><strong>Age:</strong> {{ caretaker.age }}</p>
          <p><strong>Contact:</strong> {{ caretaker.contact }}</p>
          <p><strong>Email:</strong> {{ caretaker.email }}</p>
          <p><strong>Languages:</strong> {{ caretaker.languages.join(', ') }}</p>
          <p><strong>Qualifications:</strong> {{ caretaker.qualifications.join(', ') }}</p>
          <p><strong>About:</strong> {{ caretaker.about }}</p>
          <p><strong>Resume:</strong> <a :href="`http://127.0.0.1:5000/api/resume/${caretaker.resume}`" target="_blank">View Resume</a></p>
          <button class="btn btn-primary mt-3" @click="toggleEditForm">Edit Details</button>
        </div>

        <!-- Button to Update Medical Condition -->
        <div class="text-center mb-4">
          <button class="btn btn-secondary" @click="toggleMedicalConditionForm">Update Medical Condition</button>
        </div>

        <!-- Medical Condition Form -->
        <div v-if="showMedicalConditionForm" class="card p-4 shadow-sm">
          <h4 class="mb-3">Update Medical Condition</h4>
          <form @submit.prevent="updateMedicalCondition">
            <div class="mb-3">
              <label>Select Senior Citizen</label>
              <select v-model="selectedSenior" class="form-control">
                <option v-for="senior in seniors" :key="senior.id" :value="senior.id">
                  {{ senior.name }}
                </option>
              </select>
            </div>
            <div class="mb-3">
              <label>Medical Condition</label>
              <textarea v-model="medicalCondition" class="form-control"></textarea>
            </div>
            <button type="submit" class="btn btn-primary">Update</button>
            <button type="button" class="btn btn-secondary" @click="toggleMedicalConditionForm">Cancel</button>
          </form>
        </div>

        <!--Caretaker update form-->
        <div v-if="showEditForm" class="card p-4 shadow-sm">
          <h4 class="mb-3">Edit Caretaker Details</h4>
          <form @submit.prevent="updateCaretakerDetails">
            <div class="mb-3">
              <label>Name</label>
              <input v-model="caretaker.name" type="text" class="form-control" required />
            </div>

            <div class="mb-3">
              <label>Age</label>
              <input v-model="caretaker.age" type="number" class="form-control" required />
            </div>

            <div class="mb-3">
              <label>Email</label>
              <input v-model="caretaker.email" type="email" class="form-control" required />
            </div>

            <div class="mb-3">
              <label>Languages</label>
              <MultiSelect 
                v-model="caretaker.languages" 
                :options="languageOptions" 
                filter multiple chips 
                placeholder="Select languages" 
                class="w-100" 
              />
            </div>

            <div class="mb-3">
              <label>Qualifications</label>
              <MultiSelect 
                v-model="caretaker.qualifications" 
                :options="qualificationOptions" 
                filter multiple chips 
                placeholder="Select qualifications" 
                class="w-100" 
              />
            </div>

            <div class="mb-3">
              <label>About</label>
              <textarea v-model="caretaker.about" class="form-control"></textarea>
            </div>

            <button type="submit" class="btn btn-primary">Save Changes</button>
            <button type="button" class="btn btn-secondary" @click="toggleEditForm">Cancel</button>
          </form>
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
const toggleSidebar = () => (sidebarCollapsed.value = !sidebarCollapsed.value);

const goBack = () => window.history.back();
const goForward = () => window.history.forward();
const reload = () => location.reload();
const logout = () => router.push('/');

const caretaker = ref({
  name: '',
  age: '',
  contact: '',
  email: '',
  languages: [],
  qualifications: [],
  about: '',
  resume: '',
});

const languageOptions = ref([
  'English', 
  'Hindi', 
  'Tamil', 
  'Bengali', 
  'Telugu', 
  'Other'
])

const qualificationOptions = ref([
  'B.Sc Nursing', 
  'Diploma', 
  '12th Pass', 
  'ANM', 
  'GNM', 
  'Other'
])
const seniors = ref([]);
const selectedSenior = ref('');
const medicalCondition = ref('');
const showEditForm = ref(false);
const showMedicalConditionForm = ref(false);

const fetchCaretakerDetails = async () => {
  const token = localStorage.getItem('accessToken');
  const headers = { Authorization: `Bearer ${token}` };

  try {
    const res = await fetch('http://127.0.0.1:5000/api/caretaker/profile', { headers });
    if (!res.ok) {
      console.error('Failed to fetch caretaker details:', res.statusText);
      return;
    }

    const data = await res.json();
    caretaker.value = {
      name: data.name,
      age: data.age,
      contact: data.contact,
      email: data.email,
      languages: data.languages || [],
      qualifications: data.qualifications || [],
      about: data.about || '',
      resume: data.resume,
    };
  } catch (err) {
    console.error('Error fetching caretaker details:', err);
  }
};

const fetchAssignedSeniors = async () => {
  const token = localStorage.getItem('accessToken');
  const headers = { Authorization: `Bearer ${token}` };

  try {
    const res = await fetch('http://127.0.0.1:5000/api/caretaker/dashboard', { headers });
    if (!res.ok) {
      console.error('Failed to fetch assigned seniors:', res.statusText);
      return;
    }

    seniors.value = await res.json();
  } catch (err) {
    console.error('Error fetching assigned seniors:', err);
  }
};

const toggleMedicalConditionForm = () => {
  showMedicalConditionForm.value = !showMedicalConditionForm.value;
  if (showMedicalConditionForm.value) {
    fetchAssignedSeniors();
  }
};
const toggleEditForm = () => {
  showEditForm.value = !showEditForm.value;
};

const updateMedicalCondition = async () => {
  const token = localStorage.getItem('accessToken');
  const headers = { Authorization: `Bearer ${token}`, 'Content-Type': 'application/json' };

  try {
    const res = await fetch(`http://127.0.0.1:5000/api/senior/${selectedSenior.value}/medical-condition`, {
      method: 'PUT',
      headers,
      body: JSON.stringify({ condition: medicalCondition.value }),
    });

    if (!res.ok) {
      console.error('Failed to update medical condition:', res.statusText);
      return;
    }

    alert('Medical condition updated successfully');
    toggleMedicalConditionForm();
  } catch (err) {
    console.error('Error updating medical condition:', err);
  }
};

const updateCaretakerDetails = async () => {
  const token = localStorage.getItem('accessToken');
  const headers = { Authorization: `Bearer ${token}`, 'Content-Type': 'application/json' };
  try {
    const res = await fetch(`http://127.0.0.1:5000/api/caretaker/profile`, {
      method: 'PUT',
      headers,
      body: JSON.stringify({
        name: caretaker.value.name,
        age: caretaker.value.age,
        contact: caretaker.value.contact,
        email: caretaker.value.email,
        languages: caretaker.value.languages,
        qualifications: caretaker.value.qualifications,
        about: caretaker.value.about,
      }),
    });

    if (!res.ok) {
      console.error('Failed to update Details', res.statusText);
      return;
    }

    alert('Det6ails updated successfully');
    toggleEditForm();
  } catch (err) {
    console.error('Error updating Caretaker Details:', err);
  }
}
onMounted(fetchCaretakerDetails);
</script>

<style scoped>
html, body, #app {
  margin: 0;
  padding: 0;
  height: 100%;
  width: 100%;
  overflow: hidden;
}

.main-content {
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

.nav-link.active {
  background-color: #0d6efd;
  color: white;
}

.form-scroll-container {
  max-height: 70vh;
  overflow-y: auto;
  padding: 1rem;
  border-radius: 1rem;
  background: #f9f9f9;
  box-shadow: 0 0 12px rgba(0, 0, 0, 0.1);
}
</style>
