import axios from "axios";

export function updateUserProfile(data) {
    console.log(data)
    return axios.post('/userinfo/user/profile/guest', data)
        .then(response => {
            console.log('响应数据:', response.data); // 打印响应数据
            return response.data;
        })
        .catch(error => {
            console.error('个人信息更新失败:', error);
            throw error;
        });
}

export function updateUserPwd(oldPassword, newPassword,userId) {
    const data = {
        oldPassword,
        newPassword,
        userId
    }
    console.log(data)
    return axios.post('/userinfo/user/profile/updateGuestPwd', data)
        .then(response => {
            console.log('响应数据:', response.data); // 打印响应数据
            return response.data;
        })
        .catch(error => {
            console.error('密码重置失败:', error);
            throw error;
        });
}

export function getUserProfile(id) {
    return axios.get('/userinfo/user/profile/'+id)
        .then(response => {
            console.log('响应数据:', response.data); // 打印响应数据
            return response.data;
        })
        .catch(error => {
            console.error('获取信息失败:', error);
            throw error;
        });
}

