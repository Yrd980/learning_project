<template>
  <div class="tourism">
    <el-container>
      <el-header>
        <Top/>
      </el-header>
      <el-main>
        <div id="wrapper">
          <div id="container">
            <div class="subheader">
              <div class="left">
                <span class="page-title">个人中心</span>
                <span class="page-desc">个人信息</span>
              </div>
            </div>
            <div>
              <div class="app-container">
                <el-row :gutter="20">
                  <el-col :span="6" :xs="24">
                    <el-card class="box-card">
                      <template v-slot:header>
                        <div class="clearfix">
                          <span>个人信息</span>
                        </div>
                      </template>
                      <div>
                        <el-descriptions column="1">
                          <el-descriptions-item label="用户账号名">{{ state.user.userName }}</el-descriptions-item>
                          <el-descriptions-item label="用户昵称">{{ state.user.nickName }}</el-descriptions-item>
                          <el-descriptions-item label="电话">{{ state.user.phonenumber }}</el-descriptions-item>
                          <el-descriptions-item label="用户邮箱">{{ state.user.email }}</el-descriptions-item>
                        </el-descriptions>
                      </div>
                    </el-card>
                  </el-col>
                  <el-col :span="18" :xs="24">
                    <el-card>
                      <template v-slot:header>
                        <div class="clearfix">
                          <span>修改信息</span>
                        </div>
                      </template>
                      <el-tabs>
                        <el-tab-pane label="基本资料" name="userinfo">
                          <userInfo/>
                        </el-tab-pane>
                        <el-tab-pane label="修改密码" name="resetPwd">
                          <resetPwd/>
                        </el-tab-pane>
                      </el-tabs>
                    </el-card>
                  </el-col>
                </el-row>
              </div>
            </div>
          </div>
        </div>
        <Footer/>
      </el-main>
    </el-container>
  </div>
</template>

<script setup>
import resetPwd from "./resetPwd"
import userInfo from "./userInfo";
import useUserStore from '@/store/modules/user';
import {defineComponent,reactive} from "vue";
import Footer from "@/components/Footer.vue";
import Top from "@/components/Top.vue";
import {Discount} from "@element-plus/icons-vue";
import { getUserProfile } from "@/api/system/user.js"
const state =reactive({
  user: {}
});
const userStore = useUserStore();
function getProfile(){
  console.log('state:'+state)
  getUserProfile(userStore.id).then(response => {
    console.log(response)
    state.user =response.data;
  })
}

getProfile();
</script>

<style scoped>
@import "@/assets/styles/css/style.css";
</style>
