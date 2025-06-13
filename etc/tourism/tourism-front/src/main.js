import {createApp} from 'vue'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import locale from 'element-plus/es/locale/lang/zh-cn'
import * as ElementPlusIconsVue from '@element-plus/icons-vue'
import App from './App.vue'
import router from './router'
import store from './store'

// 引入vue-amap
import VueAMap from '@vuemap/vue-amap';
import '@vuemap/vue-amap/dist/style.css';
import { createPinia } from 'pinia'
// 分页组件
import Pagination from '@/components/Pagination'

const app = createApp(App)
const pinia = createPinia()

app.component('Pagination', Pagination)
for (const [key, component] of Object.entries(ElementPlusIconsVue)) {
    app.component(key, component)
}
app.use(ElementPlus, {
    locale: locale,
})
app.use(router)
app.use(store)
app.use(VueAMap)
app.use(pinia)
app.mount('#app')
