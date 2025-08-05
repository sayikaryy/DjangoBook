<template>
 <div class="p-6 bg-gradient-to-br from-purple-100 via-blue-50 to-pink-100 min-h-screen">
    <h1 class="text-3xl font-bold mb-6 text-gray-800">👥 Manage Users</h1>

    <div v-if="loading" class="text-gray-500">Loading users...</div>
    <div v-else-if="users.length === 0" class="text-gray-500">No users found.</div>

    <table v-else class="w-full bg-white shadow rounded-xl border-collapse">
      <thead class="bg-gray-200 text-left">
        <tr>
          <th class="py-2 px-4">ID</th>
          <th class="py-2 px-4">Username</th>
          <th class="py-2 px-4">Email</th>
          <th class="py-2 px-4">Actions</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="user in users" :key="user.id" class="border-b hover:bg-gray-50">
          <td class="py-2 px-4">{{ user.id }}</td>
          
          <td class="py-2 px-4">
            <input
              v-if="editingUser === user.id"
              v-model="editedUser.username"
              class="border px-2 py-1 rounded w-full"
            />
            <span v-else>{{ user.username }}</span>
          </td>
          
          <td class="py-2 px-4">
            <input
              v-if="editingUser === user.id"
              v-model="editedUser.email"
              type="email"
              class="border px-2 py-1 rounded w-full"
            />
            <span v-else>{{ user.email || 'N/A' }}</span>
          </td>

          <td class="py-2 px-4 space-x-2">
            <button
              v-if="editingUser === user.id"
              @click="updateUser(user.id)"
              class="bg-green-600 text-white px-3 py-1 rounded hover:bg-green-700"
            >
              Save
            </button>
            <button
              v-if="editingUser === user.id"
              @click="cancelEdit"
              class="bg-gray-400 text-white px-3 py-1 rounded hover:bg-gray-500"
            >
              Cancel
            </button>
            <button
              v-else
              @click="editUser(user)"
              class="bg-blue-600 text-white px-3 py-1 rounded hover:bg-blue-700"
            >
              Edit
            </button>
            <button
              @click="deleteUser(user.id)"
              class="bg-red-600 text-white px-3 py-1 rounded hover:bg-red-700"
            >
              Delete
            </button>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      users: [],
      loading: true,
      editingUser: null,
      editedUser: {
        username: "",
        email: "",
      },
    };
  },
  methods: {
    async fetchUsers() {
      try {
        const res = await axios.get("http://127.0.0.1:8000/api/users/");
        this.users = res.data;
      } catch (err) {
        console.error("Failed to fetch users:", err);
        alert("Failed to fetch users");
      } finally {
        this.loading = false;
      }
    },
    editUser(user) {
      this.editingUser = user.id;
      this.editedUser = { username: user.username, email: user.email };
    },
    cancelEdit() {
      this.editingUser = null;
      this.editedUser = { username: "", email: "" };
    },
    async updateUser(id) {
      try {
        await axios.put(`http://127.0.0.1:8000/api/users/${id}/`, this.editedUser);
        alert("User updated successfully");
        this.editingUser = null;
        this.fetchUsers();
      } catch (err) {
        console.error("Failed to update user:", err);
        alert("Failed to update user");
      }
    },
    async deleteUser(id) {
      if (!confirm("Are you sure you want to delete this user?")) return;

      try {
        await axios.delete(`http://127.0.0.1:8000/api/users/${id}/`);
        alert("User deleted successfully");
        this.fetchUsers();
      } catch (err) {
        console.error("Failed to delete user:", err);
        alert("Failed to delete user");
      }
    },
  },
  mounted() {
    this.fetchUsers();
  },
};
</script>
