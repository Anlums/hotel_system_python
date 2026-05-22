import { reactive } from 'vue'

// 全局共享的 AI 聊天状态，切换页面不会丢失
export const aiStore = reactive({
  messages: [
    { role: 'assistant', content: '您好！我是天玺尊邸酒店的 AI 智能管家，有什么可以帮您的吗？' },
  ],
})
