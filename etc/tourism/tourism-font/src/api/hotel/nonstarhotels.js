// 登录方法

import axios from 'axios';

export function listNonstarhotels(query) {
  return axios.get('/api/guest/nonstarhotels/list', {
    params: query
  })
      .then(response => {
        console.log('响应数据:', response.data); // 打印响应数据
        return response.data;
      })
      .catch(error => {
        console.error('查询非星级酒店列表失败:', error);
        throw error;
      });
}

// 查询非星级酒店信息详细
export function getNonstarhotel(id) {
  return axios.get('/api/guest/nonstarhotels/details/' + id)
      .then(response => response.data)
      .catch(error => {
        console.error('查询非星级酒店详细信息失败:', error);
        throw error;
      });
}
// 新增非星级酒店预订信息
export function addNonstarhotelBookingMsg(data) {
  return axios.post('/api/guest/nonstarhotels/details/' + data.room_type_id,data)
      .then(response => response.data)
      .catch(error => {
        console.error('查询非星级酒店预订信息失败:', error);
        throw error;
      });
}