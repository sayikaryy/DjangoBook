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
        🛒 Cart<span v-if="cartCount > 0"> ({{ cartCount }})</span>
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

    <!-- Title -->
    <h2 class="text-2xl font-semibold mb-4">🛒 Your Cart</h2>

    <!-- Empty Cart -->
    <div v-if="cart.length === 0" class="text-gray-500 text-center">
      Your cart is empty.
    </div>

    <!-- Cart Items -->
    <div v-else class="space-y-4">
      <div
        v-for="(item, index) in cart"
        :key="item.id"
        class="flex justify-between items-center border border-gray-200 rounded p-4 shadow-sm"
      >
        <div>
          <div class="font-semibold text-lg">{{ item.book.title }}</div>
          <div class="text-sm text-gray-600">Price: ${{ item.book.price }}</div>
          <div class="mt-2">
            Quantity:
            <input
              type="number"
              v-model.number="item.quantity"
              @change="updateQuantity(index)"
              class="w-16 ml-2 border border-gray-300 px-2 py-1 rounded"
              min="1"
            />
          </div>
        </div>

        <button
          @click="removeFromCart(index)"
          class="text-red-600 font-medium hover:underline"
        >
          ✖ Remove
        </button>
      </div>

      <!-- Cart Total -->
      <div class="text-right text-lg font-semibold border-t pt-4">
        Total: ${{ cartTotal }}
      </div>
    </div>
  </div>
</template>

<script>
import axios from '@/utils/axios'; // ✅ use your custom axios instance
import { RouterLink } from 'vue-router';

export default {
  components: { RouterLink },
  data() {
    return {
      cart: [],
      tab: 'cart',
    };
  },
  computed: {
    cartTotal() {
      return this.cart
        .reduce((total, item) => total + item.book.price * item.quantity, 0)
        .toFixed(2);
    },
    cartCount() {
      return this.cart.reduce((sum, item) => sum + item.quantity, 0);
    },
    tabClass() {
      return 'bg-gray-100 text-gray-700 hover:bg-gray-200';
    },
    activeTabClass() {
      return 'bg-blue-600 text-white shadow-md';
    },
  },
  methods: {
    async fetchCart() {
      try {
        const response = await axios.get('/api/cart/');
        this.cart = response.data;
      } catch (error) {
        console.error('Failed to load cart:', error);
      }
    },
    async updateQuantity(index) {
      const item = this.cart[index];
      if (item.quantity <= 0) item.quantity = 1;

      try {
        await axios.put(`/api/cart/${item.id}/`, {
          quantity: item.quantity,
        });
      } catch (error) {
        console.error('Failed to update quantity:', error);
      }
    },
    async removeFromCart(index) {
      const item = this.cart[index];
      try {
        await axios.delete(`/api/cart/${item.id}/`);
        this.cart.splice(index, 1);
      } catch (error) {
        console.error('Failed to remove item from cart:', error);
      }
    },
  },
  mounted() {
    this.fetchCart();
  },
};
</script>

<style scoped>
input:focus {
  outline: none;
  border-color: #3a52ed;
  box-shadow: 0 0 0 2px rgba(124, 58, 237, 0.2);
}
</style>
