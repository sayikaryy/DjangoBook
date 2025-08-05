<template>
  <div class="bg-white rounded-xl shadow hover:shadow-lg transition p-4 flex flex-col h-full">
    <img 
      :src="imageUrl" 
      alt="Book Cover" 
      class="w-full h-48 object-cover rounded mb-3"
    />
    <h3 class="text-lg font-semibold text-gray-800">{{ title }}</h3>
    <p class="text-sm text-gray-500 mb-2">by {{ author }}</p>
    <p class="text-blue-600 font-bold mb-3">${{ price }}</p>
    <p v-if="stock === 0" class="text-red-500 text-sm mb-3">Out of Stock</p>
    <p v-else class="text-green-600 text-sm mb-3">In Stock: {{ stock }}</p>
    <!-- Your Add to Cart button -->
 <button 
    :disabled="stock === 0 || loading"
    @click="addToCart"
    class="mt-auto px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 disabled:bg-gray-400"
  >
    <span v-if="loading">Adding...</span>
    <span v-else>Add to Cart</span>
  </button>
  </div>
</template>

<script>
import axios from '@/utils/axios'; // Adjust path as needed
import { refreshAccessToken } from '@/utils/auth';

export default {
  props: {
  title: String,
  author: String,
  price: Number,
  stock: Number,
  bookId: Number,
  image: String,
},
computed: {
    imageUrl() {
      if (!this.image) {
        return 'https://via.placeholder.com/200x300?text=No+Image';
      }
      return this.image.startsWith('http')
        ? this.image
        : `http://127.0.0.1:8000${this.image}`;
    }
  },

  data() {
    return {
      loading: false
    };
  },
  methods: {
    async addToCart() {
      if (this.stock === 0) return;

      let token = localStorage.getItem('access');
      if (!token) {
        alert('Please log in first.');
        this.$router.push('/login');
        return;
      }

      this.loading = true;

      try {
        await axios.post('/api/cart/add/', {
          book_id: this.bookId,
          quantity: 1,
        }, {
          headers: {
            Authorization: `Bearer ${token}`
          }
        });

        alert('Added to cart!');
        this.$emit('added-to-cart');
      } catch (error) {
        if (error.response?.status === 401) {
          const newToken = await refreshAccessToken();
          if (newToken) {
            try {
              await axios.post('/api/cart/add/', {
                book_id: this.bookId,
                quantity: 1,
              }, {
                headers: {
                  Authorization: `Bearer ${newToken}`
                }
              });

              alert('Added to cart!');
              this.$emit('added-to-cart');
            } catch (err2) {
              alert('Still failed. Please login again.');
              this.$router.push('/login');
            }
          } else {
            alert('Session expired. Please login again.');
            this.$router.push('/login');
          }
        } else {
          alert('Failed to add to cart.');
          console.error(error);
        }
      } finally {
        this.loading = false;
      }
    }
  }
};
</script>


