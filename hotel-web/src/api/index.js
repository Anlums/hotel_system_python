import axios from 'axios'
import { ElMessage } from 'element-plus'

const request = axios.create({
  baseURL: '/api',
  timeout: 30000,
})

// 请求拦截器：自动带 token
request.interceptors.request.use((config) => {
  const token = localStorage.getItem('token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

// 响应拦截器：统一处理错误
request.interceptors.response.use(
  (response) => {
    const res = response.data
    // 401 → 跳回登录页
    if (response.status === 401 || res.code === 401) {
      localStorage.removeItem('token')
      localStorage.removeItem('username')
      window.location.reload()
      return Promise.reject(new Error(res.msg || '未登录'))
    }
    if (res.code !== undefined && res.code !== 200) {
      ElMessage.error(res.msg || '请求失败')
      return Promise.reject(new Error(res.msg))
    }
    return res
  },
  (error) => {
    // 401 未登录 → 跳回登录页
    if (error.response?.status === 401) {
      localStorage.removeItem('token')
      localStorage.removeItem('username')
      window.location.reload()
      return Promise.reject(error)
    }
    // 有响应但非 2xx（如 500）→ 展示后端返回的 msg
    if (error.response?.data) {
      const res = error.response.data
      ElMessage.error(res.msg || res.detail?.[0]?.msg || '请求失败')
      return Promise.reject(error)
    }
    // 无响应（网络中断、超时等）
    ElMessage.error('网络错误: ' + (error.message || '未知错误'))
    return Promise.reject(error)
  }
)

export default request
