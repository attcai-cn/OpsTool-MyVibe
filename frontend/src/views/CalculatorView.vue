<template>
  <Layout>
    <div class="calculator">
      <div class="page-header">
        <img src="/logo.svg" alt="logo" class="page-logo" />
        <span class="page-title">运维计算器</span>
      </div>
      <el-tabs type="border-card" v-model="activeTab">
        <!-- Bandwidth -->
        <el-tab-pane label="带宽转换" name="bandwidth">
          <el-card>
            <el-form :model="bwForm" label-width="100px">
              <el-form-item label="数值">
                <el-input-number v-model="bwForm.value" :min="0" :precision="2" style="width: 200px" />
              </el-form-item>
              <el-form-item label="从">
                <el-select v-model="bwForm.from_unit" style="width: 200px">
                  <el-option v-for="u in bwUnits" :key="u" :label="u" :value="u" />
                </el-select>
              </el-form-item>
              <el-form-item label="到">
                <el-select v-model="bwForm.to_unit" style="width: 200px">
                  <el-option v-for="u in bwUnits" :key="u" :label="u" :value="u" />
                </el-select>
              </el-form-item>
              <el-form-item>
                <el-button type="primary" @click="calcBw">转换</el-button>
              </el-form-item>
            </el-form>
            <div v-if="calculatorStore.bandwidthResult" class="result">
              <el-descriptions :column="1" border>
                <el-descriptions-item label="输入">{{ calculatorStore.bandwidthResult.value }} {{ calculatorStore.bandwidthResult.from }}</el-descriptions-item>
                <el-descriptions-item label="结果">
                  <strong style="color: #409EFF; font-size: 18px">{{ calculatorStore.bandwidthResult.result }} {{ calculatorStore.bandwidthResult.to }}</strong>
                </el-descriptions-item>
              </el-descriptions>
            </div>
          </el-card>
        </el-tab-pane>

        <!-- Timestamp -->
        <el-tab-pane label="时间戳转换" name="timestamp">
          <el-card>
            <el-form :model="tsForm" label-width="120px">
              <el-form-item label="Unix 时间戳">
                <el-input v-model="tsForm.timestamp" placeholder="输入秒级时间戳" clearable />
              </el-form-item>
              <el-form-item label="日期时间">
                <el-input v-model="tsForm.datetime" placeholder="格式：2024-01-01 12:00:00" clearable />
              </el-form-item>
              <el-form-item>
                <el-button type="primary" @click="calcTs">转换</el-button>
                <el-button @click="getNow">获取当前时间</el-button>
              </el-form-item>
            </el-form>
            <div v-if="calculatorStore.timestampResult" class="result">
              <el-descriptions :column="1" border>
                <el-descriptions-item label="时间戳">{{ calculatorStore.timestampResult.timestamp }}</el-descriptions-item>
                <el-descriptions-item label="UTC 时间">{{ calculatorStore.timestampResult.datetime_utc }}</el-descriptions-item>
                <el-descriptions-item label="本地时间">{{ calculatorStore.timestampResult.datetime_local }}</el-descriptions-item>
                <el-descriptions-item label="ISO">{{ calculatorStore.timestampResult.iso }}</el-descriptions-item>
              </el-descriptions>
            </div>
          </el-card>
        </el-tab-pane>

        <!-- Subnet -->
        <el-tab-pane label="IP 子网计算" name="subnet">
          <el-card>
            <el-form :model="subnetForm" label-width="100px">
              <el-form-item label="CIDR">
                <el-input v-model="subnetForm.cidr" placeholder="例如：192.168.1.0/24" clearable />
              </el-form-item>
              <el-form-item>
                <el-button type="primary" @click="calcSubnet">计算</el-button>
              </el-form-item>
            </el-form>
            <div v-if="calculatorStore.subnetResult" class="result">
              <el-descriptions :column="2" border>
                <el-descriptions-item label="网络地址">{{ calculatorStore.subnetResult.network }}</el-descriptions-item>
                <el-descriptions-item label="子网掩码">{{ calculatorStore.subnetResult.netmask }}</el-descriptions-item>
                <el-descriptions-item label="广播地址">{{ calculatorStore.subnetResult.broadcast }}</el-descriptions-item>
                <el-descriptions-item label="前缀长度">/{{ calculatorStore.subnetResult.prefixlen }}</el-descriptions-item>
                <el-descriptions-item label="可用主机数">{{ calculatorStore.subnetResult.total_hosts }}</el-descriptions-item>
                <el-descriptions-item label="IP 版本">IPv{{ calculatorStore.subnetResult.version }}</el-descriptions-item>
                <el-descriptions-item label="第一个可用主机">{{ calculatorStore.subnetResult.first_host }}</el-descriptions-item>
                <el-descriptions-item label="最后一个可用主机">{{ calculatorStore.subnetResult.last_host }}</el-descriptions-item>
              </el-descriptions>
            </div>
          </el-card>
        </el-tab-pane>
      </el-tabs>
    </div>
  </Layout>
</template>

<script setup>
import { reactive, ref } from 'vue'
import { ElMessage } from 'element-plus'
import { useCalculatorStore } from '@/stores/calculator'
import Layout from '@/components/Layout.vue'

const calculatorStore = useCalculatorStore()
const activeTab = ref('bandwidth')

const bwUnits = ['bps', 'Bps', 'Kbps', 'KBps', 'Mbps', 'MBps', 'Gbps', 'GBps']
const bwForm = reactive({
  value: 100,
  from_unit: 'Mbps',
  to_unit: 'MBps',
})

const tsForm = reactive({
  timestamp: '',
  datetime: '',
})

const subnetForm = reactive({
  cidr: '192.168.1.0/24',
})

const calcBw = async () => {
  try {
    await calculatorStore.calcBandwidth({
      value: bwForm.value,
      from_unit: bwForm.from_unit,
      to_unit: bwForm.to_unit,
    })
  } catch (e) {
    ElMessage.error(e.message || '转换失败')
  }
}

const calcTs = async () => {
  try {
    const payload = {}
    if (tsForm.timestamp) payload.timestamp = parseInt(tsForm.timestamp)
    if (tsForm.datetime) payload.datetime = tsForm.datetime
    await calculatorStore.calcTimestamp(payload)
  } catch (e) {
    ElMessage.error(e.message || '转换失败')
  }
}

const getNow = async () => {
  tsForm.timestamp = ''
  tsForm.datetime = ''
  await calculatorStore.calcTimestamp({})
}

const calcSubnet = async () => {
  try {
    await calculatorStore.calcSubnet({ cidr: subnetForm.cidr })
  } catch (e) {
    ElMessage.error(e.message || '计算失败')
  }
}
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
.result {
  margin-top: 20px;
  max-width: 600px;
}
</style>
