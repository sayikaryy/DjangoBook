<template>
  <div class="p-6 bg-gradient-to-br from-purple-100 via-blue-50 to-pink-100 min-h-screen">
    <h1 class="text-3xl font-extrabold mb-6 text-gray-800 animate-fade-in">📚 SayikaStore Dashboard</h1>

    <!-- Stats Cards -->
    <div class="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
      <router-link 
        to="/books"
        class="glass-card p-6 flex flex-col items-center animate-slide-up hover:scale-105 transition"
      >
        <h2 class="text-lg text-gray-500">Total Books</h2>
        <p class="text-3xl font-bold text-blue-600">{{ totalBooks }}</p>
      </router-link>

      <router-link 
        to="/order-admin"
        class="glass-card p-6 flex flex-col items-center animate-slide-up delay-100 hover:scale-105 transition"
      >
        <h2 class="text-lg text-gray-500">Orders</h2>
        <p class="text-3xl font-bold text-green-600">{{ totalOrders }}</p>
        <p class="text-sm text-yellow-600 mt-1">Pending: {{ pendingOrders }}</p>
      </router-link>

      <router-link 
        to="/users"
        class="glass-card p-6 flex flex-col items-center animate-slide-up delay-200 hover:scale-105 transition"
      >
        <h2 class="text-lg text-gray-500">Users</h2>
        <p class="text-3xl font-bold text-purple-600">{{ totalUsers }}</p>
      </router-link>
    </div>

    <!-- Quick Actions -->
    <div class="glass-card p-6 mb-8 animate-slide-up delay-300">
      <h2 class="text-xl font-semibold mb-4 text-gray-800">⚡ Quick Actions</h2>
      <div class="flex flex-wrap gap-4">
        <router-link to="/add-book" class="btn-action bg-blue-600 hover:bg-blue-700">➕ Add New Book</router-link>
        <router-link to="/orders" class="btn-action bg-green-600 hover:bg-green-700">📦 Manage Orders</router-link>
        <router-link to="/users" class="btn-action bg-purple-600 hover:bg-purple-700">👥 Manage Users</router-link>
      </div>
    </div>

    <!-- Books Overview -->
    <div class="glass-card p-6 mb-8 animate-slide-up delay-400">
      <h2 class="text-xl font-semibold mb-4 text-gray-800">📖 Latest Books</h2>
      <div v-if="loading" class="text-gray-500">Loading books...</div>
      <div v-else-if="books.length === 0" class="text-gray-500">No books available.</div>

      <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-5">
        <div 
          v-for="book in books" 
          :key="book.id"
          class="rounded-xl bg-white/80 backdrop-blur-lg shadow hover:shadow-lg transition transform hover:scale-105 p-4 animate-fade-in"
        >
          <img 
            :src="book.image_url || 'https://via.placeholder.com/200x300?text=No+Image'" 
            alt="Book Cover"
            class="w-full h-60 object-cover rounded-lg mb-3"
          />
          <h3 class="text-lg font-bold text-gray-800 truncate">{{ book.title }}</h3>
          <p class="text-sm text-gray-500 mb-1">by {{ book.author }}</p>
          <p class="text-blue-600 font-semibold">${{ book.price }}</p>
        </div>
      </div>
    </div>

    <!-- Recent Orders -->
    <div class="glass-card p-6 animate-slide-up delay-500">
      <h2 class="text-xl font-semibold mb-4 text-gray-800">🛒 Recent Orders</h2>
      <div v-if="loading" class="text-gray-500">Loading orders...</div>
      <div v-else-if="recentOrders.length === 0" class="text-gray-500">No recent orders.</div>

      <table v-else class="w-full border-collapse">
        <thead class="bg-gray-200 text-left">
          <tr>
            <th class="py-2 px-4">Order ID</th>
            <th class="py-2 px-4">Customer</th>
            <th class="py-2 px-4">Date</th>
            <th class="py-2 px-4">Status</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="order in recentOrders" :key="order.id" class="border-b hover:bg-gray-50 transition">
            <td class="py-2 px-4">#{{ order.id }}</td>
            <td class="py-2 px-4">{{ order.customer_name || 'Unknown' }}</td>
            <td class="py-2 px-4">{{ new Date(order.date_ordered).toLocaleDateString() }}</td>
            <td class="py-2 px-4">
              <span :class="statusClass(order.status)">
                {{ order.status }}
              </span>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      totalBooks: 0,
      totalOrders: 0,
      totalUsers: 0,
      pendingOrders: 0,
      books: [],
      recentOrders: [],
      loading: true
    };
  },
  methods: {
    statusClass(status) {
      switch (status) {
        case 'Pending': return 'text-yellow-600 font-semibold';
        case 'Shipped': return 'text-blue-600 font-semibold';
        case 'Delivered': return 'text-green-600 font-semibold';
        case 'Cancelled': return 'text-red-600 font-semibold';
        default: return 'text-gray-600';
      }
    },
    
    async fetchDashboardData() {
      try {
        const booksRes = await axios.get("http://127.0.0.1:8000/api/books/", { withCredentials: true });
        const ordersRes = await axios.get("http://127.0.0.1:8000/api/orderadmin/", { withCredentials: true });
        const usersRes = await axios.get("http://127.0.0.1:8000/api/users/", { withCredentials: true });

        this.books = booksRes.data.slice(-6).reverse();
        this.totalBooks = booksRes.data.length;
        this.totalOrders = ordersRes.data.length;
        this.totalUsers = usersRes.data.length;
        this.pendingOrders = ordersRes.data.filter(o => o.status === 'Pending').length;
        this.recentOrders = ordersRes.data.slice(-6).reverse();
      } catch (error) {
        console.error("Error fetching dashboard data:", error);
      } finally {
        this.loading = false;
      }
    }
  },
  mounted() {
    this.fetchDashboardData();
  }
};
</script>

<style scoped>
/* Glassmorphism card */
.glass-card {
  background: rgba(255, 255, 255, 0.8);
  backdrop-filter: blur(12px);
  border-radius: 1rem;
  box-shadow: 0 4px 20px rgba(0,0,0,0.05);
  transition: all 0.3s ease;
}

/* Quick Action Buttons */
.btn-action {
  padding: 0.5rem 1rem;
  color: #fff;
  border-radius: 0.5rem;
  font-weight: 500;
  transition: all 0.2s;
  transform: none;
  display: inline-block;
}
.btn-action:hover {
  transform: scale(1.05);
}

/* Fade Animation */
@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}
.animate-fade-in {
  animation: fadeIn 0.8s ease forwards;
}

/* Slide Up Animation */
@keyframes slideUp {
  from { transform: translateY(20px); opacity: 0; }
  to { transform: translateY(0); opacity: 1; }
}
.animate-slide-up {
  animation: slideUp 0s ease forwards;
}
.animate-slide-up.delay-100 { animation-delay: 0.1s; }
.animate-slide-up.delay-200 { animation-delay: 0.2s; }
.animate-slide-up.delay-300 { animation-delay: 0.3s; }
.animate-slide-up.delay-400 { animation-delay: 0.4s; }
.animate-slide-up.delay-500 { animation-delay: 0.5s; }
</style>
