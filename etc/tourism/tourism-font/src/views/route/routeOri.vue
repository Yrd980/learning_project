<template>
  <!--  &lt;!&ndash; 交通 &ndash;&gt;-->
  <!--  <el-tab-pane name="traffic" label="交通">-->
  <!--    &lt;!&ndash; 目的地输入框 &ndash;&gt;-->
  <!--    <el-input v-model="start" placeholder="请输入起点" class="input-field"/>-->

  <!--    &lt;!&ndash; 途径点输入框 &ndash;&gt;-->
  <!--    <div v-for="(waypoint, index) in waypoints" :key="index" class="waypoint-row">-->
  <!--      <el-input-->
  <!--          v-model="waypoints[index]"-->
  <!--          placeholder="请输入途径点"-->
  <!--          class="input-field"-->
  <!--      />-->
  <!--      <el-button type="danger" :icon="Delete" class="delBut" size="small" @click="removeWaypoint(index)"-->
  <!--                 circle/>-->
  <!--    </div>-->

  <!--    &lt;!&ndash; 添加途径点按钮 &ndash;&gt;-->
  <!--    <el-button type="text" icon="el-icon-plus" @click="addWaypoint">添加途径点</el-button>-->

  <!--    &lt;!&ndash; 终点输入框 &ndash;&gt;-->
  <!--    <el-input v-model="destination" placeholder="请输入终点" class="input-field"/>-->

  <!--    &lt;!&ndash; 提交导航按钮 &ndash;&gt;-->
  <!--    <el-button type="primary" @click="submitNavigation">导航</el-button>-->
  <!--    <el-button type="primary" @click="switchNav">取消</el-button>-->
  <!--    &lt;!&ndash; 交通信息展示代码 &ndash;&gt;-->
  <!--    <div v-if="nav" id="navigation"></div>-->

  <!--  </el-tab-pane>-->

  <!--  <el-form :model="form" @submit.native.prevent="handleSubmit">-->
  <!--    <el-form-item label="城市" prop="city">-->
  <!--      <el-input v-model="form.city" placeholder="请输入城市"></el-input>-->
  <!--    </el-form-item>-->
  <!--    <el-form-item label="起点" prop="start">-->
  <!--      <el-input v-model="form.start" placeholder="请输入起点"></el-input>-->
  <!--    </el-form-item>-->
  <!--    <el-form-item label="终点" prop="end">-->
  <!--      <el-input v-model="form.end" placeholder="请输入终点"></el-input>-->
  <!--    </el-form-item>-->
  <!--                    <el-form-item label="途经点" prop="waypoints">-->
  <!--                      <el-input v-model="waypointInput" placeholder="请输入途经点(可选)"></el-input>-->
  <!--                      <el-button type="primary" @click="addWaypoint">添加</el-button>-->
  <!--                      <ul>-->
  <!--                        <li v-for="(point, index) in form.waypoints" :key="index">-->
  <!--                          {{ point }}-->
  <!--                          <el-button type="danger" @click="removeWaypoint(index)">删除</el-button>-->
  <!--                        </li>-->
  <!--                      </ul>-->
  <!--                    </el-form-item>-->
  <!--    <el-form-item>-->
  <!--      <el-button type="primary" native-type="submit">搜索</el-button>-->
  <!--      <el-button type="danger" @click="switchNav">取消</el-button>-->
  <!--    </el-form-item>-->
  <!--  </el-form>-->
  <!--  &lt;!&ndash; 交通信息展示代码 &ndash;&gt;-->
  <!--  <div v-if="nav" id="navigation"></div>-->
</template>

<script setup lang="ts">

// // 添加途径点输入框
// const addWaypoint = () => {
//   waypoints.value.push('');
// }
//
// // 移除途径点输入框
// const removeWaypoint = (index) => {
//   waypoints.value.splice(index, 1);
// }
//
// const submitNavigation = async (way) => {
//   way = driving
//   let origin = await getLanAndLong(start.value);
//   let target = await getLanAndLong(destination.value);
//   if (waypoints.value.length > 0) {
//     let opts = [];
//     for (const waypoint of waypoints.value) {
//       let pos = await getLanAndLong(waypoint);
//       opts.push(new AMap.LngLat(pos));
//     }
//     way.search(origin, target, opts, (status, result) => {
//       if (status === 'complement') {
//         console.log(result.info)
//         console.log(result.routes)
//       }
//     });
//   } else {
//     way.search(origin, target, (status, result) => {
//       if (status === 'complement') {
//         console.log(result.info)
//         console.log(result.routes)
//       }
//     });
//   }
// };

// AMap.plugin("AMap.Driving", () => {
//   let drivingOptions = {
//     map: map,
//     panel: "navigation",
//     //驾车策略，包括 LEAST_TIME，LEAST_FEE, LEAST_DISTANCE,REAL_TRAFFIC
//     policy: AMap.DrivingPolicy.LEAST_TIME,
//   };
//
//   driving = new AMap.Driving(drivingOptions);
//   //根据起终点坐标规划驾车路线
// });


// const nav = ref(false) // 设置导航
// const switchNav = () => {
//   transport(recoveryPos.value[0], recoveryPos.value[1])
//   nav.value = !nav.value;
//   waypoints.value = []
//   start.value = ''
//   destination.value = ''
// }

// const addWaypoint = () => {
//   if (waypointInput.value) {
//     form.value.waypoints.push(waypointInput.value)
//     waypointInput.value = ''
//   } else {
//     ElMessage.error('请输入有效的途经点')
//   }
// }
//
// const removeWaypoint = (index) => {
//   form.value.waypoints.splice(index, 1)
// }

// // 手册案例无法跑通
// const handleSubmit = () => {
//   const points = [
//     {keyword: form.value.start, city: form.value.city},
//     ...form.value.waypoints.map(waypoint => ({keyword: waypoint, city: form.value.city})),
//     {keyword: form.value.end, city: form.value.city}
//   ]
//
//   new AMap.Driving({
//     map: map,
//     panel: "navigation",
//     //驾车策略，包括 LEAST_TIME，LEAST_FEE, LEAST_DISTANCE,REAL_TRAFFIC
//     policy: AMap.DrivingPolicy.LEAST_TIME,
//   }).search(points, (status, result) => {
//     if (status === 'complete') {
//       ElMessage.success('路线规划成功')
//       console.log(result)
//     } else if (status === 'error') {
//       ElMessage.error(`错误: ${result}`)
//     } else if (status === 'no_data') {
//       ElMessage.warning('未找到相关数据')
//     }
//   })
// }

// 导航
// const handleSubmit = async () => {
//
//   let way = new AMap.Driving({
//     map: map,
//     panel: "navigation",
//     //驾车策略，包括 LEAST_TIME，LEAST_FEE, LEAST_DISTANCE,REAL_TRAFFIC
//     policy: AMap.DrivingPolicy.LEAST_TIME,
//   })
//
//   const [origin, target] = await Promise.all([
//     getLanAndLong(form.value.start),
//     getLanAndLong(form.value.end)
//   ]);
//
//   const opts = form.value.waypoints.length > 0
//       ? await Promise.all(form.value.waypoints.map(waypoint => getLanAndLong(waypoint).then(pos => new AMap.LngLat(pos))))
//       : [];
//
//   console.log(origin)
//   console.log(target)
//   console.log(opts)
//
//   way.search(origin, target, opts, (status, result) => {
//     if (status === 'complete') {
//       ElMessage.success('路线规划成功')
//       console.log(result)
//     } else if (status === 'error') {
//       ElMessage.error(`错误: ${result}`)
//     } else if (status === 'no_data') {
//       ElMessage.warning('未找到相关数据')
//     }
//   });
// };

//点击地图添加点
// const clickMap = async e => {
//   if (click.value === false) return
//   const {lng, lat} = e.lnglat;
//   const newMarker = new AMap.Marker({
//     position: new AMap.LngLat(lng, lat),
//     anchor: 'bottom-center'
//   });
//   map.add(newMarker);
//   markers.value.push(newMarker);
//   // [{keyword: '四川大学', city: '成都市'}, {
//   //   keyword: '电子科技大学',
//   //   city: '成都市'
//   // }]
//   // driving.search(
//   //     [{keyword: '北京南站', city: '北京市'}, {keyword: '广东大厦', city: '北京市'}, {
//   //       keyword: '北京西站',
//   //       city: '北京市'
//   //     }]
//   //     , (status, result) => {
//   //       if (status === 'complete') {
//   //         ElMessage.success('路线规划成功')
//   //         console.log(result)
//   //       } else if (status === 'error') {
//   //         ElMessage.error(`错误: ${result}`)
//   //       } else if (status === 'no_data') {
//   //         ElMessage.warning('未找到相关数据')
//   //       }
//   //     })
// }


// 根据经纬度获得地址和省市区街区
// async function getGeo(lng, lat) {
//   return new Promise((resolve, reject) => {
//     geocoder.getAddress([lng, lat], (status, result) => {
//       if (status === 'complete' && result.info === 'OK') {
//         const {addressComponent, formattedAddress} = result.regeocode;
//         let {city, province, district} = addressComponent;
//         if (!city) {
//           // 直辖市
//           city = province;
//         }
//         location.value = {
//           longitude: lng,
//           latitude: lat,
//           address: formattedAddress,
//           zone: [province, city, district],
//         };
//         resolve();
//       } else {
//         reject(new Error('Failed to get address'));
//       }
//     });
//   });
// }
// const location = ref({
//   longitude: '',
//   latitude: '',
//   address: '',
//   zone: [],
// })
// const geoCodeConfig = {
//   'showButton': true,//是否显示定位按钮
//   'position': 'LB',//定位按钮的位置
//   /* LT LB RT RB */
//   'offset': [10, 20],//定位按钮距离对应角落的距离
//   'showMarker': true,//是否显示定位点
//   'markerOptions': {//自定义定位点样式，同Marker的Options
//     'content': '<img src="https://a.amap.com/jsapi_demos/static/resource/img/user.png" style="width:36px;height:36px"/>'
//   },
//   'showCircle': true,//是否显示定位精度圈
//   'circleOptions': {//定位精度圈的样式
//     'strokeColor': '#0093FF',
//     'noSelect': true,
//     'strokeOpacity': 0.5,
//     'strokeWeight': 1,
//     'fillColor': '#02B0FF',
//     'fillOpacity': 0.25
//   }
// }
// try {
//   // 使用geocoder的getLocation方法获取位置信息
//   const result =l await geocoder.getLocation(posName);
//   // 检查状态是否为complete并且信息是否为OK
//   if (result.status === "complete" && result.info === "OK") {
//     // 获取位置信息
//     const pos = result.geocodes[0].location;
//     // 解构经纬度
//     const {lng, lat} = pos;
//     // 返回经纬度数组
//     return [lng, lat];
//   } else {
//     throw new Error('Failed to get location for posName: ' + posName);
//   }
// } catch (error) {
//   // 如果发生错误，抛出错误
//   throw error;
// }
//
// // 如果有候选词列表
// let suggestions = ''
// const querySearch = (queryString, cb) => {
//   const results = queryString
//       ? suggestions.filter(queryString => {
//         return (suggestion) => {
//           return suggestion.value.toLowerCase().indexOf(queryString.toLowerCase()) === 0;
//         }
//       })
//       : suggestions;
//   // 调用callback返回建议列表的数据
//   cb(results);
// }

// //点击地图添加点
// const clickMap = async e => {
//   if (click.value === false) return
//   const {lng, lat} = e.lnglat;
//   const newMarker = new AMap.Marker({
//     position: new AMap.LngLat(lng, lat),
//     anchor: 'bottom-center'
//   });
//   map.add(newMarker);
//   markers.value.push(newMarker);
// }
//
// 逆地址处理
// const getLanAndLong = async posName => {
//
//   return new Promise((resolve, reject) => {
//     // 使用geocoder的getLocation方法获取位置信息
//     geocoder.getLocation(posName, (status, result) => {
//       // 检查状态是否为complete并且信息是否为OK
//       if (status === "complete" && result.info === "OK") {
//         // 获取位置信息
//         let pos = result.geocodes[0].location;
//         // 解构经纬度
//         let {lng, lat} = pos;
//         // 如果成功，解析成功，则使用resolve来解决Promise
//         resolve([lng, lat]);
//       } else {
//         // 如果发生错误或者没有找到结果，则使用reject来拒绝Promise
//         reject(new Error('Failed to get location for posName: ' + posName));
//       }
//     });
//
//   })
// };

// // 绘制地点marker
// const drawMarker = (longitude, latitude) => {
//   let marker = new AMap.Marker({
//     position: new AMap.LngLat(longitude, latitude),
//     anchor: 'bottom-center',
//   });
//   markers.value.push(marker);
//   // map.add(marker);
// }
</script>

<style scoped>

</style>
