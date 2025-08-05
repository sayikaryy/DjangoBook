<template>
  <div class="p-4 space-y-6">
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
  </div>
  <div>
    <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6">
      <BookCard
        v-for="book in books"
        :key="book.id"
        :bookId="book.id"
        :title="book.title"
        :author="book.author"
        :price="book.price"
        :stock="book.stock"
        :image="book.image_url"
        @edit="openEditModal"
        @delete="deleteBook"
      />
    </div>

    <!-- Edit Modal -->
    <div v-if="editingBook" class="fixed inset-0 bg-black bg-opacity-50 flex justify-center items-center z-50">
      <div class="bg-white rounded p-6 w-96 shadow-lg">
        <h2 class="text-xl font-bold mb-4">Edit Book</h2>
        <form @submit.prevent="submitEdit">
          <input v-model="editForm.title" placeholder="Title" class="mb-2 w-full p-2 border rounded" required />
          <input v-model="editForm.author" placeholder="Author" class="mb-2 w-full p-2 border rounded" required />
          <input v-model.number="editForm.price" placeholder="Price" type="number" step="0.01" class="mb-2 w-full p-2 border rounded" required />
          <input v-model.number="editForm.stock" placeholder="Stock" type="number" min="0" class="mb-2 w-full p-2 border rounded" required />
          <textarea v-model="editForm.description" placeholder="Description" class="mb-2 w-full p-2 border rounded"></textarea>

          <div class="flex justify-end gap-3">
            <button type="button" @click="closeEditModal" class="px-4 py-2 border rounded">Cancel</button>
            <button type="submit" class="px-4 py-2 bg-blue-600 text-white rounded">Save</button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'; // ✅ Added axios import
import BookCard from './Bookcard.vue';

export default {
  components: { BookCard },
  data() {
    return {
      categories: [],          // ✅ Stores categories for dropdown
      selectedCategory: '',    // ✅ Currently selected category
      searchQuery: '',         // ✅ (Optional) Used for searching
      books: [],               // ✅ List of books to display
      editingBook: null,       // ✅ ID of the book being edited
      editForm: {
        id: null,
        title: '',
        author: '',
        price: 0,
        stock: 0,
        description: ''
      }
    };
  },
  mounted() {
    this.fetchBooks();
    this.fetchCategories();
  },
  methods: {
    // ✅ Fetch books, with optional filtering by category and search
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

    // ✅ Fetch categories for the dropdown
    async fetchCategories() {
      try {
        const response = await axios.get('http://127.0.0.1:8000/api/categories/');
        this.categories = response.data;
      } catch (error) {
        console.error('Failed to fetch categories:', error);
      }
    },

    // ✅ Open modal and load book details
    async openEditModal(bookId) {
      try {
        const res = await fetch(`http://localhost:8000/api/books/${bookId}/`);
        const book = await res.json();
        this.editForm = { ...book };
        this.editingBook = bookId;
      } catch (err) {
        alert('Failed to load book details');
        console.error(err);
      }
    },

    // ✅ Close modal and reset form
    closeEditModal() {
      this.editingBook = null;
      this.editForm = {
        id: null,
        title: '',
        author: '',
        price: 0,
        stock: 0,
        description: ''
      };
    },

    // ✅ Submit edited book to backend
    async submitEdit() {
      try {
        const token = localStorage.getItem('token'); // only if needed
        const formData = new FormData();

        for (const key in this.editForm) {
          formData.append(key, this.editForm[key]);
        }

        const res = await fetch(`http://localhost:8000/api/books/${this.editForm.id}/`, {
          method: 'PUT',
          headers: token ? { 'Authorization': `Bearer ${token}` } : {},
          body: formData
        });

        if (!res.ok) {
          const errorData = await res.json();
          console.error('Update failed:', errorData);
          throw new Error(errorData.detail || 'Update failed');
        }

        const updatedBook = await res.json();
        alert('✅ Book updated successfully');

        this.books = this.books.map(b =>
          b.id === updatedBook.id ? updatedBook : b
        );

        this.closeEditModal();
      } catch (err) {
        alert('❌ Failed to update book: ' + err.message);
        console.error(err);
      }
    },

    // ✅ Delete book by ID
    async deleteBook(bookId) {
      if (!confirm('Are you sure you want to delete this book?')) return;
      try {
        const res = await fetch(`http://localhost:8000/api/books/${bookId}/`, {
          method: 'DELETE'
        });
        if (!res.ok) throw new Error('Failed to delete');
        this.books = this.books.filter(b => b.id !== bookId);
        alert('Book deleted');
      } catch (err) {
        alert('Error deleting book');
        console.error(err);
      }
    }
  }
};
</script>
