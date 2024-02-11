<template>
  <div class="profile">
    <div class="profile__info">
      <!-- avatar -->
      <v-btn
        class="profile__info-avatar"
        icon
        outlined
        color="var(--clr-main-400)"
      >
        <v-icon size="50">mdi-account-tie</v-icon>
      </v-btn>

      <!-- name -->
      <div class="profile__info-name">
        {{ $auth.user?.first_name || '' }}
        {{ $auth.user?.last_name || '' }}
      </div>

      <!-- email -->
      <div class="profile__info-email">
        {{ $auth.user?.email || '' }}
      </div>

      <!-- statistics -->
      <div class="profile__info-statistics">
        <div>
          <span class="stat-title">{{ totalReservationsCount || '?' }}</span>
          <span class="stat-text">Total Reservations</span>
        </div>
        <div>
          <span class="stat-title">{{ formatDateJoined() }}</span>
          <span class="stat-text">Date Joined</span>
        </div>
        <div>
          <span class="stat-title big-font">{{ $auth.user?.id || '' }}</span>
          <span class="stat-text">User Id</span>
        </div>
      </div>

      <!-- buttons -->
      <div class="profile__info-buttons">
        <v-btn color="var(--clr-main-700)" dark small height="40" to="/">
          Start Booking
        </v-btn>
        <v-btn
          color="var(--clr-main-700)"
          dark
          small
          height="40"
          to="/panel/reservation_history"
        >
          Booking History
        </v-btn>
      </div>
    </div>

    <!-- update profile form -->
    <div class="profile__form">
      <v-text-field
        v-model="info.first_name"
        placeholder="First Name"
        background-color="var(--clr-main-400)"
        outlined
        dense
      />
      <v-text-field
        v-model="info.last_name"
        placeholder="Last Name"
        background-color="var(--clr-main-400)"
        outlined
        dense
      />
      <v-text-field
        v-model="info.email"
        placeholder="Email"
        type="email"
        background-color="var(--clr-main-400)"
        outlined
        dense
      />
      <v-text-field
        v-model="info.password"
        placeholder="New Password"
        background-color="var(--clr-main-400)"
        outlined
        dense
      />
      <v-btn
        dark
        color="var(--clr-main-700)"
        :loading="updateProfileLoading"
        @click="onUpdateProfile"
      >
        update
      </v-btn>
    </div>
  </div>
</template>

<script>
import moment from 'moment'

export default {
  name: 'Index',

  data() {
    return {
      updateProfileLoading: false,
      totalReservationsCount: 0,

      info: {
        username: null,
        email: null,
        password: null,
        first_name: null,
        last_name: null,
      },
    }
  },

  created() {
    const user = this.$auth.user
    if (!user) return

    this.info.username = user.username
    this.info.email = user.email
    this.info.first_name = user.first_name
    this.info.last_name = user.last_name
  },

  mounted() {
    this.$services.book.history({ size: 100 }).then((response) => {
      this.totalReservationsCount = response.data.count
    })
  },

  methods: {
    onUpdateProfile() {
      this.updateProfileLoading = true

      this.info.username = this.info.email

      const payload = JSON.parse(JSON.stringify(this.info))

      for (const key in payload) {
        if (payload[key] == null) delete payload[key]
      }

      this.$services.auth
        .updateProfile(payload)
        .then(() => {
          this.$notifier.success('Profile updated successfully')
        })
        .catch(() => {
          this.$notifier.error('Please fill the entire form')
        })
        .finally(() => {
          this.updateProfileLoading = false
        })
    },

    formatDateJoined() {
      return moment(this.$auth.user?.date_joined).format('MMM Do, YYYY')
    },
  },
}
</script>

<style lang="scss" scoped>
.profile {
  color: var(--clr-main-400);

  &__info {
    display: flex;
    flex-direction: column;
    align-items: center;
    background: linear-gradient(
      180deg,
      rgba(44, 27, 71, 1) 0%,
      rgba(11, 2, 5, 1) 100%
    );

    &-avatar {
      margin-top: 1rem;
      margin-bottom: 0.5rem;
      width: 70px;
      height: 70px;
    }

    &-name {
      font-weight: 300;
      font-size: 1.3rem;
    }

    &-statistics {
      display: grid;
      grid-template-columns: 1fr 1fr 1fr;
      place-items: center;
      width: 100%;
      gap: 0.5rem;
      margin-block: 2rem;

      & > div {
        display: flex;
        flex-direction: column;
        align-items: center;

        .stat-title {
          font-weight: bold;
        }

        .stat-text {
          font-size: 0.75rem;
        }
      }
    }

    &-buttons {
      display: flex;
      column-gap: 0.5rem;
      justify-content: space-around;
      width: 100%;

      & > button,
      & > a {
        width: 150px !important;
      }
    }
  }

  &__form {
    border: 2px solid var(--clr-main-900);
    margin-inline: 1rem;
    margin-block: 1.5rem;
    border-radius: 10px;
    overflow: hidden;
    padding: 1rem;
  }
}
</style>
