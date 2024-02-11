<template>
  <v-card>
    <v-card-title>Charging Stations</v-card-title>

    <v-data-table
      :headers="headers"
      :items="list"
      :options.sync="options"
      :server-items-length="totalCount"
      :footer-props="footerProps"
      :loading="loading || $fetchState.pending"
    >
      <template #[`item.location`]="{ item }">
        <v-btn
          x-small
          depressed
          color="blue white--text"
          :href="item.location"
          target="_blank"
        >
          Show on Map
        </v-btn>
      </template>

      <template #[`item.price`]="{ item }">
        &euro;
        {{ item.price }}
      </template>

      <template #[`item.actions`]="{ item }">
        <v-tooltip top>
          <template #activator="{ on, attrs }">
            <v-btn
              v-bind="attrs"
              icon
              color="var(--clr-primary-500)"
              :to="{ name: 'cs-id', params: { id: item.id } }"
              v-on="on"
            >
              <v-icon>mdi-eye</v-icon>
            </v-btn>
          </template>
          <span>See More</span>
        </v-tooltip>
      </template>
    </v-data-table>
  </v-card>
</template>

<script>
export default {
  name: 'CSPage',

  data() {
    return {
      loading: false,
      headers: [
        { text: 'ID', value: 'id' },
        { text: 'Location', value: 'location' },
        { text: 'Power Source', value: 'power_source' },
        { text: 'Price', value: 'price' },
        { text: 'Actions', value: 'actions', sortable: false },
      ],
      list: [],
      totalCount: 0,
      options: {},
      footerProps: {
        itemsPerPageOptions: [5, 10, 20, 30, 50, 100],
      },
    }
  },

  async fetch() {
    this.loading = true

    const { query } = this.$route
    await this.$services.cs
      .list(1, query)
      .then((response) => {
        this.list = response.data.results
        this.totalCount = response.data.count
      })
      .finally(() => {
        this.loading = false
      })
  },

  head() {
    return {
      title: 'Charging Stations',
    }
  },

  watch: {
    '$route.query': '$fetch',

    options: {
      handler(newValue, oldValue) {
        if (oldValue.page) {
          this.loadList()
        }
      },
      deep: true,
    },
  },

  methods: {
    loadList() {
      this.loading = true

      const { sortBy, sortDesc, page, itemsPerPage } = this.options

      let ordering = null
      if (sortBy.length > 0) {
        ordering = sortBy[0]
        if (sortDesc[0]) {
          ordering = `-${ordering}`
        }
      }

      const query = Object.assign(
        JSON.parse(JSON.stringify(this.$route.query)),
        { ordering, size: itemsPerPage }
      )

      this.$services.cs
        .list(page ?? 1, query)
        .then((response) => {
          this.list = response.data.results
          this.totalCount = response.data.count
        })
        .finally(() => (this.loading = false))
    },
  },
}
</script>
