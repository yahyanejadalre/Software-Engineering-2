<template>
  <v-card>
    <v-card-title>
      Charging Station Details

      <v-row>
        <v-col cols="3">
          <v-select
            v-model="selectedPowerSource"
            :items="powerSources"
            label="Power Source"
            class="ml-4"
            hide-details
            outlined
            dense
          ></v-select>
        </v-col>
      </v-row>
    </v-card-title>

    <v-card-text>
      <v-row>
        <v-col cols="3">ID: {{ $route.params.id }}</v-col>
        <v-col cols="3">
          Location:

          <v-btn
            x-small
            depressed
            color="blue white--text"
            :href="location"
            target="_blank"
          >
            Show on Map
          </v-btn>
        </v-col>
        <v-col cols="3">
          Price: &euro;
          {{ price }}
        </v-col>
        <v-col v-if="batteryLevel !== null" cols="3">
          Battery Level: {{ batteryLevel }}%
        </v-col>
        <v-col cols="3">Charging Sockets: {{ list.length }}</v-col>
        <v-col cols="3">Vehicle Charged: {{ vehicleCharged ?? 0 }}</v-col>

        <v-col cols="12">
          <v-data-table
            :headers="headers"
            :items="list"
            :options.sync="options"
            :server-items-length="totalCount"
            :footer-props="footerProps"
            :loading="loading || $fetchState.pending"
            disable-sort
          >
            <template #[`item.is_available`]="{ item }">
              <span
                :class="{
                  'red--text': item.is_available,
                  'green--text': !item.is_available,
                }"
              >
                {{ item.is_available ? 'Yes' : 'No' }}
              </span>
            </template>

            <template #[`item.charging_process`]="{ item }">
              {{ chargingProcess(item) }}
            </template>

            <template #[`item.actions`]="{ item, index }">
              <v-tooltip v-if="item.is_available && !item.is_charging" top>
                <template #activator="{ on, attrs }">
                  <v-btn
                    v-bind="attrs"
                    icon
                    color="var(--clr-primary-500)"
                    @click="chargeVehicle(index)"
                    v-on="on"
                  >
                    <v-icon>mdi-car-electric</v-icon>
                  </v-btn>
                </template>
                <span>Start Charging The Vehicle</span>
              </v-tooltip>
            </template>
          </v-data-table>
        </v-col>
      </v-row>
    </v-card-text>
  </v-card>
</template>

<script>
import moment from 'moment'

export default {
  name: 'CSDetailsPage',

  data() {
    return {
      loading: false,
      headers: [
        { text: 'Type', value: 'type' },
        // { text: 'Cost', value: 'cost' },
        { text: 'Is Available', value: 'is_available' },
        { text: 'Charging Process', value: 'charging_process' },
        { text: 'Actions', value: 'actions' },
      ],
      list: [],
      totalCount: 0,
      options: {},
      footerProps: {
        itemsPerPageOptions: [5, 10, 20, 30, 50, 100],
      },
      price: 35,
      location: '#aaa',
      batteryLevel: null,
      vehicleCharged: null,
      selectedPowerSource: 'DSO',
      powerSources: ['DSO', 'Battery', 'Mix'],
      dsoPowerSourceId: null,
    }
  },

  async fetch() {
    this.loading = true

    await Promise.all([
      this.$services.cs.details(this.$route.params.id).then((response) => {
        this.selectedPowerSource = response.data.power_source
        this.price = response.data.price
        this.location = response.data.location

        this.list = response.data.sockets
        this.totalCount = this.list.length
      }),
      this.$services.cs.internal(this.$route.params.id).then((response) => {
        this.batteryLevel = response.data.battery_level
        this.vehicleCharged = response.data.vehicle_charged
      }),
      this.$services.dso.getTheActive().then((response) => {
        this.dsoPowerSourceId = response.data.results[0].identifier
      }),
    ]).finally(() => {
      this.loading = false
    })
  },

  head() {
    return {
      title: 'Charging Station Details',
    }
  },

  watch: {
    selectedPowerSource(val) {
      this.$services.cs.setPowerSource(
        this.$route.params.id,
        val,
        this.dsoPowerSourceId
      )
    },
  },

  methods: {
    ceil: Math.ceil,

    chargingProcess(item) {
      if (!item.is_charging) return ''

      const toNow = moment(item.next_available_time).toNow()

      return `${item.current_vehicle_charging_level}% (available ${toNow})`
    },

    chargeVehicle(index) {
      const item = this.list[index]

      this.loading = true

      this.$services.cs
        .charging(item.identifier)
        .then((response) => {
          this.$set(this.list, index, response.data)
        })
        .finally(() => (this.loading = false))
    },
  },
}
</script>
