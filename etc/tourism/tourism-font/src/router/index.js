import {createRouter, createWebHistory} from "vue-router";

export const constantRoutes = [
    {
        name: 'home',
        path: '/',
        component: () => import('@/views/home'),
        hidden: true,
    },
    {
        name: 'Login',
        path: '/guest/login',
        component: () => import('@/views/login'),
        hidden: true,
    },
    {
        path: '/guest/register',
        component: () => import('@/views/register'),
        hidden: true
    },
    {
        name: 'scenic',
        path: '/scenic',
        component: () => import('@/views/scenic'),
        hidden: true,
    },
    {
        name: 'order',
        path: '/order',
        component: () => import('@/views/order'),
        hidden: true,
    },
    {
       name: 'profile',
       path: '/profile',
       component: () =>import('@/views/profile/index'),
       hidden: true
    },
    {
        name: 'route',
        path: '/route',
        component: () => import('@/views/route/route'),
        hidden: true,
    },
    {
        name: 'detail',
        path: '/detail/:id',
        component: () => import('@/views/detail'),
        hidden: true,
    },
    {
        name: 'starHotel',
        path: '/guest/starhotels',
        component: () => import('@/views/hotel/starhotels/index'),
        hidden: true
    },
    {
        name: 'nonStarHotel',
        path: '/guest/nonstarhotels',
        component: () => import('@/views/hotel/nonstarhotels/index'),
        hidden: true
    },
    {
        name: 'complaint',
        path: '/complaint',
        component:() =>import('@/views/complaint'),
        hidden: true
    },
    {
        path: '/guest/starhotels/details/:hotelId',
        component: () => import('@/views/hotel/starhotels/details'),
        hidden: true
    },
    {
        path: '/guest/nonstarhotels/details/:hotelId',
        component: () => import('@/views/hotel/nonstarhotels/details'),
        hidden: true
    },
]

const router = createRouter({
    history: createWebHistory(),
    routes: constantRoutes,
});

export default router;

