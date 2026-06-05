<template>
  <div class="page-enter">
    <div class="page-header">
      <h1 class="page-title">天玺御览</h1>
      <span style="font-size:12px;color:var(--text-muted);letter-spacing:0.06em">{{ currentTime }}</span>
    </div>

    <el-row :gutter="20" style="margin-bottom:24px" class="stagger-enter">
      <el-col :span="6" v-for="item in kpiData" :key="item.label">
        <div class="kpi-card" :class="item.cls">
          <div class="kpi-icon">{{ item.icon }}</div>
          <div class="kpi-value">{{ item.value }}</div>
          <div class="kpi-label">{{ item.label }}</div>
        </div>
      </el-col>
    </el-row>

    <el-row :gutter="20" style="margin-bottom:24px">
      <el-col :span="10">
        <div class="content-card" style="height:360px">
          <div style="font-size:13px;font-weight:500;margin-bottom:12px;color:var(--text-secondary);letter-spacing:0.08em">房间状态分布</div>
          <div ref="pieChart" class="chart"></div>
        </div>
      </el-col>
      <el-col :span="14">
        <div class="content-card" style="height:360px">
          <div style="font-size:13px;font-weight:500;margin-bottom:12px;color:var(--text-secondary);letter-spacing:0.08em">营业收入趋势</div>
          <div ref="lineChart" class="chart"></div>
        </div>
      </el-col>
    </el-row>

    <el-row :gutter="20">
      <el-col :span="12">
        <div class="content-card">
          <div style="font-size:13px;font-weight:500;margin-bottom:16px;color:var(--text-secondary);letter-spacing:0.08em">财务概览</div>
          <el-row :gutter="16">
            <el-col :span="8" v-for="item in financeItems" :key="item.label">
              <div class="fi-value" style="color:var(--text-primary)">¥{{ item.value }}</div>
              <div class="fi-label">{{ item.label }}</div>
            </el-col>
          </el-row>
        </div>
      </el-col>
      <el-col :span="12">
        <div class="content-card">
          <div style="font-size:13px;font-weight:500;margin-bottom:16px;color:var(--text-secondary);letter-spacing:0.08em">今日待办</div>
          <div v-if="todayTodos.length===0" style="color:var(--text-muted);font-size:13px;padding:12px 0">暂无待办事项</div>
          <div v-for="todo in todayTodos" :key="todo.text" class="todo-item">
            <span class="todo-dot" :style="{background:todo.color}"></span>
            <span style="font-size:13px;color:var(--text-secondary)">{{ todo.text }}</span>
          </div>
        </div>
      </el-col>
    </el-row>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onBeforeUnmount, nextTick, watch } from 'vue'
import * as echarts from 'echarts'
import request from '@/api/index.js'

const stats = ref({ available: 0, booked: 0, occupied: 0, cleaning: 0 })
const paymentStats = ref({ total_deposit: 0, total_payment: 0, net_income: 0 })
const displayStats = ref({ available: 0, booked: 0, occupied: 0, cleaning: 0 })
const pieChart = ref(null); const lineChart = ref(null)
let pieInstance = null; let lineInstance = null
const currentTime = ref('')

// 数字递增动画
const animateValue = (target, key) => {
  const start = 0
  const end = target
  const duration = 800
  const startTime = performance.now()
  const step = (now) => {
    const elapsed = now - startTime
    const progress = Math.min(elapsed / duration, 1)
    // ease-out 缓动
    displayStats.value[key] = Math.round(start + (end - start) * (1 - Math.pow(1 - progress, 3)))
    if (progress < 1) requestAnimationFrame(step)
  }
  requestAnimationFrame(step)
}

watch(() => ({ ...stats.value }), (val) => {
  Object.keys(val).forEach(k => animateValue(val[k], k))
}, { deep: true })

const kpiData = computed(() => [
  { icon: '✦', value: displayStats.value.available, label: '空闲客房', cls: 'kpi-available' },
  { icon: '◆', value: displayStats.value.booked, label: '已预订', cls: 'kpi-booked' },
  { icon: '⬥', value: displayStats.value.occupied, label: '已入住', cls: 'kpi-occupied' },
  { icon: '◇', value: displayStats.value.cleaning || 0, label: '清洁中', cls: 'kpi-cleaning' },
])
const todayTodos = computed(() => { const t=[]; if(stats.value.cleaning) t.push({text:`${stats.value.cleaning} 间客房待清洁`,color:'#A67C43'}); return t })
const financeItems = computed(() => [
  {label:'押金总额',value:paymentStats.value.total_deposit},
  {label:'房费收入',value:paymentStats.value.total_payment},
  {label:'净收入',value:paymentStats.value.net_income},
])

const fetchStats = async () => { try { const r=await request.get('/rooms/statusCount'); stats.value=r.data; nextTick(()=>initPieChart()) } catch(e) { console.warn('fetchStats:', e) } }
const fetchRevenue = async () => { try { const r=await request.get('/bookings/revenue?days=7'); nextTick(()=>initLineChart(r.data)) } catch(e) { console.warn('fetchRevenue:', e) } }
const fetchPaymentStats = async () => { try{const r=await request.get('/payments/stats');paymentStats.value=r.data}catch{}}

const initPieChart = () => {
  if(!pieChart.value)return; if(!pieInstance) pieInstance=echarts.init(pieChart.value,null,{renderer:'svg'})
  pieInstance.setOption({
    tooltip:{trigger:'item',formatter:'{b}: {c}'},
    series:[{type:'pie',radius:['40%','65%'],
      label:{show:true,formatter:'{b}\n{c}',fontSize:11,color:'#8C8C8C'},
      labelLine:{lineStyle:{color:'#E8E4DE'}},
      data:[
        {value:stats.value.available,name:'空闲',itemStyle:{color:'#D6E4D3'}},
        {value:stats.value.booked,name:'已预订',itemStyle:{color:'#D2E0EC'}},
        {value:stats.value.occupied||0,name:'已入住',itemStyle:{color:'#D4C08C'}},
        {value:stats.value.cleaning||0,name:'清洁中',itemStyle:{color:'#F3E3CE'}},
      ],
    }],
  })
}

const initLineChart = (data) => {
  if(!lineChart.value||!data.length)return; if(!lineInstance) lineInstance=echarts.init(lineChart.value,null,{renderer:'svg'})
  lineInstance.setOption({
    tooltip:{trigger:'axis',formatter:'{b}<br/>营收: ¥{c}'},
    grid:{left:'3%',right:'4%',bottom:'3%',containLabel:true},
    xAxis:{type:'category',data:data.map(d=>d.date),axisLine:{show:false},axisTick:{show:false},axisLabel:{color:'#BFBFBF',fontSize:11}},
    yAxis:{type:'value',splitLine:{lineStyle:{color:'#F0EFEC'}},axisLabel:{color:'#BFBFBF',fontSize:11,formatter:'¥{value}'}},
    series:[{type:'line',smooth:true,data:data.map(d=>d.revenue),
      symbol:'circle',symbolSize:5,
      lineStyle:{color:'#B89752',width:2},
      itemStyle:{color:'#B89752'},
      areaStyle:{color:{type:'linear',x:0,y:0,x2:0,y2:1,colorStops:[{offset:0,color:'rgba(184,151,82,0.15)'},{offset:1,color:'rgba(184,151,82,0)'}]}},
    }],
  })
}

const handleResize=()=>{pieInstance?.resize();lineInstance?.resize()}
const updateTime=()=>{const d=new Date();currentTime.value=`${d.getFullYear()}.${String(d.getMonth()+1).padStart(2,'0')}.${String(d.getDate()).padStart(2,'0')}`}
onMounted(()=>{updateTime();fetchStats();fetchRevenue();fetchPaymentStats();window.addEventListener('resize',handleResize)})
onBeforeUnmount(()=>{pieInstance?.dispose();lineInstance?.dispose();window.removeEventListener('resize',handleResize)})
</script>

<style scoped>
.chart{width:100%;height:285px}
.fi-value{font-size:22px;font-weight:600;margin-bottom:4px}
.fi-label{font-size:12px;color:var(--text-secondary);letter-spacing:0.06em}
.todo-item{display:flex;align-items:center;gap:10px;padding:10px 0;border-bottom:1px solid #F0EFEC}
.todo-item:last-child{border-bottom:none}
.todo-dot{width:6px;height:6px;border-radius:50%;flex-shrink:0}
</style>
