<template>
  <div>
    <div class="page-header">
      <h2 class="page-title">🛏️ 房间管理</h2>
      <el-button type="primary" @click="openAddDialog">+ 新增房间</el-button>
    </div>

    <el-table :data="sortedRooms" border stripe style="width: 100%">
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
      <el-table-column label="操作" min-width="200">
        <template #default="{ row }">
          <el-button v-if="row.status === 0" size="small" type="success" @click="openBookDialog(row)">预订</el-button>
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

    <!-- 预订对话框 -->
    <el-dialog v-model="bookDialogVisible" title="预订房间" width="400px">
      <el-form :model="bookForm" label-width="100px">
        <el-form-item label="房间号">
          <el-input v-model="bookForm.room_number" disabled />
        </el-form-item>
        <el-form-item label="房型">
          <el-input :model-value="bookForm.room_type" disabled />
        </el-form-item>
        <el-form-item label="客人姓名">
          <el-input v-model="bookForm.guest_name" placeholder="请输入" />
        </el-form-item>
        <el-form-item label="手机号">
          <el-input v-model="bookForm.phone" placeholder="选填" />
        </el-form-item>
        <el-form-item label="入住日期">
          <div style="display: flex; gap: 6px; width: 100%">
            <el-date-picker v-model="bookForm.check_in" type="datetime" placeholder="选填（默认现在）" style="flex: 1" value-format="YYYY-MM-DD HH:mm:ss" />
            <el-button size="small" @click="bookForm.check_in = nowStr()">Now</el-button>
          </div>
        </el-form-item>
        <el-form-item label="退房日期" v-if="bookForm.check_in">
          <el-date-picker v-model="bookForm.check_out" type="datetime" placeholder="可选，默认+1天" style="width: 100%" value-format="YYYY-MM-DD HH:mm:ss" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="bookDialogVisible = false">取消</el-button>
        <el-button type="primary" :loading="bookLoading" @click="handleBook">确认预订</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import request from '@/api/index.js'

const rooms = ref([])
const dialogVisible = ref(false)
const isEdit = ref(false)
const form = ref({ room_number: '', type: '大床房', price: 100 })
const bookDialogVisible = ref(false)
const bookLoading = ref(false)
const bookForm = ref({ room_number: '', room_type: '', guest_name: '', phone: '', check_in: '', check_out: '' })

const nowStr = () => {
  const d = new Date()
  const pad = (n) => String(n).padStart(2, '0')
  return `${d.getFullYear()}-${pad(d.getMonth()+1)}-${pad(d.getDate())} ${pad(d.getHours())}:${pad(d.getMinutes())}:${pad(d.getSeconds())}`
}

const statusText = (s) => ({ 0: '空闲', 1: '已预订', 2: '已入住', 3: '清洁中' }[s] || '未知')
const statusType = (s) => ({ 0: 'success', 1: 'warning', 2: 'primary', 3: 'danger' }[s] || 'info')

// 按状态排序：空闲(0) → 清洁中(3) → 已预订(1) → 已入住(2)
const statusOrder = { 0: 0, 3: 1, 1: 2, 2: 3 }
const sortedRooms = computed(() => {
  return [...rooms.value].sort((a, b) => (statusOrder[a.status] ?? 9) - (statusOrder[b.status] ?? 9))
})

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

const openBookDialog = (row) => {
  bookForm.value = {
    room_number: row.room_number,
    room_type: row.type,
    guest_name: '',
    phone: '',
    check_in: '',
    check_out: '',
  }
  bookDialogVisible.value = true
}

const handleBook = async () => {
  if (!bookForm.value.guest_name) {
    ElMessage.warning('请填写客人姓名')
    return
  }
  bookLoading.value = true
  try {
    const params = {
      room_number: bookForm.value.room_number,
      guest_name: bookForm.value.guest_name,
      phone: bookForm.value.phone || '待补充',
      check_in_date: bookForm.value.check_in || nowStr(),
    }
    if (bookForm.value.check_out) params.check_out_date = bookForm.value.check_out
    const res = await request.post('/assign/book', null, { params })
    if (res.code === 200) {
      ElMessage.success(`🎉 ${res.msg}`)
      bookDialogVisible.value = false
      fetchRooms()
    } else {
      ElMessage.error(res.msg)
    }
  } catch (e) {
    if (!e.response?.data) ElMessage.error('预订失败')
  } finally {
    bookLoading.value = false
  }
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
