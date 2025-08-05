<template>
<nav class="bg-violet-800 shadow-md px-6 py-3 text-white flex justify-between items-center">

    <!-- Left Section -->
    <div class="flex gap-6 items-center">
      <button 
        @click="$router.push('/')" 
        class="font-semibold hover:text-yellow-300 transition"
        aria-label="Home"
      >
        🏠 Home
      </button>

      <!-- <button 
        @click="$emit('navigate', 'cart')" 
        class="relative hover:text-yellow-300 transition flex items-center gap-1"
        aria-label="Cart"
      >
        🛒 Cart
        <span 
          v-if="cartCount > 0"
          class="bg-red-500 text-xs rounded-full px-2 py-0.5 ml-1 font-bold"
        >
          {{ cartCount }}
        </span>
      </button> -->

      <button 
        v-if="isLoggedIn" 
        @click="$emit('navigate', 'orders')" 
        class="hover:text-yellow-300 transition font-medium"
        aria-label="My Orders"
      >
        📦 My Orders
      </button>
    </div>

    <!-- Right Section -->
    <div class="flex gap-6 items-center">
      <button 
        v-if="!isLoggedIn" 
        @click="$emit('navigate', 'login')" 
        class="hover:text-yellow-300 transition font-medium"
        aria-label="Login"
      >
        🚪 Logout
      </button>

      <button 
        v-if="!isLoggedIn" 
        @click="$emit('navigate', 'register')" 
        class="hover:text-yellow-300 transition font-medium"
        aria-label="Register"
      >
        ✍️ Register
      </button>

      <button 
        v-if="isLoggedIn" 
        @click="$emit('logout')" 
        class="hover:text-red-400 transition font-semibold"
        aria-label="Logout"
      >
        🚪 Logout
      </button>
    </div>
  </nav>
</template>

<script>
export default {
  props: {
    isLoggedIn: { type: Boolean, default: false },
    cartCount: { type: Number, default: 0 }
  }
}
</script>
