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
    
    <div class="mt-auto flex gap-2">
      <button 
        @click="$emit('edit', bookId)" 
        class=" flex-1 px-4 py-2 bg-green-700 text-white rounded hover:bg-yellow-600 transition"
      >
        ✏️ Edit
      </button>
      <button 
        @click="$emit('delete', bookId)" 
        class="flex-1 px-4 py-2 bg-red-800 text-white rounded hover:bg-red-700 transition"
      >
        🗑️ Delete
      </button>
    </div>
  </div>
</template>

<script>
export default {
  props: {
    bookId: { type: [String, Number], required: true },
    title: String,
    author: String,
    price: [String, Number],
    stock: Number,
    image: String
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
  }
};
</script>
