export default ($axios) => ({
  list() {
    return $axios.get('/dso/')
  },

  updateStatus() {
    return $axios.post('/dso/update_dso_status/')
  },

  activate(id) {
    return $axios.patch(`/dso/${id}/activate/`)
  },

  getTheActive() {
    return $axios.get('/dso/', {
      query: {
        active: true,
        is_available: true,
      },
    })
  },
})
