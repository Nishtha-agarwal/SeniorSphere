<template>
  <div class="card shadow">
    <div class="card-body text-center">
      <h5 class="card-title mb-3">Users vs Caretakers</h5>

      <!-- Chart container with controlled size -->
      <div style="max-width: 250px; margin: auto;">
        <Doughnut :data="chartData" :options="chartOptions" />
      </div>
    </div>
  </div>
</template>

<script setup>
import { Doughnut } from 'vue-chartjs'
import { Chart as ChartJS, ArcElement, Tooltip, Legend } from 'chart.js'
import { defineProps } from 'vue';
ChartJS.register(ArcElement, Tooltip, Legend)

// Accept chartData as a prop
defineProps({
  chartData: {
    type: Object,
    required: true
  }
});

const chartOptions = {
  responsive: true,
  maintainAspectRatio: false, // Allow flexible sizing within container
  plugins: {
    legend: {
      position: 'bottom'
    }
  }
};
</script>
