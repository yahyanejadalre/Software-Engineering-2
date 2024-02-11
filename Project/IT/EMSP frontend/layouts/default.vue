<template>
  <v-app>
    <AppBar />
    <Nuxt />
    <SnackBar />
  </v-app>
</template>

<script>
import SnackBar from '~/components/Widgets/SnackBar'
import AppBar from '~/components/Navigation/AppBar'

export default {
  name: 'DefaultLayout',

  components: { AppBar, SnackBar },

  middleware: 'auth',
}
</script>

<style>
/* sets the main background color of the greatest parent element */
.v-application--wrap {
  background-color: var(--clr-background) !important;
}
</style>
