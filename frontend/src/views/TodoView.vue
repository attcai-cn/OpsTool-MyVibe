<template>
  <Layout>
    <div class="todo-page">
      <div class="page-header">
        <img src="/logo.svg" alt="logo" class="page-logo" />
        <span class="page-title">待办事项</span>
      </div>

      <el-card>
        <template #header>
          <div class="card-header">
            <div class="filters">
              <el-radio-group v-model="filterUrgency" size="small" @change="loadTodos">
                <el-radio-button label="">全部</el-radio-button>
                <el-radio-button label="high">急</el-radio-button>
                <el-radio-button label="medium">中</el-radio-button>
                <el-radio-button label="low">缓</el-radio-button>
              </el-radio-group>
              <el-checkbox v-model="hideCompleted" @change="loadTodos">隐藏已完成</el-checkbox>
            </div>
            <el-button type="primary" @click="openCreate">新增待办</el-button>
          </div>
        </template>

        <el-table :data="todos" v-loading="loading" stripe>
          <el-table-column width="60">
            <template #default="{ row }">
              <el-checkbox
                :model-value="row.completed"
                @change="(val) => toggle(row.id, val)"
                size="large"
              />
            </template>
          </el-table-column>
          <el-table-column prop="title" label="事项" min-width="200">
            <template #default="{ row }">
              <span :class="{ 'done-text': row.completed }">{{ row.title }}</span>
            </template>
          </el-table-column>
          <el-table-column label="紧急度" width="100">
            <template #default="{ row }">
              <el-tag :type="urgencyType(row.urgency)" size="small">{{ urgencyLabel(row.urgency) }}</el-tag>
            </template>
          </el-table-column>
          <el-table-column label="截止时间" width="160">
            <template #default="{ row }">
              {{ formatDeadline(row.deadline) }}
            </template>
          </el-table-column>
          <el-table-column label="操作" width="150">
            <template #default="{ row }">
              <el-button size="small" @click="openEdit(row)">编辑</el-button>
              <el-button size="small" type="danger" @click="handleDelete(row.id)">删除</el-button>
            </template>
          </el-table-column>
        </el-table>
      </el-card>

      <el-dialog v-model="dialogVisible" :title="isEdit ? '编辑待办' : '新增待办'" width="500px">
        <el-form :model="form" :rules="rules" ref="formRef" label-width="80px">
          <el-form-item label="事项" prop="title">
            <el-input v-model="form.title" placeholder="请输入待办事项" />
          </el-form-item>
          <el-form-item label="紧急度" prop="urgency">
            <el-radio-group v-model="form.urgency">
              <el-radio-button label="high">急</el-radio-button>
              <el-radio-button label="medium">中</el-radio-button>
              <el-radio-button label="low">缓</el-radio-button>
            </el-radio-group>
          </el-form-item>
          <el-form-item label="截止时间" prop="deadline">
            <div class="deadline-picker">
              <el-date-picker
                v-model="form.date"
                type="date"
                placeholder="选择日期"
                value-format="YYYY-MM-DD"
                style="width: 150px"
              />
              <el-select v-model="form.hour" placeholder="时" style="width: 90px">
                <el-option v-for="h in 24" :key="h-1" :label="(h-1)+' 时'" :value="h-1" />
              </el-select>
            </div>
          </el-form-item>
        </el-form>
        <template #footer>
          <el-button @click="dialogVisible = false">取消</el-button>
          <el-button type="primary" @click="submit" :loading="submitting">确定</el-button>
        </template>
      </el-dialog>
    </div>
  </Layout>
</template>

<script setup>
import { reactive, ref, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { todoApi } from '@/api'
import Layout from '@/components/Layout.vue'

const loading = ref(false)
const dialogVisible = ref(false)
const submitting = ref(false)
const isEdit = ref(false)
const editId = ref(null)
const formRef = ref()

const filterUrgency = ref('')
const hideCompleted = ref(false)
const todos = ref([])

const form = reactive({
  title: '',
  urgency: 'medium',
  date: '',
  hour: 12,
})

const rules = {
  title: [{ required: true, message: '请输入事项', trigger: 'blur' }],
}

const urgencyType = (u) => {
  const map = { high: 'danger', medium: 'warning', low: 'info' }
  return map[u] || 'info'
}

const urgencyLabel = (u) => {
  const map = { high: '急', medium: '中', low: '缓' }
  return map[u] || u
}

const formatDeadline = (iso) => {
  if (!iso) return ''
  const d = new Date(iso)
  const yyyy = d.getFullYear()
  const mm = String(d.getMonth() + 1).padStart(2, '0')
  const dd = String(d.getDate()).padStart(2, '0')
  const hh = String(d.getHours()).padStart(2, '0')
  return `${yyyy}-${mm}-${dd} ${hh}:00`
}

const buildDeadline = () => {
  if (!form.date && form.hour === null) return null
  const dateStr = form.date || new Date().toISOString().slice(0, 10)
  return new Date(`${dateStr}T${String(form.hour).padStart(2, '0')}:00:00`).toISOString()
}

const loadTodos = async () => {
  loading.value = true
  try {
    const params = {}
    if (filterUrgency.value) params.urgency = filterUrgency.value
    if (hideCompleted.value) params.completed = false
    const res = await todoApi.list(params)
    todos.value = res.data.items
  } finally {
    loading.value = false
  }
}

const openCreate = () => {
  isEdit.value = false
  editId.value = null
  form.title = ''
  form.urgency = 'medium'
  form.date = ''
  form.hour = 12
  dialogVisible.value = true
}

const openEdit = (row) => {
  isEdit.value = true
  editId.value = row.id
  form.title = row.title
  form.urgency = row.urgency
  const d = new Date(row.deadline)
  form.date = `${d.getFullYear()}-${String(d.getMonth()+1).padStart(2,'0')}-${String(d.getDate()).padStart(2,'0')}`
  form.hour = d.getHours()
  dialogVisible.value = true
}

const submit = async () => {
  await formRef.value.validate()
  const deadline = buildDeadline()
  if (!deadline) {
    ElMessage.warning('请选择截止时间')
    return
  }
  submitting.value = true
  try {
    const payload = {
      title: form.title,
      urgency: form.urgency,
      deadline,
      completed: false,
    }
    if (isEdit.value) {
      await todoApi.update(editId.value, payload)
      ElMessage.success('更新成功')
    } else {
      await todoApi.create(payload)
      ElMessage.success('创建成功')
    }
    dialogVisible.value = false
    loadTodos()
  } finally {
    submitting.value = false
  }
}

const toggle = async (id, val) => {
  try {
    await todoApi.toggle(id, { completed: val })
    loadTodos()
  } catch (e) {
    ElMessage.error(e.message || '操作失败')
  }
}

const handleDelete = async (id) => {
  await ElMessageBox.confirm('确定删除该待办吗？', '提示', { type: 'warning' })
  await todoApi.remove(id)
  ElMessage.success('删除成功')
  loadTodos()
}

onMounted(() => {
  loadTodos()
})
</script>

<style scoped>
.page-header {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 16px;
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
  justify-content: space-between;
  align-items: center;
}
.filters {
  display: flex;
  align-items: center;
  gap: 16px;
}
.deadline-picker {
  display: flex;
  gap: 8px;
}
.done-text {
  text-decoration: line-through;
  color: #909399;
}
</style>
