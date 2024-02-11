export default ({ app, store }, inject) => {
  inject('notifier', {
    success(message = 'Success!', activeTime = 2000) {
      store.commit('snackbar/showMessage', {
        message,
        activeTime,
        color: 'green',
      })
    },

    warning(message = 'There might be a problem!', activeTime = 2000) {
      store.commit('snackbar/showMessage', {
        message,
        color: '#8F7000',
        activeTime,
      })
    },

    error(message = 'Failed', activeTime = 2000) {
      store.commit('snackbar/showMessage', {
        message,
        color: '#ba0020ff',
        activeTime,
      })
    },

    info(message = 'Done!', activeTime = 2000) {
      store.commit('snackbar/showMessage', {
        message,
        color: 'blue',
        activeTime,
      })
    },

    custom(message = 'Shiiit', color = 'black', activeTime = 2000) {
      store.commit('snackbar/showMessage', { message, color, activeTime })
    },
  })
}
