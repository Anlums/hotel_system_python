<template>
  <div class="page-enter">
    <div class="page-header">
      <h1 class="page-title">数据看板</h1>
      <el-tag type="info" effect="plain">{{ currentTime }}</el-tag>
    </div>

    <!-- KPI 卡片 -->
    <el-row :gutter="20" style="margin-bottom: 24px">
      <el-col :span="6">
        <div class="kpi-card kpi-available">
          <div class="kpi-icon">🟢</div>
          <div class="kpi-value count-animate">{{ stats.available }}</div>
          <div class="kpi-label">空闲房间</div>
        </div>
      </el-col>
      <el-col :span="6">
        <div class="kpi-card kpi-booked">
          <div class="kpi-icon">🟡</div>
          <div class="kpi-value count-animate">{{ stats.booked }}</div>
          <div class="kpi-label">已预订</div>
        </div>
      </el-col>
      <el-col :span="6">
        <div class="kpi-card kpi-occupied">
          <div class="kpi-icon">🔵</div>
          <div class="kpi-value count-animate">{{ stats.occupied }}</div>
          <div class="kpi-label">已入住</div>
        </div>
      </el-col>
      <el-col :span="6">
        <div class="kpi-card kpi-cleaning">
          <div class="kpi-icon">🔴</div>
          <div class="kpi-value count-animate">{{ stats.cleaning || 0 }}</div>
          <div class="kpi-label">清洁中</div>
        </div>
      </el-col>
    </el-row>

    <!-- 图表区域 -->
    <el-row :gutter="20" style="margin-bottom: 24px">
      <el-col :span="10">
        <div class="content-card" style="height: 380px">
          <div style="font-size: 15px; font-weight: 600; margin-bottom: 12px; color: var(--text-primary)">🏠 房间状态分布</div>
          <div ref="pieChart" class="chart"></div>
        </div>
      </el-col>
      <el-col :span="14">
        <div class="content-card" style="height: 380px">
          <div style="font-size: 15px; font-weight: 600; margin-bottom: 12px; color: var(--text-primary)">📈 近7天营业收入</div>
          <div ref="lineChart" class="chart"></div>
        </div>
      </el-col>
    </el-row>

    <!-- 底部卡片：财务概览 + 今日待办 -->
    <el-row :gutter="20">
      <el-col :span="12">
        <div class="content-card">
          <div style="font-size: 15px; font-weight: 600; margin-bottom: 16px; color: var(--text-primary)">💰 财务概览</div>
          <el-row :gutter="16">
            <el-col :span="8" v-for="item in financeItems" :key="item.label">
              <div class="finance-item">
                <div class="finance-value" :style="{ color: item.color }">¥{{ item.value }}</div>
                <div class="finance-label">{{ item.label }}</div>
              </div>
            </el-col>
          </el-row>
        </div>
      </el-col>
      <el-col :span="12">
        <div class="content-card">
          <div style="font-size: 15px; font-weight: 600; margin-bottom: 16px; color: var(--text-primary)">📋 今日待办</div>
          <div v-if="todayTodos.length === 0" style="color: var(--text-secondary); font-size: 14px; padding: 12px 0">暂无待办事项</div>
          <div v-for="todo in todayTodos" :key="todo.text" class="todo-item">
            <span class="todo-dot" :style="{ background: todo.color }"></span>
            <span class="todo-text">{{ todo.text }}</span>
          </div>
        </div>
      </el-col>
    </el-row>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onBeforeUnmount, nextTick } from 'vue'
import * as echarts from 'echarts'
import request from '@/api/index.js'

const stats = ref({ available: 0, booked: 0, occupied: 0, cleaning: 0 })
const paymentStats = ref({ total_deposit: 0, total_payment: 0, net_income: 0 })
const pieChart = ref(null)
const lineChart = ref(null)
let pieInstance = null
let lineInstance = null
const currentTime = ref('')

const todayTodos = computed(() => {
  const todos = []
  if (stats.value.cleaning) todos.push({ text: `${stats.value.cleaning} 间房间待清洁`, color: '#f56c6c' })
  return todos
})

const financeItems = computed(() => [
  { label: '押金总额', value: paymentStats.value.total_deposit, color: '#e6a23c' },
  { label: '房费收入', value: paymentStats.value.total_payment, color: '#67c23a' },
  { label: '净收入', value: paymentStats.value.net_income, color: '#409eff' },
])

const fetchStats = async () => {
  const res = await request.get('/rooms/statusCount')
  stats.value = res.data
  nextTick(() => initPieChart())
}

const fetchRevenue = async () => {
  const res = await request.get('/bookings/revenue?days=7')
  nextTick(() => initLineChart(res.data))
}

const fetchPaymentStats = async () => {
  try {
    const res = await request.get('/payments/stats')
    paymentStats.value = res.data
  } catch (e) { /* payments table may not exist */ }
}

const initPieChart = () => {
  if (!pieChart.value) return
  if (!pieInstance) pieInstance = echarts.init(pieChart.value)
  pieInstance.setOption({
    tooltip: { trigger: 'item', formatter: '{b}: {c}间 ({d}%)' },
    series: [{
      type: 'pie',
      radius: ['45%', '68%'],
      label: { show: true, formatter: '{b}\n{c}间', fontSize: 12 },
      emphasis: { label: { fontSize: 14, fontWeight: 'bold' } },
      data: [
        { value: stats.value.available, name: '空闲', itemStyle: { color: '#67C23A' } },
        { value: stats.value.booked, name: '已预订', itemStyle: { color: '#E6A23C' } },
        { value: stats.value.occupied || 0, name: '已入住', itemStyle: { color: '#409EFF' } },
        { value: stats.value.cleaning || 0, name: '清洁中', itemStyle: { color: '#F56C6C' } },
      ],
    }],
  })
}

const initLineChart = (data) => {
  if (!lineChart.value) return
  if (!lineInstance) lineInstance = echarts.init(lineChart.value)
  lineInstance.setOption({
    tooltip: { trigger: 'axis', formatter: '{b}<br/>营业额: ¥{c}' },
    grid: { left: '3%', right: '4%', bottom: '3%', containLabel: true },
    xAxis: { type: 'category', data: data.map(d => d.date), axisLine: { lineStyle: { color: '#ddd' } } },
    yAxis: { type: 'value', axisLabel: { formatter: '¥{value}' }, splitLine: { lineStyle: { color: '#f0f0f0' } } },
    series: [{
      type: 'line', smooth: true, data: data.map(d => d.revenue),
      areaStyle: { color: { type: 'linear', x: 0, y: 0, x2: 0, y2: 1, colorStops: [{ offset: 0, color: 'rgba(64,158,255,0.3)' }, { offset: 1, color: 'rgba(64,158,255,0.05)' }] } },
      itemStyle: { color: '#409EFF' },
      lineStyle: { width: 3 },
    }],
  })
}

const handleResize = () => { pieInstance?.resize(); lineInstance?.resize() }

const updateTime = () => {
  const d = new Date()
  currentTime.value = `${d.getFullYear()}-${String(d.getMonth()+1).padStart(2,'0')}-${String(d.getDate()).padStart(2,'0')}`
}

onMounted(() => {
  updateTime()
  fetchStats()
  fetchRevenue()
  fetchPaymentStats()
  window.addEventListener('resize', handleResize)
})

onBeforeUnmount(() => {
  pieInstance?.dispose()
  lineInstance?.dispose()
  window.removeEventListener('resize', handleResize)
})
</script>

<style scoped>
.chart { width: 100%; height: 300px; }
.finance-item { text-align: center; padding: 8px 0; }
.finance-value { font-size: 22px; font-weight: 700; }
.finance-label { font-size: 13px; color: var(--text-secondary); margin-top: 4px; }
.todo-item { display: flex; align-items: center; gap: 10px; padding: 8px 0; border-bottom: 1px solid var(--border-color); }
.todo-item:last-child { border-bottom: none; }
.todo-dot { width: 8px; height: 8px; border-radius: 50%; flex-shrink: 0; }
.todo-text { font-size: 14px; color: var(--text-primary); }
</style>
