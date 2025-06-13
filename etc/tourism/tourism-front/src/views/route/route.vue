<template>
  <Top/>
  <div class="main-container">
    <div class="subheader">
      <div class="left">
        <span class="page-title">旅游路线</span>
        <span class="page-desc">路线</span>
      </div>
    </div>
    <div class="attraction-list">
      <div class="attraction-item" v-for="attraction in attractions" :key="attraction.id">
        <img :src="attraction.image" alt="Attraction Image"/>
        <div class="attraction-info">
          <h3>{{ attraction.name }}</h3>
          <p>{{ attraction.description }}</p>
          <el-button plain @click="showMap(104.0547155875603,30.652099893495052)">
            查看
          </el-button>
        </div>
      </div>
    </div>
    <el-dialog v-model="dialogTableVisible" :visible.sync="dialogTableVisible" :key="dialogKey" title="地图"
               width="1280" :before-close="handleClose">
      <div class="map-detail-container">
        <div class="map-container">
          <el-amap
              :center="[104.0547155875603,30.6520998934950525]"
              :zoom="zoom"
              @init="initMap"
          >
            <el-amap-control-map-type :visible="visible"/>
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
          <el-input
              v-model="keyword"
              v-if="visible"
              @input="handleSearch"
              :autofocus="true"
              ref="inputValue"
              clearable
              placeholder="输入城市+关键字搜索"
              style="width: 300px"
          >
            <template #loading>
              <svg class="circular" viewBox="0 0 50 50">
                <circle class="path" cx="25" cy="25" r="20" fill="none"/>
              </svg>
            </template>
          </el-input>
          <div class="toolbar">
            <button @click="switchVisible()">
              {{ visible ? '隐藏搜索' : '显示搜索' }}
            </button>
          </div>
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

            <!-- 地址 -->
            <el-tab-pane name="addressTab" v-if="visible" label="地址">
              <div id="panel"></div>
            </el-tab-pane>

            <!-- 景点 -->
            <el-tab-pane name="scenic" label="景点">
              <div id="panel1"></div>
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
  </div>
  <Footer/>
</template>

<script setup lang="js">
import {onBeforeMount, onMounted, ref} from 'vue';
import {ElAmap} from "@vuemap/vue-amap";
import Top from "@/components/Top.vue";
import Footer from "@/components/Footer.vue";
import {getScenicspotsByScenicAreaId} from "@/api/scenic/index.js";
import {initMapApi} from "@/util/map.js";
import {attractionData} from "@/views/route/data.js";
import RouteUtil from "@/util/routeUtil.js";
import {ElMessageBox} from "element-plus";

const list = ref([])
let polylinePath // 路线坐标
const polylineColor = '#3366FF'
const polylineStyle = 'solid'
const polylineOpacity = 1
const polylineWeight = 6
let markers = ref()
onMounted(async () => {
  const res = await getScenicspotsByScenicAreaId(1)
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
        <span class="marker-desc">${p.desc}</span>
      </div>
    `,
    offset: [-20, -20]
  }));
})


// 地图属性
const zoom = ref(18)
const center = ref([])
const attractions = ref(attractionData); //临时

//函数变量
const currentWeather = ref({}) //当天天气
const forecasts = ref() //预报天气
const chooseTab = ref('weather') //切换标签页,默认展示天气
const selectPos = ref([]) //当前位置
const recoveryPos = ref([]) //存储先前的位置
const keyword = ref(''); //搜索关键字
const inputValue = ref(null) //使用el-input的expose

const form = ref({
  city: '',
  start: '',
  end: '',
  waypoints: []
})

// 配置搜索
const defaultOptions = {
  // map: map, 初始化报错因为组件进行设计模式注入
  pageSize: 6, // 单页显示结果条数
  pageIndex: 1, // 页码
  citylimit: false, // 是否强制限制在设置的城市内搜索
  autoFitView: true,
};

let dialogKey = 0 //对话框刷新
let map = null; //地图示例
let poiInfo //搜索的信息

//以下为插件名
let geocoder = null //位置
let placeSearch = null //搜索

//设置可见
const dialogTableVisible = ref(false) //弹出框
const click = ref(false) // 点击设置点
const switchClick = () => {
  click.value = !click.value;
}
const visible = ref(false) // 卫星图等展示
const switchVisible = () => {
  visible.value = !visible.value;
  transport(recoveryPos.value[0], recoveryPos.value[1])
}


const handleClose = () => {
  inputValue.value.clear()
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

  //通用搜索
  AMap.plugin('AMap.PlaceSearch', () => {
    placeSearch = createSearch('', "panel")
  })

  // 添加列表项点击事件监听
  // 无法暴露
  placeSearch.on('listElementClick', e => {
    // 当POI列表项被点击时，执行以下代码
    let tmp = e.data; // 当前选中的POI信息
    poiInfo = RouteUtil.getLocByPoi(tmp)
    let lng = poiInfo[0];
    let lat = poiInfo[1];
    transport(lng, lat);
  })

  //放大缩小
  map.plugin('AMap.ToolBar', () => {
    const toolBar = new AMap.ToolBar();
    map.addControl(toolBar);
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
  // transport(selectPos.value[0], selectPos.value[1])
};

// 点击展示地图
const showMap = async (lng, lat) => {
  dialogKey++
  dialogTableVisible.value = true
  //  方便初始化定位
  selectPos.value = [lng, lat]
  recoveryPos.value = selectPos.value //初始化
  switchVisible()
  chooseTab.value = "weather"
}

const createSearch = (type, panel) => {
  return new AMap.PlaceSearch({
    ...defaultOptions, type, panel, map
  });
}

// 单个搜索
const handleSearch = () => {
  placeSearch.search(keyword.value);
  //切换到地址页面
  chooseTab.value = "addressTab";
  // 防止出现undefined
  if (poiInfo) {
    transport(poiInfo[0], poiInfo[1])
  }
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
@import "src/assets/styles/css/style.css";

.main-container {
  display: flex;
  flex-direction: column;
  height: 800px;
}

.attraction-list {
  display: flex;
  flex-wrap: wrap;
  justify-content: space-around;
}

.attraction-item {
  width: calc(33.33% - 10px);
  margin-bottom: 20px;
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

