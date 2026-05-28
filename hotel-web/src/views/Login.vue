<template>
  <div class="login-wrapper">
    <!-- 左侧展示区 -->
    <div class="login-showcase">
      <div class="showcase-content">
        <div class="showcase-brand">TIAN XI MANSION</div>
        <div class="showcase-tagline">栖于山海 · 尊享非凡</div>
      </div>
    </div>

    <!-- 右侧登录面板 -->
    <div class="login-panel">
      <div class="panel-inner">
        <div class="login-header">
          <svg class="login-logo" width="44" height="44" viewBox="0 0 48 48" fill="none">
            <path d="M24 4L44 16v16L24 44 4 32V16L24 4z" stroke="url(#gold-grad)" stroke-width="1.5" fill="none"/>
            <path d="M24 12L36 20v8L24 36 12 28V20L24 12z" stroke="url(#gold-grad)" stroke-width="1" fill="none" opacity="0.6"/>
            <line x1="24" y1="4" x2="24" y2="44" stroke="url(#gold-grad)" stroke-width="0.5" opacity="0.3"/>
            <line x1="4" y1="24" x2="44" y2="24" stroke="url(#gold-grad)" stroke-width="0.5" opacity="0.3"/>
            <defs>
              <linearGradient id="gold-grad" x1="0" y1="0" x2="1" y2="1">
                <stop offset="0%" stop-color="#D4AF37"/>
                <stop offset="100%" stop-color="#F3E5AB"/>
              </linearGradient>
            </defs>
          </svg>
          <h2>天玺尊邸</h2>
          <p class="login-subtitle">后台运营管理平台</p>
        </div>

        <el-form :model="form" @submit.prevent="handleLogin" label-width="0" class="login-form">
          <el-form-item>
            <div class="input-wrap">
              <span class="input-icon">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M20 21v-2a4 4 0 00-4-4H8a4 4 0 00-4 4v2"/><circle cx="12" cy="7" r="4"/></svg>
              </span>
              <el-input v-model="form.username" placeholder="管理员账号" size="large" />
            </div>
          </el-form-item>
          <el-form-item>
            <div class="input-wrap">
              <span class="input-icon">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><rect x="3" y="11" width="18" height="11" rx="2" ry="2"/><path d="M7 11V7a5 5 0 0110 0v4"/></svg>
              </span>
              <el-input v-model="form.password" type="password" placeholder="管理权限密码" size="large" show-password />
            </div>
          </el-form-item>
          <el-form-item>
            <label class="remember-me">
              <input type="checkbox" v-model="remember" />
              <span class="checkmark"></span>
              记住账号
            </label>
          </el-form-item>
          <el-form-item>
            <button type="submit" class="login-btn" :disabled="loading">
              <span v-if="!loading">进入管理台</span>
              <span v-else class="btn-loading">
                <svg class="spinner" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><circle cx="12" cy="12" r="10" stroke-dasharray="31.4" stroke-dashoffset="0"/></svg>
                验证中
              </span>
            </button>
          </el-form-item>
        </el-form>

        <div class="login-footer">
          <span>Copyright © TIAN XI MANSION</span>
          <span>System v1.0.2</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { ElMessage } from 'element-plus'

const emit = defineEmits(['login-success'])
const loading = ref(false)
const remember = ref(false)
const form = reactive({ username: '', password: '' })

onMounted(() => {
  const saved = localStorage.getItem('remembered_user')
  if (saved) { form.username = saved; remember.value = true }
})

const handleLogin = async () => {
  if (!form.username || !form.password) {
    ElMessage.warning('请输入用户名和密码')
    return
  }
  loading.value = true
  try {
    const { default: axios } = await import('axios')
    const res = await axios.post('/api/auth/login', { username: form.username, password: form.password })
    const data = res.data
    if (data.code === 200) {
      localStorage.setItem('token', data.data.token)
      localStorage.setItem('username', data.data.username)
      if (remember.value) localStorage.setItem('remembered_user', form.username)
      else localStorage.removeItem('remembered_user')
      emit('login-success')
    } else {
      ElMessage.error(data.msg || '登录失败')
    }
  } catch (e) {
    ElMessage.error(e.response?.data?.msg || '登录失败: ' + (e.message || '未知错误'))
  } finally { loading.value = false }
}
</script>

<style scoped>
html, body { margin: 0; padding: 0; height: 100%; }

.login-wrapper {
  display: flex;
  min-height: 100vh;
  width: 100%;
  background:
    linear-gradient(135deg, rgba(10, 15, 30, 0.4) 0%, rgba(30, 20, 10, 0.2) 50%, rgba(10, 15, 30, 0.6) 100%),
    url('@/assets/bg.png') center/cover no-repeat;
}

/* ========== 左侧展示区 ========== */
.login-showcase {
  flex: 1;
  display: flex;
  align-items: flex-end;
  padding: 48px;
}
.showcase-content { margin-bottom: 48px; }
.showcase-brand {
  font-size: 14px;
  color: rgba(255, 255, 255, 0.4);
  letter-spacing: 0.3em;
  margin-bottom: 8px;
}
.showcase-tagline {
  font-size: 20px;
  color: rgba(255, 255, 255, 0.15);
  letter-spacing: 0.15em;
  font-style: italic;
}

/* ========== 右侧登录面板 ========== */
.login-panel {
  width: 400px;
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(8, 10, 18, 0.55);
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  border-left: 1px solid rgba(255, 255, 255, 0.06);
}
.panel-inner {
  width: 100%;
  padding: 48px 40px;
}

/* 头部 */
.login-header { text-align: center; margin-bottom: 36px; }
.login-logo { margin-bottom: 14px; }
.login-header h2 {
  margin: 0 0 6px;
  font-size: 22px;
  font-weight: 600;
  color: #fff;
  letter-spacing: 0.18em;
}
.login-subtitle {
  margin: 0;
  font-size: 12px;
  color: rgba(255, 255, 255, 0.35);
  letter-spacing: 0.12em;
}

/* 输入框 - 深色半透明石板 */
.input-wrap {
  position: relative;
  width: 100%;
}
.input-icon {
  position: absolute;
  left: 16px;
  top: 50%;
  transform: translateY(-50%);
  color: rgba(255, 255, 255, 0.2);
  z-index: 1;
  pointer-events: none;
  transition: color 0.3s;
}
:deep(.el-input__wrapper) {
  background: rgba(18, 20, 30, 0.6) !important;
  border: 1px solid rgba(255, 255, 255, 0.06) !important;
  border-radius: 10px !important;
  box-shadow: none !important;
  padding: 6px 16px 6px 46px !important;
  transition: all 0.35s !important;
}
:deep(.el-input__wrapper:hover) {
  border-color: rgba(255, 255, 255, 0.12) !important;
  background: rgba(18, 20, 30, 0.7) !important;
}
:deep(.el-input__wrapper.is-focus) {
  border-color: rgba(212, 175, 55, 0.4) !important;
  background: rgba(18, 20, 30, 0.8) !important;
  box-shadow: 0 0 24px rgba(212, 175, 55, 0.06) !important;
}
:deep(.el-input__inner) {
  color: rgba(255, 255, 255, 0.9) !important;
  font-family: inherit;
  letter-spacing: 0.04em;
  font-size: 14px !important;
}
:deep(.el-input__inner::placeholder) {
  color: rgba(255, 255, 255, 0.2) !important;
  font-size: 13px;
}

/* 记住账号 */
.remember-me {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 12px;
  color: rgba(255, 255, 255, 0.35);
  cursor: pointer;
  transition: color 0.2s;
  user-select: none;
}
.remember-me:hover { color: rgba(255, 255, 255, 0.55); }
.remember-me input { display: none; }
.checkmark {
  width: 15px; height: 15px;
  border: 1px solid rgba(255, 255, 255, 0.15);
  border-radius: 4px;
  transition: all 0.2s;
  position: relative;
  flex-shrink: 0;
}
.remember-me input:checked + .checkmark {
  background: var(--gold);
  border-color: var(--gold);
}
.remember-me input:checked + .checkmark::after {
  content: '';
  position: absolute;
  left: 4px; top: 1px;
  width: 5px; height: 9px;
  border: solid #0B0C10;
  border-width: 0 2px 2px 0;
  transform: rotate(45deg);
}

/* 登录按钮 - 金色流光 */
.login-btn {
  width: 100%;
  padding: 12px;
  background: linear-gradient(135deg, #D4AF37, #B8860B, #D4AF37);
  background-size: 200% 100%;
  border: none;
  border-radius: 10px;
  color: #0B0C10;
  font-size: 14px;
  font-weight: 600;
  letter-spacing: 0.18em;
  cursor: pointer;
  transition: all 0.4s;
  font-family: inherit;
  animation: shimmer 3s ease-in-out infinite;
}
.login-btn:hover {
  transform: scale(1.02);
  box-shadow: 0 0 30px rgba(212, 175, 55, 0.25);
}
.login-btn:active { transform: scale(0.98); }
.login-btn:disabled { opacity: 0.5; cursor: not-allowed; transform: none; }
@keyframes shimmer {
  0%, 100% { background-position: 0% 50%; }
  50% { background-position: 100% 50%; }
}

.btn-loading {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
}
.spinner { animation: spin 1s linear infinite; }
@keyframes spin { to { transform: rotate(360deg); } }

/* 底部版权 */
.login-footer {
  display: flex;
  justify-content: space-between;
  margin-top: 36px;
  font-size: 10px;
  color: rgba(255, 255, 255, 0.12);
  letter-spacing: 0.06em;
}

/* 响应式 */
@media (max-width: 768px) {
  .login-showcase { display: none; }
  .login-panel { width: 100%; min-height: 100vh; }
  .panel-inner { padding: 40px 28px; }
}
</style>
