<template>
  <Login v-if="!isLoggedIn" @login-success="isLoggedIn = true" />
  <div v-else class="app-layout">
    <!-- 顶部导航栏 -->
    <header class="top-bar">
      <div class="top-bar-left">
        <div class="brand">
          <span class="brand-icon">🏨</span>
          <span class="brand-text">天玺尊邸</span>
        </div>
        <span class="brand-subtitle">酒店管理系统</span>
      </div>
      <div class="top-bar-right">
        <span class="top-time">{{ currentTime }}</span>
        <span class="top-user">👤 {{ username }}</span>
        <el-button text size="small" style="color: rgba(255,255,255,0.7)" @click="handleLogout">退出</el-button>
      </div>
    </header>

    <div class="main-area">
      <!-- 侧边栏 -->
      <aside class="sidebar">
        <nav class="sidebar-nav">
          <div class="nav-item" :class="{ active: currentView === 'dashboard' }" @click="currentView = 'dashboard'">
            <el-icon><DataAnalysis /></el-icon><span>数据看板</span>
          </div>
          <div class="nav-item" :class="{ active: currentView === 'rooms' }" @click="currentView = 'rooms'">
            <el-icon><HomeFilled /></el-icon><span>房间管理</span>
          </div>
          <div class="nav-item" :class="{ active: currentView === 'bookings' }" @click="currentView = 'bookings'">
            <el-icon><Document /></el-icon><span>订单管理</span>
          </div>
          <div class="nav-item" :class="{ active: currentView === 'cleaning' }" @click="currentView = 'cleaning'">
            <el-icon><Brush /></el-icon><span>保洁管理</span>
          </div>
          <div class="nav-item" :class="{ active: currentView === 'room-service' }" @click="currentView = 'room-service'">
            <el-icon><Service /></el-icon><span>客房服务</span>
          </div>
          <div class="nav-item" :class="{ active: currentView === 'pricing' }" @click="currentView = 'pricing'">
            <el-icon><Coin /></el-icon><span>动态定价</span>
          </div>
          <div class="nav-item" :class="{ active: currentView === 'assign' }" @click="currentView = 'assign'">
            <el-icon><MagicStick /></el-icon><span>智能排房</span>
          </div>
          <div class="nav-item" :class="{ active: currentView === 'members' }" @click="currentView = 'members'">
            <el-icon><Avatar /></el-icon><span>会员管理</span>
          </div>
          <div class="nav-item" :class="{ active: currentView === 'payment' }" @click="currentView = 'payment'">
            <el-icon><Money /></el-icon><span>支付结算</span>
          </div>
          <div class="nav-item" :class="{ active: currentView === 'ai' }" @click="currentView = 'ai'">
            <el-icon><Cpu /></el-icon><span>AI 管家</span>
          </div>
        </nav>
      </aside>

      <!-- 主内容区 -->
      <main class="content">
        <div class="content-inner page-enter" :key="currentView">
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
      </main>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
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
const isLoggedIn = ref(!!localStorage.getItem('token'))
const username = ref(localStorage.getItem('username') || '管理员')
const currentTime = ref('')
let timer = null

const updateTime = () => {
  const d = new Date()
  currentTime.value = `${d.getFullYear()}-${String(d.getMonth()+1).padStart(2,'0')}-${String(d.getDate()).padStart(2,'0')} ${String(d.getHours()).padStart(2,'0')}:${String(d.getMinutes()).padStart(2,'0')}`
}

onMounted(() => {
  updateTime()
  timer = setInterval(updateTime, 10000)
})

onUnmounted(() => {
  clearInterval(timer)
})

const handleLogout = async () => {
  try {
    await ElMessageBox.confirm('确定要退出登录吗？', '提示')
  } catch { return }
  localStorage.removeItem('token')
  localStorage.removeItem('username')
  isLoggedIn.value = false
}
</script>

<style>
/* 引入全局样式 */
@import './assets/style.css';

.app-layout {
  display: flex;
  flex-direction: column;
  height: 100vh;
  overflow: hidden;
}

/* 顶部导航栏 */
.top-bar {
  height: 56px;
  background: var(--primary);
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 24px;
  flex-shrink: 0;
  z-index: 100;
}
.top-bar-left { display: flex; align-items: center; gap: 12px; }
.brand { display: flex; align-items: center; gap: 8px; }
.brand-icon { font-size: 24px; }
.brand-text { font-size: 18px; font-weight: 700; color: var(--accent); }
.brand-subtitle { font-size: 13px; color: rgba(255,255,255,0.5); margin-top: 4px; }
.top-bar-right { display: flex; align-items: center; gap: 16px; }
.top-time { font-size: 13px; color: rgba(255,255,255,0.5); }
.top-user { font-size: 13px; color: rgba(255,255,255,0.7); }

/* 主体区域（侧边栏 + 内容） */
.main-area {
  display: flex;
  flex: 1;
  overflow: hidden;
}

/* 侧边栏 */
.sidebar {
  width: 180px;
  background: var(--primary);
  flex-shrink: 0;
  overflow-y: auto;
  padding: 8px 0;
}
.sidebar-nav { display: flex; flex-direction: column; gap: 2px; }
.nav-item {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 11px 20px;
  cursor: pointer;
  color: rgba(255,255,255,0.6);
  font-size: 14px;
  transition: all 0.2s;
  border-left: 3px solid transparent;
}
.nav-item:hover {
  background: rgba(255,255,255,0.06);
  color: rgba(255,255,255,0.9);
}
.nav-item.active {
  background: rgba(200, 169, 110, 0.12);
  color: var(--accent);
  border-left-color: var(--accent);
}

/* 内容区 */
.content {
  flex: 1;
  overflow-y: auto;
  padding: 24px;
  background: var(--bg-main);
}
.content-inner {
  max-width: 1400px;
  margin: 0 auto;
}
</style>
