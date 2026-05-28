<template>
  <div>
    <div class="page-header">
      <h1 class="page-title">👑 会员管理</h1>
      <el-button type="primary" @click="openAddDialog">+ 新增会员</el-button>
    </div>

    <!-- 搜索 -->
    <div class="content-card search-card" style="margin-bottom: 20px; padding: 16px 20px">
      <el-form :model="searchForm" inline>
        <el-form-item label="搜索">
          <el-input v-model="searchForm.keyword" placeholder="姓名 / 手机号" clearable @keyup.enter="handleSearch" />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="handleSearch">搜索</el-button>
          <el-button @click="resetSearch">重置</el-button>
        </el-form-item>
      </el-form>
    </div>

    <!-- 会员列表 -->
    <el-table :data="members" style="width: 100%" v-loading="loading">
      <el-table-column prop="id" label="ID" width="60" />
      <el-table-column prop="name" label="姓名" width="100" />
      <el-table-column prop="phone" label="手机号" width="130" />
      <el-table-column prop="level" label="等级" width="100">
        <template #default="{ row }">
          <el-tag :type="levelType(row.level)" size="small">
            {{ levelText(row.level) }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="points" label="积分" width="80" />
      <el-table-column label="累计消费" width="120">
        <template #default="{ row }">¥{{ row.total_spent }}</template>
      </el-table-column>
      <el-table-column prop="id_card" label="身份证" width="160" />
      <el-table-column prop="email" label="邮箱" min-width="160" />
      <el-table-column label="操作" width="200" fixed="right">
        <template #default="{ row }">
          <el-button size="small" @click="openEditDialog(row)">编辑</el-button>
          <el-button size="small" @click="openPointsDialog(row)">积分</el-button>
          <el-button size="small" type="danger" @click="handleDelete(row.id)">删除</el-button>
        </template>
      </el-table-column>
    </el-table>

    <!-- 新增/编辑对话框 -->
    <el-dialog v-model="dialogVisible" :title="isEdit ? '编辑会员' : '新增会员'" width="450px">
      <el-form :model="form" label-width="80px">
        <el-form-item label="姓名">
          <el-input v-model="form.name" />
        </el-form-item>
        <el-form-item label="手机号">
          <el-input v-model="form.phone" :disabled="isEdit" />
        </el-form-item>
        <el-form-item label="身份证">
          <el-input v-model="form.id_card" />
        </el-form-item>
        <el-form-item label="邮箱">
          <el-input v-model="form.email" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="handleSave">保存</el-button>
      </template>
    </el-dialog>

    <!-- 积分调整对话框 -->
    <el-dialog v-model="pointsVisible" title="积分调整" width="400px">
      <p v-if="pointsMember" style="margin-bottom: 16px">
        当前积分: <strong>{{ pointsMember.points }}</strong>
        等级: <el-tag :type="levelType(pointsMember.level)" size="small">{{ levelText(pointsMember.level) }}</el-tag>
      </p>
      <el-form :model="pointsForm" label-width="80px">
        <el-form-item label="调整值">
          <el-input-number v-model="pointsForm.points" :min="-100000" :max="100000" style="width: 100%" />
          <span style="font-size: 12px; color: #909399">正数增加，负数扣除</span>
        </el-form-item>
        <el-form-item label="原因">
          <el-input v-model="pointsForm.reason" placeholder="如：入住奖励、消费积分" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="pointsVisible = false">取消</el-button>
        <el-button type="primary" @click="handlePoints">确认调整</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import request from '@/api/index.js'

const loading = ref(false)
const members = ref([])
const searchForm = ref({ keyword: '' })
const dialogVisible = ref(false)
const isEdit = ref(false)
const form = ref({ name: '', phone: '', id_card: '', email: '' })
const pointsVisible = ref(false)
const pointsMember = ref(null)
const pointsForm = ref({ points: 100, reason: '' })

const levelText = (l) => ({ 0: '普通会员', 1: '银卡会员', 2: '金卡会员', 3: '钻石会员' }[l] || '未知')
const levelType = (l) => ({ 0: 'info', 1: 'primary', 2: 'warning', 3: 'danger' }[l] || 'info')

const fetchMembers = async () => {
  loading.value = true
  try {
    const res = await request.get('/members/list')
    members.value = res.data || res
  } finally {
    loading.value = false
  }
}

const handleSearch = async () => {
  if (!searchForm.value.keyword) return fetchMembers()
  loading.value = true
  try {
    const res = await request.get('/members/search', { params: { keyword: searchForm.value.keyword } })
    members.value = res.data || res
  } finally {
    loading.value = false
  }
}

const resetSearch = () => {
  searchForm.value.keyword = ''
  fetchMembers()
}

const openAddDialog = () => {
  isEdit.value = false
  form.value = { name: '', phone: '', id_card: '', email: '' }
  dialogVisible.value = true
}

const openEditDialog = (row) => {
  isEdit.value = true
  form.value = { ...row }
  dialogVisible.value = true
}

const handleSave = async () => {
  if (isEdit.value) {
    await request.put('/members/update', form.value, { params: { member_id: form.value.id } })
    ElMessage.success('已更新')
  } else {
    await request.post('/members/add', form.value)
    ElMessage.success('注册成功')
  }
  dialogVisible.value = false
  fetchMembers()
}

const handleDelete = async (id) => {
  await ElMessageBox.confirm('确定删除该会员吗？')
  await request.delete('/members/delete', { params: { member_id: id } })
  ElMessage.success('已删除')
  fetchMembers()
}

const openPointsDialog = (row) => {
  pointsMember.value = row
  pointsForm.value = { points: 100, reason: '' }
  pointsVisible.value = true
}

const handlePoints = async () => {
  await request.put('/members/points', {
    member_id: pointsMember.value.id,
    points: pointsForm.value.points,
    reason: pointsForm.value.reason,
  })
  ElMessage.success('积分已调整')
  pointsVisible.value = false
  fetchMembers()
}

onMounted(fetchMembers)
</script>

<style scoped>
.page-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px; }
.page-title { font-size: 22px; margin: 0; }
.search-card { margin-bottom: 16px; }
</style>
