import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { authApi } from '@/api'

export const useAuthStore = defineStore('auth', () => {
  const token = ref(localStorage.getItem('token') || '')
  const user = ref(null)

  const isLoggedIn = computed(() => !!token.value)

  async function login(credentials) {
    const res = await authApi.login(credentials)
    token.value = res.data.access_token
    localStorage.setItem('token', token.value)
    await fetchUser()
    return res
  }

  async function register(data) {
    return authApi.register(data)
  }

  async function fetchUser() {
    try {
      const res = await authApi.me()
      user.value = res.data
      return res
    } catch {
      logout()
    }
  }

  function logout() {
    token.value = ''
    user.value = null
    localStorage.removeItem('token')
  }

  return { token, user, isLoggedIn, login, register, fetchUser, logout }
})
