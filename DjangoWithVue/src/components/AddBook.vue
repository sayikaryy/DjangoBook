<template>
     <div class="max-w-3xl mx-auto mt-10 p-6 bg-[#6f8aa8] rounded-lg shadow-md">
    <h2 class="text-2xl font-bold mb-6 text-gray-800">Add a Book</h2>
    <form @submit.prevent="submitForm" class="space-y-4" enctype="multipart/form-data">
      <!-- Title -->
      <div>
        <label class="block mb-1 font-medium text-gray-700">Title</label>
        <input v-model="form.title" type="text" class="w-full px-4 py-2 border rounded-md" required />
      </div>

      <!-- Author -->
      <div>
        <label class="block mb-1 font-medium text-gray-700">Author</label>
        <input v-model="form.author" type="text" class="w-full px-4 py-2 border rounded-md" required />
      </div>

      <!-- Price -->
      <div>
        <label class="block mb-1 font-medium text-gray-700">Price</label>
        <input v-model="form.price" type="number" step="0.01" class="w-full px-4 py-2 border rounded-md" required />
      </div>

      <!-- Stock -->
      <div>
        <label class="block mb-1 font-medium text-gray-700">Stock</label>
        <input v-model="form.stock" type="number" min="0" class="w-full px-4 py-2 border rounded-md" required />
      </div>

      <!-- Description -->
      <div>
        <label class="block mb-1 font-medium text-gray-700">Description</label>
        <textarea v-model="form.description" class="w-full px-4 py-2 border rounded-md" rows="4" required></textarea>
      </div>

      <!-- Category -->
      <div>
        <label class="block mb-1 font-medium text-gray-700">Category</label>
        <input type="text" class="w-full px-4 py-2 border rounded-md" v-model="form.category" list="categories" required />
      </div>

      <!-- Image -->
      <div>
        <label class="block mb-1 font-medium text-gray-700">Image</label>
        <input type="file" @change="handleImage" accept="image/*" class="w-full" />
      </div>

      <button type="submit" class="w-full bg-blue-600 text-white font-semibold py-2 rounded-md hover:bg-blue-700">
        Submit
      </button>
      <RouterLink to=""></RouterLink>
    </form>
    <router-view></router-view>
  </div>
</template>
<script>
import { RouterView, RouterLink } from 'vue-router';
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
        categories:'',
      },
      imageFile: null,
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
    },
    async submitForm() {
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

        alert('Book created successfully');
        this.form = {
          title: '',
          author: '',
          price: '',
          stock: '',
          description: '',
          category: '',
        };
        this.imageFile = null;
      } catch (err) {
        console.error(err);
        alert('Error submitting book');
      }
    },
  },
};
</script>