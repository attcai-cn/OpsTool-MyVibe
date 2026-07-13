import { defineStore } from 'pinia'
import { ref } from 'vue'
import { cheatsheetApi } from '@/api'

export const useCheatsheetStore = defineStore('cheatsheet', () => {
  const categories = ref([])
  const items = ref([])
  const searchResults = ref([])

  async function fetchCategories() {
    const res = await cheatsheetApi.categories()
    categories.value = res.data
    return res
  }

  async function fetchCategory(name) {
    const res = await cheatsheetApi.category(name)
    items.value = res.data
    return res
  }

  async function search(q) {
    const res = await cheatsheetApi.search(q)
    searchResults.value = res.data
    return res
  }

  return { categories, items, searchResults, fetchCategories, fetchCategory, search }
})
