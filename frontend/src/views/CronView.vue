<template>
  <Layout>
    <div class="cron-page">
      <div class="page-header">
        <img src="/logo.svg" alt="logo" class="page-logo" />
        <span class="page-title">Crontab 表达式构建器</span>
      </div>

      <el-row :gutter="20">
        <!-- 左侧：构建器 -->
        <el-col :span="12">
          <el-card>
            <template #header>
              <div class="card-header">
                <el-icon :size="18"><Timer /></el-icon>
                <span>表达式构建</span>
              </div>
            </template>

            <el-form :model="form" label-width="100px">
              <el-form-item label="执行周期">
                <el-radio-group v-model="form.mode">
                  <el-radio-button label="daily">每天</el-radio-button>
                  <el-radio-button label="weekly">每周</el-radio-button>
                </el-radio-group>
              </el-form-item>

              <el-form-item label="执行时间">
                <el-time-picker
                  v-model="form.time"
                  format="HH:mm"
                  value-format="HH:mm"
                  placeholder="选择时间"
                  style="width: 160px"
                />
              </el-form-item>

              <el-form-item label="每周几" v-if="form.mode === 'weekly'">
                <el-select v-model="form.day_of_week" placeholder="选择星期" style="width: 160px">
                  <el-option
                    v-for="item in weekOptions"
                    :key="item.value"
                    :label="item.label"
                    :value="item.value"
                  />
                </el-select>
              </el-form-item>

              <el-form-item>
                <el-button type="primary" @click="handleBuild">
                  <el-icon><MagicStick /></el-icon>
                  生成表达式
                </el-button>
              </el-form-item>
            </el-form>

            <el-divider v-if="result.expression" />

            <div v-if="result.expression" class="result-section">
              <div class="expr-box">
                <span class="expr-label">Cron 表达式</span>
                <code class="expr-code">{{ result.expression }}</code>
                <el-button
                  size="small"
                  type="primary"
                  plain
                  @click="copyExpr"
                  style="margin-left: 12px"
                >
                  <el-icon><CopyDocument /></el-icon>
                  复制
                </el-button>
              </div>

              <div class="desc-box" v-if="result.description">
                <el-tag type="info" size="large">{{ result.description }}</el-tag>
              </div>

              <div class="next-box">
                <div class="next-title">最近 5 次执行时间</div>
                <el-timeline>
                  <el-timeline-item
                    v-for="(t, idx) in result.next_executions"
                    :key="idx"
                    :type="idx === 0 ? 'primary' : ''"
                    :icon="idx === 0 ? 'Clock' : ''"
                  >
                    {{ t }}
                    <el-tag v-if="idx === 0" size="small" type="primary">最近</el-tag>
                  </el-timeline-item>
                </el-timeline>
              </div>
            </div>
          </el-card>
        </el-col>

        <!-- 右侧：调试器 -->
        <el-col :span="12">
          <el-card>
            <template #header>
              <div class="card-header">
                <el-icon :size="18"><Tools /></el-icon>
                <span>表达式调试</span>
              </div>
            </template>

            <el-form :model="debugForm" label-width="100px">
              <el-form-item label="Cron 表达式">
                <el-input
                  v-model="debugForm.expression"
                  placeholder="例如：0 2 * * 1"
                  clearable
                >
                  <template #append>
                    <el-button @click="handleParse">解析</el-button>
                  </template>
                </el-input>
              </el-form-item>
            </el-form>

            <el-divider v-if="debugResult.expression" />

            <div v-if="debugResult.expression" class="result-section">
              <div class="expr-box">
                <span class="expr-label">解析结果</span>
                <code class="expr-code">{{ debugResult.expression }}</code>
              </div>

              <div class="desc-box" v-if="debugResult.description">
                <el-tag type="success" size="large">{{ debugResult.description }}</el-tag>
              </div>

              <div class="parts-box" v-if="debugResult.parts">
                <el-descriptions :column="2" border size="small">
                  <el-descriptions-item label="分">{{ debugResult.parts.minute }}</el-descriptions-item>
                  <el-descriptions-item label="时">{{ debugResult.parts.hour }}</el-descriptions-item>
                  <el-descriptions-item label="日">{{ debugResult.parts.day }}</el-descriptions-item>
                  <el-descriptions-item label="月">{{ debugResult.parts.month }}</el-descriptions-item>
                  <el-descriptions-item label="周">{{ debugResult.parts.weekday }}</el-descriptions-item>
                </el-descriptions>
              </div>

              <div class="next-box">
                <div class="next-title">最近 5 次执行时间</div>
                <el-timeline>
                  <el-timeline-item
                    v-for="(t, idx) in debugResult.next_executions"
                    :key="idx"
                    :type="idx === 0 ? 'primary' : ''"
                  >
                    {{ t }}
                    <el-tag v-if="idx === 0" size="small" type="primary">最近</el-tag>
                  </el-timeline-item>
                </el-timeline>
              </div>
            </div>
          </el-card>
        </el-col>
      </el-row>
    </div>
  </Layout>
</template>

<script setup>
import { reactive, ref } from 'vue'
import { ElMessage } from 'element-plus'
import { cronApi } from '@/api'
import Layout from '@/components/Layout.vue'

const weekOptions = [
  { label: '周日', value: 0 },
  { label: '周一', value: 1 },
  { label: '周二', value: 2 },
  { label: '周三', value: 3 },
  { label: '周四', value: 4 },
  { label: '周五', value: 5 },
  { label: '周六', value: 6 },
]

const form = reactive({
  mode: 'daily',
  time: '02:00',
  day_of_week: 1,
})

const result = reactive({
  expression: '',
  description: '',
  next_executions: [],
})

const debugForm = reactive({
  expression: '',
})

const debugResult = reactive({
  expression: '',
  description: '',
  parts: null,
  next_executions: [],
})

const handleBuild = async () => {
  if (!form.time) {
    ElMessage.warning('请选择执行时间')
    return
  }
  const [hour, minute] = form.time.split(':').map(Number)
  try {
    const res = await cronApi.build({
      mode: form.mode,
      minute,
      hour,
      day_of_week: form.mode === 'weekly' ? form.day_of_week : undefined,
    })
    result.expression = res.data.expression
    result.description = res.data.description
    result.next_executions = res.data.next_executions
  } catch (e) {
    ElMessage.error(e.message || '生成失败')
  }
}

const handleParse = async () => {
  if (!debugForm.expression.trim()) {
    ElMessage.warning('请输入 Cron 表达式')
    return
  }
  try {
    const res = await cronApi.parse({ expression: debugForm.expression.trim() })
    debugResult.expression = res.data.expression
    debugResult.description = res.data.description
    debugResult.parts = res.data.parts
    debugResult.next_executions = res.data.next_executions
  } catch (e) {
    ElMessage.error(e.message || '解析失败')
  }
}

const copyExpr = () => {
  navigator.clipboard.writeText(result.expression).then(() => {
    ElMessage.success('已复制到剪贴板')
  })
}
</script>

<style scoped>
.page-header {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 20px;
}
.page-logo {
  width: 40px;
  height: 40px;
}
.page-title {
  font-size: 20px;
  font-weight: bold;
  color: #303133;
}
.card-header {
  display: flex;
  align-items: center;
  gap: 8px;
  font-weight: bold;
}
.result-section {
  margin-top: 8px;
}
.expr-box {
  display: flex;
  align-items: center;
  margin-bottom: 16px;
}
.expr-label {
  color: #606266;
  margin-right: 12px;
  font-size: 14px;
}
.expr-code {
  background: #f5f7fa;
  padding: 8px 16px;
  border-radius: 6px;
  font-family: 'Courier New', monospace;
  font-size: 18px;
  font-weight: bold;
  color: #409EFF;
  letter-spacing: 1px;
}
.desc-box {
  margin-bottom: 16px;
}
.parts-box {
  margin-bottom: 16px;
}
.next-box {
  margin-top: 16px;
}
.next-title {
  font-size: 14px;
  font-weight: bold;
  color: #606266;
  margin-bottom: 12px;
}
</style>
