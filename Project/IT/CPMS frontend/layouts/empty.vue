<template>
  <v-app>
    <v-main>
      <Nuxt />
      <SnackBar />
    </v-main>
  </v-app>
</template>

<script>
import SnackBar from '~/components/main/SnackBar'

export default {
  name: 'EmptyLayout',

  components: { SnackBar },
}
</script>
