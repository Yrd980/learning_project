// 登录方法

import axios from 'axios';

export function listStarhotels(query) {
  return axios.get('/api/guest/starhotels/list', {
    params: query
  })
      .then(response => {
          console.log('响应数据:', response.data); // 打印响应数据
          return response.data;
      })
      .catch(error => {
        console.error('查询星级酒店列表失败:', error);
        throw error;
      });
}

// 查询星级酒店信息详细
export function getStarhotel(id) {
  return axios.get('/api/guest/starhotels/details/' + id)
      .then(response => response.data)
      .catch(error => {
        console.error('查询星级酒店详细信息失败:', error);
        throw error;
      });
}
// 新增星级酒店预订信息
export function addStarhotelBookingMsg(data) {
  return axios.post('/api/guest/starhotels/details/' + data.room_type_id,data)
      .then(response => response.data)
      .catch(error => {
        console.error('查询星级酒店预订信息失败:', error);
        throw error;
      });
}

