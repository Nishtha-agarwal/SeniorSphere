<template>
  <div :class="['app-container', { dark: isDarkTheme }]">
    
    <Toast />

    
    <router-view />
  </div>
</template>

<script>
import Toast from 'primevue/toast';

export default {
  name: 'App',
  components: {
    Toast
  },
  data() {
    return {
      isDarkTheme: false
    };
  },
  methods: {
    toggleTheme() {
      this.isDarkTheme = !this.isDarkTheme;
    }
  }
};
</script>


<style>

.app-container {
  min-height: 100vh;
  background-color: #f8f9fa;
}

.app-container.dark {
  background-color: #121212;
  color: white;
}
</style>
