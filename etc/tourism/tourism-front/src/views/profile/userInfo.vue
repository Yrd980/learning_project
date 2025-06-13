<template>
  <el-form ref="userRef" :model="form" :rules="rules" label-width="80px">
    <el-form-item label="用户昵称" prop="nickName">
      <el-input v-model="form.nickName" maxlength="30" />
    </el-form-item>
    <el-form-item label="手机号码" prop="phonenumber">
      <el-input v-model="form.phonenumber" maxlength="11" />
    </el-form-item>
    <el-form-item label="邮箱" prop="email">
      <el-input v-model="form.email" maxlength="50" />
    </el-form-item>
    <el-form-item>
      <el-button type="primary" @click="submit">保存</el-button>
    </el-form-item>
  </el-form>
</template>

<script setup>
import { reactive , ref ,toRefs, getCurrentInstance,watch} from 'vue';
import { updateUserProfile } from "@/api/system/user";
import useUserStore from '@/store/modules/user';
const props = defineProps({
  user: {
    type: Object
  }
});
const userStore = useUserStore();
const { proxy } = getCurrentInstance();

const form = ref({});
const rules = ref({
  nickName: [{ required: true, message: "用户昵称不能为空", trigger: "blur" }],
  email: [{ required: true, message: "邮箱地址不能为空", trigger: "blur" }, { type: "email", message: "请输入正确的邮箱地址", trigger: ["blur", "change"] }],
  phonenumber: [{ required: true, message: "手机号码不能为空", trigger: "blur" }, { pattern: /^1[3|4|5|6|7|8|9][0-9]\d{8}$/, message: "请输入正确的手机号码", trigger: "blur" }],
});

function submit() {
  proxy.$refs.userRef.validate(valid => {
    if (valid) {
      // 添加用户ID到form对象中
      const updatedForm = { ...form.value, userId: userStore.id };
      console.log(updatedForm);
      updateUserProfile(updatedForm).then(response => {
        proxy.$modal.msgSuccess("修改成功");
        props.user.phonenumber = form.value.phonenumber;
        props.user.email = form.value.email;
      });
    }
  });
};
</script>

<style scoped>

</style>
