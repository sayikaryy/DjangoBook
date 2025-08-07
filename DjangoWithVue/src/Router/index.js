import { createRouter, createWebHistory } from 'vue-router';
import Home from '../components/DashBoard.vue';
import Login from '../components/Login.vue';
import Register from '../components/register.vue';
import AddBook from '../components/AddBook.vue';
import Testview from '../components/Testview.vue';
import Order from '../components/Order.vue';
import BookPage from '../components/Bookpage.vue';
import UserPage from '../components/users.vue';
import UserDashboard from '../components/user_dashboard.vue';
import Cart from '../components/Cart.vue';
import Checkout from '../components/Checkout.vue';
import OrderAdmin from '../components/Order_admin.vue';



const routes = [
  {
    path: '/cart',
    name: 'cart',
    component: Cart,
  },
  {
    path: '/checkout',
    name: 'checkout',
    component: Checkout,
  },
  {
    path: '/order-admin',
    name: 'order-admin',
    component: OrderAdmin,
  },
  
  {
    path: '/user-dashboard',
    name: 'user-dashboard',
    component: UserDashboard,
  },
  {
    path: '/',
    name: 'home',
    component: Home,
  },
  {
    path: '/register',
    name: 'register',
    component: Register,
  },
  {
    path: '/login',
    name: 'login',
    component: Login,
  },
  {
    path: '/books',
    name: 'books',
    component: BookPage,
  },

  {
    path: '/orders',
    name: 'orders',
    component: Order,
  },
  {
    path: '/users',
    name: 'users',
    component: UserPage,
  },

  {
    path: '/add-book',
    name: 'add-book',
    component: AddBook,
    children: [
      {
        path: 'testview',
        name: 'testview',
        component: Testview,
      }
    ]
  },
  // add more routes here...
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
