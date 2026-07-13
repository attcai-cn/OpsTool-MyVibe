import { defineStore } from 'pinia'
import { ref } from 'vue'
import { noteApi } from '@/api'

export const useNoteStore = defineStore('note', () => {
  const notes = ref([])
  const total = ref(0)
  const currentNote = ref(null)

  async function fetchNotes(params = {}) {
    const res = await noteApi.list(params)
    notes.value = res.data.items
    total.value = res.data.total
    return res
  }

  async function fetchNote(id) {
    const res = await noteApi.get(id)
    currentNote.value = res.data
    return res
  }

  async function createNote(data) {
    const res = await noteApi.create(data)
    return res
  }

  async function updateNote(id, data) {
    const res = await noteApi.update(id, data)
    return res
  }

  async function deleteNote(id) {
    const res = await noteApi.remove(id)
    return res
  }

  return { notes, total, currentNote, fetchNotes, fetchNote, createNote, updateNote, deleteNote }
})
