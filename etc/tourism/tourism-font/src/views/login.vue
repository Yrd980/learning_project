<template >
  <div class="login" >
      <el-form ref="loginRef" :model="loginForm" :rules="loginRules" class="login-form">
      <h3 class="title">游客服务系统</h3>
      <el-form-item prop="username">

          <el-input
              v-model="loginForm.username"
              type="text"
              size="large"
              style="width: 92%"
              auto-complete="off"
              placeholder="账号"
          >
              <template #prefix>
                  <div class="input-icon-wrapper">
                      <el-icon class="custom-icon"><User /></el-icon>
                      <div class="icon-divider"></div>
                  </div>
              </template>
          </el-input>
      </el-form-item>
      <el-form-item prop="password">
          <el-input
              v-model="loginForm.password"
              type="password"
              size="large"
              auto-complete="off"
              placeholder="密码"
              style="width: 92%"
              @keyup.enter="handleLogin"
          >
              <template #prefix>
                  <div class="input-icon-wrapper">
                      <el-icon class="custom-icon"><Lock /></el-icon>
                      <div class="icon-divider"></div>
                  </div>
              </template>
          </el-input>
      </el-form-item>
      <el-form-item prop="code" v-if="captchaEnabled">
          <el-input
              v-model="loginForm.code"
              size="large"
              auto-complete="off"
              placeholder="验证码"
              style="width: 63%"
              @keyup.enter="handleLogin"
          >
              <template #prefix>
                  <div class="input-icon-wrapper">
                      <el-icon class="custom-icon"><CollectionTag /></el-icon>
                      <div class="icon-divider"></div>
                  </div>
              </template>
          </el-input>
          <div class="login-code">
              <img src="../assets/images/codeimg.png" class="login-code-img"/>
          </div>
      </el-form-item>
      <el-checkbox v-model="loginForm.rememberMe" style="margin:0px 0px 25px 0px;">记住密码</el-checkbox>
      <el-form-item style="width:100%;">
          <el-button
              :loading="loading"
              size="large"
              type="primary"
              style="width:100%;"
              @click.prevent="handleLogin"
          >
              <span v-if="!loading">登 录</span>
              <span v-else>登 录 中...</span>
          </el-button>
          <div style="float: right;" v-if="register">
              <router-link class="link-type" :to="'/guest/register'">立即注册</router-link>
          </div>
      </el-form-item>
  </el-form>
  </div>
</template>

<script setup>
import Cookies from "js-cookie";
import useUserStore from '@/store/modules/user'
import {useRoute, useRouter} from "vue-router";
import { getCurrentInstance, ref, watch } from 'vue';
import { ElMessage } from 'element-plus';
const userStore = useUserStore()
const route = useRoute();
const router = useRouter();
const { proxy } = getCurrentInstance();

const loginForm = ref({
  username: "",
  password: "",
  rememberMe: false,
  code: "",
  uuid: ""
});

const loginRules = {
  username: [{ required: true, trigger: "blur", message: "请输入您的账号" }],
  password: [{ required: true, trigger: "blur", message: "请输入您的密码" }],
  code: [{ required: true, trigger: "change", message: "请输入验证码" }]
};

const loading = ref(false);
// 验证码开关
const captchaEnabled = ref(true);
// 注册开关
const register = ref(true);
const redirect = ref(undefined);

watch(route, (newRoute) => {
    redirect.value = newRoute.query && newRoute.query.redirect;
}, { immediate: true });

function handleLogin() {
  proxy.$refs.loginRef.validate(valid => {
    if (valid) {
      loading.value = true;
      // 勾选了需要记住密码设置在 cookie 中设置记住用户名和密码
      if (loginForm.value.rememberMe) {
        Cookies.set("username", loginForm.value.username, { expires: 30 });
        Cookies.set("password", loginForm.value.password, { expires: 30 });
        Cookies.set("rememberMe", loginForm.value.rememberMe, { expires: 30 });
      } else {
        // 否则移除
        Cookies.remove("username");
        Cookies.remove("password");
        Cookies.remove("rememberMe");
      }
      // 调用action的登录方法

      userStore.login(loginForm.value).then(() => {
          // 登录成功后的逻辑代码
          ElMessage.success('登录成功'); // 弹出登录成功消息
          // 延迟一秒刷新页面
          setTimeout(() => {
              // 将 hotelId 传递给路由，跳转到详情页面
              proxy.$router.push(`/guest/starhotels`);
          }, 1000);
      })
    }
  });
}



function getCookie() {
  const username = Cookies.get("username");
  const password = Cookies.get("password");
  const rememberMe = Cookies.get("rememberMe");
  loginForm.value = {
    username: username === undefined ? loginForm.value.username : username,
    password: password === undefined ? loginForm.value.password : password,
    rememberMe: rememberMe === undefined ? false : Boolean(rememberMe)
  };
}

getCookie();
</script>

<style  scoped>
.login {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  width: 100vw;
  background-image: url("../assets/images/backimage.jpg");
  background-size: cover;
    background-repeat: no-repeat;
  background-position: center;
}
.title {
  margin: 0px auto 30px auto;
  text-align: center;
  color: #707070;
}

.login-form {
    background-color: rgba(255, 255, 255, 0.8);
    padding: 30px;
    border-radius: 10px;
    box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
    width: 400px;
}
.login-code {
  width: 33%;
  height: 40px;
  float: right;
}
.login-code-img {
  height: 40px;
  width: 100px;
  padding-left: 12px;
}
.input-icon-wrapper {
    display: flex;
    align-items: center;
}
.custom-icon {
    display: flex;
    align-items: center;
    color: #4a4a4a;
    font-size: 20px;
}
.icon-divider {
    width: 1px;
    height: 24px;
    background-color: #dcdfe6;
    margin-left: 8px;
}
</style>
