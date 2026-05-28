<template>
  <div class="page-enter">
    <div class="page-header">
      <h1 class="page-title">天玺首席 · 灵犀阁</h1>
    </div>

    <div class="chat-container content-card">
      <!-- 消息列表 -->
      <div class="message-list" ref="msgList">
        <div v-for="(msg, i) in aiStore.messages" :key="i"
             :class="['message', msg.role === 'user' ? 'user-msg' : 'ai-msg']">
          <div class="msg-label">{{ msg.role === 'user' ? '您' : '天玺管家' }}</div>
          <div class="msg-content">{{ msg.content }}</div>
        </div>
        <div v-if="loading" class="message ai-msg">
          <div class="msg-label">天玺管家</div>
          <div class="msg-content thinking-dots">思考中<span>.</span><span>.</span><span>.</span></div>
        </div>
      </div>

      <!-- 输入区 -->
      <div class="input-area">
        <el-input
          v-model="inputText"
          placeholder="请输入需求，如：推荐一间安静的房间..."
          :disabled="loading"
          @keyup.enter="sendMessage"
          clearable
        />
        <button class="send-btn" @click="sendMessage" :disabled="loading || !inputText.trim()">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="22" y1="2" x2="11" y2="13"/><polygon points="22 2 15 22 11 13 2 9 22 2"/></svg>
        </button>
      </div>
    </div>
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
  nextTick(() => { if (msgList.value) msgList.value.scrollTop = msgList.value.scrollHeight })
}

watch(() => aiStore.messages.length, () => scrollBottom())
onMounted(() => scrollBottom())

const sendMessage = async () => {
  if (!inputText.value.trim() || loading.value) return
  const text = inputText.value
  aiStore.messages.push({ role: 'user', content: text })
  inputText.value = ''
  loading.value = true
  try {
    const res = await request.post('/agent/chat', { messages: aiStore.messages })
    aiStore.messages.push({ role: 'assistant', content: res.content })
  } catch {
    aiStore.messages.push({ role: 'assistant', content: 'AI 服务暂时不可用，请稍后再试。' })
  } finally { loading.value = false }
}
</script>

<style scoped>
.chat-container {
  display: flex;
  flex-direction: column;
  height: calc(100vh - 140px);
  padding: 0;
  overflow: hidden;
}

/* 消息列表 */
.message-list {
  flex: 1;
  overflow-y: auto;
  padding: 24px;
}
.message { margin-bottom: 20px; max-width: 72%; }
.user-msg { margin-left: auto; text-align: right; }
.ai-msg { margin-right: auto; }

.msg-label {
  font-size: 11px;
  color: var(--text-muted);
  margin-bottom: 6px;
  letter-spacing: 0.08em;
}
.user-msg .msg-label { text-align: right; }

.msg-content {
  display: inline-block;
  padding: 12px 18px;
  border-radius: 14px;
  font-size: 14px;
  line-height: 1.7;
  white-space: pre-wrap;
  text-align: left;
  letter-spacing: 0.04em;
}
.user-msg .msg-content {
  background: var(--bg-card);
  border: 1px solid var(--border-light);
  color: var(--text-primary);
  border-bottom-right-radius: 4px;
}
.ai-msg .msg-content {
  background: #F0F4F8;
  border: 1px solid #E2E8F0;
  color: var(--text-primary);
  border-bottom-left-radius: 4px;
}

/* 思考动画 */
.thinking-dots span { animation: dotPulse 1.4s infinite; opacity: 0; }
.thinking-dots span:nth-child(1) { animation-delay: 0s; }
.thinking-dots span:nth-child(2) { animation-delay: 0.2s; }
.thinking-dots span:nth-child(3) { animation-delay: 0.4s; }
@keyframes dotPulse {
  0%, 60%, 100% { opacity: 0; }
  30% { opacity: 1; }
}

/* 输入区 */
.input-area {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 16px 24px;
  border-top: 1px solid var(--border-light);
  background: var(--bg-card);
}
.input-area :deep(.el-input__wrapper) {
  border: 1px solid var(--border-light) !important;
  border-radius: var(--radius-sm) !important;
  padding: 8px 14px !important;
  background: var(--bg-main) !important;
}
.input-area :deep(.el-input__wrapper.is-focus) {
  border-color: var(--gold) !important;
}

.send-btn {
  width: 40px; height: 40px;
  display: flex; align-items: center; justify-content: center;
  background: var(--gold);
  border: none; border-radius: 10px;
  color: #fff;
  cursor: pointer;
  transition: var(--transition);
  flex-shrink: 0;
}
.send-btn:hover { background: var(--gold-light); }
.send-btn:disabled { opacity: 0.4; cursor: not-allowed; }
</style>
