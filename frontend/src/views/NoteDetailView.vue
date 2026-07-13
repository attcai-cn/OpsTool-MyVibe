<template>
  <Layout>
    <div class="note-detail">
      <el-card v-loading="loading">
        <template #header>
          <div class="card-header">
            <el-button @click="$router.push('/notes')">返回</el-button>
            <el-button type="primary" @click="handleSave" :loading="saving">保存</el-button>
          </div>
        </template>

        <el-form :model="form" :rules="rules" ref="formRef" label-width="60px">
          <el-form-item label="标题" prop="title">
            <el-input v-model="form.title" />
          </el-form-item>
          <el-form-item label="标签">
            <el-input v-model="form.tags" placeholder="逗号分隔" />
          </el-form-item>
          <el-form-item label="内容" prop="content">
            <el-input v-model="form.content" type="textarea" :rows="16" />
          </el-form-item>
        </el-form>
      </el-card>
    </div>
  </Layout>
</template>

<script setup>
import { reactive, ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { useNoteStore } from '@/stores/note'
import Layout from '@/components/Layout.vue'

const route = useRoute()
const router = useRouter()
const noteStore = useNoteStore()
const loading = ref(false)
const saving = ref(false)
const formRef = ref()

const form = reactive({
  title: '',
  content: '',
  tags: '',
})

const rules = {
  title: [{ required: true, message: '请输入标题', trigger: 'blur' }],
  content: [{ required: true, message: '请输入内容', trigger: 'blur' }],
}

const id = parseInt(route.params.id)

onMounted(async () => {
  loading.value = true
  try {
    await noteStore.fetchNote(id)
    const n = noteStore.currentNote
    if (n) {
      form.title = n.title
      form.content = n.content
      form.tags = n.tags
    }
  } finally {
    loading.value = false
  }
})

const handleSave = async () => {
  await formRef.value.validate()
  saving.value = true
  try {
    await noteStore.updateNote(id, { ...form })
    ElMessage.success('保存成功')
    router.push('/notes')
  } finally {
    saving.value = false
  }
}
</script>

<style scoped>
.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
</style>
