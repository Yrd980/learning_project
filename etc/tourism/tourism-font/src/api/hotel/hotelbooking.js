import axios from "axios";

export function listbookings(query) {
    return axios.get('/hotel/starbookings/listall', {
        params: query
    })
        .then(response => {
            console.log('响应数据:', response.data); // 打印响应数据
            return response.data;
        })
        .catch(error => {
            console.error('查询订单列表失败:', error);
            throw error;
        });
}
