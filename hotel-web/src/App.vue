<template>
  <Login v-if="!isLoggedIn" @login-success="isLoggedIn = true" />
  <div v-else class="app-container">
    <!-- 侧边栏 -->
    <div class="sidebar">
      <div class="sidebar-header">
        <span>🏨 天玺尊邸</span>
        <el-button size="small" text style="color: #fff" @click="handleLogout">退出</el-button>
      </div>
      <div class="sidebar-menu">
        <div class="menu-item" :class="{ active: currentView === 'dashboard' }"
             @click="currentView = 'dashboard'">
          <el-icon><DataAnalysis /></el-icon> 数据看板
        </div>
        <div class="menu-item" :class="{ active: currentView === 'rooms' }"
             @click="currentView = 'rooms'">
          <el-icon><HomeFilled /></el-icon> 房间管理
        </div>
        <div class="menu-item" :class="{ active: currentView === 'bookings' }"
             @click="currentView = 'bookings'">
          <el-icon><Document /></el-icon> 订单管理
        </div>
        <div class="menu-item" :class="{ active: currentView === 'cleaning' }"
             @click="currentView = 'cleaning'">
          <el-icon><Brush /></el-icon> 保洁管理
        </div>
        <div class="menu-item" :class="{ active: currentView === 'room-service' }"
             @click="currentView = 'room-service'">
          <el-icon><Service /></el-icon> 客房服务
        </div>
        <div class="menu-item" :class="{ active: currentView === 'pricing' }"
             @click="currentView = 'pricing'">
          <el-icon><Coin /></el-icon> 动态定价
        </div>
        <div class="menu-item" :class="{ active: currentView === 'assign' }"
             @click="currentView = 'assign'">
          <el-icon><MagicStick /></el-icon> 智能排房
        </div>
        <div class="menu-item" :class="{ active: currentView === 'members' }"
             @click="currentView = 'members'">
          <el-icon><Avatar /></el-icon> 会员管理
        </div>
        <div class="menu-item" :class="{ active: currentView === 'payment' }"
             @click="currentView = 'payment'">
          <el-icon><Money /></el-icon> 支付结算
        </div>
        <div class="menu-item" :class="{ active: currentView === 'ai' }"
             @click="currentView = 'ai'">
          <el-icon><Cpu /></el-icon> AI 管家
        </div>
      </div>
    </div>

    <!-- 主内容区 -->
    <div class="main-content">
      <Dashboard v-if="currentView === 'dashboard'" />
      <RoomManager v-if="currentView === 'rooms'" />
      <BookingManager v-if="currentView === 'bookings'" />
      <CleaningManagement v-if="currentView === 'cleaning'" />
      <RoomService v-if="currentView === 'room-service'" />
      <DynamicPricing v-if="currentView === 'pricing'" />
      <SmartAssign v-if="currentView === 'assign'" />
      <MemberManager v-if="currentView === 'members'" />
      <PaymentManager v-if="currentView === 'payment'" />
      <AiChat v-if="currentView === 'ai'" />
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { ElMessageBox } from 'element-plus'
import Login from './views/Login.vue'
import Dashboard from './views/Dashboard.vue'
import RoomManager from './views/RoomManager.vue'
import BookingManager from './views/BookingManager.vue'
import CleaningManagement from './views/CleaningManagement.vue'
import RoomService from './views/RoomService.vue'
import DynamicPricing from './views/DynamicPricing.vue'
import SmartAssign from './views/SmartAssign.vue'
import MemberManager from './views/MemberManager.vue'
import PaymentManager from './views/PaymentManager.vue'
import AiChat from './views/AiChat.vue'

const currentView = ref('dashboard')

// 检查登录状态
const isLoggedIn = ref(!!localStorage.getItem('token'))

const handleLogout = async () => {
  try {
    await ElMessageBox.confirm('确定要退出登录吗？', '提示')
  } catch {
    return
  }
  localStorage.removeItem('token')
  localStorage.removeItem('username')
  isLoggedIn.value = false
}
</script>

<!-- 原有的样式保持不变 -->
<style>
* { margin: 0; padding: 0; box-sizing: border-box; }
html, body, #app { height: 100%; width: 100%; font-family: 'Helvetica Neue', Helvetica, 'PingFang SC', 'Microsoft YaHei', sans-serif; }
.app-container { display: flex; height: 100vh; }

.sidebar {
  width: 200px;
  background: #1a1a2e;
  color: #fff;
  display: flex;
  flex-direction: column;
  flex-shrink: 0;
}
.sidebar-header {
  padding: 20px 16px;
  font-size: 18px;
  font-weight: bold;
  border-bottom: 1px solid rgba(255,255,255,0.1);
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.sidebar-menu { flex: 1; overflow-y: auto; padding: 8px 0; }
.menu-item {
  padding: 12px 20px;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 8px;
  color: rgba(255,255,255,0.7);
  transition: all 0.2s;
  font-size: 14px;
}
.menu-item:hover { background: rgba(255,255,255,0.08); color: #fff; }
.menu-item.active { background: rgba(64,158,255,0.2); color: #409eff; border-right: 3px solid #409eff; }

.main-content { flex: 1; overflow-y: auto; padding: 20px; background: #f5f7fa; }
</style>
