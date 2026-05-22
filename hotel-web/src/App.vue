<template>
  <div class="app-container">
    <!-- 侧边栏 -->
    <div class="sidebar">
      <div class="sidebar-header">🏨 天玺尊邸</div>
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
import { ref } from 'vue'
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
</script>
