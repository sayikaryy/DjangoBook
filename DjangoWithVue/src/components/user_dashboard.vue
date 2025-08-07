<template>
  <div class="p-4 space-y-6 max-w-7xl mx-auto">
    <!-- Navigation Tabs -->
    <div class="flex flex-wrap gap-3 mb-6">
      <RouterLink
        to="/user-dashboard"
        :class="tab === 'books' ? activeTabClass : tabClass"
        class="px-4 py-2 rounded font-medium transition"
        @click.native="tab = 'books'"
      >
        📚 Books
      </RouterLink>

      <RouterLink
        to="/cart"
        :class="tab === 'cart' ? activeTabClass : tabClass"
        class="px-4 py-2 rounded font-medium transition"
        @click.native="tab = 'cart'"
      >
        🛒 Cart
      </RouterLink>

      <RouterLink
        to="/checkout"
        :class="tab === 'checkout' ? activeTabClass : tabClass"
        class="px-4 py-2 rounded font-medium transition"
        @click.native="tab = 'checkout'"
      >
        💸 Checkout
      </RouterLink>

      <RouterLink
        to="/orders"
        :class="tab === 'orders' ? activeTabClass : tabClass"
        class="px-4 py-2 rounded font-medium transition"
        @click.native="tab = 'orders'"
      >
        🧾 Order History
      </RouterLink>
    </div>

    <!-- Books Tab -->
    <div v-if="tab === 'books'">
      <!-- Filters -->
      <div class="flex flex-col sm:flex-row justify-between items-center gap-4">
        <input
          v-model="searchQuery"
          @input="fetchBooks"
          type="text"
          placeholder="Search by title or author..."
          class="border border-gray-300 rounded px-4 py-2 w-full sm:w-1/2"
        />
        <select
          v-model="selectedCategory"
          @change="fetchBooks"
          class="border border-gray-300 rounded px-4 py-2 w-full sm:w-1/4"
        >
          <option value="">All Categories</option>
          <option v-for="category in categories" :key="category.id" :value="category.id">
            {{ category.name }}
          </option>
        </select>
      </div>

      <!-- Books -->
      <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6 mt-6">
        <BookUser
          v-for="book in books"
          :key="book.id"
          :book-id="book.id"
          :title="book.title"
          :author="book.author"
          :price="book.price"
          :stock="book.stock"
          :image="book.image_url"
          @add-to-cart="() => addToCart(book.id)"
        />
      </div>

      <!-- No Results -->
      <div v-if="books.length === 0" class="text-center text-gray-500 mt-10">
        No books found.
      </div>
    </div>

    <!-- Cart Placeholder -->
    <div v-else-if="tab === 'cart'" class="text-center text-lg text-gray-600">
      🛒 Cart page (coming soon)
    </div>

    <!-- Checkout -->
    <div v-else-if="tab === 'checkout'" class="text-center text-lg text-gray-600">
      💸 Checkout page (coming soon)
    </div>

    <!-- Orders -->
    <div v-else-if="tab === 'orders'" class="text-center text-lg text-gray-600">
      🧾 Order history (coming soon)
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import BookUser from './book_user.vue';
import { useRouter } from 'vue-router';

export default {
  components: { BookUser },

  data() {
    return {
      tab: 'books',
      books: [],
      categories: [],
      selectedCategory: '',
      searchQuery: '',
      cart: [],
    };
  },

  setup() {
    const router = useRouter();

    // Return router so it can be used inside methods via this.router
    return { router };
  },
  mounted() {
    this.fetchBooks();
    this.fetchCategories();
    this.loadCart();
  },
  computed: {
    cartTotal() {
      return this.cart
        .reduce(
          (total, item) => total + parseFloat(item.book_price || item.price) * item.quantity,
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
    async fetchBooks() {
      try {
        let url = 'http://localhost:8000/api/books/';
        const params = [];

        if (this.selectedCategory) {
          params.push(`category=${this.selectedCategory}`);
        }

        if (this.searchQuery) {
          params.push(`search=${this.searchQuery}`);
        }

        if (params.length) {
          url += '?' + params.join('&');
        }

        const res = await fetch(url);
        const data = await res.json();
        this.books = data;
      } catch (err) {
        console.error('Error loading books:', err);
      }
    },
    async fetchCategories() {
      try {
        const response = await axios.get('http://127.0.0.1:8000/api/categories/');
        this.categories = response.data;
      } catch (error) {
        console.error('Failed to fetch categories:', error);
      }
    },
    
    async loadCart() {
      try {
        const response = await axios.get('http://127.0.0.1:8000/api/cart/', {
          withCredentials: true,
        });
        this.cart = response.data;
      } catch (error) {
        console.error('Failed to fetch cart from API:', error);
        this.cart = [];
      }
    },
   async addToCart(bookId) {
  const book = this.books.find(b => b.id === bookId);
  if (!book || book.stock <= 0) return;

  axios.post(
    'http://127.0.0.1:8000/api/cart/add/',
    { book_id: bookId, quantity: 1 },
    { withCredentials: true }
  )
  .then(() => {
    book.stock -= 1;

    const existingIndex = this.cart.findIndex(item => item.bookId === bookId);

    if (existingIndex !== -1) {
      const updatedItem = {
        ...this.cart[existingIndex],
        quantity: this.cart[existingIndex].quantity + 1,
      };
      this.$set(this.cart, existingIndex, updatedItem);
    } else {
      this.cart = [
        ...this.cart,
        {
          bookId: book.id,
          title: book.title,
          price: Number(book.price),
          quantity: 1,
        },
      ];
    }

    // Show alert then redirect after user clicks OK
    alert("Added to cart!");
    this.$router.push('/cart'); // Redirect to /cart
  })
  .catch(error => {
    console.error("Failed to add to cart:", error);
    alert("Failed to add to cart");
  });
},
mounted() {
  this.fetchBooks();
  axios.get("http://127.0.0.1:8000/api/categories/", { withCredentials: true })
    .then(res => {
      this.categories = res.data;
    })
    .catch(err => console.error("Failed to load categories", err));
}
  },
  
  
};
</script>


<style scoped>
input:focus,
select:focus {
  outline: none;
  border-color: #0000dcdd;
  box-shadow: 0 0 0 2px rgba(124, 58, 237, 0.2);
}
</style>
