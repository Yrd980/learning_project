import axios, {AxiosInstance} from "axios";

// const isDev = process.env.NODE_ENV === 'development';

const myAxios: AxiosInstance = axios.create({
    // baseURL: isDev ? 'http://localhost:9205/' : '',

});

myAxios.defaults.withCredentials = true; // 配置为true

// Add a request interceptor
myAxios.interceptors.request.use(function (config) {
    // Do something before request is sent
    return config;
}, function (error) {
    // Do something with request error
    return Promise.reject(error);
});

// Add a response interceptor
myAxios.interceptors.response.use(function (response) {
    return response.data;
}, function (error) {
    return Promise.reject(error);
});

export default myAxios;
