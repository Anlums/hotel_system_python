<template>
  <div>
    <div class="page-header">
      <h1 class="page-title">💰 支付结算</h1>
    </div>

    <!-- 统计卡片 -->
    <el-row :gutter="16" class="stat-row">
      <el-col :span="6">
        <el-card shadow="hover" class="stat-card">
          <div class="stat-value" style="color: #e6a23c">¥{{ stats.total_deposit }}</div>
          <div class="stat-label">押金总额</div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card shadow="hover" class="stat-card">
          <div class="stat-value" style="color: #67c23a">¥{{ stats.total_payment }}</div>
          <div class="stat-label">房费收入</div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card shadow="hover" class="stat-card">
          <div class="stat-value" style="color: #f56c6c">¥{{ stats.total_refund }}</div>
          <div class="stat-label">已退款</div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card shadow="hover" class="stat-card">
          <div class="stat-value" style="color: #409eff">¥{{ stats.net_income }}</div>
          <div class="stat-label">净收入</div>
        </el-card>
      </el-col>
    </el-row>

    <!-- 搜索 -->
    <div class="content-card search-card" style="margin-bottom: 20px; padding: 16px 20px">
      <el-form :inline="true">
        <el-form-item label="订单ID">
          <el-input-number v-model="searchBookingId" :min="0" placeholder="按订单号筛选" clearable style="width: 160px" />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="fetchPayments">查询</el-button>
          <el-button @click="searchBookingId = null; fetchPayments()">全部</el-button>
        </el-form-item>
      </el-form>
    </div>

    <!-- 支付记录表 -->
    <el-table :data="payments" style="width: 100%" v-loading="loading">
      <el-table-column prop="id" label="ID" width="60" />
      <el-table-column prop="booking_id" label="订单ID" width="80" />
      <el-table-column label="类型" width="100">
        <template #default="{ row }">
          <el-tag :type="typeTag(row.type)" size="small">{{ typeText(row.type) }}</el-tag>
        </template>
      </el-table-column>
      <el-table-column label="金额" width="120">
        <template #default="{ row }">
          <span :style="{ color: row.amount >= 0 ? '#67c23a' : '#f56c6c', fontWeight: 'bold' }">
            {{ row.amount >= 0 ? '+' : '' }}¥{{ row.amount }}
          </span>
        </template>
      </el-table-column>
      <el-table-column prop="method" label="支付方式" width="100">
        <template #default="{ row }"> {{ methodText(row.method) }} </template>
      </el-table-column>
      <el-table-column prop="status" label="状态" width="90">
        <template #default="{ row }">
          <el-tag :type="row.status === 'completed' ? 'success' : 'info'" size="small">
            {{ row.status === 'completed' ? '已完成' : '已退款' }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="remark" label="备注" min-width="200" />
      <el-table-column prop="operator" label="操作人" width="80" />
      <el-table-column prop="created_at" label="时间" width="160">
        <template #default="{ row }">{{ formatTime(row.created_at) }}</template>
      </el-table-column>
    </el-table>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import request from '@/api/index.js'

const loading = ref(false)
const payments = ref([])
const stats = ref({ total_deposit: 0, total_payment: 0, total_refund: 0, net_income: 0 })
const searchBookingId = ref(null)

const typeText = (t) => ({ deposit: '押金', payment: '房费', refund: '退款' }[t] || t)
const typeTag = (t) => ({ deposit: 'warning', payment: 'success', refund: 'danger' }[t] || 'info')
const methodText = (m) => ({ cash: '现金', wechat: '微信', alipay: '支付宝', card: '银行卡' }[m] || m)

const fetchPayments = async () => {
  loading.value = true
  try {
    const params = {}
    if (searchBookingId.value) params.booking_id = searchBookingId.value
    const res = await request.get('/payments/list', { params })
    payments.value = res.data
  } finally {
    loading.value = false
  }
}

const fetchStats = async () => {
  const res = await request.get('/payments/stats')
  stats.value = res.data
}

const formatTime = (t) => t ? t.replace('T', ' ').slice(0, 16) : '-'

onMounted(() => {
  fetchPayments()
  fetchStats()
})
</script>

<style scoped>
.page-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px; }
.page-title { font-size: 22px; margin: 0; }
.stat-row { margin-bottom: 20px; }
.stat-card { text-align: center; padding: 20px 0; }
.stat-value { font-size: 32px; font-weight: bold; }
.stat-label { font-size: 14px; color: #909399; margin-top: 8px; }
.search-card { margin-bottom: 16px; }
</style>
