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
        🛒 Cart<span v-if="cartCount > 0"> ({{ cartCount }})</span>
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

    <!-- Books Section -->
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
          <option
            v-for="category in categories"
            :key="category.id"
            :value="category.id"
          >
            {{ category.name }}
          </option>
        </select>
      </div>

      <!-- Book Grid -->
      <div
        class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6 mt-6"
      >
        <BookUser
          v-for="book in books"
          :key="book.id"
          :book-id="book.id"
          :title="book.title"
          :author="book.author"
          :price="book.price"
          :stock="book.stock"
          :image="book.image_url"
          @add-to-cart="addToCart(book.id)"
        />
      </div>

      <!-- No Results -->
      <div v-if="books.length === 0" class="text-center text-gray-500 mt-10">
        No books found.
      </div>
    </div>

    <!-- Placeholder Sections -->
    <div v-else-if="tab === 'cart'" class="text-center text-lg text-gray-600">
      🛒 Cart page (coming soon)
    </div>
    <div v-else-if="tab === 'checkout'" class="text-center text-lg text-gray-600">
      💸 Checkout page (coming soon)
    </div>
    <div v-else-if="tab === 'orders'" class="text-center text-lg text-gray-600">
      🧾 Order history (coming soon)
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import BookUser from './book_user.vue';

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
  mounted() {
    this.fetchBooks();
    this.fetchCategories();
    this.loadCart();
  },
  computed: {
    cartCount() {
      // You can change to .length if you want unique items instead of total quantity
      return this.cart.reduce((sum, item) => sum + item.quantity, 0);
    },
    tabClass() {
      return 'bg-gray-100 text-gray-700 hover:bg-gray-200';
    },
    activeTabClass() {
      return 'bg-blue-600 text-white';
    },
  },
  methods: {
    async fetchBooks() {
      try {
        const response = await axios.get('http://127.0.0.1:8000/api/books/', {
          params: {
            category: this.selectedCategory,
            search: this.searchQuery,
          },
        });
        this.books = response.data;
      } catch (error) {
        console.error('Failed to fetch books:', error);
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
    loadCart() {
      const stored = localStorage.getItem('cart');
      this.cart = stored ? JSON.parse(stored) : [];
    },
    addToCart(bookId) {
      const book = this.books.find((b) => b.id === bookId);
      if (!book || book.stock <= 0) return;

      const cartCopy = [...this.cart];
      const existingItem = cartCopy.find((item) => item.bookId === bookId);

      if (existingItem) {
        existingItem.quantity += 1;
      } else {
        cartCopy.push({
          bookId: book.id,
          title: book.title,
          price: Number(book.price),
          quantity: 1,
        });
      }

      book.stock -= 1;
      this.cart = cartCopy;
      localStorage.setItem('cart', JSON.stringify(this.cart));
    },
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
