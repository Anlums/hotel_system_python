<template>
  <div class="ai-page">
    <h2 class="page-title">🤖 AI 智能管家</h2>
    <el-card class="chat-card">
      <!-- 消息列表 -->
      <div class="message-list" ref="msgList">
        <div v-for="(msg, i) in aiStore.messages" :key="i"
             :class="['message', msg.role === 'user' ? 'user-msg' : 'ai-msg']">
          <div class="msg-label">{{ msg.role === 'user' ? '👤 您' : '🤖 管家' }}</div>
          <div class="msg-content">{{ msg.content }}</div>
        </div>
        <div v-if="loading" class="message ai-msg">
          <div class="msg-label">🤖 管家</div>
          <div class="msg-content">正在思考...</div>
        </div>
      </div>

      <!-- 输入区 -->
      <div class="input-area">
        <el-input
          v-model="inputText"
          type="textarea"
          :rows="3"
          placeholder="请输入您的需求，例如：帮我推荐一间安静的房间..."
          :disabled="loading"
        />
        <el-button type="primary" class="send-btn" @click="sendMessage" :loading="loading">
          {{ loading ? '思考中...' : '发送' }}
        </el-button>
      </div>
    </el-card>
  </div>
</template>

<script setup>
import { ref, nextTick, watch, onMounted } from 'vue'
import request from '@/api/index.js'
import { aiStore } from '@/stores/ai.js'

const inputText = ref('')
const loading = ref(false)
const msgList = ref(null)

const scrollBottom = () => {
  nextTick(() => {
    if (msgList.value) {
      msgList.value.scrollTop = msgList.value.scrollHeight
    }
  })
}

// 每次有新消息自动滚到底
watch(() => aiStore.messages.length, () => scrollBottom())

// 页面挂载时也滚到底（切换页面回来时）
onMounted(() => scrollBottom())

const sendMessage = async () => {
  if (!inputText.value.trim() || loading.value) return
  const text = inputText.value
  aiStore.messages.push({ role: 'user', content: text })
  inputText.value = ''
  loading.value = true

  try {
    // 把完整对话历史发给后端
    const res = await request.post('/agent/chat', { messages: aiStore.messages })
    aiStore.messages.push({ role: 'assistant', content: res.content })
  } catch {
    aiStore.messages.push({ role: 'assistant', content: 'AI 服务暂时不可用，请稍后再试。' })
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.page-title { font-size: 22px; margin-bottom: 20px; }
.chat-card { height: calc(100vh - 120px); display: flex; flex-direction: column; }
.message-list { flex: 1; overflow-y: auto; padding: 16px; margin-bottom: 16px;
  background: #fafafa; border-radius: 8px; }
.message { margin-bottom: 16px; max-width: 80%; }
.user-msg { margin-left: auto; text-align: right; }
.ai-msg { margin-right: auto; }
.msg-label { font-size: 12px; color: #909399; margin-bottom: 4px; }
.msg-content { display: inline-block; padding: 10px 16px; border-radius: 12px;
  font-size: 14px; line-height: 1.6; white-space: pre-wrap; text-align: left; }
.user-msg .msg-content { background: #409eff; color: #fff; border-bottom-right-radius: 4px; }
.ai-msg .msg-content { background: #fff; color: #303133; border: 1px solid #e4e7ed;
  border-bottom-left-radius: 4px; }
.input-area { display: flex; gap: 12px; align-items: flex-end; }
.send-btn { height: 75px; width: 100px; }
</style>
