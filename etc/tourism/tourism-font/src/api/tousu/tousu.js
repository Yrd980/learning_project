// 登录方法

import axios from 'axios';

export function listTousu(id) {
    return axios.get('/api/guest/complaint/'+id)
        .then(response => {
            console.log('响应数据:', response.data); // 打印响应数据
            return response.data;
        })
        .catch(error => {
            console.error('查询星级酒店列表失败:', error);
            throw error;
        });
}
