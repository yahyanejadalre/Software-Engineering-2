<template>
  <v-navigation-drawer
    dark
    :value="value"
    absolute
    temporary
    color="var(--clr-background)"
    @input="$emit('input', $event)"
  >
    <v-list-item>
      <v-list-item-avatar>
        <v-btn icon outlined color="var(--clr-main-400)">
          <v-icon>mdi-account-tie</v-icon>
        </v-btn>
      </v-list-item-avatar>

      <v-list-item-content>
        <v-list-item-title class="font-color">
          {{ $auth.user?.first_name || '??' }}
        </v-list-item-title>
      </v-list-item-content>
    </v-list-item>

    <v-divider></v-divider>

    <v-list dense>
      <v-list-item
        v-for="item in items"
        :key="item.title"
        link
        :to="item.to"
        exact
      >
        <v-list-item-icon>
          <v-icon color="var(--clr-main-400)">{{ item.icon }}</v-icon>
        </v-list-item-icon>

        <v-list-item-content>
          <v-list-item-title class="font-color">
            {{ item.title }}
          </v-list-item-title>
        </v-list-item-content>
      </v-list-item>
    </v-list>

    <!-- logout -->
    <template #append>
      <v-list-item @click="logout">
        <v-list-item-icon>
          <v-icon color="var(--clr-main-400)">mdi-logout-variant</v-icon>
        </v-list-item-icon>

        <v-list-item-content>
          <v-list-item-title class="font-color">Logout</v-list-item-title>
        </v-list-item-content>
      </v-list-item>
    </template>
  </v-navigation-drawer>
</template>

<script>
export default {
  name: 'NavigationDrawer',

  props: {
    value: {
      type: Boolean,
      default: false,
    },
  },

  data() {
    return {
      items: [
        { title: 'Home', icon: 'mdi-home', to: '/' },
        {
          title: 'Booking History',
          icon: 'mdi-view-list',
          to: '/panel/reservation_history',
        },
        {
          title: 'Profile Information',
          icon: 'mdi-account-edit',
          to: '/panel',
        },
      ],
    }
  },

  methods: {
    async logout() {
      await this.$auth.logout()
    },
  },
}
</script>
