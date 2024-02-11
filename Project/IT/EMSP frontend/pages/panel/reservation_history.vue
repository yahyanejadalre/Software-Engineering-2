<template>
  <div class="res-history contained">
    <v-data-table
      :items="bookingHistoryList"
      :loading="listLoading"
      :headers="headers"
      dark
      class="res-history__table"
      :options.sync="options"
      :server-items-length="totalServerItemsCount"
    >
      <template #[`item.created_at`]="{ item }">
        {{ formatDateTime(item.created_at) }}
      </template>

      <template #[`item.start_time`]="{ item }">
        {{ formatDateTime(item.start_time) }}
      </template>

      <template #[`item.end_time`]="{ item }">
        {{ formatDateTime(item.end_time) }}
      </template>

      <template #[`item.price`]="{ item }"> {{ item.price }} € </template>

      <template #[`item.actions`]="{ item }">
        <v-btn
          color="var(--clr-main-400)"
          icon
          @click="onShowQrCode(item.unique_code)"
        >
          <v-icon>mdi-eye</v-icon>
        </v-btn>
      </template>
    </v-data-table>

    <Modal v-model="qrCode.dialog">
      <VueQrcode :value="qrCode.value" :options="{ width: 200 }"></VueQrcode>
    </Modal>
  </div>
</template>

<script>
import moment from 'moment'
import VueQrcode from '@chenfengyuan/vue-qrcode'
import Modal from '@/components/Dialogs/Modal'

export default {
  name: 'ReservationHistory',

  components: { Modal, VueQrcode },

  data() {
    return {
      listLoading: false,
      bookingHistoryList: [],

      options: {},
      totalServerItemsCount: 0,

      qrCode: {
        dialog: false,
        value: 'No Text',
      },

      headers: [
        { text: '#', value: 'id' },
        { text: 'Book Date', value: 'created_at' },
        { text: 'Charging Start', value: 'start_time' },
        { text: 'Charging End', value: 'end_time' },
        { text: 'Price', value: 'price' },
        { text: 'Status', value: 'status' },
        { text: 'QrCode', value: 'actions' },
      ],
    }
  },

  watch: {
    options: {
      handler(newValue, oldValue) {
        if (oldValue.page) {
          this.loadList()
        }
      },
      deep: true,
    },
  },

  mounted() {
    this.listLoading = true

    this.$services.book
      .history({ page: 1 })
      .then((response) => {
        this.bookingHistoryList = response.data.results
        this.totalServerItemsCount = response.data.count
      })
      .finally(() => {
        this.listLoading = false
      })
  },

  methods: {
    loadList() {
      this.listLoading = true

      const { sortBy, sortDesc, page, itemsPerPage } = this.options

      let ordering = null
      if (sortBy.length > 0) {
        ordering = sortBy[0]
        if (sortDesc[0]) {
          ordering = `-${ordering}`
        }
      }

      const query = { ordering, size: itemsPerPage, page }

      this.$services.book
        .history(query)
        .then((response) => {
          this.bookingHistoryList = response.data.results
          this.totalServerItemsCount = response.data.count
        })
        .finally(() => (this.listLoading = false))
    },

    onShowQrCode(uniqueCode) {
      this.qrCode.dialog = true
      this.qrCode.value = uniqueCode
    },

    formatDateTime(dateTime) {
      return moment(dateTime).format('YYYY-MM-DD HH:mm')
    },
  },
}
</script>

<style lang="scss" scoped>
.res-history {
  padding-block: 1rem;

  &__table {
    background-color: var(--clr-background);
    border: 2px solid var(--clr-main-900);
    border-radius: 10px;
    overflow: hidden;

    &::v-deep th {
      background-color: var(--clr-main-700) !important;
    }

    &::v-deep tr:hover {
      background-color: var(--clr-main-900) !important;
    }

    &::v-deep .v-data-table__mobile-row {
      min-height: 40px !important;
    }
  }
}
</style>
