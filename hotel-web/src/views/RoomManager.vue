<template>
  <div>
    <div class="page-header">
      <h2 class="page-title">🛏️ 房间管理</h2>
      <el-button type="primary" @click="openAddDialog">+ 新增房间</el-button>
    </div>

    <el-table :data="rooms" border stripe style="width: 100%">
      <el-table-column prop="id" label="ID" width="60" />
      <el-table-column prop="room_number" label="房间号" width="120" />
      <el-table-column prop="type" label="房型" width="150" />
      <el-table-column prop="price" label="价格 (¥/晚)" width="120">
        <template #default="{ row }">
          ¥{{ row.price }}
        </template>
      </el-table-column>
      <el-table-column prop="status" label="状态" width="120">
        <template #default="{ row }">
          <el-tag :type="statusType(row.status)" size="small">
            {{ statusText(row.status) }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column label="操作" min-width="160">
        <template #default="{ row }">
          <el-button size="small" @click="openEditDialog(row)">编辑</el-button>
          <el-button size="small" type="danger" @click="handleDelete(row.id)">删除</el-button>
        </template>
      </el-table-column>
    </el-table>

    <!-- 新增/编辑对话框 -->
    <el-dialog v-model="dialogVisible" :title="isEdit ? '编辑房间' : '新增房间'" width="400px">
      <el-form :model="form" label-width="100px">
        <el-form-item label="房间号">
          <el-input v-model="form.room_number" :disabled="isEdit" />
        </el-form-item>
        <el-form-item label="房型">
          <el-select v-model="form.type" style="width: 100%">
            <el-option label="大床房" value="大床房" />
            <el-option label="双床房" value="双床房" />
            <el-option label="商务套房" value="商务套房" />
            <el-option label="豪华套房" value="豪华套房" />
            <el-option label="总统套房" value="总统套房" />
          </el-select>
        </el-form-item>
        <el-form-item label="价格">
          <el-input-number v-model="form.price" :min="50" :max="9999" style="width: 100%" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="handleSave">保存</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import request from '@/api/index.js'

const rooms = ref([])
const dialogVisible = ref(false)
const isEdit = ref(false)
const form = ref({ room_number: '', type: '大床房', price: 100 })

const statusText = (s) => ({ 0: '空闲', 1: '已预订', 2: '已入住', 3: '清洁中' }[s] || '未知')
const statusType = (s) => ({ 0: 'success', 1: 'warning', 2: 'primary', 3: 'danger' }[s] || 'info')

const fetchRooms = async () => {
  rooms.value = await request.get('/rooms/allRoom')
}

const openAddDialog = () => {
  isEdit.value = false
  form.value = { room_number: '', type: '大床房', price: 100 }
  dialogVisible.value = true
}

const openEditDialog = (row) => {
  isEdit.value = true
  form.value = { ...row }
  dialogVisible.value = true
}

const handleSave = async () => {
  if (isEdit.value) {
    await request.put(`/rooms/update?room_id=${form.value.id}`, form.value)
    ElMessage.success('修改成功')
  } else {
    await request.post('/rooms/insertRoom', form.value)
    ElMessage.success('新增成功')
  }
  dialogVisible.value = false
  fetchRooms()
}

const handleDelete = async (id) => {
  await ElMessageBox.confirm('确定删除该房间吗？')
  await request.delete(`/rooms/delete?id=${id}`)
  ElMessage.success('删除成功')
  fetchRooms()
}

onMounted(fetchRooms)
</script>

<style scoped>
.page-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px; }
.page-title { font-size: 22px; margin: 0; }
</style>
