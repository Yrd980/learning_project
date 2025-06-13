import request from '@/utils/request'

// 查询投诉处理列表
export function listHandlingresults(query) {
  return request({
    url: '/complaint/handlingresults/list',
    method: 'get',
    params: query
  })
}

// 查询投诉处理详细
export function getHandlingresults(id) {
  return request({
    url: '/complaint/handlingresults/' + id,
    method: 'get'
  })
}

// 新增投诉处理
export function addHandlingresults(data) {
  return request({
    url: '/complaint/handlingresults',
    method: 'post',
    data: data
  })
}

// 修改投诉处理
export function updateHandlingresults(data) {
  return request({
    url: '/complaint/handlingresults',
    method: 'put',
    data: data
  })
}

// 删除投诉处理
export function delHandlingresults(id) {
  return request({
    url: '/complaint/handlingresults/' + id,
    method: 'delete'
  })
}
