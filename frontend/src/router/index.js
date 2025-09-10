import { createRouter, createWebHistory } from 'vue-router';

import HomePage from '../components/HomePage.vue';
import UserLogin from '../components/UserLogin.vue';
import RegisterCaretaker from '../components/RegisterCaretaker.vue';
import RegisterSeniorCitizen from '../components/RegisterSeniorCitizen.vue';
import AdminDashboard from '../components/AdminDashboard.vue';
import FamilyDashboard from '../components/FamilyDashboard.vue';
import Routine from '../components/caretaker_routine.vue';
import Dashboard from '../components/caretaker_dash.vue';
import Profile from '../components/caretaker_profile.vue';
import Stats from '../components/caretaker_stats.vue';
import SeniorDashboard from '../components/SeniorDashboard.vue';
import SeniorProfile from '../components/SeniorProfile.vue';
import SeniorResources from '../components/SeniorResources.vue';
import SeniorSupport from '../components/SeniorSupport.vue';

const routes = [
  { path: '/',name: "HomePage", component: HomePage },
  { path: '/login', name: "UserLogin", component: UserLogin },
  { path: '/Register/Caretaker', name: "RegisterCaretaker", component: RegisterCaretaker },
  { path: '/Register/SeniorCitizen', name: "RegisterSeniorCitizen", component: RegisterSeniorCitizen },
  { path: '/admin', name: "AdminDashboard", component: AdminDashboard },
  { path: '/family', name: "FamilyDashboard", component: FamilyDashboard },
  { path: '/caretaker_dash', name:"CaretakerDashboard", component: Dashboard },
  { path: '/caretaker_routine', name:"DailyRoutine", component: Routine },
  { path: '/caretaker_profile', name:"Profile", component: Profile },
  { path: '/caretaker_stats', name:"Statistics", component: Stats },
  { path: '/dashboard', component: SeniorDashboard },
  { path: '/profile', component: SeniorProfile },
  { path: '/support', component: SeniorSupport },
  { path: '/resources', component: SeniorResources }
  
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;