<template>
  <v-app>
    <Nuxt />
    <SnackBar />
  </v-app>
</template>

<script>
import SnackBar from '~/components/Widgets/SnackBar'

export default {
  name: 'EmptyLayout',

  components: { SnackBar },
}
</script>

<style>
/* sets the main background color of the greatest parent element */
.v-application--wrap {
  background-color: var(--clr-background) !important;
}
</style>
