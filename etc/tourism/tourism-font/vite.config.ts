import {defineConfig} from 'vite'
import vue from '@vitejs/plugin-vue'
import AutoImport from 'unplugin-auto-import/vite'
import Components from 'unplugin-vue-components/vite'
import {ElementPlusResolver} from 'unplugin-vue-components/resolvers'
import path from 'path'
// @ts-ignore
import {VueAmapResolver} from "@vuemap/unplugin-resolver"

// https://vitejs.dev/config/
export default defineConfig({
    plugins: [
        vue(),
        AutoImport({
            resolvers: [ElementPlusResolver({
                exclude: /^ElAmap[A-Z]*/
            }), VueAmapResolver()],
        }),
        Components({
            resolvers: [ElementPlusResolver({
                exclude: /^ElAmap[A-Z]*/
            }), VueAmapResolver()],
            include: [/\.vue$/, /\.vue\?vue/, /\.tsx$/, /\.tsx\?tsx/],
        }),
    ],
    resolve: {
        alias: {
            '~': path.resolve(__dirname, './'),
            '@': path.resolve(__dirname, './src'),

        },
        extensions: ['.mjs', '.js', '.ts', '.jsx', '.tsx', '.json', '.vue']
    },
    server: {
        proxy: {
            '/api': {
                // target: 'https://restapi.amap.com',
                target: 'http://localhost:9215/',
                changeOrigin: true,
                rewrite: (path) => path.replace(/^\/api/, ''),
                secure: false,
            },
            '/emer': {
                target: 'http://localhost:9208/',
                changeOrigin: true,
                rewrite: (path) => path.replace(/^\/emer/, ''),
                secure: false,
            },
            '/map': {
                target: 'https://restapi.amap.com',
                changeOrigin: true,
                rewrite: (path) => path.replace(/^\/map/, ''),
                secure: false,
            },
            '/hotel': {
                target: 'http://localhost:9206/',
                changeOrigin: true,
                rewrite: (path) => path.replace(/^\/hotel/, ''),
                secure: false,
            },
            '/userinfo': {
                target: 'http://localhost:9201/',
                changeOrigin: true,
                rewrite: (path) => path.replace(/^\/userinfo/, ''),
                secure: false,
            },
            '/scenic': {
                target: 'http://localhost:9215/',
                changeOrigin: true,
                rewrite: (path) => path.replace(/^\/senic/, ''),
                secure: false,
            },
            '/pos': {
                target: 'http://api.tianditu.gov.cn',
                changeOrigin: true,
                rewrite: (path) => path.replace(/^\/pos/, ''),
                secure: false,
            },
            '/comp': {
                target: 'http://localhost:9209/',
                changeOrigin: true,
                rewrite: (path) => path.replace(/^\/comp/, ''),
                secure: false,
            }
        },
    }
})
