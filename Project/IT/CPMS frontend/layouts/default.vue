<template>
  <v-app>
    <navigation-drawer v-model="drawer" />
    <SnackBar />

    <v-main>
      <v-container>
        <nuxt />
      </v-container>
    </v-main>
  </v-app>
</template>

<script>
import NavigationDrawer from '~/components/main/NavigationDrawer'
import SnackBar from '~/components/main/SnackBar'

export default {
  name: 'DefaultLayout',

  components: { SnackBar, NavigationDrawer },

  middleware: 'auth',

  data() {
    return {
      drawer: false,
    }
  },
}
</script>
