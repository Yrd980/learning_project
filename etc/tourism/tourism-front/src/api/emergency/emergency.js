import axios from 'axios';

export function listEmergencyinfo(query) {
    return axios.get('/emer/emergencyinfo/list', {
        params: query
    })
        .then(response => {
            console.log('响应数据:', response.data); // 打印响应数据
            return response.data;
        })
        .catch(error => {
            console.error('查询应急信息列表失败:', error);
            throw error;
        });
}
