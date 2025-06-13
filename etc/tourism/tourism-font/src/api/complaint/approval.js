import request from '@/utils/request'

// 查询投诉审批列表
export function listApproval(query) {
  return request({
    url: '/complaint/approval/list',
    method: 'get',
    params: query
  })
}

// 查询投诉审批详细
export function getApproval(id) {
  return request({
    url: '/complaint/approval/' + id,
    method: 'get'
  })
}

// 新增投诉审批
export function addApproval(data) {
  return request({
    url: '/complaint/approval',
    method: 'post',
    data: data
  })
}

// 修改投诉审批
export function updateApproval(data) {
  return request({
    url: '/complaint/approval',
    method: 'put',
    data: data
  })
}

// 删除投诉审批
export function delApproval(id) {
  return request({
    url: '/complaint/approval/' + id,
    method: 'delete'
  })
}
