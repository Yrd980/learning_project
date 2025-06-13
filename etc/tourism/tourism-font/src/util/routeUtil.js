import {lazyAMapApiLoaderInstance, useCitySearch, useGeolocation, useWeather} from "@vuemap/vue-amap";
import myAxios from "@/plugins/myAxios.ts";
import mapConfig from "@/config/mapConfig.js";

// 获取天气 需要传入市 如南京市
async function getWeather(pos) {
    await lazyAMapApiLoaderInstance;
    const res = await useWeather();
    const {getLive, getForecast} = res;
    const liveResult = await getLive(pos);
    const forecastResult = await getForecast(pos);
    return [liveResult, forecastResult];
}

function getCity() {
    lazyAMapApiLoaderInstance.then(() => {
        useCitySearch().then(res => {
            const {getLocalCity} = res;
            getLocalCity().then(cityResult => {
                center.value = cityResult.bounds.getCenter().toArray()
                console.log('cityResult: ', cityResult)
                return cityResult;
            })
        })
    })
}

function getGeolocation() {
    lazyAMapApiLoaderInstance.then(() => {
        useGeolocation({
            enableHighAccuracy: true,
            needAddress: true
        }).then(res => {
            const {getCurrentPosition, getCityInfo} = res;
            getCurrentPosition().then(currentPosition => {
                center.value = currentPosition.position.toArray();
                console.log('currentPosition: ', currentPosition)
            });
            getCityInfo().then(cityResult => {
                console.log('cityResult: ', cityResult)
            })
        })

    })
}

const keyService = mapConfig.key_service

const skyUrl = "/pos/geocoder";

//获取经纬度
const getLocation = async (address) => {
    const apiKey = mapConfig.key_sky; // 替换为您的API密钥
    const ds = JSON.stringify({keyWord: address});
    const url = `${skyUrl}?ds=${ds}&tk=${apiKey}`;

    try {
        const response = await myAxios.get(url);
        console.log(response)
        if (response.status !== "0") {
            throw new Error(`API error! status: ${response.data.status}, msg:${response.data.msg}`);
        }
        return [response.location.lon, response.location.lat];
    } catch (error) {
        console.error("Failed to get location:", error);
        return null; // 或者抛出错误，取决于你的错误处理策略
    }
};

//地图
const url = `/map/v3/geocode/regeo` //防止跨域

async function getPosition(lng, lat) {
    const location = `${lng},${lat}`;
    const params = {
        key: keyService,
        location
    };

    try {
        const res = await myAxios.get(url, {params});
        if (res.status === '1' && res.info === 'OK') {
            const {addressComponent, formatted_address} = res.regeocode;
            const {province, district} = addressComponent;
            let city = addressComponent.city;

            if (city.length === 0) {
                city = province;
            } else if (Array.isArray(city)) {
                city = city[0];
            }

            return {
                address: formatted_address,
                province,
                city,
                district,
            };
        }
    } catch (error) {
        console.error('Error fetching position:', error);
        throw error;
    }
}

function isValidLatitude(latitude) {
    return latitude >= -90 && latitude <= 90;
}

function isValidLongitude(longitude) {
    return longitude >= -180 && longitude <= 180;
}

function getLocByPoi(poiInfo) {
    if (poiInfo) {
        let tmp = poiInfo.entr_location.pos[0];
        let lng
        let lat
        if (isValidLongitude(tmp)) {
            lng = tmp;
            lat = poiInfo.entr_location.pos[1];
        } else {
            lng = poiInfo.location.lng
            lat = poiInfo.location.lat
        }
        return [lng, lat];
    }
}


export default {
    getWeather, getCity, getGeolocation, getPosition, isValidLongitude,
    getLocByPoi, getLocation
}

