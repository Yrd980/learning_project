<template>
  <el-tabs
      style="height: 50px;
      display: flex;
      justify-content: center;"
      @tab-click="handleClick"
  >
    <el-tab-pane label="首页" name="home"></el-tab-pane>
    <el-tab-pane label="景点" name="scenic"></el-tab-pane>
    <el-tab-pane label="星级酒店" name="starHotel"></el-tab-pane>
    <el-tab-pane label="非星级酒店" name="nonStarHotel"></el-tab-pane>
<!--    <el-tab-pane label="路线" name="route"></el-tab-pane>-->
    <el-tab-pane label="我的订单" name="order"></el-tab-pane>
    <el-tab-pane label="个人中心" name="profile"></el-tab-pane>
    <el-tab-pane label="发起投诉" name="complaint"></el-tab-pane>

  </el-tabs>
  <!--  <slide/>-->
</template>

<script setup>
import router from "@/router/index.js";

const handleClick = (pane) => {
  let tabName = pane.props.name
  // 根据选中的标签页名称跳转到对应的路由
  router.push({
    name: tabName
  });
  console.log(tabName)
}

</script>

<style scoped>

</style>
