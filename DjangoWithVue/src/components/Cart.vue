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
        v-for="item in cart"
        :key="item.id"
        class="flex justify-between items-center border border-gray-200 rounded p-4 shadow-sm"
      >
        <div>
          <div class="font-semibold text-lg">{{ item.book_title }}</div>
          <div class="text-sm text-gray-600">Price: ${{ item.book_price }}</div>
          <div class="mt-2">
            Quantity:
            <input
              type="number"
              v-model.number="item.quantity"
              @change="updateQuantity(item)"
              class="w-16 ml-2 border border-gray-300 px-2 py-1 rounded"
              min="1"
            />
          </div>
        </div>

        <button
          @click="removeFromCart(item.id)"
          class="text-red-600 font-medium hover:underline"
        >
          ✖ Remove
        </button>
      </div>

      <div class="flex justify-between items-center">
        <!-- Cart Total -->
        <div class="text-right text-lg font-semibold pt-4">
          Total: ${{ cartTotal }}
        </div>
        <button
          @click="checkout"
          class="mt-4 px-4 py-2 bg-green-600 text-white rounded hover:bg-green-700"
          :disabled="cart.length === 0"
        >
          💳 Checkout
        </button>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "@/utils/axios";
import { RouterLink } from "vue-router";
import { API_BASE_URL } from "../utils/auth";

export default {
  components: { RouterLink },
  data() {
    return {
      cart: [],
      tab: "cart",
    };
  },
  computed: {
    cartTotal() {
      return this.cart
        .reduce(
          (total, item) => total + parseFloat(item.book_price) * item.quantity,
          0
        )
        .toFixed(2);
    },
    cartCount() {
      return this.cart.reduce((sum, item) => sum + item.quantity, 0);
    },
    tabClass() {
      return "bg-gray-100 text-gray-700 hover:bg-gray-200";
    },
    activeTabClass() {
      return "bg-blue-600 text-white shadow-md";
    },
  },
  methods: {
    async checkout() {
      if (this.cart.length === 0) {
        alert("Your cart is empty!");
        return;
      }

      try {
        const response = await axios.post(
          API_BASE_URL + "/api/checkout/",
          {},
          { withCredentials: true }
        );
        alert("Order placed successfully!");
        this.cart = []; // Clear local cart after checkout
        // Optionally redirect to orders page
        this.$router.push("/orders");
      } catch (error) {
        console.error("Checkout failed:", error);
        alert("Failed to place order. Please try again.");
      }
    },

    async fetchCart() {
      try {
        const response = await axios.get(`${API_BASE_URL}/api/cart/`, {
          withCredentials: true,
        });
        this.cart = response.data;
      } catch (error) {
        console.error("❌ Failed to load cart:", error);
      }
    },

    async updateQuantity(item) {
      if (item.quantity < 1) item.quantity = 1;

      try {
        await axios.put(
          `${API_BASE_URL}/api/cart/items/${item.id}/`,
          { quantity: item.quantity },
          { withCredentials: true }
        );
        console.log("✅ Quantity updated");
      } catch (error) {
        console.error("❌ Failed to update quantity:", error);
      }
    },

    async removeFromCart(itemId) {
      try {
        await axios.delete(`${API_BASE_URL}/api/cart/items/${itemId}/`, {
          withCredentials: true,
        });
        this.cart = this.cart.filter((item) => item.id !== itemId);
        console.log("✅ Item removed");
      } catch (error) {
        console.error("❌ Failed to remove item from cart:", error);
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
