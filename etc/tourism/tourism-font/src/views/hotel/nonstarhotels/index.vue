<template>
    <div class="app-container">
        <el-container>
            <el-header>
                <Top/>
            </el-header>
            <el-main>
                <div class="subheader">
                    <div class="left">
                        <span class="page-title">度假村民宿</span>
                        <span class="page-desc">民宿寄情，乡野间，绿意盎然。</span>
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
                    <el-col :span="8" v-for="hotel in nonStarhotelsList" :key="hotel.id">
                        <el-card class="hotel-card" @click="goToHotelDetail(hotel.id)">
                            <img :src="hotel.imageUrl" class="hotel-image" />
                            <div class="hotel-info">
                                <h3>{{ hotel.name }}</h3>
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

<script setup name="NonStarhotels">
import {getCurrentInstance, reactive, ref, toRefs} from 'vue';
import {listNonstarhotels,} from "@/api/hotel/nonstarhotels";
import Top from "@/components/Top.vue";

const { proxy } = getCurrentInstance();

const nonStarhotelsList = ref([]);
const open = ref(false);
const loading = ref(true);
const showSearch = ref(true);
const ids = ref([]);
const total = ref(0);
const title = ref("");

const data = reactive({
    form: {},
    queryParams: {
        pageNum: 1,
        pageSize: 9,
        name: null,
        rating: null,
        address: null
    },
    rules: {
        name: [
            { required: true, message: "酒店名不能为空", trigger: "blur" }
        ],
        totalQuantity: [
            { required: true, message: "总销量不能为空", trigger: "blur" }
        ],
        address: [
            { required: true, message: "地址不能为空", trigger: "blur" }
        ]
    }
});

const { queryParams, form, rules } = toRefs(data);

function getList() {
    loading.value = true;
    console.log(111111111)
    listNonstarhotels(queryParams.value).then(response => {
        nonStarhotelsList.value = response.rows;
        total.value = response.total;
        loading.value = false;
    });
}

function handleQuery() {
    queryParams.value.pageNum = 1;
    getList();
}

function resetQuery() {
    proxy.resetForm("queryRef");
    handleQuery();
}

function handleSelectionChange(selection) {
    ids.value = selection.map(item => item.id);
}



function goToHotelDetail(hotelId) {
    // 检查 hotelId 是否有效
    if (hotelId !== undefined && hotelId !== null) {
        // 将 hotelId 转换为 Long 类型，或者直接发送给后端
        proxy.$router.push(`/guest/nonstarhotels/details/${hotelId}`);
    } else {
        // 处理 hotelId 未定义的情况，可以给出提示或采取其他操作
        console.error('Hotel ID is undefined or null');
    }
}

getList();
</script>


