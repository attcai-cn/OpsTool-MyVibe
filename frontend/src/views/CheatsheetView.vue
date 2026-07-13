<template>
  <Layout>
    <div class="cheatsheet">
      <el-card>
        <template #header>
          <div class="card-header">
            <span>运维速查表</span>
            <el-input
              v-model="searchQuery"
              placeholder="搜索命令"
              clearable
              style="width: 300px"
              @keyup.enter="handleSearch"
            >
              <template #append>
                <el-button @click="handleSearch">
                  <el-icon><Search /></el-icon>
                </el-button>
              </template>
            </el-input>
          </div>
        </template>

        <el-row :gutter="20">
          <el-col :span="5">
            <el-menu
              :default-active="activeCategory"
              @select="handleSelect"
              class="category-menu"
            >
              <el-menu-item v-for="cat in categories" :key="cat" :index="cat">
                <span style="text-transform: capitalize">{{ cat }}</span>
              </el-menu-item>
            </el-menu>
          </el-col>
          <el-col :span="19">
            <el-table :data="displayItems" v-loading="loading" stripe>
              <el-table-column prop="command" label="命令" min-width="280">
                <template #default="{ row }">
                  <code class="cmd">{{ row.command }}</code>
                </template>
              </el-table-column>
              <el-table-column prop="description" label="说明" min-width="200" />
              <el-table-column prop="example" label="示例" min-width="280">
                <template #default="{ row }">
                  <code class="example">{{ row.example }}</code>
                </template>
              </el-table-column>
            </el-table>
          </el-col>
        </el-row>
      </el-card>
    </div>
  </Layout>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useCheatsheetStore } from '@/stores/cheatsheet'
import Layout from '@/components/Layout.vue'

const store = useCheatsheetStore()
const loading = ref(false)
const activeCategory = ref('linux')
const searchQuery = ref('')
const isSearch = ref(false)

const categories = computed(() => store.categories)
const displayItems = computed(() => isSearch.value ? store.searchResults : store.items)

const loadCategories = async () => {
  await store.fetchCategories()
  if (categories.value.length > 0) {
    activeCategory.value = categories.value[0]
    await loadCategory(categories.value[0])
  }
}

const loadCategory = async (name) => {
  loading.value = true
  isSearch.value = false
  try {
    await store.fetchCategory(name)
  } finally {
    loading.value = false
  }
}

const handleSelect = (index) => {
  activeCategory.value = index
  loadCategory(index)
}

const handleSearch = async () => {
  if (!searchQuery.value.trim()) {
    isSearch.value = false
    loadCategory(activeCategory.value)
    return
  }
  loading.value = true
  isSearch.value = true
  try {
    await store.search(searchQuery.value)
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  loadCategories()
})
</script>

<style scoped>
.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.category-menu {
  border-right: none;
}
code.cmd {
  background: #f5f7fa;
  padding: 4px 8px;
  border-radius: 4px;
  color: #409EFF;
  font-family: monospace;
  font-weight: bold;
}
code.example {
  color: #67C23A;
  font-family: monospace;
  font-size: 12px;
}
</style>
