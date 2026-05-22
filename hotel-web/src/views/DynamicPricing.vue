<template>
  <div>
    <div class="page-header">
      <h2 class="page-title">🤖 AI 动态定价</h2>
      <el-button type="primary" :loading="loading" @click="handleAnalyze">
        <el-icon><Cpu /></el-icon> AI 智能分析
      </el-button>
    </div>

    <!-- AI 分析结论 -->
    <el-card v-if="analysis" class="analysis-card" shadow="hover">
      <template #header>📈 AI 收益分析</template>
      <p style="font-size: 15px; margin: 0">{{ analysis }}</p>
    </el-card>

    <!-- 价格对比表 -->
    <h3 v-if="suggestions.length" style="margin: 20px 0 12px">💡 AI 建议价格</h3>
    <el-table :data="suggestions" border stripe style="width: 100%" v-if="suggestions.length">
      <el-table-column prop="room_type" label="房型" width="120" />
      <el-table-column label="房间数" width="80">
        <template #default="{ row }">{{ row.count }}间</template>
      </el-table-column>
      <el-table-column label="空闲" width="70">
        <template #default="{ row }">{{ row.available }}间</template>
      </el-table-column>
      <el-table-column label="入住率" width="100">
        <template #default="{ row }">
          <el-tag :type="occType(row.occupancy_rate)" size="small">
            {{ row.occupancy_rate }}%
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column label="当前价格" width="120">
        <template #default="{ row }">¥{{ row.current_price }}</template>
      </el-table-column>
      <el-table-column label="AI 建议价格" width="120">
        <template #default="{ row }">
          <span style="font-weight: bold; color: #e6a23c; font-size: 16px">
            ¥{{ row.suggested_price }}
          </span>
        </template>
      </el-table-column>
      <el-table-column label="调价幅度" width="120">
        <template #default="{ row }">
          <span :style="{ color: diffColor(row.current_price, row.suggested_price) }">
            {{ calcDiff(row.current_price, row.suggested_price) }}
          </span>
        </template>
      </el-table-column>
      <el-table-column label="理由" min-width="200">
        <template #default="{ row }">{{ row.reason }}</template>
      </el-table-column>
      <el-table-column label="操作" width="120">
        <template #default="{ row }">
          <el-button size="small" type="warning" @click="handleApply(row)">
            应用价格
          </el-button>
        </template>
      </el-table-column>
    </el-table>

    <!-- 调价历史 -->
    <h3 style="margin: 24px 0 12px">📜 调价历史</h3>
    <el-table :data="history" border stripe style="width: 100%">
      <el-table-column prop="room_type" label="房型" width="120" />
      <el-table-column label="原价" width="100">
        <template #default="{ row }">¥{{ row.old_price }}</template>
      </el-table-column>
      <el-table-column label="新价" width="100">
        <template #default="{ row }">¥{{ row.new_price }}</template>
      </el-table-column>
      <el-table-column prop="reason" label="调价原因" min-width="250" />
      <el-table-column prop="created_at" label="调价时间" width="170">
        <template #default="{ row }">{{ formatTime(row.created_at) }}</template>
      </el-table-column>
    </el-table>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import request from '@/api/index.js'

const loading = ref(false)
const analysis = ref('')
const suggestions = ref([])
const history = ref([])

const occType = (rate) => {
  if (rate >= 70) return 'danger'
  if (rate >= 40) return 'warning'
  return 'success'
}

const calcDiff = (oldP, newP) => {
  if (!oldP || !newP) return '-'
  const diff = ((newP - oldP) / oldP * 100).toFixed(1)
  return diff > 0 ? `+${diff}%` : `${diff}%`
}

const diffColor = (oldP, newP) => {
  if (!oldP || !newP) return '#909399'
  return newP >= oldP ? '#f56c6c' : '#67c23a'
}

const handleAnalyze = async () => {
  loading.value = true
  try {
    const res = await request.get('/pricing/analyze')
    if (res.code === 200) {
      analysis.value = res.data.analysis
      suggestions.value = res.data.suggestions || []
      ElMessage.success('AI 分析完成')
    } else {
      ElMessage.error(res.msg || '分析失败')
    }
  } catch (e) {
    ElMessage.error('AI 分析请求失败')
  } finally {
    loading.value = false
  }
}

const handleApply = async (item) => {
  try {
    const res = await request.post('/pricing/apply', {
      room_type: item.room_type,
      new_price: item.suggested_price,
      reason: item.reason,
    })
    if (res.code === 200) {
      ElMessage.success(res.msg)
      fetchHistory()
    } else {
      ElMessage.error(res.msg)
    }
  } catch (e) {
    ElMessage.error('调价失败')
  }
}

const fetchHistory = async () => {
  const res = await request.get('/pricing/history')
  history.value = res.data || res
}

const formatTime = (t) => t ? t.replace('T', ' ').slice(0, 16) : null

onMounted(fetchHistory)
</script>

<style scoped>
.page-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px; }
.page-title { font-size: 22px; margin: 0; }
.analysis-card { background: #f0f9eb; border-color: #e1f3d8; }
.analysis-card p { color: #606266; }
</style>
