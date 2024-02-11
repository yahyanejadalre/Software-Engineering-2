export default ($axios) => ({
  list(page = 1, query) {
    const params = Object.assign({ page }, query)

    return $axios.get('/admin/cs/', { params })
  },

  details(id) {
    return $axios.get(`/admin/cs/${id}/`)
  },

  external(id) {
    return $axios.get(`/admin/cs/${id}/external_status/`)
  },

  internal(id) {
    return $axios.get(`/admin/cs/${id}/internal_status/`)
  },

  charging(id) {
    return $axios.patch(`/admin/socket/${id}/`, { is_charging: true })
  },

  setPowerSource(id, source, sourceId) {
    const data = { power_source: source }
    if (source !== 'Battery') {
      data.source_id = sourceId
    }

    return $axios.patch(`/admin/cs/${id}/set_power_source/`, data)
  },
})
