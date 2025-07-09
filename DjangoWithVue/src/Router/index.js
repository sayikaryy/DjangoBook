import { createRouter, createWebHistory } from 'vue-router';

import Login from '../components/Login.vue';
import AddBook from '../components/AddBook.vue';
import Testview from '../components/Testview.vue'; // Example component, can be removed if not needed
const routes = [
  {
    path: '',
    name: 'login',
    component: Login, // only logged-in users can access
  },
  {
    path: '/add-book',
    name: 'add-book',
    component: AddBook,
    children: [
        {
            path: 'testview',
            name: '/testview',
            component: Testview, // This can be the same or a different component for adding a book
        }
    ]
  }
  // add more routes here...
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;