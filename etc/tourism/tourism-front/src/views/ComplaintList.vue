<template>
    <div>
        <el-table :data="complaintResults" style="width: 100%">
            <el-table-column prop="content" label="投诉内容"></el-table-column>
            <el-table-column label="当前状态" align="center" prop="status">
            </el-table-column>
            <el-table-column prop="submitTime" label="处理日期" width="180"></el-table-column>
        </el-table>

    </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { listTousu } from "@/api/tousu/tousu";
import useUserStore from '@/store/modules/user'
// 使用用户存储实例
const userStore = useUserStore();
// 示例数据，可以从API获取
const complaintResults = ref([]);
onMounted (  () => {

    console.log(userStore.id)
    // 在这里可以调用API获取数据
     getList(userStore.id);
});

// 获取星级酒店列表的函数
async function getList(id) {
    complaintResults.value = await listTousu(id);
    console.log('Complaint Results:', complaintResults.value);

}
</script>

<style scoped>
.el-table {
    margin-top: 20px;
}
</style>
