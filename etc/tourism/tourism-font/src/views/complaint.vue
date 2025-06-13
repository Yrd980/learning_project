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
                <span class="page-title">投诉信息</span>
                <span class="page-desc">发起投诉</span>
              </div>
            </div>
            <div>
              <el-form :model="form" label-position="top">
                <el-form-item label="投诉内容" prop="content">
                  <el-input type="textarea" placeholder="请输入内容" @input="change($event)" v-model="form.content"/>
                </el-form-item>
              </el-form>
                <div class="dialog-footer">
                  <el-button type="primary" @click="submitForm">确 定</el-button>
                </div>
            </div>
            <ComplaintList/>
          </div>
        </div>
        <Footer/>
      </el-main>
    </el-container>
  </div>
</template>

<script setup>
import useUserStore from '@/store/modules/user'
import Footer from "@/components/Footer.vue";
import Top from "@/components/Top.vue";
import ComplaintList from "@/views/ComplaintList.vue";
import {addComplaints} from "@/api/complaint/complaints.js";
import {ref,getCurrentInstance} from "vue";


const { proxy } = getCurrentInstance();
const userStore = useUserStore();
const form = ref({});


/** 提交按钮 */
function submitForm() {
  console.log(form.value)
    const updatedForm = { ...form.value, userId: userStore.id };
    console.log(updatedForm)
        addComplaints(updatedForm).then(response => {

        })
}

function change(e){
  this.$forceUpdate()
}
</script>

<style scoped>
@import "@/assets/styles/css/style.css";
</style>
