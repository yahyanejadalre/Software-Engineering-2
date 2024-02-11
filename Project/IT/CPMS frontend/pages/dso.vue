<template>
  <v-card>
    <v-card-title>
      DSOs

      <v-btn
        small
        color="green white--text"
        depressed
        class="ml-2"
        @click="updateStatus"
      >
        Update Status
      </v-btn>
    </v-card-title>

    <v-data-table
      :headers="headers"
      :items="list"
      :options.sync="options"
      :server-items-length="totalCount"
      :footer-props="footerProps"
      :loading="loading || $fetchState.pending"
      disable-sort
    >
      <template #[`item.actions`]="{ item, index }">
        <v-tooltip
          v-if="totalCount > 1 && item.is_available && !item.active"
          top
        >
          <template #activator="{ on, attrs }">
            <v-btn
              v-bind="attrs"
              icon
              color="var(--clr-primary-500)"
              @click="activate(index)"
              v-on="on"
            >
              <v-icon>mdi-lightning-bolt-circle</v-icon>
            </v-btn>
          </template>
          <span>Acquire Energy</span>
        </v-tooltip>
      </template>
    </v-data-table>
  </v-card>
</template>

<script>
export default {
  name: 'DSOPage',

  data() {
    return {
      loading: false,
      headers: [
        { text: 'ID', value: 'id' },
        { text: 'Name', value: 'name' },
        { text: 'Price', value: 'price' },
        { text: 'Actions', value: 'actions' },
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

    await this.$services.dso
      .list()
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
      title: 'DSOs',
    }
  },

  methods: {
    async updateStatus() {
      this.loading = true

      await this.$services.dso.updateStatus().then((response) => {
        this.$notifier.success(response.data.message)

        this.$fetch()
      })
    },

    async activate(index) {
      this.loading = true

      await this.$services.dso
        .activate(this.list[index].id)
        .then((response) => {
          this.$notifier.success(response.data.message)

          this.$fetch()
        })
    },
  },
}
</script>
