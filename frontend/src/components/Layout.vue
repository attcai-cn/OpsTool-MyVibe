<template>
  <el-container class="layout">
    <el-aside width="220px" class="aside">
      <div class="logo">
        <img src="/logo.svg" alt="logo" class="logo-img" />
        <span>运维小工具</span>
      </div>
      <el-menu
        :default-active="$route.path"
        router
        class="menu"
        background-color="#304156"
        text-color="#bfcbd9"
        active-text-color="#409EFF"
      >
        <el-menu-item index="/">
          <el-icon><HomeFilled /></el-icon>
          <span>首页</span>
        </el-menu-item>
        <el-menu-item index="/notes">
          <el-icon><Document /></el-icon>
          <span>笔记</span>
        </el-menu-item>
        <el-menu-item index="/cheatsheet">
          <el-icon><Collection /></el-icon>
          <span>速查表</span>
        </el-menu-item>
        <el-menu-item index="/calculator">
          <el-icon><Sort /></el-icon>
          <span>计算器</span>
        </el-menu-item>
        <el-menu-item index="/cron">
          <el-icon><Timer /></el-icon>
          <span>Cron 表达式</span>
        </el-menu-item>
        <el-menu-item index="/todos">
          <el-icon><List /></el-icon>
          <span>待办</span>
        </el-menu-item>
      </el-menu>
    </el-aside>
    <el-container>
      <el-header class="header">
        <div class="header-right">
          <el-dropdown @command="handleCommand">
            <span class="user-info">
              <el-icon><UserFilled /></el-icon>
              {{ authStore.user?.username || '用户' }}
              <el-icon class="el-icon--right"><arrow-down /></el-icon>
            </span>
            <template #dropdown>
              <el-dropdown-menu>
                <el-dropdown-item command="logout">退出登录</el-dropdown-item>
              </el-dropdown-menu>
            </template>
          </el-dropdown>
        </div>
      </el-header>
      <el-main class="main">
        <slot />
      </el-main>
    </el-container>
  </el-container>
</template>

<script setup>
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { ElMessage } from 'element-plus'

const router = useRouter()
const authStore = useAuthStore()

const handleCommand = (cmd) => {
  if (cmd === 'logout') {
    authStore.logout()
    ElMessage.success('已退出登录')
    router.push('/login')
  }
}
</script>

<style scoped>
.layout {
  height: 100vh;
}
.aside {
  background-color: #304156;
}
.logo {
  height: 60px;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
  color: #fff;
  font-size: 18px;
  font-weight: bold;
  border-bottom: 1px solid #1f2d3d;
}
.logo-img {
  width: 32px;
  height: 32px;
}
.menu {
  border-right: none;
}
.header {
  background-color: #fff;
  box-shadow: 0 1px 4px rgba(0,0,0,0.08);
  display: flex;
  align-items: center;
  justify-content: flex-end;
}
.header-right {
  display: flex;
  align-items: center;
}
.user-info {
  cursor: pointer;
  color: #606266;
  display: flex;
  align-items: center;
  gap: 4px;
}
.main {
  background-color: #f0f2f5;
  padding: 20px;
  overflow-y: auto;
}
</style>
