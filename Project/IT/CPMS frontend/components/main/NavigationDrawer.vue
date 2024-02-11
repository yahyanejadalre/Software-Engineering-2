<template>
  <v-navigation-drawer
    :value="value"
    fixed
    app
    clipped
    :permanent="$vuetify.breakpoint.mdAndUp"
    :temporary="$vuetify.breakpoint.smAndDown"
    @input="(v) => $emit('input', v)"
  >
    <v-list>
      <v-list-item>
        <v-list-item-avatar>
          <v-img :src="avatar"></v-img>
        </v-list-item-avatar>
      </v-list-item>

      <v-list-item>
        <v-list-item-content>
          <v-list-item-title class="title">
            {{ fullname }}
          </v-list-item-title>
          <v-list-item-subtitle>
            {{ email }}
          </v-list-item-subtitle>
        </v-list-item-content>
      </v-list-item>
    </v-list>

    <v-divider></v-divider>

    <v-list rounded nav dense>
      <v-list-item-group color="primary">
        <v-list-item v-for="(item, i) in items" :key="i" :to="item.to" exact>
          <v-list-item-icon>
            <v-icon color="var(--clr-primary-500)">{{ item.icon }}</v-icon>
          </v-list-item-icon>

          <v-list-item-content>
            <v-list-item-title>
              {{ item.text }}
            </v-list-item-title>
          </v-list-item-content>
        </v-list-item>
      </v-list-item-group>
    </v-list>

    <template #append>
      <v-list-item @click="logout">
        <v-list-item-icon>
          <v-icon color="var(--clr-primary-500)">mdi-logout</v-icon>
        </v-list-item-icon>

        <v-list-item-content>
          <v-list-item-title>Logout</v-list-item-title>
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
        {
          text: 'Charging Stations',
          icon: 'mdi-ev-station',
          to: '/',
        },
        {
          text: 'DSOs',
          icon: 'mdi-lightning-bolt-outline',
          to: '/dso',
        },
      ],
    }
  },

  computed: {
    avatar() {
      // if (this.$auth.user && this.$auth.user.avatar) {
      //   return this.$auth.user.avatar
      // }

      return require('~/static/default-user.jpg')
    },

    fullname() {
      let fullname =
        this.$auth.user.first_name + ' ' + this.$auth.user.last_name
      fullname = fullname.trim()

      return fullname || '[No Name]'
    },

    email() {
      return this.$auth.user.email || ''
    },
  },

  methods: {
    async logout() {
      await this.$auth.logout()
    },
  },
}
</script>
