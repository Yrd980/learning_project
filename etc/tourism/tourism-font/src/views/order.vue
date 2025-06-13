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
                <span class="page-title">我的订单</span>
                <span class="page-desc">订单列表</span>
              </div>
            </div>
            <div>
              <el-table :data="bookingOrderDataView" height="250" style="width: 100%" stripe>
                <el-table-column label="酒店名称" align="center" prop="hotelName" />
                <el-table-column label="房型名称" align="center" prop="roomTypeName" />
                <el-table-column label="联系方式" align="center" prop="contactNumber" />
                <el-table-column label="是否确认" align="center">
                  <template #default="scope">
                    <span>{{ scope.row.recorded === 1 ? '已确认' : '未确认' }}</span>
                  </template>
                </el-table-column>

                <el-table-column label="开房时间" align="center" prop="checkInTime" width="180">

                </el-table-column>
                <el-table-column label="退房时间" align="center" prop="checkOutTime" width="180">

                </el-table-column>
                <el-table-column label="住客姓名" align="center" prop="guestName" />
              </el-table>
            </div>
          </div>
        </div>
        <Footer/>
      </el-main>
    </el-container>
  </div>
</template>

<script setup >
import { reactive , ref ,toRefs} from 'vue';
import useUserStore from '@/store/modules/user';
import Footer from "@/components/Footer.vue";
import Top from "@/components/Top.vue";
import {listbookings} from "@/api/hotel/hotelbooking.js"
const data = reactive({
  form: {},
  queryParams: {
    pageNum: 1,
    pageSize: 10,
    hotelName: null,
    roomTypeName: null,
    guestId: null,
    recorded: null,
    guestName: null,
  }
});
const userStore = useUserStore();
const loading = ref(true);
const total = ref(0);
const bookingOrderData =ref([]);
const bookingOrderDataView =ref([]);
const { queryParams, form} = toRefs(data);
function getList() {
  loading.value = true;
  listbookings(queryParams.value).then(response => {
    bookingOrderData.value = response.rows;
    bookingOrderDataView.value = response.rows.filter(item => item.guestId === userStore.id);
    total.value = response.total;
    loading.value = false;
    if(userStore.id === 1){
      bookingOrderDataView.value = bookingOrderData.value;
    }
  });
}
getList();
</script>

<style scoped>
@import "@/assets/styles/css/style.css";
</style>
