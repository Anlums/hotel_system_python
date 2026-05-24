<template>
  <div class="login-wrapper">
    <div class="login-card">
      <div class="login-header">
        <div class="login-icon">🏨</div>
        <h2>天玺尊邸酒店管理系统</h2>
        <p class="login-subtitle">请登录以继续</p>
      </div>
      <el-form :model="form" @submit.prevent="handleLogin" label-width="0">
        <el-form-item>
          <el-input v-model="form.username" placeholder="用户名" size="large" prefix-icon="User" />
        </el-form-item>
        <el-form-item>
          <el-input v-model="form.password" type="password" placeholder="密码" size="large" prefix-icon="Lock" show-password />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" size="large" style="width: 100%" :loading="loading" native-type="submit">
            登 录
          </el-button>
        </el-form-item>
      </el-form>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { ElMessage } from 'element-plus'
import request from '@/api/index.js'

const emit = defineEmits(['login-success'])
const loading = ref(false)
const form = reactive({ username: '', password: '' })

const handleLogin = async () => {
  if (!form.username || !form.password) {
    ElMessage.warning('请输入用户名和密码')
    return
  }
  loading.value = true
  try {
    // 直接调 axios（不经过拦截器的 baseURL，因为登录不需要 token）
    const { default: axios } = await import('axios')
    const res = await axios.post('/api/auth/login', { username: form.username, password: form.password })
    const data = res.data
    if (data.code === 200) {
      localStorage.setItem('token', data.data.token)
      localStorage.setItem('username', data.data.username)
      emit('login-success')
    } else {
      ElMessage.error(data.msg || '登录失败')
    }
  } catch (e) {
    if (e.response?.data?.msg) {
      ElMessage.error(e.response.data.msg)
    } else {
      ElMessage.error('登录失败: ' + (e.message || '未知错误'))
    }
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.login-wrapper {
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 100vh;
  background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
}
.login-card {
  width: 400px;
  padding: 40px;
  background: #fff;
  border-radius: 12px;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
}
.login-header {
  text-align: center;
  margin-bottom: 30px;
}
.login-icon {
  font-size: 48px;
  margin-bottom: 10px;
}
.login-header h2 {
  margin: 0 0 8px;
  font-size: 22px;
  color: #303133;
}
.login-subtitle {
  margin: 0;
  font-size: 14px;
  color: #909399;
}
</style>
