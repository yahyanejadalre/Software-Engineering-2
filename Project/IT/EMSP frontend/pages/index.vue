<template>
  <div class="cs contained">
    <v-stepper v-model="stepperValue" vertical dark class="stepper">
      <!-- step 1: select date and time -->
      <v-stepper-step :complete="stepperValue > 1" step="1">
        Select date and time
        <small>All fields are required.</small>
      </v-stepper-step>
      <v-stepper-content step="1">
        <div class="cs-form">
          <DatePicker v-model="date.start" label="Start Date" :min="today" />
          <TimePicker
            v-model="time.start"
            label="Start Time"
            :min="startTimeMin"
            :disabled="date.start == null"
          />

          <DatePicker
            v-model="date.end"
            label="End Date"
            :min="date.start"
            :disabled="date.start == null"
          />
          <TimePicker
            v-model="time.end"
            label="End Time"
            :min="endTimeMin"
            :disabled="date.end == null"
          />
        </div>
        <v-btn color="var(--clr-main-700)" @click="onCompleteStep1">
          Continue
        </v-btn>
      </v-stepper-content>

      <!-- step 2 -->
      <v-stepper-step :complete="stepperValue > 2" step="2">
        Find the best charging station
      </v-stepper-step>
      <v-stepper-content step="2">
        <v-select
          v-model="sortBy"
          outlined
          dense
          dark
          color="var(--clr-main-400)"
          label="Sort by"
          :items="sortItems"
          clearable
          @click:clear="sortBy = null"
          @change="onCompleteStep1"
        />

        <!-- charging station cards -->
        <ul v-if="csList.length > 0" class="cs-list">
          <li v-for="station in csList" :key="station.id">
            <div class="main-row" @click="expandStationCard(station)">
              <span class="id">
                {{ station.id }}
              </span>

              <span class="price">
                {{ station.price }}
                <span class="unit"> € </span>
              </span>

              {{ station.power_source }}

              <v-btn
                class="location"
                icon
                color="var(--clr-main-700)"
                :href="station.location"
                target="_blank"
              >
                <v-icon>mdi-map-marker-multiple</v-icon>
              </v-btn>
            </div>

            <div v-if="station.loading" class="progress centered">
              <v-progress-circular indeterminate color="var(--clr-main-400)" />
            </div>

            <div v-if="selectedStation.id === station.id" class="details-row">
              <v-simple-table dark class="table">
                <template #default>
                  <thead>
                    <tr>
                      <th class="text-left">Socket</th>
                      <th class="text-left">Speed</th>
                      <th class="text-center"></th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr
                      v-for="(item, index) in selectedStation.charging_sockets"
                      :key="item.name"
                    >
                      <td>{{ ++index }}</td>
                      <td>
                        {{ item.type }}
                        <v-icon
                          v-if="item.type === 'Fast' || item.type === 'Rapid'"
                          style="width: 17px"
                          color="var(--clr-main-400)"
                        >
                          mdi-flash
                        </v-icon>
                        <v-icon
                          v-if="item.type === 'Rapid'"
                          style="width: 1px"
                          color="var(--clr-main-400)"
                        >
                          mdi-flash
                        </v-icon>
                      </td>
                      <td class="text-right">
                        <v-btn
                          color="var(--clr-main-700)"
                          @click="onBookSocket(item)"
                        >
                          book
                        </v-btn>
                      </td>
                    </tr>
                  </tbody>
                </template>
              </v-simple-table>
            </div>
          </li>
        </ul>
        <v-btn color="var(--clr-main-700)" @click="stepperValue = 1">
          Previous Step
        </v-btn>
      </v-stepper-content>
    </v-stepper>
  </div>
</template>

<script>
import moment from 'moment'
import DatePicker from '~/components/Modified/DatePicker'
import TimePicker from '~/components/Modified/TimePicker'

export default {
  name: 'Index',

  components: { DatePicker, TimePicker },

  data() {
    return {
      today: moment().format(),
      stepperValue: 1,

      csList: [],
      loadingList: false,

      selectedStation: {},
      loadingGetStationDetails: false,

      date: {
        start: null,
        end: null,
      },

      time: {
        start: null,
        end: null,
      },

      sortBy: null,
      sortItems: [
        {
          text: 'Location',
          value: 'location',
        },
        {
          text: 'Price',
          value: 'price',
        },
        {
          text: 'Discount',
          value: 'discount',
        },
        {
          text: 'Power source',
          value: 'power_source',
        },
      ],
    }
  },

  computed: {
    startTimeMin() {
      if (!moment(this.date.start).isSame(moment(), 'day')) return undefined

      return moment().format('HH:mm')
    },

    endTimeMin() {
      if (this.date.start === this.date.end) return this.time.start
      return undefined
    },
  },

  methods: {
    expandStationCard(station) {
      if (this.loadingGetStationDetails) {
        return
      }

      // expand and shrink
      if (station.id === this.selectedStation.id) {
        this.selectedStation = {}
        return
      }

      // close old one before opening new one
      this.selectedStation = {}
      // this loading is global
      this.loadingGetStationDetails = true

      // this one is for each station card
      station.loading = true

      this.$services.cs
        .details(station.id)
        .then((response) => {
          this.selectedStation = response.data
        })
        .finally(() => {
          this.loadingGetStationDetails = false
          station.loading = false
        })
    },

    async onCompleteStep1() {
      this.loadingList = true

      const form = Object.values(this.date).concat(Object.values(this.time))

      if (form.includes(null)) {
        this.$notifier.error('Please fill all fields')
        return
      }

      const data = {
        start_time: `${this.date.start} ${this.time.start}`,
        end_time: `${this.date.end} ${this.time.end}`,
        size: 100,
        ...(this.sortBy && { ordering: this.sortBy }),
      }

      if (data.ordering === 'location') {
        await navigator.geolocation.getCurrentPosition(
          (res) => {
            data.latitude = res.coords.latitude
            data.longitude = res.coords.longitude

            this.loadList(data)
            this.stepperValue = 2
          },
          () => {
            this.$notifier.error('Location access denied! :(')
            this.csList = []
          }
        )
      } else {
        await this.loadList(data)
        this.stepperValue = 2
      }
    },

    async loadList(data) {
      await this.$services.cs
        .list(data)
        .then((response) => {
          this.csList = response.data.results

          this.csList.forEach((e) => {
            this.$set(e, 'loading', false)
          })
        })
        .catch((err) => {
          this.$notifier.error(err)
        })
        .finally(() => {
          this.loadingList = false
        })
    },

    onBookSocket(item) {
      const payload = {
        start_time: this.date.start + ' ' + this.time.start,
        end_time: this.date.end + ' ' + this.time.end,
        charging_socket: item.identifier,
      }

      this.$services.book
        .create(payload)
        .then(() => {
          this.$notifier.success('booking successful')
          this.$router.push('/panel/reservation_history')
        })
        .catch(() => this.$notifier.error())
    },
  },
}
</script>

<style lang="scss" scoped>
.cs {
  width: 100%;
  padding-inline: 0 !important;
}

.cs-list {
  margin-bottom: 1rem;
  padding-inline: 0.1rem !important;

  li {
    border-radius: 10px;
    overflow: hidden;
    border-bottom: 2px solid var(--clr-main-700);

    .main-row {
      background-color: var(--clr-main-400);
      color: var(--clr-background);
      padding: 0.5rem 1rem;
      display: grid;
      grid-template-columns: 50px 1fr 1fr 50px;
      place-items: center;

      .id {
        justify-self: start;
      }

      .price {
        font-size: 1.25rem;
        font-weight: bold;

        .unit {
          opacity: 0.8;
          font-size: 0.9rem;
        }
      }

      .location {
        justify-self: end;
      }
    }

    &:hover {
      outline: 2px solid var(--clr-main-700);
    }

    &:not(:last-child) {
      margin-bottom: 1rem;
    }

    .details-row {
      .table {
        background-color: var(--clr-main-900);

        tbody tr:hover {
          background-color: var(--clr-main-900) !important;
          opacity: 0.9;
        }
      }
    }

    .progress {
      padding: 0.5rem;
      background-color: var(--clr-main-900);
    }
  }
}

.cs-form {
  margin-top: 0.4rem;
}

.stepper {
  background-color: var(--clr-background);
}
</style>
