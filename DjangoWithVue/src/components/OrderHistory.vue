<template>
  <div class="p-4 space-y-6">
    <h2 class="text-xl font-semibold">🧾 Order History</h2>

    <div v-if="orders.length === 0" class="text-gray-500">
      No orders found.
    </div>

    <div v-else class="space-y-4">
      <div
        v-for="order in orders"
        :key="order.id"
        class="border p-4 rounded"
      >
        <div class="font-semibold">Order #{{ order.id }}</div>
        <div>Date: {{ order.date }}</div>
        <div>Total: ${{ order.total }}</div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      orders: [],
    };
  },
  mounted() {
    this.fetchOrderHistory();
  },
  methods: {
    async fetchOrderHistory() {
      try {
        const response = await axios.get('http://127.0.0.1:8000/api/orders/');
        this.orders = response.data;
      } catch (error) {
        console.error('Failed to fetch order history:', error);
      }
    },
  },
};
</script>
