export const state = () => ({
  message: null,
  color: null,
  activeTime: null,
})

export const mutations = {
  showMessage(state, { message, color, activeTime }) {
    state.message = message
    state.color = color
    state.activeTime = activeTime
  },
}
