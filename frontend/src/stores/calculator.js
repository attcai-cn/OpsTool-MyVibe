import { defineStore } from 'pinia'
import { ref } from 'vue'
import { calculatorApi } from '@/api'

export const useCalculatorStore = defineStore('calculator', () => {
  const bandwidthResult = ref(null)
  const timestampResult = ref(null)
  const subnetResult = ref(null)

  async function calcBandwidth(data) {
    const res = await calculatorApi.bandwidth(data)
    bandwidthResult.value = res.data
    return res
  }

  async function calcTimestamp(data) {
    const res = await calculatorApi.timestamp(data)
    timestampResult.value = res.data
    return res
  }

  async function calcSubnet(data) {
    const res = await calculatorApi.subnet(data)
    subnetResult.value = res.data
    return res
  }

  return { bandwidthResult, timestampResult, subnetResult, calcBandwidth, calcTimestamp, calcSubnet }
})
