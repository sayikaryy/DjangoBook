<template>
  <div>
    <Navbar 
      :isLoggedIn="isLoggedIn" 
      :cartCount="cart.length" 
      @navigate="handleNavigate" 
      @logout="logout" 
    />
    <router-view />
  </div>
</template>

<script>
import Bookpage from './components/Bookpage.vue';
import Navbar from './components/Navbar.vue';

export default {
  components: { Navbar },
  data() {
    return {
      isLoggedIn: false,
      cart: []
    };
  },
  methods: {
    handleNavigate(page) {
      // Map the emitted page to router paths
      const routeMap = {
        home: '/',
        cart: '/cart',
        orders: '/orders',
        login: '/login',
        register: '/register'
        
        
        
      };
      const path = routeMap[page] || '/';
      this.$router.push(path);
    },
    logout() {
      this.isLoggedIn = false;
      this.cart = [];
      localStorage.removeItem('token');
      this.$router.push('/login');
    }
  },
  mounted() {
    const token = localStorage.getItem('token');
    if (token) {
      this.isLoggedIn = true;
      // Load cart or other data if needed
    }
  }
};
</script>
