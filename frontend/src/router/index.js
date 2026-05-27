import { createRouter, createWebHistory } from 'vue-router'
import HomeView from "@/components/HomeView.vue";
import AdminLogin from '@/components/AdminLogin.vue';
import UserLogin from '@/components/UserLogin.vue';
import ManagerLogin from '@/components/ManagerLogin.vue';
import ManagerSignup from '@/components/ManagerSignup.vue';
import UserSignup from '@/components/UserSignup.vue';
import AdminDashboard from '@/components/AdminDashboard.vue';
import CreateCategory from '@/components/CreateCategory.vue';
import EditCategory from '@/components/EditCategory.vue';
import ManagerDashboard from '@/components/ManagerDashboard.vue';
import EditProduct from '@/components/EditProduct.vue';
import CustomerDashboard from '@/components/CustomerDashboard.vue';
import CustomerCart from '@/components/CustomerCart.vue';
import CustomerOrders from '@/components/CustomerOrders.vue';

// ✅ Helper to decode JWT and get role
function getRoleFromToken() {
    const token = localStorage.getItem('token');
    if (!token) return null;
    try {
        const payload = JSON.parse(atob(token.split('.')[1]));
        // Flask JWT identity is JSON string: {"role": "...", "id": ...}
        const identity = JSON.parse(payload.sub);
        return identity.role;
    } catch (e) {
        return null;
    }
}

const router = createRouter({
    history: createWebHistory(import.meta.env.BASE_URL),
    routes: [
        {
            path: '/',
            name: 'home',
            component: HomeView,
        },
        {
            path: '/admin-login',
            name: 'admin-login',
            component: AdminLogin,
        },
        {
            path: '/user-login',
            name: 'user-login',
            component: UserLogin,
        },
        {
            path: '/manager-login',
            name: 'manager-login',
            component: ManagerLogin,
        },
        {
            path: '/manager-signup',
            name: 'manager-signup',
            component: ManagerSignup,
        },
        {
            path: '/user-signup',
            name: 'user-signup',
            component: UserSignup,
        },
        {
            path: '/admin',
            name: 'admin-dashboard',
            component: AdminDashboard,
            meta: { requiresAuth: true, role: 'admin' },  // ✅ guard
        },
        {
            path: '/create-category',
            name: 'create-category',
            component: CreateCategory,
            meta: { requiresAuth: true, role: 'admin' },  // ✅ guard
        },
        {
            path: '/edit-category/:id',
            name: 'edit-category',
            component: EditCategory,
            meta: { requiresAuth: true, role: 'admin' },  // ✅ guard
        },
        {
            path: '/manager',
            name: 'manager-dashboard',
            component: ManagerDashboard,
            meta: { requiresAuth: true, role: 'manager' }, // ✅ guard
        },
        {
            path: '/edit-product/:id',
            name: 'edit-product',
            component: EditProduct,
            meta: { requiresAuth: true, role: 'manager' }, // ✅ guard
        },
        {
            path: '/customer',
            name: 'customer-dashboard',
            component: CustomerDashboard,
            meta: { requiresAuth: true, role: 'customer' }, // ✅ guard
        },
        {
            path: '/customer/cart',
            name: 'customer-cart',
            component: CustomerCart,
            meta: { requiresAuth: true, role: 'customer' }, // ✅ guard
        },
        {
            path: '/customer/orders',
            name: 'customer-orders',
            component: CustomerOrders,
            meta: { requiresAuth: true, role: 'customer' }, // ✅ guard
        },
    ]
})

// ✅ Global navigation guard
router.beforeEach((to, from, next) => {
    if (!to.meta.requiresAuth) {
        return next(); // public route, allow
    }

    const role = getRoleFromToken();

    if (!role) {
        // Not logged in — redirect to correct login page
        if (to.meta.role === 'admin') return next('/admin-login');
        if (to.meta.role === 'manager') return next('/manager-login');
        return next('/');
    }

    if (role !== to.meta.role) {
        // Wrong role — redirect away
        alert("Access denied");
        if (role === 'admin') return next('/admin');
        if (role === 'manager') return next('/manager');
        return next('/');
    }

    next(); // ✅ correct role, allow
});

export default router