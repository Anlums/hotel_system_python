<template>
  <div>
    <div class="page-header">
      <h2 class="page-title">🧹 保洁工单管理</h2>
    </div>

    <el-card class="tip-card" shadow="hover">
      <p>💡 退房时会自动生成保洁工单，房间状态变为「清洁中」。保洁完成后点击「完成」，房间恢复「空闲」。</p>
    </el-card>

    <!-- 待处理工单 -->
    <h3 style="margin: 16px 0 12px">待处理工单</h3>
    <el-table :data="pendingTasks" border stripe style="width: 100%">
      <el-table-column prop="id" label="工单号" width="80" />
      <el-table-column prop="room_number" label="房间号" width="100" />
      <el-table-column prop="status" label="状态" width="100">
        <template #default="{ row }">
          <el-tag :type="row.status === 0 ? 'danger' : 'warning'" size="small">
            {{ row.status === 0 ? '待清洁' : '清洁中' }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="assignee" label="保洁人员" width="120">
        <template #default="{ row }">
          <span v-if="row.assignee">{{ row.assignee }}</span>
          <el-input v-else v-model="assignInput[row.id]" placeholder="输入姓名" size="small" style="width: 100px" />
        </template>
      </el-table-column>
      <el-table-column prop="created_at" label="创建时间" width="170">
        <template #default="{ row }">{{ formatTime(row.created_at) }}</template>
      </el-table-column>
      <el-table-column label="操作" min-width="180">
        <template #default="{ row }">
          <el-button size="small" type="primary"
                     @click="handleAssign(row.id)"
                     v-if="!row.assignee && assignInput[row.id]">
            指派
          </el-button>
          <el-button size="small" type="success"
                     @click="handleComplete(row.id)"
                     v-if="row.status === 1 || row.assignee">
            完成清洁
          </el-button>
        </template>
      </el-table-column>
    </el-table>

    <!-- 已完成工单 -->
    <h3 style="margin: 24px 0 12px">历史记录</h3>
    <el-table :data="allTasks" border stripe style="width: 100%">
      <el-table-column prop="id" label="工单号" width="80" />
      <el-table-column prop="room_number" label="房间号" width="80" />
      <el-table-column prop="assignee" label="保洁员" width="100" />
      <el-table-column prop="status" label="状态" width="80">
        <template #default="{ row }">
          <el-tag :type="row.status === 2 ? 'success' : 'info'" size="small">
            {{ row.status === 2 ? '已完成' : row.status === 0 ? '待清洁' : '清洁中' }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="created_at" label="创建时间" width="170">
        <template #default="{ row }">{{ formatTime(row.created_at) }}</template>
      </el-table-column>
      <el-table-column prop="completed_at" label="完成时间" width="170">
        <template #default="{ row }">{{ formatTime(row.completed_at) || '-' }}</template>
      </el-table-column>
    </el-table>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import request from '@/api/index.js'

const allTasks = ref([])
const pendingTasks = ref([])
const assignInput = ref({})

const fetchAll = async () => {
  const res = await request.get('/cleaning/list')
  allTasks.value = res.data
  const res2 = await request.get('/cleaning/pending')
  pendingTasks.value = res2.data
}

const handleAssign = async (taskId) => {
  const name = assignInput.value[taskId]
  if (!name) return ElMessage.warning('请输入保洁人员姓名')
  await request.put(`/cleaning/assign?task_id=${taskId}&assignee=${encodeURIComponent(name)}`)
  ElMessage.success('已指派')
  assignInput.value[taskId] = ''
  fetchAll()
}

const handleComplete = async (taskId) => {
  await request.put(`/cleaning/complete?task_id=${taskId}`)
  ElMessage.success('清洁完成，房间已恢复空闲')
  fetchAll()
}

const formatTime = (t) => t ? t.replace('T', ' ').slice(0, 16) : null

onMounted(fetchAll)
</script>

<style scoped>
.page-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px; }
.page-title { font-size: 22px; margin: 0; }
.tip-card { background: #ecf5ff; border-color: #d9ecff; }
.tip-card p { margin: 0; color: #606266; font-size: 14px; }
</style>
