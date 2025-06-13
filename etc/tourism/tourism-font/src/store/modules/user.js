import { login1, logout, getInfo } from '@/api/login'
import { computed } from 'vue';
import defAva from '@/assets/images/profile.jpg'
import { defineStore } from 'pinia'
import { useStore } from 'vuex';
// 访问存储的用户数据
import store from '@/store';
const useUserStore = defineStore(
  'user',
  {
    state: () => ({
      id: -1,
      name: '',
      avatar: '',
      roles: [],
      permissions: []
    }),
    actions: {
      // 登录
      async login(userInfo) {
        const username = userInfo.username.trim()
        const password = userInfo.password
        const code = 5374
        const uuid = userInfo.uuid
        const userData = await login1(username, password);
        this.id = userData.user_id;
        this.name = userData.user_name;
        this.avatar = (userData.avatar == "" || userData.avatar == null) ? defAva : userData.avatar;
        return userData;

        // return new Promise((resolve, reject) => {
        //   login1(username, password).then(response => {
        //     console.log(userData)
        //     let data = response.data
        //     this.id = data.userId
        //     this.name = data.userName
        //     this.avatar = (data.avatar == "" || data.avatar == null) ? defAva : data.avatar;
        //     resolve()
        //   }).catch(error => {
        //     reject(error)
        //   })
        // })
      },
      // 获取用户信息
      getInfo() {
        return new Promise((resolve, reject) => {
          getInfo().then(res => {
            const user = res.user
            const avatar = (user.avatar == "" || user.avatar == null) ? defAva : user.avatar;

            if (res.roles && res.roles.length > 0) { // 验证返回的roles是否是一个非空数组
              this.roles = res.roles
              this.permissions = res.permissions
            } else {
              this.roles = ['ROLE_DEFAULT']
            }
            this.id = user.userId
            this.name = user.userName
            this.avatar = avatar
            resolve(res)
          }).catch(error => {
            reject(error)
          })
        })
      },
      // 退出系统
      logOut() {
        return new Promise((resolve, reject) => {
          logout().then(() => {
            this.id = -1  // 将id设置为未登录状态
            this.name = ''
            this.avatar = ''
            this.roles = []
            this.permissions = []
            resolve()
          }).catch(error => {
            reject(error)
          })
        })
      }
    }
  })

export default useUserStore
