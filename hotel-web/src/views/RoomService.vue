<template>
  <div>
    <div class="page-header">
      <h1 class="page-title">🛎️ 客房服务</h1>
    </div>

    <el-tabs v-model="activeTab">
      <!-- ====== 服务菜单 ====== -->
      <el-tab-pane label="📋 服务菜单" name="menu">
        <div class="toolbar">
          <el-button type="primary" @click="showAddDialog = true">+ 新增项目</el-button>
        </div>

        <el-table :data="menuItems" style="width: 100%">
          <el-table-column prop="id" label="ID" width="60" />
          <el-table-column prop="name" label="项目名称" width="160" />
          <el-table-column prop="category" label="分类" width="100">
            <template #default="{ row }">
              <el-tag :type="categoryType(row.category)" size="small">{{ row.category }}</el-tag>
            </template>
          </el-table-column>
          <el-table-column prop="price" label="价格" width="100">
            <template #default="{ row }">¥{{ row.price }}</template>
          </el-table-column>
          <el-table-column prop="available" label="状态" width="80">
            <template #default="{ row }">
              <el-tag :type="row.available ? 'success' : 'info'" size="small">
                {{ row.available ? '上架' : '下架' }}
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column label="操作" min-width="120">
            <template #default="{ row }">
              <el-button size="small" type="danger" @click="handleDeleteItem(row.id)">删除</el-button>
            </template>
          </el-table-column>
        </el-table>

        <!-- 新增菜单项对话框 -->
        <el-dialog v-model="showAddDialog" title="新增服务项目" width="400px">
          <el-form :model="menuForm" label-width="80px">
            <el-form-item label="名称">
              <el-input v-model="menuForm.name" />
            </el-form-item>
            <el-form-item label="分类">
              <el-select v-model="menuForm.category" style="width: 100%">
                <el-option label="餐饮" value="餐饮" />
                <el-option label="饮品" value="饮品" />
                <el-option label="日用品" value="日用品" />
                <el-option label="其他" value="其他" />
              </el-select>
            </el-form-item>
            <el-form-item label="价格">
              <el-input-number v-model="menuForm.price" :min="1" :max="9999" style="width: 100%" />
            </el-form-item>
          </el-form>
          <template #footer>
            <el-button @click="showAddDialog = false">取消</el-button>
            <el-button type="primary" @click="handleAddItem">保存</el-button>
          </template>
        </el-dialog>
      </el-tab-pane>

      <!-- ====== 订单管理 ====== -->
      <el-tab-pane label="📦 订单管理" name="orders">
        <!-- 下单区 -->
        <div class="content-card order-card" style="margin-bottom: 20px; padding: 16px 20px">
          <h4 style="margin-top: 0; margin-bottom: 16px">🆕 新建服务订单</h4>
          <el-form :model="orderForm" label-width="100px" inline>
            <el-form-item label="房间号">
              <el-input-number v-model="orderForm.room_number" :min="100" :max="999" />
            </el-form-item>
            <el-form-item label="客人姓名">
              <el-input v-model="orderForm.guest_name" placeholder="可选" />
            </el-form-item>
          </el-form>

          <el-table :data="cart" style="width: 100%; margin-bottom: 12px">
            <el-table-column prop="name" label="项目" width="160" />
            <el-table-column prop="price" label="单价" width="80">
              <template #default="{ row }">¥{{ row.price }}</template>
            </el-table-column>
            <el-table-column label="数量" width="140">
              <template #default="{ row }">
                <el-input-number v-model="row.qty" :min="1" :max="99" size="small" controls-position="right" style="width: 110px" />
              </template>
            </el-table-column>
            <el-table-column label="小计" width="100">
              <template #default="{ row }">¥{{ (row.price * row.qty).toFixed(2) }}</template>
            </el-table-column>
            <el-table-column label="操作" width="80">
              <template #default="{ row }">
                <el-button size="small" type="danger" @click="removeFromCart(row)">移除</el-button>
              </template>
            </el-table-column>
          </el-table>

          <div style="display: flex; justify-content: space-between; align-items: center">
            <div>
              <el-select v-model="selectedMenuItem" placeholder="选择服务项目" style="width: 200px" @change="addToCart">
                <el-option v-for="item in menuItems" :key="item.id" :label="item.name" :value="item" :disabled="!item.available" />
              </el-select>
              <span style="margin-left: 16px; font-size: 16px; font-weight: bold">
                合计: ¥{{ cartTotal }}
              </span>
            </div>
            <el-button type="primary" :disabled="cart.length === 0" @click="handlePlaceOrder">
              提交订单
            </el-button>
          </div>
        </div>

        <!-- 待处理订单 -->
        <h3 style="margin: 20px 0 12px">待处理订单</h3>
        <el-table :data="pendingOrders" style="width: 100%">
          <el-table-column prop="id" label="单号" width="70" />
          <el-table-column prop="room_number" label="房间" width="70" />
          <el-table-column label="项目" min-width="200">
            <template #default="{ row }">
              <div v-for="(it, i) in parseItems(row.items)" :key="i" style="font-size: 13px">
                {{ it.name }} × {{ it.qty || 1 }}
              </div>
            </template>
          </el-table-column>
          <el-table-column label="金额" width="80">
            <template #default="{ row }">¥{{ row.total_amount }}</template>
          </el-table-column>
          <el-table-column prop="status" label="状态" width="90">
            <template #default="{ row }">
              <el-tag :type="row.status === 0 ? 'warning' : 'primary'" size="small">
                {{ row.status === 0 ? '待处理' : '配送中' }}
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column prop="created_at" label="下单时间" width="170">
            <template #default="{ row }">{{ formatTime(row.created_at) }}</template>
          </el-table-column>
          <el-table-column label="操作" min-width="170">
            <template #default="{ row }">
              <el-button size="small" type="warning" @click="handleAccept(row.id)" v-if="row.status === 0">
                接单配送
              </el-button>
              <el-button size="small" type="success" @click="handleDeliver(row.id)" v-if="row.status === 1">
                送达完成
              </el-button>
            </template>
          </el-table-column>
        </el-table>

        <!-- 历史记录 -->
        <h3 style="margin: 24px 0 12px">历史记录</h3>
        <el-table :data="allOrders" style="width: 100%">
          <el-table-column prop="id" label="单号" width="70" />
          <el-table-column prop="room_number" label="房间" width="70" />
          <el-table-column label="项目" min-width="200">
            <template #default="{ row }">
              <div v-for="(it, i) in parseItems(row.items)" :key="i" style="font-size: 13px">
                {{ it.name }} × {{ it.qty || 1 }}
              </div>
            </template>
          </el-table-column>
          <el-table-column label="金额" width="80">
            <template #default="{ row }">¥{{ row.total_amount }}</template>
          </el-table-column>
          <el-table-column prop="status" label="状态" width="90">
            <template #default="{ row }">
              <el-tag :type="statusHistoryTag(row.status)" size="small">
                {{ statusHistoryText(row.status) }}
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column prop="created_at" label="下单时间" width="170">
            <template #default="{ row }">{{ formatTime(row.created_at) }}</template>
          </el-table-column>
          <el-table-column prop="completed_at" label="完成时间" width="170">
            <template #default="{ row }">{{ formatTime(row.completed_at) || '-' }}</template>
          </el-table-column>
        </el-table>
      </el-tab-pane>
    </el-tabs>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import request from '@/api/index.js'

const activeTab = ref('menu')

// 菜单
const menuItems = ref([])
const showAddDialog = ref(false)
const menuForm = ref({ name: '', category: '餐饮', price: 10 })

const categoryType = (c) => ({ 餐饮: 'success', 饮品: 'warning', 日用品: 'primary' }[c] || 'info')

const statusHistoryTag = (s) => ({ 0: 'info', 1: 'warning', 2: 'success' }[s] || 'info')
const statusHistoryText = (s) => ({ 0: '待处理', 1: '配送中', 2: '已送达' }[s] || '已取消')

const fetchMenu = async () => {
  const res = await request.get('/room-service/menu')
  menuItems.value = res.data || res
}

const handleAddItem = async () => {
  await request.post('/room-service/menu', menuForm.value)
  ElMessage.success('已添加')
  showAddDialog.value = false
  fetchMenu()
}

const handleDeleteItem = async (id) => {
  await request.delete(`/room-service/menu/${id}`)
  ElMessage.success('已删除')
  fetchMenu()
}

// 下单
const orderForm = ref({ room_number: 101, guest_name: '' })
const selectedMenuItem = ref(null)
const cart = ref([])

const addToCart = (item) => {
  const existing = cart.value.find((c) => c.id === item.id)
  if (existing) {
    existing.qty++
  } else {
    cart.value.push({ ...item, qty: 1, price: Number(item.price) })
  }
  selectedMenuItem.value = null
}

const removeFromCart = (item) => {
  cart.value = cart.value.filter((c) => c.id !== item.id)
}

const cartTotal = computed(() => cart.value.reduce((s, c) => s + c.price * c.qty, 0).toFixed(2))

const handlePlaceOrder = async () => {
  const items = JSON.stringify(cart.value.map((c) => ({ name: c.name, price: c.price, qty: c.qty })))
  await request.post('/room-service/order', {
    room_number: orderForm.value.room_number,
    guest_name: orderForm.value.guest_name || null,
    items,
    total_amount: parseFloat(cartTotal.value),
  })
  ElMessage.success('下单成功')
  cart.value = []
  fetchPendingOrders()
  fetchAllOrders()
}

// 订单
const pendingOrders = ref([])
const allOrders = ref([])

const parseItems = (itemsStr) => {
  try { return JSON.parse(itemsStr) } catch { return [] }
}

const fetchPendingOrders = async () => {
  const res = await request.get('/room-service/pending')
  pendingOrders.value = res.data || res
}

const fetchAllOrders = async () => {
  const res = await request.get('/room-service/orders')
  allOrders.value = res.data || res
}

const handleAccept = async (id) => {
  await request.put(`/room-service/accept/${id}`)
  ElMessage.success('开始配送')
  fetchPendingOrders()
  fetchAllOrders()
}

const handleDeliver = async (id) => {
  await request.put(`/room-service/deliver/${id}`)
  ElMessage.success('已送达')
  fetchPendingOrders()
  fetchAllOrders()
}

const formatTime = (t) => t ? t.replace('T', ' ').slice(0, 16) : null

onMounted(() => {
  fetchMenu()
  fetchPendingOrders()
  fetchAllOrders()
})
</script>

<style scoped>
.page-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px; }
.page-title { font-size: 22px; margin: 0; }
.toolbar { margin-bottom: 16px; }
.order-card { margin-bottom: 0; }
</style>
