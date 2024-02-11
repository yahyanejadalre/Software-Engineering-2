<template>
  <v-container class="h-100 d-flex align-center">
    <v-row class="justify-center">
      <v-col cols="12" md="8" class="text-center">
        <h1>Charge Point Management System</h1>
      </v-col>

      <v-col cols="12" md="8">
        <login-form />
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import LoginForm from '~/components/auth/LoginForm'

export default {
  components: { LoginForm },

  layout: 'empty',

  head() {
    return {
      titleTemplate: 'Charge Point Management System',
    }
  },
}
</script>

<style scoped>
.h-100 {
  height: 100%;
}
</style>
