

// 查询投诉处理列表
import axios from "axios";

export function listComplaints(query) {
  return request({
    url: '/complaint/complaints/list',
    method: 'get',
    params: query
  })
}

// 查询投诉处理详细
export function getComplaints(id) {
  return request({
    url: '/complaint/complaints/' + id,
    method: 'get'
  })
}

// 新增投诉处理
export function addComplaints(data) {
  console.log(data)
  return axios.post('/comp/complaints/complaintsGuest',data)
      .then(response => {
        console.log('响应数据:', response.data); // 打印响应数据
        return response.data;
      })
      .catch(error => {
        console.error('获取信息失败:', error);
        throw error;
      });
}

// 修改投诉处理
export function updateComplaints(data) {
  return request({
    url: '/complaint/complaints',
    method: 'put',
    data: data
  })
}

// 删除投诉处理
export function delComplaints(id) {
  return request({
    url: '/complaint/complaints/' + id,
    method: 'delete'
  })
}
