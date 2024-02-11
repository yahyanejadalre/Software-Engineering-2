export default ($axios) => ({
  register(data) {
    return $axios.post('/user/register/', data)
  },

  updateProfile(data) {
    return $axios.put('/user/profile/', data)
  },
})
