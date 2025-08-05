<template>
  <div class="min-h-screen flex items-center justify-center bg-gray-100 px-4">
    <div class="w-full max-w-sm bg-white border border-gray-200 rounded-xl p-6 shadow-sm">
      <h2 class="text-2xl font-semibold text-gray-800 text-center mb-6">Register</h2>

      <form @submit.prevent="handleRegister" class="space-y-4">
        <!-- Username -->
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Username</label>
          <input
            v-model="username"
            type="text"
            required
            class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            placeholder="Enter a username"
          />
        </div>

        <!-- Email -->
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Email</label>
          <input
            v-model="email"
            type="email"
            required
            class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            placeholder="Enter your email"
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
            placeholder="Create a password"
          />
        </div>

        <!-- Submit Button -->
        <button
          type="submit"
          class="w-full bg-green-600 text-white py-2 rounded-md hover:bg-green-700 transition"
        >
          Sign Up
        </button>

        <!-- Link -->
        <p class="text-sm text-center text-gray-500 mt-4">
          Already have an account?
          <RouterLink to="/login" class="text-blue-600 hover:underline">
            Log in
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
      username: '',
      email: '',
      password: '',
    };
  },
  methods: {
    async handleRegister() {
      try {
        const response = await axios.post(
          'http://127.0.0.1:8000/api/register/', // Django endpoint
          {
            username: this.username,
            email: this.email,
            password: this.password,
          },
          {
            headers: {
              'Content-Type': 'application/json',
            },
          }
        );

        console.log('Registration successful:', response.data);
        alert('Registration successful! Please log in.');
        this.$router.push('/user-dashboard');

      } catch (error) {
        console.error('Registration failed:', error.response?.data || error);
        alert('Registration failed. Please check your input.');
      }
    },
  },
};
</script>
