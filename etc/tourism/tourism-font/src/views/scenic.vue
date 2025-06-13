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
                <span class="page-title">景点浏览</span>
                <span class="page-desc">网罗天下美景，助您直达完美之旅。</span>
              </div>
            </div>
          </div>
        </div>

        <div id="content">
          <div class="user-searchbox">
            <el-input
                v-model="searchInput"
                id="search-spots-input"
                class="user-search"
                placeholder="搜索景点"/>
            <!--            <el-button-->
            <!--                id="search-spots"-->
            <!--                @click="handleSearch"-->
            <!--                :icon="Search"-->
            <!--                circle-->
            <!--            />-->
          </div>
        </div>

        <div class="card-container">
          <el-row :gutter="8">
            <el-col v-for="(item, index) in filteredItems" :key="index" :span="6" v-memo="[item]">
              <el-card class="box-card">
                <img :src="item.pic_url" class="card-image" alt="Image">
                <div style="padding: 12px;">
                  <span class="card-name">{{ item.name }}</span>
                  <div class="card-description">{{ item.desc }}</div>
                  <router-link
                      :to="{ name: 'detail', params: { id: item.id }}"
                  >
                    查看详情
                  </router-link>
                </div>
              </el-card>
            </el-col>
          </el-row>

        </div>
      </el-main>
      <Footer style="margin-top:40px;"/>
    </el-container>
  </div>
</template>

<script setup>
import {computed, onMounted, ref} from 'vue'
import Top from "@/components/Top.vue";
import {getAllScenicareas} from "@/api/scenic/index.js";

const searchInput = ref('')
const items = ref([])

// 计算属性，根据搜索关键词过滤景点
const filteredItems = computed(() => {
  console.log(items.value)
  if (!searchInput.value) {
    return items.value
  }
  return items.value.filter(item =>
      item.name.includes(searchInput.value) ||
      item.desc.includes(searchInput.value)
  )
})


onMounted(async () => {
  const res = await getAllScenicareas()
  items.value = res.data
})

</script>

<style scoped>
@import "@/assets/styles/css/style.css";

</style>


