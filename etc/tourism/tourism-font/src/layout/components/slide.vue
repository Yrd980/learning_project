<template>
  <div class="block text-center">
    <el-carousel :interval="4000" type="card" height="400px">
      <el-carousel-item v-for="(item,index) in images" :key="index">
        <img :src="item" alt="" class="carousel-image"/>
      </el-carousel-item>
    </el-carousel>
  </div>
</template>

<script setup lang="ts">
import {ref} from "vue";

const images = ref([
  'src/assets/images/uploads/1280x800/202006026651.jpg',
  'src/assets/images/uploads/1280x800/202006026651.jpg',
  'src/assets/images/uploads/1280x800/202006026651.jpg',
  'src/assets/images/uploads/1280x800/202006026651.jpg',

])
</script>

<style scoped>


.el-carousel__item h3 {
  color: #475669;
  opacity: 0.75;
  line-height: 150px;
  margin: 0;
  text-align: center;
}

.carousel-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

</style>
