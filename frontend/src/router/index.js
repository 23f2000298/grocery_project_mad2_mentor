import {createRouter,createWebHistory} from 'vue-router'
import HomeView from "@/components/HomeView.vue";
import AdminLogin from '@/components/AdminLogin.vue';
import UserLogin from '@/components/UserLogin.vue';
import ManagerLogin from '@/components/ManagerLogin.vue';

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
    ]
})

export default router