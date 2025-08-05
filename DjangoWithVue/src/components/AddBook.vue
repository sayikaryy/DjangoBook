<template>
  <div class="p-8 bg-gradient-to-br from-purple-100 via-blue-50 to-pink-100 min-h-screen flex justify-center items-center">
    <div class="w-full max-w-2xl bg-white/80 backdrop-blur-lg rounded-2xl shadow-xl p-8 transform transition-all duration-300 hover:shadow-2xl animate-fade-in">
      
      <!-- Header -->
      <div class="flex justify-between items-center mb-6">
        <h2 class="text-3xl font-extrabold text-gray-800 flex items-center gap-2">
          📖 Add New Book
        </h2>
        <router-link 
          to="/"
          class="px-4 py-1.5 bg-gray-200 text-gray-700 rounded-lg hover:bg-gray-300 transition"
        >
          ← Back
        </router-link>
      </div>

      <!-- Form -->
      <form @submit.prevent="submitForm" class="space-y-5" enctype="multipart/form-data">
        
        <!-- Title -->
        <div class="animate-slide-up">
          <label class="block mb-1 font-semibold text-gray-700">Title</label>
          <input v-model="form.title" type="text" placeholder="Enter book title"
            class="w-full px-4 py-2 border rounded-xl focus:ring-2 focus:ring-purple-400 outline-none transition" required />
        </div>

        <!-- Author -->
        <div class="animate-slide-up delay-100">
          <label class="block mb-1 font-semibold text-gray-700">Author</label>
          <input v-model="form.author" type="text" placeholder="Enter author name"
            class="w-full px-4 py-2 border rounded-xl focus:ring-2 focus:ring-purple-400 outline-none transition" required />
        </div>

        <!-- Price & Stock -->
        <div class="grid grid-cols-2 gap-4 animate-slide-up delay-200">
          <div>
            <label class="block mb-1 font-semibold text-gray-700">Price ($)</label>
            <input v-model="form.price" type="number" step="0.01" placeholder="0.00"
              class="w-full px-4 py-2 border rounded-xl focus:ring-2 focus:ring-purple-400 outline-none transition" required />
          </div>
          <div>
            <label class="block mb-1 font-semibold text-gray-700">Stock</label>
            <input v-model="form.stock" type="number" min="0" placeholder="0"
              class="w-full px-4 py-2 border rounded-xl focus:ring-2 focus:ring-purple-400 outline-none transition" required />
          </div>
        </div>

        <!-- Description -->
        <div class="animate-slide-up delay-300">
          <label class="block mb-1 font-semibold text-gray-700">Description</label>
          <textarea v-model="form.description" rows="4" placeholder="Write a short description"
            class="w-full px-4 py-2 border rounded-xl focus:ring-2 focus:ring-purple-400 outline-none transition" required></textarea>
        </div>

        <!-- Category -->
        <div class="animate-slide-up delay-400">
          <label class="block mb-1 font-semibold text-gray-700">Category</label>
          <select v-model="form.category"
            class="w-full px-4 py-2 border rounded-xl bg-white focus:ring-2 focus:ring-purple-400 outline-none transition" required>
            <option value="">Select Category</option>
            <option v-for="cat in categories" :key="cat.id" :value="cat.id">
              {{ cat.name }}
            </option>
          </select>
        </div>

        <!-- Image Upload -->
        <div class="animate-slide-up delay-500">
          <label class="block mb-1 font-semibold text-gray-700">Book Cover</label>
          <input type="file" @change="handleImage" accept="image/*"
            class="w-full border p-2 rounded-xl bg-gray-50 cursor-pointer file:mr-4 file:py-2 file:px-4 file:border-0 file:bg-purple-600 file:text-white file:rounded-lg hover:file:bg-purple-700 transition" />
        </div>

        <!-- Image Preview -->
        <transition name="fade">
          <div v-if="preview" class="mt-3 animate-fade-in">
            <p class="text-sm text-gray-600 mb-2">Preview:</p>
            <img :src="preview" class="w-40 h-52 object-cover rounded-lg border shadow" />
          </div>
        </transition>

        <!-- Submit Button -->
        <div class="mt-6">
          <button type="submit"
            :disabled="loading"
            class="w-full bg-purple-600 text-white font-semibold py-3 rounded-xl hover:bg-purple-700 transition transform hover:scale-85 flex items-center justify-center gap-2 disabled:bg-gray-400">
            <span v-if="loading" class="loader"></span>
            <span v-else>➕ Add Book</span>
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      form: {
        title: '',
        author: '',
        price: '',
        stock: '',
        description: '',
        category: '',
      },
      categories: [],
      imageFile: null,
      preview: null,
      loading: false,
    };
  },
  mounted() {
    this.fetchCategories();
  },
  methods: {
    async fetchCategories() {
      try {
        const res = await fetch('http://localhost:8000/api/categories/');
        this.categories = await res.json();
      } catch (err) {
        console.error('Failed to load categories:', err);
      }
    },
    handleImage(event) {
      this.imageFile = event.target.files[0];
      if (this.imageFile) {
        this.preview = URL.createObjectURL(this.imageFile);
      }
    },
    async submitForm() {
      this.loading = true;
      const formData = new FormData();
      for (let key in this.form) {
        formData.append(key, this.form[key]);
      }
      if (this.imageFile) {
        formData.append('image', this.imageFile);
      }

      try {
        const res = await fetch('http://localhost:8000/api/books/', {
          method: 'POST',
          body: formData,
        });

        if (!res.ok) throw new Error('Failed to create book');

        alert('✅ Book created successfully');
        this.$router.push('/');

        this.form = { title: '', author: '', price: '', stock: '', description: '', category: '' };
        this.imageFile = null;
        this.preview = null;
      } catch (err) {
        console.error(err);
        alert('❌ Error submitting book');
      } finally {
        this.loading = false;
      }
    },
  },
};
</script>

<style scoped>
/* Fade animation */
.fade-enter-active, .fade-leave-active {
  transition: opacity 0.5s;
}
.fade-enter, .fade-leave-to {
  opacity: 0;
}

/* Slide-up animation */
@keyframes slideUp {
  from { transform: translateY(20px); opacity: 0; }
  to { transform: translateY(0); opacity: 1; }
}
.animate-slide-up {
  animation: slideUp 0.5s ease forwards;
}
.animate-slide-up.delay-100 { animation-delay: 0.1s; }
.animate-slide-up.delay-200 { animation-delay: 0.2s; }
.animate-slide-up.delay-300 { animation-delay: 0.3s; }
.animate-slide-up.delay-400 { animation-delay: 0.4s; }
.animate-slide-up.delay-500 { animation-delay: 0.5s; }

/* Fade-in */
@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}
.animate-fade-in {
  animation: fadeIn 0.8s ease forwards;
}

/* Loader spinner */
.loader {
  border: 3px solid #f3f3f3;
  border-top: 3px solid white;
  border-radius: 50%;
  width: 18px;
  height: 18px;
  animation: spin 0.8s linear infinite;
}
@keyframes spin {
  to { transform: rotate(360deg); }
}
</style>
