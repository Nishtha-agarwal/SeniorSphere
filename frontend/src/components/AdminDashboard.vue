<template>
  <div class="d-flex vh-100 overflow-hidden">
    <!-- Sidebar -->
    <aside :class="['bg-dark text-white p-3 d-flex flex-column sidebar', { 'd-none': isSmallScreen && !sidebarVisible }]" style="width: 220px;">
      <div class="d-flex justify-content-between mb-4">
        <button @click="goBack" class="btn btn-outline-light btn-sm">←</button>
        <button @click="goForward" class="btn btn-outline-light btn-sm">→</button>
        <button @click="reload" class="btn btn-outline-light btn-sm">⟳</button>
      </div>
      <ul class="nav flex-column">
        <li class="nav-item mb-2">
          <button class="btn btn-outline-light w-100 text-start" @click="setView('stats')">Dashboard</button>
        </li>
        <li class="nav-item mb-2">
          <button class="btn btn-outline-light w-100 text-start" @click="setView('requests')">View Requests</button>
        </li>
        <li class="nav-item mb-2">
          <button class="btn btn-outline-light w-100 text-start" @click="setView('users')">View Users</button>
        </li>
        <li class="nav-item mb-2">
          <button class="btn btn-outline-light w-100 text-start" @click="setView('mapping')">Caretaker Assignment</button>
        </li>
      </ul>
    </aside>

    <!-- Main Content -->
    <main class="flex-grow-1 d-flex flex-column bg-light">
      <header class="bg-white border-bottom d-flex justify-content-between align-items-center p-3 shadow-sm">
        <div class="d-flex align-items-center">
          <button class="btn btn-outline-secondary d-md-none me-2" @click="toggleSidebar">☰</button>
          <img src="@/assets/logo.jpeg" alt="Logo" width="32" height="32" class="me-2" />
          <h5 class="mb-0 text-dark">SeniorSphere</h5>
        </div>
        <button class="btn btn-danger" @click="logout">Logout</button>
      </header>

      <div class="p-4 overflow-auto">
        <!-- Show "Admin Dashboard" only in the Dashboard view -->
        <h2 class="mb-3" v-if="currentView === 'stats'">Admin Dashboard</h2>

        <!-- Stats View -->
        <div v-if="currentView === 'stats'">
          <div class="row">
            <!-- Stats Cards -->
            <div class="col-md-3 mb-3">
              <div class="card text-white bg-primary shadow">
                <div class="card-body">
                  <h5 class="card-title">Total Users</h5>
                  <p class="card-text fs-4">{{ userCount + caretakerCount }}</p>
                </div>
              </div>
            </div>
            <div class="col-md-3 mb-3">
              <div class="card text-white bg-success shadow">
                <div class="card-body">
                  <h5 class="card-title">Senior Citizens</h5>
                  <p class="card-text fs-4">{{ userCount }}</p>
                </div>
              </div>
            </div>
            <div class="col-md-3 mb-3">
              <div class="card text-white bg-info shadow">
                <div class="card-body">
                  <h5 class="card-title">Caretakers</h5>
                  <p class="card-text fs-4">{{ caretakerCount }}</p>
                </div>
              </div>
            </div>
            <div class="col-md-3 mb-3">
              <div class="card text-white bg-warning shadow">
                <div class="card-body">
                  <h5 class="card-title">Pending Requests</h5>
                  <p class="card-text fs-4">{{ requests.length }}</p>
                </div>
              </div>
            </div>
          </div>

          <!-- Doughnut Chart -->
          <div class="row mt-4">
            <div class="col-md-6">
              <h5>Distribution of Users</h5>
              <DoughnutChart :chartData="doughnutChartData" />
            </div>
          </div>
        </div>

        <!-- Caretaker Requests View -->
        <div v-if="currentView === 'requests'">
          <h4>Caretaker Requests</h4>
          <div v-if="requests.length > 0">
            <div v-for="req in requests" :key="req.id" class="card mb-3">
              <div class="card-body">
                <h5 class="card-title">{{ req.name }}</h5>
                <p class="card-text">{{ req.about }}</p>
                <p><strong>Email:</strong> {{ req.email }}</p>
                <p><strong>Qualification:</strong> {{ req.qualification }}</p>
                <p><strong>Languages:</strong> {{ req.languages }}</p>
                <div>
                  <button class="btn btn-success btn-sm me-2" @click="handleCaretakerRequest(req.id, 'approve')">Approve</button>
                  <button class="btn btn-danger btn-sm" @click="handleCaretakerRequest(req.id, 'reject')">Reject</button>
                </div>
              </div>
            </div>
          </div>
          <div v-else>
            <p class="text-muted">No requests available.</p>
          </div>
        </div>

        <!-- Users View -->
        <div v-if="currentView === 'users'">
          <h4>All Users</h4>
          <div class="row">
            <div v-for="user in users" :key="user.id" class="col-md-3 mb-3">
              <div class="card text-white" :class="getUserCardClass(user.role)" style="cursor: pointer;" data-bs-toggle="modal" data-bs-target="#userDetailsModal" @click="selectUser(user)">
                <div class="card-body">
                  <h5 class="card-title">{{ user.name }}</h5>
                  <p class="card-text">{{ user.role }}</p>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Caretaker Assignment Section -->
        <div v-if="currentView === 'mapping'">
          <h4>Assign Caretakers to Senior Citizens</h4>
          <div class="row">
            <!-- Select Senior Citizen -->
            <div class="col-md-6 mb-3">
              <label for="seniorSelect" class="form-label">Select Senior Citizen</label>
              <select id="seniorSelect" class="form-select" v-model="selectedSenior">
                <option disabled value="">Select Senior Citizen</option>
                <option v-for="senior in filteredUsers" :key="senior.id" :value="senior">
                  {{ senior.name }}
                </option>
              </select>
            </div>
          </div>

          <!-- If a Senior Citizen is Selected -->
          <div v-if="selectedSenior">
            <!-- If the Senior Citizen is Already Assigned -->
            <div v-if="selectedSenior.assignedCaretaker">
              <p><strong>Assigned Caretaker:</strong> {{ getCaretakerName(selectedSenior.assignedCaretaker) }}</p>
              <button class="btn btn-danger" @click="unassignCaretaker(selectedSenior.id)">Unassign Caretaker</button>
            </div>

            <!-- If the Senior Citizen is Not Assigned -->
            <div v-else>
              <div class="row">
                <div class="col-md-6 mb-3">
                  <label for="caretakerSelect" class="form-label">Select Caretaker</label>
                  <select id="caretakerSelect" class="form-select" v-model="selectedCaretaker">
                    <option disabled value="">Select Caretaker</option>
                    <option v-for="caretaker in caretakers" :key="caretaker.id" :value="caretaker.id">
                      {{ caretaker.name }}
                    </option>
                  </select>
                </div>
              </div>
              <button class="btn btn-primary" @click="assignCaretakerToSenior">Assign Caretaker</button>
            </div>
          </div>
        </div>

        <!-- User Details Modal -->
        <div class="modal fade" id="userDetailsModal" tabindex="-1" aria-labelledby="userDetailsModalLabel" aria-hidden="true">
          <div class="modal-dialog modal-lg">
            <div class="modal-content">
              <div class="modal-header">
                <h5 class="modal-title" id="userDetailsModalLabel">{{ selectedUser?.name }}</h5>
                <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
              </div>
              <div class="modal-body">
                <p><strong>Role:</strong> {{ selectedUser?.role }}</p>
                <p v-if="selectedUser?.age"><strong>Age:</strong> {{ selectedUser.age }}</p>
                <p v-if="selectedUser?.contact"><strong>Contact:</strong> {{ selectedUser.contact }}</p>
                <p v-if="selectedUser?.languages"><strong>Languages:</strong> {{ selectedUser.languages }}</p>
                <p v-if="selectedUser?.city"><strong>City:</strong> {{ selectedUser.city }}</p>
                <p v-if="selectedUser?.state"><strong>State:</strong> {{ selectedUser.state }}</p>
                <p v-if="selectedUser?.qualification"><strong>Qualification:</strong> {{ selectedUser.qualification }}</p>
                <p v-if="selectedUser?.about"><strong>About:</strong> {{ selectedUser.about }}</p>
                <p v-if="selectedUser?.resumePath">
                <strong>Resume:</strong>
                <a :href="`http://127.0.0.1:5000/api/resume/${selectedUser.resumePath}`" target="_blank">View Resume</a>
              </p>
              </div>
              <div class="modal-footer">
                <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
                <button
                  v-if="selectedUser?.role === 'Caretaker' && !selectedUser?.isBlocked"
                  type="button"
                  class="btn btn-danger"
                  @click="blockCaretaker(selectedUser.id, 'block')"
                >
                  Block Caretaker
                </button>
                <button
                  v-if="selectedUser?.role === 'Caretaker' && selectedUser?.isBlocked"
                  type="button"
                  class="btn btn-success"
                  @click="blockCaretaker(selectedUser.id, 'unblock')"
                >
                  Unblock Caretaker
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onBeforeUnmount } from 'vue'
import { useRouter } from 'vue-router'
import DoughnutChart from './DoughnutChart.vue'

const router = useRouter()
const isSmallScreen = ref(false)
const sidebarVisible = ref(false)
const currentView = ref('stats')
const selectedUser = ref(null)
const userCount = ref(0)
const caretakerCount = ref(0)
const requests = ref([])
const users = ref([])
const selectedSenior = ref('');
const selectedCaretaker = ref('');


const checkScreenSize = () => {
  isSmallScreen.value = window.innerWidth < 768
  if (!isSmallScreen.value) sidebarVisible.value = false
}
onMounted(() => {
  checkScreenSize()
  window.addEventListener('resize', checkScreenSize)
  fetchDashboardData()
  fetchUsersData()
  fetchCaretakerRequests()
})
onBeforeUnmount(() => window.removeEventListener('resize', checkScreenSize))

const toggleSidebar = () => sidebarVisible.value = !sidebarVisible.value
const goBack = () => window.history.back()
const goForward = () => window.history.forward()
const reload = () => location.reload()
const logout = () => {
  localStorage.clear();
  router.push('/login')
}

const caretakers = computed(() => users.value.filter(u => u.role === 'Caretaker' && !u.isBlocked))
const filteredUsers = computed(() => users.value.filter(u => u.role === 'Senior Citizen' ))

const setView = (view) => {
  currentView.value = view
  selectUser.value = null
}
const selectUser = (user) => {
  selectedUser.value = user
}

// Get the card class based on the user's role
const getUserCardClass = (role) => {
  switch (role) {
    case 'Admin':
      return 'bg-danger';
    case 'Senior Citizen':
      return 'bg-primary';
    case 'Caretaker':
      return 'bg-success';
    default:
      return 'bg-secondary';
  }
};


const doughnutChartData = computed(() => ({
  labels: ['Senior Citizens', 'Caretakers'],
  datasets: [
    {
      data: [userCount.value, caretakerCount.value],
      backgroundColor: ['#4e73df', '#1cc88a'], // Colors for Senior Citizens and Caretakers
      hoverOffset: 4
    }
  ]
}));

async function fetchDashboardData() {
  try {
    const res = await fetch('http://127.0.0.1:5000/api/admin/dashboard', {
      method: 'GET',
      headers: {
        'Authorization': `Bearer ${localStorage.getItem('accessToken')}`
      }
    })
    if (!res.ok) throw new Error('Failed to fetch dashboard data')
    const data = await res.json()
  console.log('Dashboard data:', data)
    userCount.value = data.user_count
    caretakerCount.value = data.caretaker_count
  } catch (err) {
    console.error(err)
    alert('Error fetching dashboard data')
  }
}

const fetchUsersData = async () => {
  try {
    const res = await fetch('http://127.0.0.1:5000/api/admin/users', {
      method: 'GET',
      headers: {
        'Authorization': `Bearer ${localStorage.getItem('accessToken')}`
      }
    })
    if (!res.ok) throw new Error('Failed to fetch users data')
    users.value = await res.json()
  } catch (err) {
    console.error(err)
    alert('Error fetching users data')
  }
}

async function fetchCaretakerRequests() {
  try {
    console.log('Fetching caretaker requests...');
    const res = await fetch('http://127.0.0.1:5000/api/admin/caretaker-requests', {
      method: 'GET',
      headers: {
        'Authorization': `Bearer ${localStorage.getItem('accessToken')}`
      }
    });
    if (!res.ok) throw new Error('Failed to fetch caretaker requests');
    const data = await res.json();
    requests.value = data;
  } catch (err) {
    console.error(err);
    alert('Error fetching caretaker requests');
  }
}

async function handleCaretakerRequest(id, action) {
  try {
    const res = await fetch('http://127.0.0.1:5000/api/admin/approve-caretaker', {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${localStorage.getItem('accessToken')}`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ caretaker_id: id, action })
    });
    if (!res.ok) throw new Error('Failed to process caretaker request');
    const data = await res.json();
    alert(data.message);
    fetchCaretakerRequests(); // Refresh the requests list
  } catch (err) {
    console.error(err);
    alert('Error processing caretaker request');
  }
}

const assignCaretakerToSenior = async () => {
  if (!selectedSenior.value || !selectedCaretaker.value) {
    alert('Please select both a senior citizen and a caretaker.');
    return;
  }

  try {
    const res = await fetch('http://127.0.0.1:5000/api/admin/assign-caretaker', {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${localStorage.getItem('accessToken')}`,
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        senior_id: selectedSenior.value.id,
        caretaker_id: selectedCaretaker.value,
      }),
    });

    if (!res.ok) throw new Error('Failed to assign caretaker');
    const data = await res.json();
    alert(data.message);

    // Refresh the users list to reflect the updated assignments
    fetchUsersData();
    selectedSenior.value = null;
    selectedCaretaker.value = '';
  } catch (err) {
    console.error(err);
    alert('Error assigning caretaker');
  }
};

const unassignCaretaker = async (seniorId) => {
  if (!confirm('Are you sure you want to unassign the caretaker?')) return;

  try {
    const res = await fetch('http://127.0.0.1:5000/api/admin/assign-caretaker', {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${localStorage.getItem('accessToken')}`,
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        senior_id: seniorId,
        caretaker_id: null, // Unassign by setting caretaker_id to null
      }),
    });

    if (!res.ok) throw new Error('Failed to unassign caretaker');
    const data = await res.json();
    alert(data.message);

    // Refresh the users list to reflect the updated assignments
    fetchUsersData();
    selectedSenior.value = null;
  } catch (err) {
    console.error(err);
    alert('Error unassigning caretaker');
  }
};

const getCaretakerName = (caretakerId) => {
  const caretaker = caretakers.value.find((c) => c.id === caretakerId);
  return caretaker ? caretaker.name : 'Unknown';
};

async function blockCaretaker(caretakerId, action) {
  const confirmationMessage =
    action === "block"
      ? "Are you sure you want to block this caretaker?"
      : "Are you sure you want to unblock this caretaker?";
  if (!confirm(confirmationMessage)) return;

  try {
    const res = await fetch('http://127.0.0.1:5000/api/admin/block-caretaker', {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${localStorage.getItem('accessToken')}`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ caretaker_id: caretakerId, action })
    });

    if (!res.ok) throw new Error(`Failed to ${action} caretaker`);
    const data = await res.json();
    alert(data.message);

    // Update the UI to reflect the blocked/unblocked status
    const caretaker = users.value.find(user => user.id === caretakerId);
    if (caretaker) caretaker.isBlocked = action === "block";

    // Close the modal
    const modal = document.getElementById('userDetailsModal');
    if (modal) modal.querySelector('.btn-close').click();
  } catch (err) {
    console.error(err);
    alert(`Error trying to ${action} caretaker`);
  }
}


</script>

<style>
.sidebar {
  width: 220px;
  min-width: 220px;
}
</style>