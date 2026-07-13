import axios from 'axios'
import { ElMessage } from 'element-plus'
import router from '@/router'

const api = axios.create({
  baseURL: '/api/v1',
  timeout: 10000,
})

api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => Promise.reject(error)
)

api.interceptors.response.use(
  (response) => {
    const data = response.data
    if (data.code !== 200) {
      ElMessage.error(data.message || '请求失败')
      return Promise.reject(new Error(data.message))
    }
    return data
  },
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('token')
      router.push('/login')
      ElMessage.error('登录已过期，请重新登录')
    } else {
      ElMessage.error(error.response?.data?.message || '网络错误')
    }
    return Promise.reject(error)
  }
)

export default api

export const authApi = {
  register: (data) => api.post('/auth/register', data),
  login: (data) => api.post('/auth/login', data),
  me: () => api.get('/auth/me'),
}

export const noteApi = {
  list: (params) => api.get('/notes', { params }),
  get: (id) => api.get(`/notes/${id}`),
  create: (data) => api.post('/notes', data),
  update: (id, data) => api.put(`/notes/${id}`, data),
  remove: (id) => api.delete(`/notes/${id}`),
}

export const cheatsheetApi = {
  categories: () => api.get('/cheatsheet/categories'),
  category: (name) => api.get(`/cheatsheet/${name}`),
  search: (q) => api.get('/cheatsheet/search/all', { params: { q } }),
}

export const calculatorApi = {
  bandwidth: (data) => api.post('/calculator/bandwidth', data),
  timestamp: (data) => api.post('/calculator/timestamp', data),
  subnet: (data) => api.post('/calculator/subnet', data),
}

export const cronApi = {
  build: (data) => api.post('/cron/build', data),
  parse: (data) => api.post('/cron/parse', data),
}

export const todoApi = {
  list: (params) => api.get('/todos', { params }),
  get: (id) => api.get(`/todos/${id}`),
  create: (data) => api.post('/todos', data),
  update: (id, data) => api.put(`/todos/${id}`, data),
  toggle: (id, data) => api.patch(`/todos/${id}/complete`, data),
  remove: (id) => api.delete(`/todos/${id}`),
}
