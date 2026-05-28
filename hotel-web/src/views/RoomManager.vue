<template>
  <div class="page-enter">
    <div class="page-header">
      <h1 class="page-title">房间管理</h1>
      <div style="display: flex; gap: 12px">
        <el-input v-model="searchKey" placeholder="搜索房间号..." prefix-icon="Search" clearable style="width: 200px" />
        <el-button type="primary" @click="openAddDialog">+ 新增房间</el-button>
      </div>
    </div>

    <!-- 图例 -->
    <div class="legend-bar">
      <span class="legend-item"><span class="dot" style="background: #67c23a"></span> 空闲</span>
      <span class="legend-item"><span class="dot" style="background: #e6a23c"></span> 已预订</span>
      <span class="legend-item"><span class="dot" style="background: #409eff"></span> 已入住</span>
      <span class="legend-item"><span class="dot" style="background: #f56c6c"></span> 清洁中</span>
      <span style="flex:1"></span>
      <span style="font-size:13px;color:var(--text-secondary)">共 {{ filteredRooms.length }} 间</span>
    </div>

    <!-- 房间网格 -->
    <div class="room-grid">
      <div v-for="room in filteredRooms" :key="room.id" class="room-card" :class="'status-' + room.status" @click="openRoomDetail(room)">
        <div class="room-number">{{ room.room_number }}</div>
        <div class="room-type">{{ room.type }}</div>
        <div class="room-price">¥{{ room.price }}</div>
        <div class="room-status-tag">{{ statusText(room.status) }}</div>
      </div>
    </div>

    <!-- 新增/编辑对话框 -->
    <el-dialog v-model="dialogVisible" :title="isEdit ? '编辑房间' : '新增房间'" width="400px">
      <el-form :model="form" label-width="80px">
        <el-form-item label="房间号"><el-input v-model="form.room_number" :disabled="isEdit" /></el-form-item>
        <el-form-item label="房型">
          <el-select v-model="form.type" style="width:100%">
            <el-option label="标准间" value="标准间" /><el-option label="大床房" value="大床房" /><el-option label="双床房" value="双床房" />
            <el-option label="商务套房" value="商务套房" /><el-option label="豪华套房" value="豪华套房" /><el-option label="总统套房" value="总统套房" />
            <el-option label="亲子房" value="亲子房" /><el-option label="爱情房间" value="爱情房间" /><el-option label="小床房" value="小床房" />
          </el-select>
        </el-form-item>
        <el-form-item label="价格"><el-input-number v-model="form.price" :min="50" :max="9999" style="width:100%" /></el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="handleSave">保存</el-button>
      </template>
    </el-dialog>

    <!-- 房间详情弹窗 -->
    <el-dialog v-model="detailVisible" title="房间详情" width="420px">
      <div v-if="selectedRoom" class="room-detail">
        <div class="detail-row"><span class="detail-label">房间号</span><span class="detail-value">{{ selectedRoom.room_number }}</span></div>
        <div class="detail-row"><span class="detail-label">房型</span><span class="detail-value">{{ selectedRoom.type }}</span></div>
        <div class="detail-row"><span class="detail-label">价格</span><span class="detail-value">¥{{ selectedRoom.price }}/晚</span></div>
        <div class="detail-row"><span class="detail-label">状态</span><el-tag :type="statusType(selectedRoom.status)" size="small">{{ statusText(selectedRoom.status) }}</el-tag></div>
      </div>
      <template #footer>
        <el-button @click="detailVisible = false">关闭</el-button>
        <el-button v-if="selectedRoom?.status === 0" type="success" @click="quickBook">预订</el-button>
        <el-button @click="editFromDetail">编辑</el-button>
        <el-button type="danger" @click="handleDelete(selectedRoom?.id)">删除</el-button>
      </template>
    </el-dialog>

    <!-- 快捷预订弹窗 -->
    <el-dialog v-model="bookVisible" title="快捷预订" width="380px">
      <el-form :model="bookForm" label-width="90px">
        <el-form-item label="房间"><el-input :model-value="'#' + bookForm.room_number + ' ' + bookForm.room_type" disabled /></el-form-item>
        <el-form-item label="客人姓名"><el-input v-model="bookForm.guest_name" /></el-form-item>
        <el-form-item label="手机号"><el-input v-model="bookForm.phone" /></el-form-item>
        <el-form-item label="入住时间"><el-date-picker v-model="bookForm.check_in" type="datetime" placeholder="默认现在" style="width:100%" value-format="YYYY-MM-DD HH:mm:ss" /></el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="bookVisible = false">取消</el-button>
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
const searchKey = ref('')
const dialogVisible = ref(false)
const isEdit = ref(false)
const form = ref({ room_number: '', type: '大床房', price: 100 })
const detailVisible = ref(false)
const selectedRoom = ref(null)
const bookVisible = ref(false)
const bookLoading = ref(false)
const bookForm = ref({ room_number: '', room_type: '', guest_name: '', phone: '', check_in: '' })

const nowStr = () => {
  const d = new Date()
  return `${d.getFullYear()}-${String(d.getMonth()+1).padStart(2,'0')}-${String(d.getDate()).padStart(2,'0')} ${String(d.getHours()).padStart(2,'0')}:${String(d.getMinutes()).padStart(2,'0')}:${String(d.getSeconds()).padStart(2,'0')}`
}
const statusText = (s) => ({ 0: '空闲', 1: '已预订', 2: '已入住', 3: '清洁中' }[s] || '未知')
const statusType = (s) => ({ 0: 'success', 1: 'warning', 2: 'primary', 3: 'danger' }[s] || 'info')
const statusOrder = { 0: 0, 3: 1, 1: 2, 2: 3 }
const sortedRooms = computed(() => [...rooms.value].sort((a, b) => (statusOrder[a.status] ?? 9) - (statusOrder[b.status] ?? 9)))
const filteredRooms = computed(() => {
  if (!searchKey.value) return sortedRooms.value
  return sortedRooms.value.filter(r => String(r.room_number).includes(searchKey.value))
})

const fetchRooms = async () => { rooms.value = await request.get('/rooms/allRoom') }

const openAddDialog = () => {
  isEdit.value = false; form.value = { room_number: '', type: '大床房', price: 100 }; dialogVisible.value = true
}
const openRoomDetail = (room) => { selectedRoom.value = room; detailVisible.value = true }
const editFromDetail = () => {
  if (!selectedRoom.value) return; form.value = { ...selectedRoom.value }; isEdit.value = true; detailVisible.value = false; dialogVisible.value = true
}
const quickBook = () => {
  const room = selectedRoom.value; if (!room) return
  bookForm.value = { room_number: room.room_number, room_type: room.type, guest_name: '', phone: '', check_in: '' }
  bookVisible.value = true; detailVisible.value = false
}

const handleBook = async () => {
  if (!bookForm.value.guest_name) { ElMessage.warning('请填写客人姓名'); return }
  bookLoading.value = true
  try {
    const params = {
      room_number: bookForm.value.room_number, guest_name: bookForm.value.guest_name,
      phone: bookForm.value.phone || '待补充', check_in_date: bookForm.value.check_in || nowStr(),
    }
    const res = await request.post('/assign/book', null, { params })
    if (res.code === 200) { ElMessage.success(res.msg); bookVisible.value = false; fetchRooms() } else { ElMessage.error(res.msg) }
  } catch (e) { if (!e.response?.data) ElMessage.error('预订失败')
  } finally { bookLoading.value = false }
}

const handleSave = async () => {
  if (isEdit.value) { await request.put(`/rooms/update?room_id=${form.value.id}`, form.value); ElMessage.success('修改成功') }
  else { await request.post('/rooms/insertRoom', form.value); ElMessage.success('新增成功') }
  dialogVisible.value = false; fetchRooms()
}

const handleDelete = async (id) => {
  await ElMessageBox.confirm('确定删除该房间吗？')
  await request.delete(`/rooms/delete?id=${id}`)
  ElMessage.success('删除成功'); detailVisible.value = false; fetchRooms()
}

onMounted(fetchRooms)
</script>

<style scoped>
.legend-bar {
  display: flex; align-items: center; gap: 20px;
  padding: 12px 16px;
  background: var(--bg-card);
  border-radius: var(--radius-sm);
  border: 1px solid var(--border-color);
  margin-bottom: 20px;
}
.legend-item { display: flex; align-items: center; gap: 6px; font-size: 13px; color: var(--text-secondary); }
.dot { width: 10px; height: 10px; border-radius: 50%; display: inline-block; }

.room-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
  gap: 14px;
}

.room-card {
  background: var(--bg-card);
  border-radius: var(--radius);
  padding: 16px;
  text-align: center;
  cursor: pointer;
  border: 1px solid var(--border-color);
  transition: all 0.25s ease;
  position: relative;
  overflow: hidden;
}
.room-card:hover { transform: translateY(-4px); box-shadow: var(--shadow-md); }
.room-card::before {
  content: ''; position: absolute; top: 0; left: 0; right: 0; height: 4px;
}
.room-card.status-0::before { background: #67c23a; }
.room-card.status-1::before { background: #e6a23c; }
.room-card.status-2::before { background: #409eff; }
.room-card.status-3::before { background: #f56c6c; }

.room-number { font-size: 22px; font-weight: 700; color: var(--text-primary); margin-top: 4px; }
.room-type { font-size: 13px; color: var(--text-secondary); margin: 4px 0 2px; }
.room-price { font-size: 14px; color: var(--accent); font-weight: 600; }
.room-status-tag {
  display: inline-block; font-size: 11px; padding: 2px 10px; border-radius: 10px; margin-top: 6px;
}
.status-0 .room-status-tag { background: #e1f3d8; color: #67c23a; }
.status-1 .room-status-tag { background: #faecd8; color: #e6a23c; }
.status-2 .room-status-tag { background: #d9ecff; color: #409eff; }
.status-3 .room-status-tag { background: #fde2e2; color: #f56c6c; }

.room-detail { padding: 8px 0; }
.detail-row { display: flex; padding: 10px 0; border-bottom: 1px solid var(--border-color); }
.detail-row:last-child { border-bottom: none; }
.detail-label { width: 80px; color: var(--text-secondary); font-size: 14px; }
.detail-value { flex: 1; font-size: 14px; color: var(--text-primary); font-weight: 500; }
</style>
