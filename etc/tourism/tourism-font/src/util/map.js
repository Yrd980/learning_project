import mapConfig from "@/config/mapConfig.js";
import {initAMapApiLoader} from "@vuemap/vue-amap";

// 初始化vue-amap
export function initMapApi() {
    initAMapApiLoader({
        // 高德的key
        key: mapConfig.key,
        securityJsCode: mapConfig.securityJsCode, // 新版key需要配合安全密钥使用
        Loca: {
            version: '2.0.0'
        } // 如果需要使用loca组件库，需要加载Loca
    });
}
