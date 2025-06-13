<template xmlns="http://www.w3.org/1999/html">
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
                <span class="page-title">景点推荐</span>
                <span class="page-desc">网罗天下美景，助您直达完美之旅。</span>
                <!-- 链接到地图，显示酒店位置 -->
                <el-button style="transform: translateX(100px)" plain @click="showMap(selectPos[0],selectPos[1])">
                  显示路线
                </el-button>
              </div>
            </div>
          </div>
        </div>
        <div class="container">
          <div class="left-side">
            <!-- 左边内容 -->
            <el-card v-for="(item, index) in scenic" :key="index" class="box-card1">
              <img :src="item.pic_url" class="card-image1" alt="Image">
              <div>
                <div class="card-description1">{{ item.desc }}</div>
              </div>
            </el-card>
            <div class="reviews">
              <!-- 使用el-scrollbar实现点评列表滚动 -->
              <el-scrollbar style="margin-top: 40px" height="800px">
                <!-- 遍历并显示可见的点评列表 -->
                <div v-for="review in reviewList" :key="review.id" class="scrollbar-demo-item01">
                  <div class="review-head">
                    <div class="review-head-left">
                      <!-- 显示点评用户头像 -->
                      <img :src="review.avatar" class="visitor-image" alt="visitor image"/>
                      <!-- 显示点评用户名称 -->
                      <h3>{{ review.guest_name }}</h3>
                    </div>
                    <div class="review-head-right">
                      <!-- 显示点评评分，并根据评分设置颜色 -->
                      <p><strong>评分:</strong>
                        <span class="rating" :style="{ color: ratingColor(review.rating) }">
                                                {{ review.rating }}
                                                </span>
                        / 100
                      </p>
                    </div>
                  </div>
                  <div class="review-content">
                    <div class="review-card-left">
                      <!-- 显示点评的时间 -->
                      <p>{{ review.review_date }}</p>
                    </div>
                    <div class="review-card-right">
                      <!-- 显示点评内容 -->
                      {{ review.content }}
                    </div>
                  </div>
                </div>
              </el-scrollbar>
            </div>
          </div>
          <div class="right-side">
            <div class="widget categories">
              <div class="h3 widget-title">
                分类目录
              </div>
              <div class="widget-content">
                <ul>
                  <li>
                    <a href="#"><span class="ui-icon ui-icon-triangle-1-e"></span> 旅游目的地</a>
                    <small>23</small>
                  </li>
                  <li>
                    <a href="#"><span class="ui-icon ui-icon-triangle-1-e"></span> 旅游小贴士</a>
                    <small>12</small>
                  </li>
                  <li>
                    <a href="#"><span class="ui-icon ui-icon-triangle-1-e"></span> 旅游新闻</a>
                    <small>9</small>
                  </li>
                  <li>
                    <a href="#"><span class="ui-icon ui-icon-triangle-1-e"></span> 特价旅游</a>
                    <small>19</small>
                  </li>
                </ul>
              </div>
            </div>

            <div class="widget tabs-widget">
              <div class="h3 widget-title">
                最新评论
              </div>
              <div class="widget-content">
                <div class="tabs">
                  <div class="tab-item">
                    <strong>用户名:</strong> {{ newestReview.guest_name }}
                  </div>
                  <div class="tab-item">
                    <strong>点评内容:</strong> {{ newestReview.content }}
                  </div>
                </div>
              </div>
            </div>

            <div class="widget accordion-widget">
              <div class="h3 widget-title">
                注意事项
              </div>
              <div class="widget-content">
                <div class="accordion">
                  <el-collapse v-model="activeName" accordion>
                    <el-collapse-item title="旅行保障" name="1">
                      <div class="acc-content">
                        <p>
                          先进的管理和控制体系是我们的又一核心优势。我们将服务过程分割成多个环节，以细化的指标控制不同环节，并建立起一套精益服务体系。同时，我们还将制造业的质量管理方法——六西格玛体系成功运用于旅行业。目前，我们各项服务指标均已接近国际领先水平，服务质量和客户满意度也随之大幅提升。</p>
                      </div>
                    </el-collapse-item>
                    <el-collapse-item title="出现保障" name="2">
                      <div class="acc-content">
                        <p>
                          出门必带的东西，要知道我们是会出去放松的，自然不会带很多的东西，但这几件东西一定不能忘，最重要的就是身份证和银行卡，现在什么都是安全为主，如果没有身份证车票、住宿，门票都买不到，即使你到了景点都只能眼巴巴的看着别人去游玩，第二就是银行卡，很多人觉得现在都是网上支付，微信、支付宝应有尽有，其实不然这些是都需要手机，如果在外手机没电了，或是不小心遗失，这时候银行卡就会发挥巨大的作用，所以为了以防万一，一定要带一张有钱的银行卡。</p>
                      </div>
                    </el-collapse-item>
                    <el-collapse-item title="疾病预防" name="3">
                      <div class="acc-content">
                        <p>了解当地医疗制度、费用情况，结合自身身体情况制订适宜的医疗计划，选择购买适合的医疗保险。
                          应急救治
                          了解附近药店、医院的具体位置，熟记当地的急救电话。并将相关信息记录留存备用。
                          关注疫情
                          关注当地报纸、电视等新闻媒体，了解有无疫情爆发。
                          饮食卫生
                          日常生活注意饮食卫生，照顾好自己的身体。
                          不吃不新鲜的食物和变质食物，不吃陌生人交给的食物，不吃捡拾得来的食物，不采摘食用蘑菇和其它不认识的食物。
                          注意食品保质期和保质方法。加工菜豆、豆浆等豆类食品时须充分加热。不吃发芽、发霉的土豆和花生。保持饮用水和厨房用水清洁干净，否则，应把水煮沸或进行消毒处理后饮用。
                          中毒救治
                          发生食物中毒，应立即停止食用可疑食品，赴医院寻求专业救治，或在专业人员指导下，采取饮水、催吐、导泻等方法进行自救。
                          尊重风俗
                          伊斯兰国家禁酒，禁止食用动物血液、猪肉和有利齿利爪的猛兽（如狗肉）、非反刍动物（如驴肉）或自死动物（包括因打、摔、触、勒、电等原因而死的动物）。
                          抑制传染病
                          有效抑制传染病的流行，关键在于切断传染病的传播链：即控制传染源、切断传播途径、保护易感染人群。
                          预防先行
                          养成讲卫生的好习惯，注意个人卫生、食品卫生、环境卫生。
                          加强身体锻炼，提高免疫能力。
                          按规定接种疫苗。对传染病人要早发现、早报告、早治疗、早隔离。防止交叉感染。</p>
                      </div>
                    </el-collapse-item>
                  </el-collapse>
                </div>
              </div>
            </div>

            <div class="widget tag-widget">
              <div class="h3 widget-title">
                热门标签
              </div>
              <div class="widget-content">
                <div class="tag-cloud">
                  <a href="#">国内游</a>
                  <a href="#">五一欢乐游</a>
                  <a href="#">国庆七天乐</a>
                  <a href="#">欧洲</a>
                  <a href="#">东南亚</a>
                  <a href="#">家庭</a>
                </div>
              </div>
            </div>
          </div>
        </div>
        <el-dialog v-model="dialogTableVisible"
                   :visible.sync="dialogTableVisible"
                   :key="dialogKey" title="地图"
                   style="width: 1000px"
                   :before-close="handleClose">
          <div class="map-detail-container">
            <div class="map-container">
              <el-amap
                  :center="selectPos"
                  :zoom="zoom"
                  @init="initMap"
              >
                <el-amap-control-map-type :visible="visible"/>
                <el-amap-marker
                    :position="selectPos"
                />
                <el-amap-polyline
                    :path="polylinePath"
                    :stroke-color="polylineColor"
                    :stroke-style="polylineStyle"
                    :stroke-opacity="polylineOpacity"
                    :stroke-weight="polylineWeight"
                />
                <el-amap-marker
                    v-for="(marker, index) in markers"
                    :key="index"
                    :position="marker.position"
                    :content="marker.content"
                    :offset="marker.offset"
                />

              </el-amap>
            </div>
            <div class="detail-container">
              <el-tabs v-model="chooseTab" type="card" stretch>
                <!-- 当前天气 -->
                <el-tab-pane name="weather" label="当前天气">
                  <div id="weatherContainer">
                    <div id="currentWeather">
                      <h2>当前天气</h2>
                      <p><strong>天气状况：</strong>{{ currentWeather.weather }}</p>
                      <p><strong>温度：</strong>{{ currentWeather.temperature }}°C</p>
                      <p><strong>风向：</strong>{{ currentWeather.windDirection }}</p>
                      <p><strong>风力：</strong>{{ currentWeather.windPower }}</p>
                      <p><strong>湿度：</strong>{{ currentWeather.humidity }}%</p>
                    </div>
                    <div id="forecastWeather">
                      <h2>天气预报</h2>
                      <ul id="forecastList">
                        <li v-for="(forecast, index) in forecasts" :key="index">
                          <p>日期: {{ forecast.date }}
                            白天: {{ forecast.dayWeather }}, {{ forecast.dayTemp }}°C, {{ forecast.dayWindDir }}风
                            {{ forecast.dayWindPower }}级
                            夜间: {{ forecast.nightWeather }}, {{ forecast.nightTemp }}°C, {{ forecast.nightWindDir }}风
                            {{ forecast.nightWindPower }}级
                          </p>
                        </li>
                      </ul>
                    </div>
                  </div>
                </el-tab-pane>

                <!-- 景点 -->
                <el-tab-pane name="scenic" label="景点">
                  <div id="panel1"></div>
                  <div id="panel"></div>
                </el-tab-pane>

                <!-- 美食 -->
                <el-tab-pane name="food" label="美食">
                  <div id="panel2"></div>
                </el-tab-pane>

                <!-- 附近的旅店 -->
                <el-tab-pane name="hotel" label="住宿">
                  <div id="panel3"></div>
                </el-tab-pane>
              </el-tabs>
            </div>
          </div>
        </el-dialog>
      </el-main>
      <Footer/>
    </el-container>
  </div>
</template>

<script setup>
import Top from "@/components/Top.vue";
import {computed, onBeforeMount, onMounted, ref} from "vue";
import {useRoute} from "vue-router";
import {getScenicspotsByScenicAreaId} from "@/api/scenic/index.js";
import {ElAmap} from "@vuemap/vue-amap";
import RouteUtil from "@/util/routeUtil.js";
import {initMapApi} from "@/util/map.js";
import {ElMessageBox} from "element-plus"

const activeName = ref('1')
const list = ref([])
let polylinePath // 路线坐标
const polylineColor = '#3366FF'
const polylineStyle = 'solid'
const polylineOpacity = 1
const polylineWeight = 6
let markers = ref()
const route = useRoute() //使用钩子函数获取路由
const scenic = ref({
  id: 1,
  name: "",
  description: "",
  images: [],
  position: [104.0547155875603, 30.652099893495052], // 经度, 纬度
})


// 根据日期排序的函数
const sortByDate = (a, b) => new Date(b.review_date) - new Date(a.review_date);

// 计算属性，返回按日期排序的点评列表
const sortedReviews = computed(() => {
  return [...reviewList.value].sort(sortByDate);
});

// 获取最新的点评
const newestReview = computed(() => {
  return sortedReviews.value[0];
});

const reviewList = ref([
  {
    id: 1,
    avatar: 'https://via.placeholder.com/150', // 示例头像URL
    guest_name: '张三',
    rating: 90,
    review_date: '2023-12-01',
    content: '这个地方风景优美，服务也非常好，下次还会再来。'
  },
  {
    id: 2,
    avatar: 'https://via.placeholder.com/150', // 示例头像URL
    guest_name: '李四',
    rating: 95,
    review_date: '2023-11-20',
    content: '非常棒的体验，强烈推荐给朋友们。'
  },
  {
    id: 3,
    avatar: 'https://via.placeholder.com/150', // 示例头像URL
    guest_name: '王五',
    rating: 85,
    review_date: '2023-10-15',
    content: '景色不错，但是人有点多，希望下次能更安静一些。'
  },
  {
    id: 4,
    avatar: 'https://via.placeholder.com/150', // 示例头像URL
    guest_name: '赵六',
    rating: 100,
    review_date: '2023-09-10',
    content: '完美的一次旅行，一切都超出了预期！'
  },
  // ... 可以添加更多点评
]);

// 评分颜色计算函数
const ratingColor = (rating) => {
  if (rating >= 90) return '#00FF00'; // 绿色
  if (rating >= 60) return '#7FFF00'; // 黄绿色
  if (rating >= 40) return '#FFFF00'; // 黄色
  if (rating >= 20) return '#FFA500'; // 橙色
  return '#FF0000'; // 红色
};

onMounted(async () => {
  let index = route.params.id
  const res = await getScenicspotsByScenicAreaId(index)
  scenic.value = res.data
  // selectPos.value = await RouteUtil.getLocation(scenic.value[0].name)
  selectPos.value = [104.0547155875603, 30.652099893495052]
  // 使用map函数批量处理每个地址对象
  list.value = res.data.map(item => {
    const positionArray = item.address.split(',').map(Number);
    return {
      ...item, // 展开原始对象
      position: positionArray // 添加新的position属性
    };
  });

  polylinePath = list.value.map(p => p.position)// 路线坐标
  markers.value = list.value.map((p, index) => ({
    position: p.position,
    content: `
      <div class="marker">
        <div class="marker-index">${index + 1}</div>
        <span style="color: red">${p.desc}</span>
      </div>
    `,
    offset: [-20, -20]
  }));

})


// 地图属性
const zoom = ref(17)
const center = ref([104.0547155875603, 30.652099893495052])

//函数变量
const currentWeather = ref({}) //当天天气
const forecasts = ref() //预报天气
const chooseTab = ref('weather') //切换标签页,默认展示天气
const selectPos = ref([]) //当前位置
const recoveryPos = ref([]) //存储先前的位置

const form = ref({
  city: '',
  start: '',
  end: '',
  waypoints: []
})


let dialogKey = 0 //对话框刷新
let map = null; //地图示例

//以下为插件名
let geocoder = null //位置

//设置可见
const dialogTableVisible = ref(false) //弹出框
const click = ref(false) // 点击设置点

const visible = ref(false) // 卫星图等展示
const switchVisible = () => {
  visible.value = !visible.value;
  transport(recoveryPos.value[0], recoveryPos.value[1])
}

let placeSearch = null

const handleClose = () => {
  ElMessageBox.confirm('确认关闭地图吗')
      .then(() => {
        dialogTableVisible.value = !dialogTableVisible.value
        done()
      })
      .catch(() => {
        // catch error
      })
}

// 获得地图变量使用插件
const initMap = (mapInstance) => {


  map = mapInstance;
  //添加插件
  AMap.plugin('AMap.Geocoder', () => {
    geocoder = new AMap.Geocoder({
      // ...geoCodeConfig, 'offset': new AMap.Pixel(-18, -36),
    })
  })

  //放大缩小
  map.plugin('AMap.ToolBar', () => {
    const toolBar = new AMap.ToolBar();
    map.addControl(toolBar);
  })

  AMap.plugin('AMap.PlaceSearch', () => {
    placeSearch = createSearch('', "panel")
  })

  //定位
  map.plugin('AMap.Geolocation', () => {
    const navigation = new AMap.Geolocation({
      enableHighAccuracy: true,//是否使用高精度定位，默认:true
      timeout: 10000,          //超过10秒后停止定位，默认：5s
      position: 'LB',    //定位按钮的停靠位置
      offset: [10, 36], //定位按钮与设置的停靠位置的偏移量，默认：[10, 20]
      zoomToAccuracy: true,   //定位成功后是否自动调整地图视野到定位点
    });
    map.addControl(navigation);
  })


};

const createSearch = (type, panel) => {
  return new AMap.PlaceSearch({
    type, panel, map
  });
}


// 点击展示地图
const showMap = async () => {
  dialogKey++
  dialogTableVisible.value = true
  //  方便初始化定位
  recoveryPos.value = selectPos.value //初始化
  switchVisible()
  chooseTab.value = "weather"
}

//初始化标签页
const initTab = () => {
  const tabOptions = {
    'scenic': {type: '景点', panel: "panel1"},
    'food': {type: '餐饮服务', panel: "panel2"},
    'hotel': {type: '住宿', panel: "panel3"}
  };

  for (const [key, value] of Object.entries(tabOptions)) {
    let placeSearch = createSearch(value.type, value.panel);
    placeSearch.searchNearBy('', selectPos.value, 600, function (status, result) {
          if (status === 'complete') {
            console.log(key + " " + chooseTab.value)
          } else {
            console.log('搜索失败');
          }
        }
    )
  }
}

// 跳转
const transport = async (lng, lat) => {
  const res = await RouteUtil.getPosition(lng, lat)
  recoveryPos.value = selectPos.value //便于还原
  selectPos.value = [lng, lat]
  const city = res.city
  const weatherData = await RouteUtil.getWeather(city);
  // 提取当前天气
  currentWeather.value = weatherData[0];
  // 提取天气预报
  forecasts.value = weatherData[1].forecasts;
  initTab()
  map.setZoomAndCenter(zoom.value, selectPos.value);
}

//加快初始化
onBeforeMount(() => {
  initMapApi()
})
</script>

<style scoped>
@import "@/assets/styles/css/style.css";

.container {
  display: flex;
}

.left-side {
  flex: 0 0 40%; /* 占据宽度60%，剩余40%给右边的div */
  margin-left: 260px;
  margin-right: 30px;
  background-color: #f0f0f0;
}

.right-side {
  flex: 0 0 22%; /* 占据宽度40%，剩余60%给左边的div */
  background-color: #ddd;
}


.left {
  flex: 5;
}

.tabs {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
}

.tab-item {
  margin: 10px 3px;
  text-align: left;
}


a {
  display: block;
  margin-bottom: 20px;
}


.slider-demo-block .demonstration + .cost {
  flex: 0 0 70%;
}

:deep(.el-dialog) {
  width: 480px;
  background: rgba(255, 255, 255, 0.5);
  z-index: 9999;
}

:deep(.el-overlay) {
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(0.5px) !important;
}

.scrollbar-demo-item01 {
  margin-top: 30px;
  margin-left: 5px;
  margin-right: 5px;
  display: flex;
  flex: 3;
  flex-direction: column;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
  height: 300px;
  border-radius: 8px;
  color: #000;
}

.review-head {
  display: flex;
  align-items: flex-start;
}

.review-head-left {
  flex: 2;
  padding-right: 15px;
  padding-left: 20px;
}

.visitor-image {
  max-width: 80px;
  max-height: 80px;
  object-fit: cover;
  padding-top: 20px;
}

.review-head-right {
  flex: 4;
}

.rating {
  font-weight: bold;
  color: #1890ff;
  font-size: 30px;
}

.review-content {
  display: flex;
  align-items: flex-start;
}

.review-card-left {
  padding-right: 15px;
  padding-left: 20px;
  flex: 2;
}

.review-card-right {
  flex: 4;
  padding-right: 20px;
  word-wrap: break-word; /* 使单词在必要时换行 */
  white-space: normal; /* 允许文本换行 */
  overflow-wrap: break-word; /* 支持更现代的浏览器，允许在必要时换行 */
  word-break: break-all; /* 强制在长词或 URL 中的任意位置换行 */
}

.box-card1 {
  transition: 0.3s;
  width: 100%;
  min-width: 220px;
}

.card-image1 {
  width: 100%;
  height: 300px;
  object-fit: cover;
}

.card-description1 {
  text-align: center;
  /* 当内容超出最大高度时显示滚动条 */
  overflow: auto;
  color: #666;
  margin-top: 10px;
}

.map-detail-container {
  display: flex;
  height: 600px;
}

.map-container {
  flex: 6;
  height: 100%;
}

.detail-container {
  display: flex;
  flex-direction: column;
  flex: 4;
  background-color: #f9f9f9;
  height: 100%;
}

#panel {
  width: 400px;
  height: 500px;
}

#panel1 {
  width: 400px;
  height: 500px;
}

#panel2 {
  width: 400px;
  height: 500px;
}

#panel3 {
  width: 400px;
  height: 500px;
}

.marker {
  display: flex; /* 使用flex布局 */
  flex-direction: row; /* 水平排列子元素 */
  align-items: center; /* 垂直居中对齐 */
  justify-content: center; /* 水平居中对齐 */
  background-color: #fff;
  border: 1px solid #ccc;
  border-radius: 4px;
  padding: 5px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
}

.marker-index,
.marker-desc,
.marker-id {
  margin: 0 5px; /* 只设置左右间距 */
  text-align: center; /* 文本居中 */
  white-space: nowrap; /* 防止内容换行 */
}

.marker-index {
  font-size: 16px;
  font-weight: bold;
  color: #333;
}

.marker-desc {
  color: red;
  font-size: 14px;
}

.marker-id {
  font-size: 12px;
  color: #666;
}

</style>
