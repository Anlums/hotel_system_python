<template>
  <div class="page-enter">
    <div class="page-header">
      <h1 class="page-title">尊邸行宫 · 舆图</h1>
      <div style="display:flex;gap:12px">
        <el-input v-model="searchKey" placeholder="搜索房号..." clearable style="width:180px" />
        <el-button type="primary" @click="openAddDialog">+ 新增</el-button>
      </div>
    </div>

    <!-- 图例 -->
    <div class="legend-bar">
      <span class="legend-item"><span class="gem" style="background:#D6E4D3"></span> 空闲</span>
      <span class="legend-item"><span class="gem" style="background:#D2E0EC"></span> 已预订</span>
      <span class="legend-item"><span class="gem" style="background:var(--gold)"></span> 已入住</span>
      <span class="legend-item"><span class="gem" style="background:#F3E3CE"></span> 清洁中</span>
      <span style="flex:1"></span>
      <span style="font-size:12px;color:var(--text-muted)">共 {{ filteredRooms.length }} 间</span>
    </div>

    <!-- 房间网格 -->
    <div class="room-grid">
      <div v-for="room in filteredRooms" :key="room.id" class="room-card" :class="'status-' + room.status" @click="openRoomDetail(room)">
        <div class="status-glow breathe"></div>
        <div class="room-number">{{ room.room_number }}</div>
        <div class="room-type">{{ room.type }}</div>
        <div class="room-price">¥{{ room.price }}</div>
        <div class="room-badge">{{ statusText(room.status) }}</div>
      </div>
    </div>

    <el-dialog v-model="dialogVisible" :title="isEdit ? '编辑房间' : '新增房间'" width="400px">
      <el-form :model="form" label-width="70px">
        <el-form-item label="房号"><el-input v-model="form.room_number" :disabled="isEdit" /></el-form-item>
        <el-form-item label="房型"><el-select v-model="form.type" style="width:100%">
          <el-option label="标准间" value="标准间" /><el-option label="大床房" value="大床房" /><el-option label="双床房" value="双床房" />
          <el-option label="商务套房" value="商务套房" /><el-option label="豪华套房" value="豪华套房" /><el-option label="总统套房" value="总统套房" />
          <el-option label="亲子房" value="亲子房" /><el-option label="爱情房间" value="爱情房间" /><el-option label="小床房" value="小床房" />
        </el-select></el-form-item>
        <el-form-item label="价格"><el-input-number v-model="form.price" :min="50" :max="9999" style="width:100%" /></el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="dialogVisible=false">取消</el-button>
        <el-button type="primary" @click="handleSave">保存</el-button>
      </template>
    </el-dialog>

    <el-dialog v-model="detailVisible" title="房间详情" width="400px">
      <div v-if="selectedRoom" class="detail-wrap" :class="'detail-' + selectedRoom.status">
        <div class="detail-header">
          <span class="detail-room-number">{{ selectedRoom.room_number }}</span>
          <span class="detail-badge">{{ statusText(selectedRoom.status) }}</span>
        </div>
        <div class="detail-body">
          <div class="detail-row"><span>房型</span><span>{{ selectedRoom.type }}</span></div>
          <div class="detail-row"><span>价格</span><span>¥{{ selectedRoom.price }}/晚</span></div>
        </div>
      </div>
      <template #footer>
        <el-button @click="detailVisible=false">关闭</el-button>
        <el-button v-if="selectedRoom?.status===0" type="primary" @click="quickBook">预订</el-button>
        <el-button @click="editFromDetail">编辑</el-button>
        <el-button style="color:var(--burgundy);border-color:rgba(139,26,26,0.3)" @click="handleDelete(selectedRoom?.id)">删除</el-button>
      </template>
    </el-dialog>

    <el-dialog v-model="bookVisible" title="快捷预订" width="380px">
      <el-form :model="bookForm" label-width="80px">
        <el-form-item label="房间"><el-input :model-value="'#'+bookForm.room_number+' '+bookForm.room_type" disabled /></el-form-item>
        <el-form-item label="客人"><el-input v-model="bookForm.guest_name" /></el-form-item>
        <el-form-item label="手机"><el-input v-model="bookForm.phone" /></el-form-item>
        <el-form-item label="入住"><el-date-picker v-model="bookForm.check_in" type="datetime" placeholder="默认现在" style="width:100%" value-format="YYYY-MM-DD HH:mm:ss" /></el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="bookVisible=false">取消</el-button>
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

const nowStr = () => { const d=new Date(); return `${d.getFullYear()}-${String(d.getMonth()+1).padStart(2,'0')}-${String(d.getDate()).padStart(2,'0')} ${String(d.getHours()).padStart(2,'0')}:${String(d.getMinutes()).padStart(2,'0')}:${String(d.getSeconds()).padStart(2,'0')}` }
const statusText = (s) => ({ 0: '空闲', 1: '已预订', 2: '已入住', 3: '清洁中' }[s] || '未知')
const statusOrder = { 0: 0, 3: 1, 1: 2, 2: 3 }
const sortedRooms = computed(() => [...rooms.value].sort((a,b) => (statusOrder[a.status]??9) - (statusOrder[b.status]??9)))
const filteredRooms = computed(() => { if (!searchKey.value) return sortedRooms.value; return sortedRooms.value.filter(r => String(r.room_number).includes(searchKey.value)) })

const fetchRooms = async () => { rooms.value = await request.get('/rooms/allRoom') }
const openAddDialog = () => { isEdit.value=false; form.value={room_number:'',type:'大床房',price:100}; dialogVisible.value=true }
const openRoomDetail = (room) => { selectedRoom.value=room; detailVisible.value=true }
const editFromDetail = () => { if (!selectedRoom.value) return; form.value={...selectedRoom.value}; isEdit.value=true; detailVisible.value=false; dialogVisible.value=true }
const quickBook = () => { const r=selectedRoom.value; if(!r) return; bookForm.value={room_number:r.room_number,room_type:r.type,guest_name:'',phone:'',check_in:''}; bookVisible.value=true; detailVisible.value=false }

const handleBook = async () => {
  if (!bookForm.value.guest_name) { ElMessage.warning('请填写客人姓名'); return }
  bookLoading.value=true
  try {
    const params={room_number:bookForm.value.room_number,guest_name:bookForm.value.guest_name,phone:bookForm.value.phone||'待补充',check_in_date:bookForm.value.check_in||nowStr()}
    const res=await request.post('/assign/book',null,{params})
    if (res.code===200) { ElMessage.success(res.msg); bookVisible.value=false; fetchRooms() } else ElMessage.error(res.msg)
  } catch(e) { if(!e.response?.data) ElMessage.error('预订失败') } finally { bookLoading.value=false }
}

const handleSave = async () => {
  if (isEdit.value) { await request.put(`/rooms/update?room_id=${form.value.id}`,form.value); ElMessage.success('修改成功') }
  else { await request.post('/rooms/insertRoom',form.value); ElMessage.success('新增成功') }
  dialogVisible.value=false; fetchRooms()
}

const handleDelete = async (id) => {
  await ElMessageBox.confirm('确定删除该房间吗？')
  await request.delete(`/rooms/delete?id=${id}`)
  ElMessage.success('删除成功'); detailVisible.value=false; fetchRooms()
}

onMounted(fetchRooms)
</script>

<style scoped>
.legend-bar {
  display: flex; align-items: center; gap: 20px;
  padding: 12px 20px;
  background: var(--bg-card);
  border-radius: var(--radius-sm);
  box-shadow: var(--shadow-card);
  margin-bottom: 20px;
}
.legend-item { display: flex; align-items: center; gap: 8px; font-size: 12px; color: var(--text-secondary); letter-spacing: 0.08em; }
.gem { width: 8px; height: 8px; border-radius: 50%; }

.room-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(140px, 1fr));
  gap: 14px;
}

.room-card {
  background: var(--bg-card);
  box-shadow: var(--shadow-card);
  border-radius: var(--radius);
  padding: 18px 14px;
  text-align: center;
  cursor: pointer;
  transition: all 0.4s cubic-bezier(0.25,0.46,0.45,0.94);
  position: relative;
  overflow: hidden;
}
.room-card:hover {
  transform: translateY(-4px);
  box-shadow: var(--shadow-hover);
}
/* 顶部状态光晕 */
.status-glow {
  position: absolute;
  top: -8px;
  left: 50%;
  transform: translateX(-50%);
  width: 40px;
  height: 4px;
  border-radius: 2px;
}
.status-0 .status-glow { background: #D6E4D3; }
.status-1 .status-glow { background: #D2E0EC; }
.status-2 .status-glow { background: var(--gold); }
.status-3 .status-glow { background: #F3E3CE; }

.room-number { font-size: 24px; font-weight: 700; color: var(--text-primary); margin-top: 4px; }
.room-type { font-size: 12px; color: var(--text-muted); margin: 6px 0 2px; letter-spacing: 0.08em; }
.room-price { font-size: 14px; color: var(--gold); font-weight: 600; }
.room-badge {
  display: inline-block; font-size: 10px; letter-spacing: 0.1em;
  padding: 2px 12px; border-radius: 10px; margin-top: 8px;
}
.status-0 .room-badge { background: rgba(138,167,143,0.12); color: #8AA78F; }
.status-1 .room-badge { background: rgba(140,161,181,0.12); color: #8CA1B5; }
.status-2 .room-badge { background: rgba(212,175,55,0.12); color: var(--gold-light); }
.status-3 .room-badge { background: rgba(188,110,110,0.12); color: #BC6E6E; }

/* 详情弹窗 */
.detail-wrap { padding: 8px 0; }
.detail-header { display: flex; align-items: center; justify-content: space-between; margin-bottom: 20px; }
.detail-room-number { font-size: 32px; font-weight: 700; color: var(--text-primary); }
.detail-badge { font-size: 12px; padding: 4px 16px; border-radius: 12px; letter-spacing: 0.08em; }
.detail-0 .detail-badge { background: rgba(138,167,143,0.12); color: #8AA78F; }
.detail-1 .detail-badge { background: rgba(140,161,181,0.12); color: #8CA1B5; }
.detail-2 .detail-badge { background: rgba(212,175,55,0.12); color: var(--gold-light); }
.detail-3 .detail-badge { background: rgba(188,110,110,0.12); color: #BC6E6E; }
.detail-row { display: flex; justify-content: space-between; padding: 12px 0; border-bottom: 1px solid var(--border-subtle); font-size: 14px; }
.detail-row:last-child { border-bottom: none; }
.detail-row span:first-child { color: var(--text-muted); }
.detail-row span:last-child { color: var(--text-primary); font-weight: 500; }
</style>
