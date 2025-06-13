<template>
  <div class="tourism">
    <el-container>
      <el-header>
        <Top/>
      </el-header>
      <el-main>
        <slide style="margin-bottom: 40px"/>
        <div id="wrapper">
          <div id="container">
            <section id="content">

              <!--newsletter -->

              <div class="emergency">
                <el-table :data="emergencyinfoListView" border :default-sort="{ prop: 'priority', order: 'descending' }"
                          :header-cell-style="{backgroundColor: '#fdf6ec'}">
                  <el-table-column prop="content" label="应急信息预警" width="200"></el-table-column>
                  <el-table-column prop="priority" label="应急信息预警" width="200" v-id="false"></el-table-column>
                </el-table>
              </div>

              <div class="hr">
                <hr/>
              </div>

              <div class="one-third">
                <h3 class="icon32 icon-tick thin">技术领先</h3>
                <p>
                  我们一直将技术创新视为企业的活力源泉，在提升研发能力方面不遗余力。我们建立了一整套现代化服务系统，包括：国际机票、酒店预订平台、客户管理系统、房量管理系统、呼叫排队系统、订单处理系统、服务质量监控系统等。依靠这些先进的服务和管理系统，我们为会员提供更加便捷和高效的服务。</p>
              </div>

              <div class="one-third">
                <h3 class="icon32 icon-tick thin">规模经营</h3>
                <p>
                  服务规模化和资源规模化是我们的核心优势之一。我们在全球200个国家和地区与近80万家酒店建立了长期稳定的合作关系，其机票预订网络已覆盖国际国内绝大多数航线。规模化的运营不仅可以为会员提供更多优质的旅行选择，还保障了服务的标准化，确保服务质量，并降低运营成本。</p>
              </div>

              <div class="one-third last">
                <h3 class="icon32 icon-tick thin">体系规范</h3>
                <p>
                  先进的管理和控制体系是我们的又一核心优势。我们将服务过程分割成多个环节，以细化的指标控制不同环节，并建立起一套精益服务体系。同时，我们还将制造业的质量管理方法——六西格玛体系成功运用于旅行业。目前，我们各项服务指标均已接近国际领先水平，服务质量和客户满意度也随之大幅提升。</p>
              </div>

              <div class="hr">
                <hr/>
              </div>

              <!--newsection -->
              <div class="section-title">
                <span class="h3">热门目的地</span>
                <router-link style="float: right" to="/recommend">查看目的地</router-link>
              </div>

              <div class="card-container" style="transform: translateX(-10px)">
                <el-row :gutter="8">
                  <el-col v-for="(item, index) in items" :key="index" :span="6">
                    <el-card class="box-card">
                      <img :src="item.image" class="card-image" alt="Image">
                      <div style="padding: 12px;">
                        <span class="card-name">{{ item.name }}</span>
                        <div class="card-description">{{ item.description }}</div>
                      </div>
                    </el-card>
                  </el-col>
                </el-row>
              </div>

              <br class="clear"/>
            </section>
          </div>
        </div>
        <Footer/>
      </el-main>
    </el-container>
  </div>
</template>


<script setup>
import Top from "@/components/Top.vue";
import Footer from "@/components/Footer.vue";
import Slide from "@/layout/components/slide.vue";
import useUserStore from '@/store/modules/user'
import {reactive, ref, toRefs} from 'vue'
import {listEmergencyinfo} from "@/api/emergency/emergency.js";
const emergencyinfoList = ref([]);
const emergencyinfoListView = ref([]);
const userStore = useUserStore();
const size = ref('default')
const labelPosition = ref('right')
const loading = ref(true);  // 控制加载状态
const total = ref(0);  // 总条目数
const data = reactive({
  form: {},
  queryParams: {
    pageNum: 1,
    pageSize: 10,
    content: null,
  },
});
const sizeForm = reactive({
  name: '',
  region: '',
  date1: '',
  date2: '',
  delivery: false,
  type: [],
  resource: '',
  desc: '',
})
const { queryParams, form } = toRefs(data);
const items = [
  {image: 'src/assets/images/uploads/1280x800/login-background.jpg', name: 'Name 1', description: 'Description 1'},
  {image: 'https://via.placeholder.com/150', name: 'Name 2', description: 'Description 2'},
  {image: 'https://via.placeholder.com/150', name: 'Name 3', description: 'Description 3'},
  {image: 'https://via.placeholder.com/150', name: 'Name 4', description: 'Description 4'},
  {image: 'https://via.placeholder.com/150', name: 'Name 5', description: 'Description 5'},
  {image: 'https://via.placeholder.com/150', name: 'Name 6', description: 'Description 6'},
  {image: 'https://via.placeholder.com/150', name: 'Name 7', description: 'Description 7'},
  {image: 'https://via.placeholder.com/150', name: 'Name 8', description: 'Description 8'},

]

function onSubmit() {
  console.log('submit!')
}

function getList() {
  loading.value = true;  // 设置加载状态
  listEmergencyinfo(queryParams.value).then(response => {
    const currentTime = new Date();  // 获取当前时间的 Date 对象
    emergencyinfoList.value = response.rows;
    emergencyinfoListView.value = response.rows.filter(item => {
      const validityTime = new Date(item.validity);  // 将 validity 转换为 Date 对象
      return item.status === 1 && validityTime > currentTime;
    });
    total.value = response.total;
    loading.value = false;
  });
}


getList();
</script>


<style scoped>
@import "src/assets/styles/css/style.css";

.form_btn {
  display: flex;
  justify-content: space-between; /* 按钮之间留有空间 */
  align-items: center; /* 垂直居中对齐 */
}

.el-button {
  float: right;
  margin-right: 10px; /* 按钮之间的间距 */
}

.emergency {
  width: 200px;
  position: absolute;
  top: 20px;
  right: -220px;
}
</style>
