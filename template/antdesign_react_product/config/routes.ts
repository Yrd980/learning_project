export default [
  {
    path: '/user',
    layout: false,
    routes: [{ path: '/user/login', component: './User/Login', name: 'login' }],
  },
  { path: '/welcome', icon: 'smile', component: './Welcome', name: 'welcome' },
  {
    path: '/admin',
    icon: 'crown',
    name: 'admin',
    access: 'canAdmin',
    routes: [
      { path: '/admin', redirect: '/admin/sub-page' },
      { path: '/admin/sub-page', component: './Admin', name: 'sub-page' },
    ],
  },
  { icon: 'table', path: '/list', component: './TableList', name: 'tableList' },
  { path: '*', layout: false, component: './404', name: '404' },
];
