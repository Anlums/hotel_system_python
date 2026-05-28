<template>
  <Login v-if="!isLoggedIn" @login-success="isLoggedIn = true" />
  <div v-else class="app-layout">
    <!-- 顶部流光金线 -->
    <div class="top-aurora"></div>

    <!-- 悬浮玻璃导航栏 -->
    <aside class="glass-dock">
      <div class="dock-brand">🏨</div>
      <nav class="dock-nav">
        <div class="dock-item" :class="{ active: currentView === 'dashboard' }" :title="'数据看板'" @click="currentView = 'dashboard'">
          <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><rect x="3" y="3" width="7" height="7" rx="1"/><rect x="14" y="3" width="7" height="7" rx="1"/><rect x="3" y="14" width="7" height="7" rx="1"/><rect x="14" y="14" width="7" height="7" rx="1"/></svg>
        </div>
        <div class="dock-item" :class="{ active: currentView === 'rooms' }" :title="'房间管理'" @click="currentView = 'rooms'">
          <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M3 21h18M3 7v14M21 7v14M3 3l9 4 9-4"/></svg>
        </div>
        <div class="dock-item" :class="{ active: currentView === 'bookings' }" :title="'订单管理'" @click="currentView = 'bookings'">
          <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M14 2H6a2 2 0 00-2 2v16a2 2 0 002 2h12a2 2 0 002-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="16" y1="13" x2="8" y2="13"/><line x1="16" y1="17" x2="8" y2="17"/></svg>
        </div>
        <div class="dock-item" :class="{ active: currentView === 'cleaning' }" :title="'保洁管理'" @click="currentView = 'cleaning'">
          <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M20 2L4 20M4 2l16 18"/></svg>
        </div>
        <div class="dock-item" :class="{ active: currentView === 'room-service' }" :title="'客房服务'" @click="currentView = 'room-service'">
          <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M12 2L2 7l10 5 10-5-10-5zM2 17l10 5 10-5M2 12l10 5 10-5"/></svg>
        </div>
        <div class="dock-item" :class="{ active: currentView === 'pricing' }" :title="'动态定价'" @click="currentView = 'pricing'">
          <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><line x1="12" y1="1" x2="12" y2="23"/><path d="M17 5H9.5a3.5 3.5 0 000 7h5a3.5 3.5 0 010 7H6"/></svg>
        </div>
        <div class="dock-item" :class="{ active: currentView === 'assign' }" :title="'智能排房'" @click="currentView = 'assign'">
          <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><circle cx="12" cy="12" r="10"/><path d="M12 6v6l4 2"/></svg>
        </div>
        <div class="dock-item" :class="{ active: currentView === 'members' }" :title="'会员管理'" @click="currentView = 'members'">
          <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M17 21v-2a4 4 0 00-4-4H5a4 4 0 00-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M23 21v-2a4 4 0 00-3-3.87"/><path d="M16 3.13a4 4 0 010 7.75"/></svg>
        </div>
        <div class="dock-item" :class="{ active: currentView === 'payment' }" :title="'支付结算'" @click="currentView = 'payment'">
          <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><rect x="1" y="4" width="22" height="16" rx="2"/><line x1="1" y1="10" x2="23" y2="10"/></svg>
        </div>
        <div class="dock-item" :class="{ active: currentView === 'ai' }" :title="'AI 管家'" @click="currentView = 'ai'">
          <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M12 2a4 4 0 014 4v2a4 4 0 01-8 0V6a4 4 0 014-4z"/><path d="M19.07 8.07A10 10 0 014.93 8.07M4.93 15.93a10 10 0 0114.14 0"/><path d="M12 22v-6"/></svg>
        </div>
      </nav>
      <div class="dock-footer">
        <div class="dock-item" title="退出" @click="handleLogout">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M9 21H5a2 2 0 01-2-2V5a2 2 0 012-2h4"/><polyline points="16 17 21 12 16 7"/><line x1="21" y1="12" x2="9" y2="12"/></svg>
        </div>
      </div>
    </aside>

    <!-- 主内容区 -->
    <main class="main-area">
      <!-- 顶部栏 -->
      <header class="top-bar">
        <div class="top-left">
          <span class="brand-mark">✦</span>
          <span class="brand-en">TIAN XI</span>
          <span class="brand-divider">|</span>
          <span class="brand-cn">天玺尊邸</span>
        </div>
        <div class="top-right">
          <span class="top-time">{{ currentTime }}</span>
          <span class="top-user-divider"></span>
          <span class="top-user">{{ username }}</span>
        </div>
      </header>

      <!-- 内容 -->
      <div class="content-scroll">
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
      </div>
    </main>
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
  const pad = (n) => String(n).padStart(2, '0')
  currentTime.value = `${d.getFullYear()}.${pad(d.getMonth()+1)}.${pad(d.getDate())}  ${pad(d.getHours())}:${pad(d.getMinutes())}`
}

onMounted(() => { updateTime(); timer = setInterval(updateTime, 10000) })
onUnmounted(() => { clearInterval(timer) })

const handleLogout = async () => {
  try { await ElMessageBox.confirm('确定要退出吗？', '') } catch { return }
  localStorage.removeItem('token'); localStorage.removeItem('username')
  isLoggedIn.value = false
}
</script>

<style>
@import './assets/style.css';

/* ========== 布局 ========== */
.app-layout {
  display: flex;
  height: 100vh;
  background: var(--bg-deep);
  overflow: hidden;
}

/* 顶部流光金线 */
.top-aurora {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  height: 1px;
  background: linear-gradient(90deg, transparent, var(--gold), var(--gold-light), var(--gold), transparent);
  z-index: 1000;
  animation: aurora 3s ease-in-out infinite;
}
@keyframes aurora {
  0% { opacity: 0.3; }
  50% { opacity: 1; }
  100% { opacity: 0.3; }
}

/* ========== 悬浮玻璃 Dock ========== */
.glass-dock {
  display: flex;
  flex-direction: column;
  align-items: center;
  width: 72px;
  margin: 20px 0 20px 20px;
  padding: 16px 0;
  background: rgba(11, 12, 16, 0.6);
  backdrop-filter: blur(30px);
  -webkit-backdrop-filter: blur(30px);
  border: 1px solid var(--border-gold);
  border-radius: 20px;
  flex-shrink: 0;
  z-index: 10;
}
.dock-brand {
  font-size: 28px;
  margin-bottom: 20px;
  cursor: default;
}
.dock-nav {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 4px;
}
.dock-item {
  width: 44px;
  height: 44px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 12px;
  color: var(--text-muted);
  cursor: pointer;
  transition: all 0.3s;
  position: relative;
}
.dock-item:hover {
  color: var(--gold-light);
  background: rgba(212, 175, 55, 0.08);
}
.dock-item.active {
  color: var(--gold);
  background: rgba(212, 175, 55, 0.12);
}
.dock-item.active::after {
  content: '';
  position: absolute;
  right: -8px;
  top: 50%;
  transform: translateY(-50%);
  width: 3px;
  height: 16px;
  background: var(--gold);
  border-radius: 2px;
  box-shadow: 0 0 8px var(--gold-glow);
}
.dock-footer { margin-top: auto; padding-top: 8px; border-top: 1px solid var(--border-subtle); }

/* ========== 主区域 ========== */
.main-area {
  flex: 1;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

/* 顶部栏 */
.top-bar {
  height: 56px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 32px;
  flex-shrink: 0;
  background: rgba(11, 12, 16, 0.4);
  backdrop-filter: blur(20px);
  border-bottom: 1px solid var(--border-subtle);
}
.top-left { display: flex; align-items: center; gap: 12px; }
.brand-mark { color: var(--gold); font-size: 16px; }
.brand-en { font-size: 16px; font-weight: 700; color: var(--gold); letter-spacing: 0.2em; }
.brand-divider { color: var(--text-muted); font-size: 14px; }
.brand-cn { font-size: 14px; color: var(--text-secondary); letter-spacing: 0.1em; }
.top-right { display: flex; align-items: center; gap: 16px; }
.top-time { font-size: 13px; color: var(--text-muted); letter-spacing: 0.08em; }
.top-user-divider { width: 1px; height: 16px; background: var(--border-subtle); }
.top-user { font-size: 13px; color: var(--text-secondary); }

/* 内容滚动区 */
.content-scroll {
  flex: 1;
  overflow-y: auto;
  padding: 28px 32px;
}
.content-inner {
  max-width: 1400px;
  margin: 0 auto;
}
</style>
