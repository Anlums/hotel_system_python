<template>
  <div class="page-enter">
    <div class="page-header">
      <h1 class="page-title">御旨编年 · 宫闱调度</h1>
      <el-button type="primary" @click="openAddDialog">+ 新增订单</el-button>
    </div>

    <!-- 搜索栏 -->
    <div class="content-card" style="margin-bottom: 20px; padding: 16px 20px">
      <el-form :inline="true" :model="searchForm">
        <el-form-item label="客人">
          <el-input v-model="searchForm.guest_name" placeholder="模糊搜索" clearable />
        </el-form-item>
        <el-form-item label="房号">
          <el-input v-model="searchForm.room_number" placeholder="精确匹配" clearable />
        </el-form-item>
        <el-form-item label="状态">
          <el-select v-model="searchForm.status" clearable placeholder="全部" style="width: 120px">
            <el-option label="已预约" :value="1" />
            <el-option label="已入住" :value="2" />
            <el-option label="已退房" :value="3" />
            <el-option label="已取消" :value="4" />
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="fetchBookings">搜索</el-button>
          <el-button @click="resetSearch">重置</el-button>
        </el-form-item>
      </el-form>
    </div>

    <!-- 订单表格 -->
    <el-table :data="bookings" style="width: 100%" class="booking-table">
      <el-table-column prop="id" label="ID" width="60" />
      <el-table-column prop="room_number" label="房间号" width="80" />
      <el-table-column prop="guest_name" label="客人" min-width="80" />
      <el-table-column prop="phone" label="电话" width="120" />
      <el-table-column prop="check_in_date" label="入住" width="155">
        <template #default="{ row }">{{ formatTime(row.check_in_date) }}</template>
      </el-table-column>
      <el-table-column prop="check_out_date" label="退房" width="155">
        <template #default="{ row }">{{ formatTime(row.check_out_date) }}</template>
      </el-table-column>
      <el-table-column prop="total_amount" label="金额" width="80">
        <template #default="{ row }">¥{{ row.total_amount || '-' }}</template>
      </el-table-column>
      <el-table-column prop="status" label="状态" width="80">
        <template #default="{ row }">
          <el-tag :type="statusTag(row.status)" size="small">
            {{ statusText(row.status) }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column label="操作" min-width="360">
        <template #default="{ row }">
          <div class="action-btns">
            <el-button size="small" @click="openEditDialog(row)" v-if="row.status === 1">编辑</el-button>
            <el-button size="small" type="success" @click="openDepositDialog(row)" v-if="row.status === 1">入住</el-button>
            <el-button size="small" type="warning" @click="openSettleDialog(row)" v-if="row.status === 2">退房</el-button>
            <el-button size="small" @click="handleCancel(row.id)" v-if="row.status === 1">取消</el-button>
            <el-button size="small" type="danger" @click="handleDelete(row.id)">删除</el-button>
          </div>
        </template>
      </el-table-column>
    </el-table>

    <!-- 新增/编辑对话框 -->
    <el-dialog v-model="dialogVisible" :title="isEdit ? '编辑订单' : '新增订单'" width="500px">
      <el-form :model="form" label-width="110px">
        <el-form-item label="客人姓名">
          <el-input v-model="form.guest_name" />
        </el-form-item>
        <el-form-item label="电话">
          <el-input v-model="form.phone" />
        </el-form-item>
        <el-form-item label="房间号">
          <el-input-number v-model="form.room_number" :min="1" style="width: 100%" />
        </el-form-item>
        <el-form-item label="入住日期">
          <div style="display: flex; gap: 6px; width: 100%">
            <el-date-picker v-model="form.check_in_date" type="datetime" value-format="YYYY-MM-DD HH:mm:ss"
              placeholder="选择日期时间" style="flex: 1" />
            <el-button size="small" @click="form.check_in_date = nowStr()">Now</el-button>
          </div>
        </el-form-item>
        <el-form-item label="退房日期" v-if="isEdit">
          <el-date-picker v-model="form.check_out_date" type="datetime" value-format="YYYY-MM-DD HH:mm:ss"
            placeholder="可选" style="width: 100%" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="handleSave">保存</el-button>
      </template>
    </el-dialog>

    <!-- 入住押金对话框 -->
    <el-dialog v-model="depositVisible" title="💳 办理入住 - 收取押金" width="450px">
      <p v-if="depositBooking" style="margin-bottom: 16px">
        客人: <strong>{{ depositBooking.guest_name }}</strong>
        &nbsp;|&nbsp; 房间: <strong>{{ depositBooking.room_number }}</strong>
        &nbsp;|&nbsp; 入住: {{ formatTime(depositBooking.check_in_date) }}
      </p>
      <el-form :model="depositForm" label-width="100px">
        <el-form-item label="押金金额">
          <el-input-number v-model="depositForm.amount" :min="100" :max="10000" :step="100" style="width: 100%" />
        </el-form-item>
        <el-form-item label="支付方式">
          <el-select v-model="depositForm.method" style="width: 100%">
            <el-option label="现金" value="cash" />
            <el-option label="微信" value="wechat" />
            <el-option label="支付宝" value="alipay" />
            <el-option label="银行卡" value="card" />
          </el-select>
        </el-form-item>
        <el-form-item label="备注">
          <el-input v-model="depositForm.remark" placeholder="可选" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="depositVisible = false">取消</el-button>
        <el-button type="primary" :loading="depositLoading" @click="handleDepositAndCheckIn">
          确认入住
        </el-button>
      </template>
    </el-dialog>

    <!-- 退房结算对话框 -->
    <el-dialog v-model="settleVisible" title="🧾 退房结算" width="500px">
      <div v-if="settleInfo">
        <el-descriptions :column="2" border size="small">
          <el-descriptions-item label="客人">{{ settleBooking?.guest_name }}</el-descriptions-item>
          <el-descriptions-item label="房间号">{{ settleBooking?.room_number }}</el-descriptions-item>
          <el-descriptions-item label="入住日期">{{ formatTime(settleBooking?.check_in_date) }}</el-descriptions-item>
          <el-descriptions-item label="房型/单价">¥{{ settleInfo.room_price }}/晚</el-descriptions-item>
          <el-descriptions-item label="入住天数">{{ settleInfo.days }} 天</el-descriptions-item>
          <el-descriptions-item label="已付押金" span="2">
            <span style="color: #e6a23c; font-weight: bold">¥{{ settleInfo.deposit }}</span>
          </el-descriptions-item>
        </el-descriptions>

        <el-divider />

        <div class="settle-summary">
          <div class="settle-row">
            <span>房费合计：</span>
            <span>¥{{ settleInfo.room_price }} × {{ settleInfo.days }}天 = <strong>¥{{ settleInfo.total_bill }}</strong></span>
          </div>
          <div class="settle-row">
            <span>已付押金：</span>
            <span style="color: #e6a23c; font-weight: bold">- ¥{{ settleInfo.deposit }}</span>
          </div>
          <el-divider />
          <div class="settle-row settle-final" :style="{ color: settleInfo.balance >= 0 ? '#67c23a' : '#f56c6c' }">
            <span style="font-size: 18px">{{ settleInfo.balance >= 0 ? '应补金额' : '应退金额' }}：</span>
            <span style="font-size: 22px; font-weight: bold">¥{{ Math.abs(settleInfo.balance) }}</span>
          </div>
        </div>

        <el-form :model="settleForm" label-width="100px" style="margin-top: 16px">
          <el-form-item label="支付方式" v-if="settleInfo.balance > 0">
            <el-select v-model="settleForm.method" style="width: 100%">
              <el-option label="现金" value="cash" />
              <el-option label="微信" value="wechat" />
              <el-option label="支付宝" value="alipay" />
              <el-option label="银行卡" value="card" />
            </el-select>
          </el-form-item>
        </el-form>
      </div>
      <div v-else style="text-align: center; padding: 20px">
        <el-icon class="is-loading" :size="24"><Loading /></el-icon>
        <p>计算中...</p>
      </div>
      <template #footer>
        <el-button @click="settleVisible = false">取消</el-button>
        <el-button type="primary" :loading="settleLoading" @click="handleSettleAndCheckOut">
          确认结算
        </el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import request from '@/api/index.js'

const bookings = ref([])
const dialogVisible = ref(false)
const isEdit = ref(false)
const editId = ref(null)
const searchForm = ref({ guest_name: '', room_number: '', status: '' })
const form = ref({
  guest_name: '', phone: '', room_number: 101,
  check_in_date: '', check_out_date: '',
})

// 押金相关
const depositVisible = ref(false)
const depositLoading = ref(false)
const depositBooking = ref(null)
const depositForm = ref({ amount: 500, method: 'cash', remark: '' })

// 结算相关
const settleVisible = ref(false)
const settleLoading = ref(false)
const settleBooking = ref(null)
const settleInfo = ref(null)
const settleForm = ref({ method: 'cash' })

const fetchBookings = async () => {
  const params = {}
  if (searchForm.value.guest_name) params.guest_name = searchForm.value.guest_name
  if (searchForm.value.room_number) params.room_number = searchForm.value.room_number
  if (searchForm.value.status !== '' && searchForm.value.status !== null) params.status = searchForm.value.status
  const res = await request.get('/bookings/search', { params })
  bookings.value = res.data
}

const resetSearch = () => {
  searchForm.value = { guest_name: '', room_number: '', status: '' }
  fetchBookings()
}

const openAddDialog = () => {
  isEdit.value = false
  editId.value = null
  form.value = { guest_name: '', phone: '', room_number: 101, check_in_date: nowStr(), check_out_date: '' }
  dialogVisible.value = true
}

const openEditDialog = (row) => {
  isEdit.value = true
  editId.value = row.id
  form.value = {
    guest_name: row.guest_name,
    phone: row.phone,
    room_number: row.room_number,
    check_in_date: row.check_in_date?.slice(0, 10) || '',
    check_out_date: row.check_out_date?.slice(0, 10) || '',
  }
  dialogVisible.value = true
}

const handleSave = async () => {
  if (!form.value.check_in_date) {
    ElMessage.warning('请填写入住日期')
    return
  }
  if (isEdit.value) {
    await request.put(`/bookings/update?id=${editId.value}`, form.value)
    ElMessage.success('修改成功')
  } else {
    await request.post('/bookings/placeOrder', form.value)
    ElMessage.success('下单成功')
  }
  dialogVisible.value = false
  fetchBookings()
}

// ---- 入住押金 ----
const openDepositDialog = (row) => {
  depositBooking.value = row
  depositForm.value = { amount: 500, method: 'cash', remark: '' }
  depositVisible.value = true
}

const handleDepositAndCheckIn = async () => {
  depositLoading.value = true
  try {
    // 先收押金
    const depositRes = await request.post('/payments/deposit', {
      booking_id: depositBooking.value.id,
      amount: depositForm.value.amount,
      method: depositForm.value.method,
      remark: depositForm.value.remark || undefined,
      operator: '前台',
    })
    // 再办入住
    await request.put(`/bookings/checkIn?id=${depositBooking.value.id}`)
    ElMessage.success(`入住成功，押金 ¥${depositForm.value.amount} 已收取`)
    depositVisible.value = false
    fetchBookings()
  } catch (e) {
    ElMessage.error('入住失败: ' + (e.message || '未知错误'))
  } finally {
    depositLoading.value = false
  }
}

// ---- 退房结算 ----
const openSettleDialog = async (row) => {
  settleBooking.value = row
  settleInfo.value = null
  settleForm.value = { method: 'cash' }
  settleVisible.value = true

  try {
    // 获取房间信息（单价）
    const roomRes = await request.get('/rooms/get', { params: { room_number: row.room_number } })
    const room = roomRes.data

    // 获取该订单的押金记录
    const paymentRes = await request.get('/payments/list', { params: { booking_id: row.id } })
    const depositPayments = paymentRes.data.filter(p => p.type === 'deposit' && p.status === 'completed')
    const depositTotal = depositPayments.reduce((sum, p) => sum + parseFloat(p.amount), 0)

    // 计算天数
    const checkIn = new Date(row.check_in_date)
    const now = new Date()
    const days = Math.max(1, Math.floor((now - checkIn) / (1000 * 60 * 60 * 24)))

    const roomPrice = parseFloat(room.price)
    const totalBill = roomPrice * days
    const balance = totalBill - depositTotal

    settleInfo.value = {
      room_price: roomPrice,
      days,
      deposit: depositTotal,
      total_bill: totalBill,
      balance: parseFloat(balance.toFixed(2)),
    }
  } catch (e) {
    ElMessage.error('获取结算信息失败')
    settleVisible.value = false
  }
}

const handleSettleAndCheckOut = async () => {
  settleLoading.value = true
  try {
    // 先结算
    await request.post('/payments/settle', {
      booking_id: settleBooking.value.id,
      method: settleForm.value.method,
      operator: '前台',
    })
    // 再退房
    await request.put(`/bookings/checkOut?id=${settleBooking.value.id}`)
    ElMessage.success('退房结算完成')
    settleVisible.value = false
    fetchBookings()
  } catch (e) {
    ElMessage.error('结算失败: ' + (e.message || '未知错误'))
  } finally {
    settleLoading.value = false
  }
}

// ---- 取消 / 删除 ----
const handleCancel = async (id) => {
  await ElMessageBox.confirm('确定取消该订单吗？')
  await request.put(`/bookings/cancel?id=${id}`)
  ElMessage.success('已取消')
  fetchBookings()
}

const handleDelete = async (id) => {
  await ElMessageBox.confirm('确定删除该订单吗？')
  await request.delete(`/bookings/delete?id=${id}`)
  ElMessage.success('删除成功')
  fetchBookings()
}

const formatTime = (t) => t ? t.replace('T', ' ').slice(0, 16) : '-'
const nowStr = () => {
  const d = new Date()
  const pad = (n) => String(n).padStart(2, '0')
  return `${d.getFullYear()}-${pad(d.getMonth()+1)}-${pad(d.getDate())} ${pad(d.getHours())}:${pad(d.getMinutes())}:${pad(d.getSeconds())}`
}
const statusText = (s) => ({ 1: '已预约', 2: '已入住', 3: '已退房', 4: '已取消' }[s] || '未知')
const statusTag = (s) => ({ 1: 'warning', 2: 'primary', 3: 'success', 4: 'info' }[s] || 'info')

onMounted(fetchBookings)
</script>

<style scoped>
.page-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px; }
.action-btns { display: flex; flex-wrap: nowrap; gap: 4px; }
.settle-summary { padding: 0 10px; }
.settle-row { display: flex; justify-content: space-between; padding: 8px 0; font-size: 15px; }
.settle-final { padding: 12px 0; }
</style>
