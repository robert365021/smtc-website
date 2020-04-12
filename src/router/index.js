import Vue from 'vue';
import VueRouter from 'vue-router';

Vue.use(VueRouter);

import County from '../views/County.vue';
import Home from '../views/Home.vue';

const routes = [
  {
    path: '/',
    name: 'home',
    component: Home,
  },
  {
    path: '/county',
    name: 'county',
    component: County,
  },
];

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes,
});

export default router;
