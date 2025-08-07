<template>
  <div class="p-4 space-y-6">
    <!-- Navigation Tabs -->
    <div class="flex flex-wrap gap-4 mb-6">
      <RouterLink
        to="/user-dashboard"
        class="px-4 py-2 rounded font-medium transition"
        :class="tab === 'books' ? activeTabClass : tabClass"
        @click="tab = 'books'"
      >
        📚 Books
      </RouterLink>

      <RouterLink
        to="/cart"
        class="px-4 py-2 rounded font-medium transition"
        :class="tab === 'cart' ? activeTabClass : tabClass"
        @click="tab = 'cart'"
      >
        🛒 Cart
      </RouterLink>

      <RouterLink
        to="/checkout"
        class="px-4 py-2 rounded font-medium transition"
        :class="tab === 'checkout' ? activeTabClass : tabClass"
        @click="tab = 'checkout'"
      >
        💸 Checkout
      </RouterLink>

      <RouterLink
        to="/orders"
        class="px-4 py-2 rounded font-medium transition"
        :class="tab === 'orders' ? activeTabClass : tabClass"
        @click="tab = 'orders'"
      >
        🧾 Order History
      </RouterLink>
    </div>

    <!-- Cart Summary -->
    <div>
      <h2 class="text-xl font-semibold mb-4">💳 Checkout</h2>

      <div v-if="cart.length === 0" class="text-gray-500">
        Your cart is empty.
      </div>

      <div v-else class="space-y-4">
        <div
          v-for="item in cart"
          :key="item.bookId"
          class="border p-4 rounded flex justify-between items-center"
        >
          <div>
            <div class="font-semibold">{{ item.title }}</div>
            <div>Price: ${{ item.price }}</div>
            <div>Quantity: {{ item.quantity }}</div>
          </div>
          <div class="font-semibold">
            ${{ (item.price * item.quantity).toFixed(2) }}
          </div>
        </div>

        <div class="text-right text-lg font-semibold">
          Total: ${{ cartTotal }}
        </div>

        <!-- Payment Method -->
        <div>
          <label class="block mb-2 font-medium">Payment Method</label>
          <select v-model="paymentMethod" class="border px-4 py-2 rounded w-full max-w-sm">
            <option disabled value="">Select a payment method</option>
            <option value="Cash">Cash</option>
            <option value="ABA Bank">ABA Bank</option>
            <option value="Acleda Bank">Acleda Bank</option>
          </select>
        </div>

        <!-- Confirm Button -->
        <button
          @click="checkout"
          class="bg-green-600 text-white px-6 py-2 rounded hover:bg-green-700 transition"
          :disabled="loading || !paymentMethod"
        >
          {{ loading ? 'Processing...' : 'Confirm Order' }}
        </button>

        <!-- Error Message -->
        <div v-if="error" class="text-red-600 mt-2">
          {{ error }}
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
      cart: [],
      paymentMethod: '',
      loading: false,
      error: '',
      tab: 'checkout',
      tabClass: 'bg-gray-100 hover:bg-gray-200',
      activeTabClass: 'bg-blue-600 text-white',
    };
  },
  computed: {
    cartTotal() {
      return this.cart
        .reduce((total, item) => total + item.price * item.quantity, 0)
        .toFixed(2);
    },
  },
  methods: {
    loadCart() {
      const stored = localStorage.getItem('cart');
      this.cart = stored ? JSON.parse(stored) : [];
    },
    async checkout() {
      this.error = '';
      this.loading = true;

      try {
        const token = localStorage.getItem('token'); // adjust if using cookies

        const response = await axios.post(
          '/api/orders/',
          {
            items: this.cart.map((item) => ({
              book_id: item.bookId,
              quantity: item.quantity,
            })),
            payment_method: this.paymentMethod,
          },
          {
            headers: {
              Authorization: `Bearer ${token}`,
            },
          }
        );

        // Clear cart
        localStorage.removeItem('cart');
        this.cart = [];

        // Redirect to order history
        this.$router.push('/orders');
      } catch (err) {
        console.error(err);
        this.error = err.response?.data?.detail || 'Checkout failed. Please try again.';
      } finally {
        this.loading = false;
      }
    },
  },
  
  mounted() {
    this.loadCart();
  },
};
</script>
