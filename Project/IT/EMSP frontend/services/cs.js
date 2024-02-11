export default ($axios) => ({
  list(params) {
    return $axios.get('/cs/', { params })
  },

  details(id) {
    return $axios.get(`/cs/${id}/`)
  },
})
