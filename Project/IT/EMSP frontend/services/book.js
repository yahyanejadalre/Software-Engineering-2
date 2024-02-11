export default ($axios) => ({
  create(data) {
    return $axios.post('/booking/', data)
  },

  history(params) {
    return $axios.get('/booking/', { params })
  },
})
