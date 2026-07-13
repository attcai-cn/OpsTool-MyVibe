<template>
  <Layout>
    <div class="notes">
      <el-card>
        <template #header>
          <div class="card-header">
            <span>我的笔记</span>
            <el-button type="primary" @click="handleCreate">新建笔记</el-button>
          </div>
        </template>

        <el-form :inline="true" :model="query" class="search-form">
          <el-form-item>
            <el-input v-model="query.q" placeholder="搜索标题或内容" clearable />
          </el-form-item>
          <el-form-item>
            <el-input v-model="query.tag" placeholder="标签过滤" clearable />
          </el-form-item>
          <el-form-item>
            <el-button type="primary" @click="loadNotes">查询</el-button>
          </el-form-item>
        </el-form>

        <el-table :data="noteStore.notes" style="width: 100%" v-loading="loading">
          <el-table-column prop="title" label="标题" min-width="200">
            <template #default="{ row }">
              <el-link type="primary" @click="$router.push(`/notes/${row.id}`)">{{ row.title }}</el-link>
            </template>
          </el-table-column>
          <el-table-column prop="tags" label="标签" width="150" />
          <el-table-column prop="created_at" label="创建时间" width="180">
            <template #default="{ row }">
              {{ formatDate(row.created_at) }}
            </template>
          </el-table-column>
          <el-table-column label="操作" width="150">
            <template #default="{ row }">
              <el-button size="small" @click="$router.push(`/notes/${row.id}`)">编辑</el-button>
              <el-button size="small" type="danger" @click="handleDelete(row.id)">删除</el-button>
            </template>
          </el-table-column>
        </el-table>

        <div class="pagination" v-if="noteStore.total > 0">
          <el-pagination
            layout="prev, pager, next"
            :total="noteStore.total"
            :page-size="query.limit"
            v-model:current-page="query.page"
            @current-change="loadNotes"
          />
        </div>
      </el-card>

      <el-dialog v-model="dialogVisible" title="新建笔记" width="600px">
        <el-form :model="form" :rules="formRules" ref="formRef" label-width="60px">
          <el-form-item label="标题" prop="title">
            <el-input v-model="form.title" />
          </el-form-item>
          <el-form-item label="标签">
            <el-input v-model="form.tags" placeholder="逗号分隔" />
          </el-form-item>
          <el-form-item label="内容" prop="content">
            <el-input v-model="form.content" type="textarea" :rows="8" />
          </el-form-item>
        </el-form>
        <template #footer>
          <el-button @click="dialogVisible = false">取消</el-button>
          <el-button type="primary" @click="submitCreate" :loading="submitting">确定</el-button>
        </template>
      </el-dialog>
    </div>
  </Layout>
</template>

<script setup>
import { reactive, ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import { useNoteStore } from '@/stores/note'
import Layout from '@/components/Layout.vue'

const router = useRouter()
const noteStore = useNoteStore()
const loading = ref(false)
const dialogVisible = ref(false)
const submitting = ref(false)
const formRef = ref()

const query = reactive({
  q: '',
  tag: '',
  page: 1,
  limit: 10,
})

const form = reactive({
  title: '',
  content: '',
  tags: '',
})

const formRules = {
  title: [{ required: true, message: '请输入标题', trigger: 'blur' }],
  content: [{ required: true, message: '请输入内容', trigger: 'blur' }],
}

const loadNotes = async () => {
  loading.value = true
  try {
    await noteStore.fetchNotes({
      q: query.q || undefined,
      tag: query.tag || undefined,
      skip: (query.page - 1) * query.limit,
      limit: query.limit,
    })
  } finally {
    loading.value = false
  }
}

const handleCreate = () => {
  form.title = ''
  form.content = ''
  form.tags = ''
  dialogVisible.value = true
}

const submitCreate = async () => {
  await formRef.value.validate()
  submitting.value = true
  try {
    await noteStore.createNote({ ...form })
    ElMessage.success('创建成功')
    dialogVisible.value = false
    loadNotes()
  } finally {
    submitting.value = false
  }
}

const handleDelete = async (id) => {
  await ElMessageBox.confirm('确定删除该笔记吗？', '提示', { type: 'warning' })
  await noteStore.deleteNote(id)
  ElMessage.success('删除成功')
  loadNotes()
}

const formatDate = (str) => {
  if (!str) return ''
  const d = new Date(str)
  return d.toLocaleString()
}

onMounted(() => {
  loadNotes()
})
</script>

<style scoped>
.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.search-form {
  margin-bottom: 16px;
}
.pagination {
  margin-top: 16px;
  display: flex;
  justify-content: flex-end;
}
</style>
