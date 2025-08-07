<template>
  <div class="p-6 bg-gray-100 min-h-screen">
    <!-- Tabs -->
  

    <h1 class="text-3xl font-bold mb-6 text-gray-800">🛒 Admin Order Management</h1>

    <!-- Loading state -->
    <div v-if="loading" class="text-gray-500">Loading orders...</div>

    <!-- Empty orders -->
    <div v-else-if="orders.length === 0" class="text-gray-500">No orders found.</div>

    <!-- Orders list -->
    <div v-else class="space-y-6">
      <div
        v-for="order in orders"
        :key="order.id"
        class="bg-white rounded-xl shadow p-5 border"
      >
        <!-- Order Header -->
        <div class="flex justify-between items-center mb-3">
          <div>
            <p class="font-semibold">Order #{{ order.id }}</p>
            <p class="text-gray-500 text-sm">Customer: {{ order.customer_name || 'Unknown' }}</p>
            <p class="text-gray-500 text-sm">Date: {{ formatDate(order.date_ordered) }}</p>
          </div>
          <div>
            <select
              v-model="order.status"
              @change="updateStatus(order)"
              class="border rounded px-2 py-1"
            >
              <option>Pending</option>
              <option>Shipped</option>
              <option>Delivered</option>
              <option>Cancelled</option>
            </select>
          </div>
        </div>

        <!-- Order Items -->
        <table class="w-full text-left border-collapse">
          <thead>
            <tr class="bg-gray-100">
              <th class="p-2">Book</th>
              <th class="p-2">Quantity</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="item in order.items" :key="item.id" class="border-b">
              <td class="p-2">{{ item.book_title }}</td>
              <td class="p-2">{{ item.quantity }}</td>
            </tr>
          </tbody>
        </table>

        <!-- Order Footer -->
        <div class="mt-3 flex justify-end">
          <p class="font-bold text-lg">Total: ${{ order.total_amount || 0 }}</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      orders: [],
      loading: true,
      tab: 'orders',
      cart: []
    };
  },

  methods: {
    async fetchOrders() {
      try {
        const res = await axios.get("http://127.0.0.1:8000/api/orderadmin/", {
          withCredentials: true
        });

        this.orders = res.data.map(order => ({
          id: order.id,
          customer_name: order.customer?.user?.username || "Guest",
          date_ordered: order.date_ordered,
          status: order.status,
          total_amount: order.total_amount || 0,
          items: order.items.map(i => ({
            id: i.id,
            book_title: i.book_title || i.book,
            quantity: i.quantity
          }))
        }));
      } catch (err) {
        console.error("Error fetching orders:", err);
      } finally {
        this.loading = false;
      }
    },

    async updateStatus(order) {
      try {
        await axios.patch(`http://127.0.0.1:8000/api/orders/${order.id}/`, {
          status: order.status
        });
        alert(`Order #${order.id} status updated to ${order.status}`);
      } catch (err) {
        console.error("Error updating status:", err);
        alert("Failed to update status");
      }
    },

    formatDate(date) {
      return new Date(date).toLocaleString();
    }
  },

  computed: {
    cartCount() {
      return this.cart.reduce((sum, item) => sum + item.quantity, 0);
    },
    tabClass() {
      return 'bg-gray-100 text-gray-700 hover:bg-gray-200';
    },
    activeTabClass() {
      return 'bg-blue-600 text-white';
    }
  },

  mounted() {
    this.fetchOrders();

    // Load cart from localStorage (you can replace this with API logic if needed)
    const cartData = localStorage.getItem('cart');
    if (cartData) {
      try {
        this.cart = JSON.parse(cartData);
      } catch (e) {
        console.warn("Invalid cart JSON");
      }
    }
  }
};
</script>
