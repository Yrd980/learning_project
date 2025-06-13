<template>
    <div class="app-container">
        <el-container>
            <el-header>
                <Top/>
            </el-header>
            <el-main>
                <div class="subheader">
                    <div class="left">
                        <span class="page-title">星级酒店</span>
                        <span class="page-desc">以卓越之姿，恭候您的光临。</span>
                    </div>
                </div>
                <el-form :model="queryParams" ref="queryRef" :inline="true" v-show="showSearch" label-width="68px">
                    <el-form-item label="酒店名" prop="name">
                        <el-input
                            v-model="queryParams.name"
                            placeholder="请输入酒店名"
                            clearable
                            @keyup.enter="handleQuery"
                        />
                    </el-form-item>
                    <el-form-item label="酒店星级" prop="starLevel">
                        <el-input
                            v-model="queryParams.starLevel"
                            placeholder="请输入星级"
                            clearable
                            @keyup.enter="handleQuery"
                        />
                    </el-form-item>
                    <el-form-item label="地址" prop="address">
                        <el-input
                            v-model="queryParams.address"
                            placeholder="请输入地址"
                            clearable
                            @keyup.enter="handleQuery"
                        />
                    </el-form-item>
                    <el-form-item>
                        <el-button type="primary" icon="Search" @click="handleQuery">搜索</el-button>
                        <el-button icon="Refresh" @click="resetQuery">重置</el-button>
                    </el-form-item>
                </el-form>

                <el-row :gutter="20" class="hotel-cards">
                    <el-col :span="8" v-for="hotel in starhotelsList" :key="hotel.id">
                        <el-card class="hotel-card" @click="goToHotelDetail(hotel.id)">
                            <img :src="hotel.imageUrl" class="hotel-image" />
                            <div class="hotel-info">
                                <h3>{{ hotel.name }}</h3>
                                <p>星级: {{ hotel.starLevel }}</p>
                                <p>地址: {{ hotel.address }}</p>
                                <p>￥ <span class="price">{{ hotel.minPrice }}</span> 起</p>
                            </div>
                        </el-card>
                    </el-col>
                </el-row>
                <pagination
                    v-show="total>0"
                    :total="total"
                    v-model:page="queryParams.pageNum"
                    v-model:limit="queryParams.pageSize"
                    @pagination="getList"
                />
            </el-main>
        </el-container>
    </div>
</template>
<style scoped>
@import "@/assets/styles/css/style.css";
.hotel-cards {
    margin-top: 20px;
}
.hotel-card {
    cursor: pointer;
    transition: transform 0.3s;
}
.hotel-card:hover {
    transform: scale(1.05);
}
.hotel-image {
    width: 100%;
    height: 200px;
    object-fit: cover;
}
.hotel-info {
    padding: 15px;
}
.price {
    color: #409EFF;
    font-weight: bold;
    font-size: 30px;
}
</style>

<script setup name="Starhotels">
import { ref, reactive, toRefs, getCurrentInstance } from 'vue';
import { listStarhotels } from "@/api/hotel/starhotels";
import Top from "@/components/Top.vue";

// 获取当前组件实例的代理对象
const { proxy } = getCurrentInstance();

// 定义星级酒店列表
const starhotelsList = ref([]);  // 存储酒店列表
const open = ref(false);  // 控制搜索面板的展开与收起
const loading = ref(true);  // 控制加载状态
const showSearch = ref(true);  // 控制搜索面板的显示与隐藏
const ids = ref([]);  // 存储选中的酒店ID
const total = ref(0);  // 总条目数
const title = ref("");  // 搜索标题

// 定义表单数据和校验规则
const data = reactive({
    form: {},  // 表单数据
    queryParams: {  // 查询参数
        pageNum: 1,
        pageSize: 9,
        name: null,  // 酒店名称
        starLevel: null,  // 酒店星级
        address: null  // 酒店地址
    },
    rules: {  // 表单校验规则
        name: [
            { required: true, message: "星级酒店名不能为空", trigger: "blur" }
        ],
        starLevel: [
            { required: true, message: "酒店星级不能为空", trigger: "blur" }
        ],
        totalQuantity: [
            { required: true, message: "总销量不能为空", trigger: "blur" }
        ],
        address: [
            { required: true, message: "地址不能为空", trigger: "blur" }
        ]
    }
});

const { queryParams, form, rules } = toRefs(data);  // 将 reactive 数据转换为 refs

// 获取星级酒店列表的函数
function getList() {
    loading.value = true;  // 设置加载状态
    listStarhotels(queryParams.value).then(response => {
        starhotelsList.value = response.rows;  // 将返回的数据赋值给 starhotelsList
        total.value = response.total;  // 设置总条目数
        loading.value = false;  // 取消加载状态
        console.log('Star Hotels List:', starhotelsList.value);
    });
}

// 处理查询的函数
function handleQuery() {
    queryParams.value.pageNum = 1;  // 查询时重置页码为 1
    getList();  // 调用获取列表函数
}

// 重置查询参数的函数
function resetQuery() {
    proxy.resetForm("queryRef");  // 重置表单
    handleQuery();  // 重新查询
}

// 跳转到酒店详情页面的函数
function goToHotelDetail(hotelId) {
    // 检查 hotelId 是否有效
    if (hotelId !== undefined && hotelId !== null) {
        // 将 hotelId 传递给路由，跳转到详情页面
        proxy.$router.push(`/guest/starhotels/details/${hotelId}`);
    } else {
        // 处理 hotelId 未定义的情况，可以给出提示或采取其他操作
        console.error('Hotel ID is undefined or null');
    }
}

// 组件挂载时获取星级酒店列表
getList();
</script>


