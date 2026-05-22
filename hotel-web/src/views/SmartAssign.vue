<template>
  <div>
    <div class="page-header">
      <h2 class="page-title">🧠 AI 智能排房</h2>
    </div>

    <el-row :gutter="20">
      <!-- 左侧：输入区 -->
      <el-col :span="8">
        <el-card class="input-card">
          <template #header>📝 客人需求</template>
          <el-form :model="form" label-width="100px">
            <el-form-item label="入住人数">
              <el-input-number v-model="form.guest_count" :min="1" :max="10" style="width: 100%" />
            </el-form-item>
            <el-form-item label="客人姓名">
              <el-input v-model="form.guest_name" placeholder="用于快速下单" />
            </el-form-item>
            <el-form-item label="手机号">
              <el-input v-model="form.phone" placeholder="选填" />
            </el-form-item>
            <el-form-item label="入住日期">
              <div style="display: flex; gap: 6px; width: 100%">
                <el-date-picker v-model="form.check_in" type="datetime" placeholder="选填" style="flex: 1" value-format="YYYY-MM-DD HH:mm:ss" />
                <el-button size="small" @click="form.check_in = nowStr()">Now</el-button>
              </div>
            </el-form-item>
            <el-form-item label="退房日期" v-if="form.check_in">
              <el-date-picker v-model="form.check_out" type="datetime" placeholder="可选，默认+1天" style="width: 100%" value-format="YYYY-MM-DD HH:mm:ss" />
            </el-form-item>
            <el-form-item label="偏好要求">
              <el-select v-model="form.preferences" style="width: 100%" placeholder="选择或输入">
                <el-option label="安静（高层/角落）" value="安静，高层，角落" />
                <el-option label="商务出行" value="商务，办公方便" />
                <el-option label="家庭亲子" value="亲子，空间大" />
                <el-option label="浪漫情侣" value="浪漫，情侣" />
                <el-option label="经济实惠" value="经济实惠，性价比高" />
              </el-select>
            </el-form-item>
            <el-form-item label="自定义偏好">
              <el-input v-model="form.custom_pref" placeholder="其他要求..." />
            </el-form-item>
            <el-form-item>
              <el-button type="primary" :loading="loading" size="large" style="width: 100%" @click="handleRecommend">
                <el-icon><Cpu /></el-icon> AI 智能推荐
              </el-button>
            </el-form-item>
          </el-form>
        </el-card>
      </el-col>

      <!-- 右侧：推荐结果 -->
      <el-col :span="16">
        <!-- AI 分析 -->
        <el-card v-if="analysis" class="analysis-card" shadow="hover">
          <template #header>💡 AI 分析</template>
          <p style="font-size: 15px; margin: 0">{{ analysis }}</p>
        </el-card>

        <!-- 空状态引导 -->
        <el-card v-if="!analysis && !loading" class="empty-card" shadow="hover">
          <div style="text-align: center; padding: 40px 0; color: #909399">
            <el-icon style="font-size: 64px; margin-bottom: 16px"><Cpu /></el-icon>
            <p style="font-size: 16px">填写左侧客人需求，点击「AI 智能推荐」</p>
            <p>系统将根据入住人数、偏好和房间情况，智能推荐最优房间</p>
          </div>
        </el-card>

        <!-- 推荐列表 -->
        <div v-if="suggestions.length" style="margin-top: 16px">
          <h3 style="margin: 0 0 12px">🏆 推荐方案（按优先级排序）</h3>
          <div v-for="(item, idx) in suggestions" :key="idx" class="rec-card" :class="'rec-rank-' + (idx + 1)">
            <div class="rec-rank">{{ idx + 1 }}</div>
            <div class="rec-body">
              <div class="rec-header">
                <span class="rec-room">房间 {{ item.room_number }}</span>
                <el-tag>{{ item.room_type }}</el-tag>
                <span class="rec-price">¥{{ item.price }}/晚</span>
                <el-tag :type="scoreType(item.score)" class="rec-score">评分 {{ item.score }}</el-tag>
              </div>
              <div class="rec-reason">{{ item.reason }}</div>
              <div class="rec-actions">
                <el-button size="small" type="primary" @click="handleQuickBook(item)">一键下单</el-button>
              </div>
            </div>
          </div>
        </div>
      </el-col>
    </el-row>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { ElMessage } from 'element-plus'
import request from '@/api/index.js'

const loading = ref(false)
const form = ref({
  guest_count: 1,
  guest_name: '',
  phone: '',
  check_in: '',
  check_out: '',
  preferences: '',
  custom_pref: '',
})
const analysis = ref('')
const suggestions = ref([])

const nowStr = () => {
  const d = new Date()
  const pad = (n) => String(n).padStart(2, '0')
  return `${d.getFullYear()}-${pad(d.getMonth()+1)}-${pad(d.getDate())} ${pad(d.getHours())}:${pad(d.getMinutes())}:${pad(d.getSeconds())}`
}

const preferences = computed(() => {
  const parts = []
  if (form.value.preferences) parts.push(form.value.preferences)
  if (form.value.custom_pref) parts.push(form.value.custom_pref)
  return parts.join('，')
})

const scoreType = (s) => {
  if (s >= 90) return 'success'
  if (s >= 70) return 'warning'
  return 'danger'
}

const handleRecommend = async () => {
  loading.value = true
  analysis.value = ''
  suggestions.value = []
  try {
    const pref = preferences.value
    const res = await request.get('/assign/recommend', {
      params: { guest_count: form.value.guest_count, preferences: pref || '无' },
    })
    if (res.code === 200) {
      analysis.value = res.data.analysis
      suggestions.value = res.data.suggestions || []
    } else {
      ElMessage.error(res.msg || '推荐失败')
    }
  } catch (e) {
    if (!e.response?.data) {
      ElMessage.error('AI 推荐请求失败')
    }
  } finally {
    loading.value = false
  }
}

const handleQuickBook = async (item) => {
  if (!form.value.guest_name) {
    ElMessage.warning('请填写客人姓名')
    return
  }
  if (!form.value.check_in) {
    ElMessage.warning('请填写入住日期')
    return
  }
  try {
    const params = {
      room_number: item.room_number,
      guest_name: form.value.guest_name,
      phone: form.value.phone || '待补充',
      check_in_date: form.value.check_in,
    }
    if (form.value.check_out) params.check_out_date = form.value.check_out
    const res = await request.post('/assign/book', null, { params })
    if (res.code === 200) {
      ElMessage.success(`🎉 ${res.msg}`)
    } else {
      ElMessage.error(res.msg)
    }
  } catch (e) {
    if (!e.response?.data) {
      ElMessage.error('下单失败: ' + (e.message || '未知错误'))
    }
  }
}
</script>

<style scoped>
.page-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px; }
.page-title { font-size: 22px; margin: 0; }
.input-card { margin-bottom: 20px; }
.analysis-card { background: #f0f9eb; border-color: #e1f3d8; margin-bottom: 0; }
.analysis-card p { color: #606266; }
.empty-card { margin-bottom: 20px; }

.rec-card {
  display: flex;
  border: 1px solid #ebeef5;
  border-radius: 8px;
  margin-bottom: 12px;
  overflow: hidden;
  transition: box-shadow 0.3s;
}
.rec-card:hover { box-shadow: 0 2px 12px rgba(0,0,0,0.1); }
.rec-rank-1 { border-left: 4px solid #e6a23c; }
.rec-rank-2 { border-left: 4px solid #909399; }
.rec-rank-3 { border-left: 4px solid #cd7f32; }

.rec-rank {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 48px;
  font-size: 24px;
  font-weight: bold;
  color: #fff;
}
.rec-rank-1 .rec-rank { background: #e6a23c; }
.rec-rank-2 .rec-rank { background: #909399; }
.rec-rank-3 .rec-rank { background: #cd7f32; }

.rec-body { flex: 1; padding: 14px 16px; }
.rec-header { display: flex; align-items: center; gap: 12px; margin-bottom: 8px; }
.rec-room { font-size: 18px; font-weight: bold; }
.rec-price { font-size: 16px; color: #e6a23c; font-weight: bold; }
.rec-score { margin-left: auto; }
.rec-reason { font-size: 14px; color: #606266; margin-bottom: 10px; }
.rec-actions { display: flex; gap: 8px; }
</style>
