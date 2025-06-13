import getPosition from '../util/routeUtil.js';
// 定义测试用的经纬度
const testLng = 121.4737;
const testLat = 31.2304;

// 调用getPosition函数并处理结果
getPosition(testLng, testLat)
    .then(data => {
        console.log('Position data:', data);
        // 在这里可以添加更多的断言来验证数据
    })
    .catch(error => {
        console.error('Error getting position:', error);
    });
