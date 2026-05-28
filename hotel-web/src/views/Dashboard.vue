<template>
  <div class="page-enter">
    <div class="page-header">
      <h1 class="page-title">天玺御览</h1>
      <span style="font-size:12px;color:var(--text-muted);letter-spacing:0.08em">{{ currentTime }}</span>
    </div>

    <!-- 流光 KPI 卡片 -->
    <el-row :gutter="20" style="margin-bottom: 24px">
      <el-col :span="6" v-for="item in kpiData" :key="item.label">
        <div class="kpi-card" :class="item.cls">
          <div class="kpi-icon">{{ item.icon }}</div>
          <div class="kpi-value count-animate">{{ item.value }}</div>
          <div class="kpi-label">{{ item.label }}</div>
        </div>
      </el-col>
    </el-row>

    <!-- 图表 -->
    <el-row :gutter="20" style="margin-bottom: 24px">
      <el-col :span="10">
        <div class="content-card" style="height: 380px">
          <div style="font-size:13px;font-weight:600;margin-bottom:12px;color:var(--gold);letter-spacing:0.1em">🏠 房间状态分布</div>
          <div ref="pieChart" class="chart"></div>
        </div>
      </el-col>
      <el-col :span="14">
        <div class="content-card" style="height: 380px">
          <div style="font-size:13px;font-weight:600;margin-bottom:12px;color:var(--gold);letter-spacing:0.1em">📈 营业收入趋势</div>
          <div ref="lineChart" class="chart"></div>
        </div>
      </el-col>
    </el-row>

    <!-- 财务概览 -->
    <el-row :gutter="20">
      <el-col :span="12">
        <div class="content-card">
          <div style="font-size:13px;font-weight:600;margin-bottom:16px;color:var(--gold);letter-spacing:0.1em">💰 财务概览</div>
          <el-row :gutter="16">
            <el-col :span="8" v-for="item in financeItems" :key="item.label">
              <div class="finance-item">
                <div class="finance-value" style="color:var(--gold)">¥{{ item.value }}</div>
                <div class="finance-label">{{ item.label }}</div>
              </div>
            </el-col>
          </el-row>
        </div>
      </el-col>
      <el-col :span="12">
        <div class="content-card">
          <div style="font-size:13px;font-weight:600;margin-bottom:16px;color:var(--gold);letter-spacing:0.1em">📋 今日待办</div>
          <div v-if="todayTodos.length === 0" style="color:var(--text-muted);font-size:13px;padding:12px 0">— 暂无待办事项 —</div>
          <div v-for="todo in todayTodos" :key="todo.text" class="todo-item">
            <span class="todo-dot breathe" :style="{background:todo.color}"></span>
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

const kpiData = computed(() => [
  { icon: '🟢', value: stats.value.available, label: '空闲客房', cls: 'kpi-available' },
  { icon: '🔷', value: stats.value.booked, label: '已预订', cls: 'kpi-booked' },
  { icon: '⭐', value: stats.value.occupied, label: '已入住', cls: 'kpi-occupied' },
  { icon: '🔶', value: stats.value.cleaning || 0, label: '清洁中', cls: 'kpi-cleaning' },
])

const todayTodos = computed(() => {
  const todos = []
  if (stats.value.cleaning) todos.push({ text: `${stats.value.cleaning} 间客房待清洁`, color: '#8B1A1A' })
  return todos
})

const financeItems = computed(() => [
  { label: '押金总额', value: paymentStats.value.total_deposit },
  { label: '房费收入', value: paymentStats.value.total_payment },
  { label: '净收入', value: paymentStats.value.net_income },
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
  try { const res = await request.get('/payments/stats'); paymentStats.value = res.data } catch {}
}

const initPieChart = () => {
  if (!pieChart.value) return
  if (!pieInstance) pieInstance = echarts.init(pieChart.value, null, { renderer: 'svg' })
  pieInstance.setOption({
    tooltip: { trigger: 'item', formatter: '{b}: {c} 间' },
    series: [{
      type: 'pie', radius: ['42%', '68%'],
      label: { show: true, formatter: '{b}\n{c}', fontSize: 11, color: '#8B8982' },
      labelLine: { lineStyle: { color: 'rgba(212,175,55,0.15)' } },
      data: [
        { value: stats.value.available, name: '空闲', itemStyle: { color: new echarts.graphic.LinearGradient(0,0,0,1, [{offset:0,color:'#2E7D32'},{offset:1,color:'#1B5E20'}]) } },
        { value: stats.value.booked, name: '已预订', itemStyle: { color: new echarts.graphic.LinearGradient(0,0,0,1, [{offset:0,color:'#1565C0'},{offset:1,color:'#0D47A1'}]) } },
        { value: stats.value.occupied || 0, name: '已入住', itemStyle: { color: new echarts.graphic.LinearGradient(0,0,0,1, [{offset:0,color:'#D4AF37'},{offset:1,color:'#B8860B'}]) } },
        { value: stats.value.cleaning || 0, name: '清洁中', itemStyle: { color: new echarts.graphic.LinearGradient(0,0,0,1, [{offset:0,color:'#8B1A1A'},{offset:1,color:'#5C1010'}]) } },
      ],
    }],
  })
}

const initLineChart = (data) => {
  if (!lineChart.value || !data.length) return
  if (!lineInstance) lineInstance = echarts.init(lineChart.value, null, { renderer: 'svg' })
  lineInstance.setOption({
    tooltip: { trigger: 'axis', formatter: '{b}<br/>营收: ¥{c}' },
    grid: { left: '3%', right: '4%', bottom: '3%', containLabel: true },
    xAxis: { type: 'category', data: data.map(d => d.date), axisLine: { show: false }, axisTick: { show: false }, axisLabel: { color: '#5A5955', fontSize: 11 } },
    yAxis: { type: 'value', splitLine: { lineStyle: { color: 'rgba(255,255,255,0.03)' } }, axisLabel: { color: '#5A5955', fontSize: 11, formatter: '¥{value}' } },
    series: [{
      type: 'line', smooth: true, data: data.map(d => d.revenue),
      symbol: 'circle', symbolSize: 6,
      lineStyle: { color: '#D4AF37', width: 2.5 },
      itemStyle: { color: '#D4AF37' },
      areaStyle: { color: { type: 'linear', x: 0, y: 0, x2: 0, y2: 1, colorStops: [{ offset: 0, color: 'rgba(212,175,55,0.2)' }, { offset: 1, color: 'rgba(212,175,55,0)' }] } },
    }],
  })
}

const handleResize = () => { pieInstance?.resize(); lineInstance?.resize() }

const updateTime = () => {
  const d = new Date()
  currentTime.value = `${d.getFullYear()}.${String(d.getMonth()+1).padStart(2,'0')}.${String(d.getDate()).padStart(2,'0')}`
}

onMounted(() => { updateTime(); fetchStats(); fetchRevenue(); fetchPaymentStats(); window.addEventListener('resize', handleResize) })
onBeforeUnmount(() => { pieInstance?.dispose(); lineInstance?.dispose(); window.removeEventListener('resize', handleResize) })
</script>

<style scoped>
.chart { width: 100%; height: 300px; }
.finance-item { text-align: center; padding: 12px 0; }
.finance-value { font-size: 24px; font-weight: 700; }
.finance-label { font-size: 12px; color: var(--text-muted); margin-top: 6px; letter-spacing: 0.08em; }
.todo-item { display: flex; align-items: center; gap: 10px; padding: 10px 0; border-bottom: 1px solid var(--border-subtle); }
.todo-item:last-child { border-bottom: none; }
.todo-dot { width: 6px; height: 6px; border-radius: 50%; flex-shrink: 0; }
.todo-text { font-size: 13px; color: var(--text-secondary); }
</style>
