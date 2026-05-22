<template>
  <div>
    <h2 class="page-title">📊 运营数据看板</h2>

    <!-- 统计卡片 -->
    <el-row :gutter="16" class="stat-row">
      <el-col :span="3">
        <el-card shadow="hover" class="stat-card">
          <div class="stat-value" style="color: #67c23a">{{ stats.available }}</div>
          <div class="stat-label">空闲房间</div>
        </el-card>
      </el-col>
      <el-col :span="3">
        <el-card shadow="hover" class="stat-card">
          <div class="stat-value" style="color: #e6a23c">{{ stats.booked }}</div>
          <div class="stat-label">已预订</div>
        </el-card>
      </el-col>
      <el-col :span="3">
        <el-card shadow="hover" class="stat-card">
          <div class="stat-value" style="color: #409eff">{{ stats.occupied }}</div>
          <div class="stat-label">已入住</div>
        </el-card>
      </el-col>
      <el-col :span="3">
        <el-card shadow="hover" class="stat-card">
          <div class="stat-value" style="color: #f56c6c">{{ stats.cleaning || 0 }}</div>
          <div class="stat-label">清洁中</div>
        </el-card>
      </el-col>
      <el-col :span="3">
        <el-card shadow="hover" class="stat-card">
          <div class="stat-value" style="color: #909399">{{ totalRooms }}</div>
          <div class="stat-label">房间总数</div>
        </el-card>
      </el-col>
      <el-col :span="3">
        <el-card shadow="hover" class="stat-card">
          <div class="stat-value" style="color: #e6a23c">¥{{ paymentStats.total_deposit }}</div>
          <div class="stat-label">押金总额</div>
        </el-card>
      </el-col>
      <el-col :span="3">
        <el-card shadow="hover" class="stat-card">
          <div class="stat-value" style="color: #67c23a">¥{{ paymentStats.total_payment }}</div>
          <div class="stat-label">房费收入</div>
        </el-card>
      </el-col>
      <el-col :span="3">
        <el-card shadow="hover" class="stat-card">
          <div class="stat-value" style="color: #409eff">¥{{ paymentStats.net_income }}</div>
          <div class="stat-label">净收入</div>
        </el-card>
      </el-col>
    </el-row>

    <!-- 图表 -->
    <el-row :gutter="20">
      <el-col :span="10">
        <el-card class="chart-card">
          <template #header>房间状态分布</template>
          <div ref="pieChart" class="chart"></div>
        </el-card>
      </el-col>
      <el-col :span="14">
        <el-card class="chart-card">
          <template #header>近7天营业额趋势</template>
          <div ref="lineChart" class="chart"></div>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount, nextTick } from 'vue'
import * as echarts from 'echarts'
import request from '@/api/index.js'

const stats = ref({ available: 0, booked: 0, occupied: 0 })
const totalRooms = ref(0)
const paymentStats = ref({ total_deposit: 0, total_payment: 0, net_income: 0 })
const pieChart = ref(null)
const lineChart = ref(null)
let pieInstance = null
let lineInstance = null

const fetchStats = async () => {
  const res = await request.get('/rooms/statusCount')
  stats.value = res.data
  totalRooms.value = res.data.available + res.data.booked
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
  } catch (e) {
    // payments table may not exist yet
  }
}

const initPieChart = () => {
  if (!pieChart.value) return
  if (!pieInstance) pieInstance = echarts.init(pieChart.value)
  pieInstance.setOption({
    tooltip: { trigger: 'item' },
    series: [{
      type: 'pie',
      radius: ['50%', '70%'],
      data: [
        { value: stats.value.available, name: '空闲', itemStyle: { color: '#67C23A' } },
        { value: stats.value.booked, name: '已预订', itemStyle: { color: '#E6A23C' } },
        { value: stats.value.occupied || 0, name: '已入住', itemStyle: { color: '#409EFF' } },
        { value: stats.value.cleaning || 0, name: '清洁中', itemStyle: { color: '#F56C6C' } },
      ],
      label: { show: true, formatter: '{b}: {c}间' },
    }],
  })
}

const initLineChart = (data) => {
  if (!lineChart.value) return
  if (!lineInstance) lineInstance = echarts.init(lineChart.value)
  const dates = data.map((d) => d.date)
  const revenues = data.map((d) => d.revenue)
  lineInstance.setOption({
    tooltip: { trigger: 'axis', formatter: '{b}<br/>营业额: ¥{c}' },
    xAxis: { type: 'category', data: dates },
    yAxis: { type: 'value', axisLabel: { formatter: '¥{value}' } },
    series: [{
      type: 'line', smooth: true, data: revenues,
      areaStyle: { color: 'rgba(64,158,255,0.2)' },
      itemStyle: { color: '#409EFF' },
      lineStyle: { width: 3 },
    }],
  })
}

const handleResize = () => {
  pieInstance?.resize()
  lineInstance?.resize()
}

onMounted(() => {
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
.page-title { margin-bottom: 20px; font-size: 22px; }
.stat-row { margin-bottom: 20px; }
.stat-card { text-align: center; padding: 20px 0; }
.stat-value { font-size: 36px; font-weight: bold; }
.stat-label { font-size: 14px; color: #909399; margin-top: 8px; }
.chart-card { height: 400px; margin-bottom: 20px; }
.chart { width: 100%; height: 320px; }
</style>
