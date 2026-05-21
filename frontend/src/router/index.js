import {createRouter,createWebHistory} from 'vue-router'
import HomeView from "@/components/HomeView.vue";
import AdminLogin from '@/components/AdminLogin.vue';
import UserLogin from '@/components/UserLogin.vue';
import ManagerLogin from '@/components/ManagerLogin.vue';
import ManagerSignup from '@/components/ManagerSignup.vue';
import UserSignup from '@/components/UserSignup.vue';
import AdminDashboard from '@/components/AdminDashboard.vue';  // removed duplicate UserLogin import
import CreateCategory from '../components/CreateCategory.vue';

const router = createRouter({
    history:createWebHistory(import.meta.env.BASE_URL),
    routes:[{
        path:'/',
        name:'home',
        component:HomeView,
    },
    {
        path:'/admin-login',
        name:'admin-login',
        component:AdminLogin,
    },
    {
        path:'/user-login',
        name:'user-login',
        component:UserLogin,
    },
    {
        path:'/manager-login',
        name:'manager-login',
        component:ManagerLogin,
    },
    {
        path:'/manager-signup',
        name:'manager-signup',
        component:ManagerSignup,
    },
    {
        path:'/user-signup',
        name:'user-signup',
        component:UserSignup,
    },
    {
        path:'/admin',
        name:'admin-dashboard',
        component:AdminDashboard,
    },
    {
        path:'/create-category',
        name:'create-category',
        component:CreateCategory,
    }
    ]
})

export default router