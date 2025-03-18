export default [
  { path: '/user', layout: false, routes: [{ path: '/user/login', component: './User/Login' , name: 'login' }] },
  { path: '/welcome', icon: 'smile', component: './Welcome' },
  {
    path: '/admin',
    icon: 'crown',
    access: 'canAdmin',
    routes: [
      { path: '/admin', redirect: '/admin/sub-page' },
      { path: '/admin/sub-page', component: './Admin' },
    ],
  },
  { icon: 'table', path: '/list', component: './TableList' , name: 'tableList' },
  { path: '/', redirect: '/welcome' , name: 'welcome' },
  { path: '*', layout: false, component: './404' , name: '404' },
];
