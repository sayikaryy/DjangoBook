<!-- src/views/Login.vue -->
<template>
  <div class="min-h-screen flex items-center justify-center bg-gray-100 px-4">
    <div class="w-full max-w-sm bg-white border border-gray-200 rounded-xl p-6 shadow-sm">
      <h2 class="text-2xl font-semibold text-gray-800 text-center mb-6">Login</h2>

      <form @submit.prevent="handleLogin" class="space-y-4">
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Username</label>
          <input v-model="username" type="text" required
            class="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500"
            placeholder="Enter your username" />
        </div>

        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Password</label>
          <input v-model="password" type="password" required
            class="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500"
            placeholder="Enter your password" />
        </div>

        <button type="submit" class="w-full bg-blue-600 text-white py-2 rounded-md hover:bg-blue-700 transition">
          Log In
        </button>

        <p class="text-sm text-center text-gray-500 mt-4">
          Don't have an account?
          <RouterLink to="/register" class="text-blue-600 hover:underline">Sign up</RouterLink>
        </p>
      </form>
    </div>
  </div>
</template>

<script>
import axios from 'axios'; // Axios with auth setup
import { API_BASE_URL } from '../utils/auth';
export default {
  data() {
    return {
      API_BASE_URL,
      username: '',
      password: '',
    };
  },
  methods: {
  async handleLogin() {
  try {
    const res = await axios.post(API_BASE_URL+ '/api/token/', {
      username: this.username,
      password: this.password,
    }, { withCredentials: true }); // IMPORTANT: send cookies

    // Don't save tokens to localStorage anymore

    // You can still store user role if returned in response:
    // if ('is_admin' in res.data) {
    //   localStorage.setItem('is_admin', res.data.is_admin);
    // }

    // Redirect
    if (res.data.is_admin) {
      this.$router.push('/'); // Admin dashboard
    } else {
      this.$router.push('/user-dashboard'); // User dashboard
    }
  } catch (err) {
    console.error(err);
    alert('Login failed. Please check your credentials.');
  }
}

  },
};
</script>.
