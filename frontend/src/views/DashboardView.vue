<template>
  <Layout>
    <div class="dashboard">
      <el-row :gutter="20">
        <el-col :span="6">
          <el-card class="stat-card" @click="$router.push('/notes')">
            <el-icon :size="40" color="#409EFF"><Document /></el-icon>
            <div class="stat-title">我的笔记</div>
            <div class="stat-desc">记录运维心得与方案</div>
          </el-card>
        </el-col>
        <el-col :span="6">
          <el-card class="stat-card" @click="$router.push('/cheatsheet')">
            <el-icon :size="40" color="#67C23A"><Collection /></el-icon>
            <div class="stat-title">速查表</div>
            <div class="stat-desc">Linux / Docker / K8s 常用命令</div>
          </el-card>
        </el-col>
        <el-col :span="6">
          <el-card class="stat-card" @click="$router.push('/calculator')">
            <el-icon :size="40" color="#E6A23C"><Tools /></el-icon>
            <div class="stat-title">计算器</div>
            <div class="stat-desc">带宽、时间戳、子网计算</div>
          </el-card>
        </el-col>
        <el-col :span="6">
          <el-card class="stat-card" @click="$router.push('/cron')">
            <el-icon :size="40" color="#909399"><Timer /></el-icon>
            <div class="stat-title">Cron 表达式</div>
            <div class="stat-desc">构建与调试定时任务</div>
          </el-card>
        </el-col>
      </el-row>

      <el-row :gutter="20" style="margin-top: 20px">
        <el-col :span="6" :offset="9">
          <el-card class="stat-card" @click="$router.push('/todos')">
            <el-icon :size="40" color="#F56C6C"><List /></el-icon>
            <div class="stat-title">待办</div>
            <div class="stat-desc">按紧急度管理任务</div>
          </el-card>
        </el-col>
      </el-row>

      <el-card class="welcome-card" style="margin-top: 20px">
        <h3>欢迎使用运维小工具</h3>
        <p>本工具提供以下功能：</p>
        <ul>
          <li><strong>笔记</strong>：随时记录运维过程中的问题与解决方案</li>
          <li><strong>速查表</strong>：快速查阅常用运维命令，支持搜索</li>
          <li><strong>计算器</strong>：带宽单位转换、Unix 时间戳转换、IP 子网计算</li>
          <li><strong>Cron 表达式</strong>：通过可视化选项生成 Crontab 表达式，并预览最近执行时间</li>
          <li><strong>待办</strong>：按紧急度（缓/中/急）管理任务，精确到某日某时截止</li>
        </ul>
      </el-card>
    </div>
  </Layout>
</template>

<script setup>
import Layout from '@/components/Layout.vue'
</script>

<style scoped>
.stat-card {
  text-align: center;
  cursor: pointer;
  transition: transform 0.2s;
}
.stat-card:hover {
  transform: translateY(-4px);
}
.stat-title {
  font-size: 18px;
  font-weight: bold;
  margin-top: 12px;
  color: #303133;
}
.stat-desc {
  font-size: 13px;
  color: #909399;
  margin-top: 4px;
}
.welcome-card ul {
  padding-left: 20px;
  color: #606266;
  line-height: 2;
}
</style>
