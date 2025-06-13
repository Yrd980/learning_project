import request from '@/utils/request'

// 查询投诉评价列表
export function listFeedbackresults(query) {
  return request({
    url: '/complaint/feedbackresults/list',
    method: 'get',
    params: query
  })
}

// 查询投诉评价详细
export function getFeedbackresults(id) {
  return request({
    url: '/complaint/feedbackresults/' + id,
    method: 'get'
  })
}

// 新增投诉评价
export function addFeedbackresults(data) {
  return request({
    url: '/complaint/feedbackresults',
    method: 'post',
    data: data
  })
}

// 修改投诉评价
export function updateFeedbackresults(data) {
  return request({
    url: '/complaint/feedbackresults',
    method: 'put',
    data: data
  })
}

// 删除投诉评价
export function delFeedbackresults(id) {
  return request({
    url: '/complaint/feedbackresults/' + id,
    method: 'delete'
  })
}
