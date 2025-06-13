// 引入 Axios

// 定义基础URL，根据您的后端服务地址进行修改
import myAxios from "@/plugins/myAxios.ts";

const API_BASE_URL = '/scenic';

// 获取所有景区区域
export const getAllScenicareas = () => {
    return myAxios.get(`${API_BASE_URL}/scenicArea/list`);
};

// 根据景区区域ID获取所有景点
export const getScenicspotsByScenicAreaId = (scenicAreaId) => {
    return myAxios.get(`${API_BASE_URL}/scenicSpots/list`, {
        params: { scenicAreaId }
    });
};

