<template>
  <div class="d-flex vh-100">
    <!-- Sidebar -->
    <aside :class="['bg-dark text-white p-3 d-flex flex-column', sidebarCollapsed ? 'd-none d-md-flex' : '']" style="width: 220px;">
      <div class="d-flex justify-content-between mb-4">
        <button @click="goBack" class="btn btn-outline-light btn-sm">←</button>
        <button @click="goForward" class="btn btn-outline-light btn-sm">→</button>

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
        <div class="d-flex gap-2">
          <button class="btn btn-outline-dark" @click="downloadDummyPDF">📄Export PDF</button>
          <button class="btn btn-danger" @click="logout">Logout</button>
        </div>
      </header>

      <!-- Assigned Senior Citizens Table -->
      <div class="p-4">
        <h5 class="fw-bold mb-3">👥 Assigned Senior Citizens</h5>
        <div class="table-responsive">
          <table class="table table-bordered table-hover">
            <thead class="table-dark">
              <tr>
                <th>Name</th>
                <th>Age</th>
                <th>Location</th>
                <th>Health Condition</th>
                <th>Action</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="senior in seniors" :key="senior.id">
                <td>{{ senior.name }}</td>
                <td>{{ senior.age }}</td>
                <td>{{ senior.city }}</td>
                <td>{{ senior.medCon }}</td>
                <td><button class="btn btn-sm btn-info" @click="viewDetails(senior)">View Details</button></td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <!-- Emergency Section -->
      <div class="emergency-area bg-white p-4 rounded shadow-sm mb-4 border border-danger">
        <h5 class="fw-bold text-danger mb-3">🚨 Emergency Alerts</h5>
        <div v-if="emergencyCases.length">
          <ul class="list-group">
            <li
              v-for="(caseItem, index) in emergencyCases"
              :key="index"
              class="list-group-item d-flex justify-content-between align-items-center"
            >
              <button class="btn btn-danger w-100 text-start" @click="resolveEmergency(caseItem)">
                <strong>{{ caseItem.name }}</strong> — <span class="text-white">{{ caseItem.issue }}</span>
              </button>
            </li>
          </ul>
        </div>
        <p v-else class="text-muted">No emergency alerts at the moment.</p>
      </div>

      <!-- Missed Tasks -->
      <div class="mb-4 px-4">
        <h6 class="mt-3">❌ Missed Tasks</h6>
        <ul class="list-group">
          <li v-for="(task, i) in missedTasks" :key="i" class="list-group-item d-flex justify-content-between align-items-center">
            {{ task.date }} - {{ task.senior }} missed {{ task.task }}
            <span class="badge bg-danger">Missed</span>
          </li>
        </ul>
      </div>

      <!-- SOS Alerts -->
      <div class="mb-4 px-4">
        <h6>🆘 SOS Alerts</h6>
        <ul class="list-group">
          <li v-for="(sos, i) in sosAlerts" :key="i" class="list-group-item d-flex justify-content-between align-items-center">
            {{ sos.time }} - {{ sos.senior }} pressed SOS ({{ sos.reason }})
            <span 
              class="badge"
              :class="sos.isResolved ? 'bg-success text-white' : 'bg-warning text-dark'"
            >
              {{ sos.isResolved ? 'Resolved' : 'Pending' }}
            </span>

            <span class="badge bg-warning text-dark">SOS</span>
          </li>
        </ul>
      </div>

      <!-- Raised Queries -->
      <div class="mb-4 px-4">
  <h6>❓ Raised Queries</h6>
  <ul class="list-group">
    <li 
      v-for="(query, i) in raisedQueries" 
      :key="i" 
      class="list-group-item d-flex justify-content-between align-items-center"
    >
      <div>
        {{ query.date }} - {{ query.senior }} asked: "{{ query.question }}"
      </div>

      <div class="d-flex align-items-center gap-2">
        <span 
          class="badge" 
          :class="query.status==='Resolved' ? 'bg-success text-white' : 'bg-warning text-dark'"
        >
          {{ query.status }}
        </span>
        <button v-if="query.status !== 'Resolved'"
          class="btn btn-sm" 
          :class="query.status === 'Resolved' ? 'btn-secondary' : 'btn-primary'" 
          @click="resolveQuery(query.queryId)"
        >
          Resolve
        </button>
      </div>
    </li>
  </ul>
</div>

    </main>
  </div>
</template>

<script setup>
import { onMounted, ref } from 'vue';
import { useRouter } from 'vue-router';

const router = useRouter();
const sidebarCollapsed = ref(false);
const seniors = ref([]);
const emergencyCases = ref([]);
const missedTasks = ref([]);
const sosAlerts = ref([]);
const raisedQueries = ref([]);

const goBack = () => window.history.back();
const goForward = () => window.history.forward();

const logout = () => {
  localStorage.clear();
  router.push('/login');
};

const toggleSidebar = () => {
  sidebarCollapsed.value = !sidebarCollapsed.value;
};

const fetchData = async () => {
  const token = localStorage.getItem('accessToken');
  const headers = { Authorization: `Bearer ${token}` };

  try {
    seniors.value = await fetch('http://127.0.0.1:5000/api/caretaker/dashboard', { headers }).then((r) => r.json());
    emergencyCases.value = await fetch('http://127.0.0.1:5000/api/caretaker/emergencies', { headers }).then((r) => r.json());
    missedTasks.value = await fetch('http://127.0.0.1:5000/api/caretaker/missed-tasks', { headers }).then((r) => r.json());
    sosAlerts.value = await fetch('http://127.0.0.1:5000/api/caretaker/sos-alerts', { headers }).then((r) => r.json());
    raisedQueries.value = await fetch('http://127.0.0.1:5000/api/caretaker/queries', { headers }).then((r) => r.json());
  } catch (err) {
    console.error('Error fetching data:', err);
  }
};

const resolveQuery = async (queryId) => {
  const token = localStorage.getItem('accessToken');
  const headers = {
    Authorization: `Bearer ${token}`,
    'Content-Type': 'application/json'
  };

  try {
    await fetch('http://127.0.0.1:5000/api/caretaker/queries', {
      method: 'PUT',
      headers,
      body: JSON.stringify({ queryId })
    })
    // show message
    alert('Query resolved successfully!');
  }
     catch (err) {
    console.error('Error resolving Query:', err);
  }
}

const resolveEmergency = async (caseItem) => {
  const token = localStorage.getItem('accessToken');
  const headers = {
    Authorization: `Bearer ${token}`,
    'Content-Type': 'application/json'
  };

  try {
    await fetch('http://127.0.0.1:5000/api/caretaker/emergencies', {
      method: 'PUT',
      headers,
      body: JSON.stringify({ alertId: caseItem.alertId })
    });

    // remove from list in frontend
    emergencyCases.value = emergencyCases.value.filter(e => e.alertId !== caseItem.alertId);
  } catch (err) {
    console.error('Error resolving emergency:', err);
  }
};

// function formatTime(timeStr) {
//   if (!timeStr) return ""
//   // Split on "T" → take only the time part
//   const parts = timeStr.split("T")
//   if (parts.length < 2) return timeStr

//   const timePart = parts[1].slice(0,5) // "23:15"
//   return timePart
// }

onMounted(fetchData);

const viewDetails = (senior) => {
  alert(`Viewing details of ${senior.name}\nLocation: ${senior.city}\nCondition: ${senior.medCon}\nContact: ${senior.contact}\nEmergency Contact: ${senior.emergencyContactName} (${senior.emergencyContact})\nEmail: ${senior.emergencyEmail}`);
};

const downloadDummyPDF = () => {
  const content = `SeniorSphere Report\n\n- Missed Tasks: ${missedTasks.value.length}\n- SOS Alerts: ${sosAlerts.value.length}\n- Queries Raised: ${raisedQueries.value.length}`;
  const blob = new Blob([content], { type: 'application/pdf' });
  const link = document.createElement('a');
  link.href = URL.createObjectURL(blob);
  link.download = 'Caretaker_Report.pdf';
  link.click();
};
</script>

<style scoped>
html, body, #app {
  margin: 0;
  padding: 0;
  height: 100%;
  width: 100%;
}

.emergency-area {
  border-left: 5px solid red;
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
</style>
