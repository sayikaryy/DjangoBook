<template>
  <div class="min-h-screen flex items-center justify-center bg-gray-100 px-4">
    <div class="w-full max-w-sm bg-white border border-gray-200 rounded-xl p-6 shadow-sm">
      <h2 class="text-2xl font-semibold text-gray-800 text-center mb-6">Login</h2>

      <form @submit.prevent="handleLogin" class="space-y-4">
        <!-- Email -->
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Username</label>
          <input
            v-model="email"
            type="text"
            required
            class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            placeholder="Enter your username"
          />
        </div>

        <!-- Password -->
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Password</label>
          <input
            v-model="password"
            type="password"
            required
            class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            placeholder="Enter your password"
          />
        </div>

        <!-- Submit Button -->
        <button
          type="submit"
          class="w-full bg-blue-600 text-white py-2 rounded-md hover:bg-blue-700 transition"
        >
          Sign In
        </button>

        <!-- Link -->
        <p class="text-sm text-center text-gray-500 mt-4">
          Don't have an account?
          <RouterLink to="/register" class="text-blue-600 hover:underline">
            Sign up
          </RouterLink>
        </p>
      </form>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import { RouterLink } from 'vue-router';

export default {
  data() {
    return {
      email: '',
      password: '',
    };
  },
  methods: {
    async handleLogin() {
      try {
        const response = await axios.post(
          'http://localhost:8000/api/token/',
          {
            username: this.email,
            password: this.password,
          },
          {
            withCredentials: true, // include HttpOnly cookies
            headers: {
              'Content-Type': 'application/json',
            },
          }
        );

        console.log('Login successful:', response.data);
        this.$router.push('/add-book');

      } catch (error) {
        console.error('Login failed:', error);
        alert('Login failed. Please check your credentials.');
      }
    },
  },
};
</script>
