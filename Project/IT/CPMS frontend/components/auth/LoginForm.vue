<template>
  <v-card :loading="loading">
    <v-card-title>
      <span class="headline">Login</span>
    </v-card-title>

    <v-card-subtitle class="mt-0">
      Enter your credentials to log in.
    </v-card-subtitle>

    <v-card-text>
      <v-form
        ref="form"
        v-model="valid"
        lazy-validation
        @submit.prevent="login"
      >
        <v-container>
          <v-row>
            <v-col cols="12">
              <v-text-field
                v-model="username"
                label="Username"
                prepend-inner-icon="mdi-account"
                :rules="usernameRules"
                hide-details="auto"
                required
                @keyup.enter="login"
              ></v-text-field>
            </v-col>

            <v-col cols="12">
              <v-text-field
                v-model="password"
                label="Password"
                prepend-inner-icon="mdi-lock-outline"
                :rules="passwordRules"
                type="password"
                required
                @keyup.enter="login"
              ></v-text-field>
            </v-col>
          </v-row>
        </v-container>
      </v-form>
    </v-card-text>
    <v-card-actions>
      <v-spacer></v-spacer>
      <v-btn
        color="blue darken-1"
        text
        :loading="loading"
        :disabled="loading"
        @click="login"
      >
        Login
      </v-btn>
    </v-card-actions>
  </v-card>
</template>

<script>
export default {
  name: 'LoginForm',

  data() {
    return {
      valid: false,

      username: '',
      password: '',

      usernameRules: [(v) => !!v || 'This field is required!'],

      passwordRules: [
        (v) => !!v || 'This field is required!',
        (v) => v.length >= 4 || 'Must be at least 4 characters long',
      ],

      loading: false,
    }
  },

  methods: {
    async login() {
      if (!this.$refs.form.validate()) {
        return
      }

      const credentials = {
        username: this.username,
        password: this.password,
      }

      this.loading = true

      await this.$auth
        .loginWith('local', {
          data: credentials,
        })
        .then(() => {
          this.$notifier.success()
        })
        .catch(() => {
          this.$notifier.error('Username or Password is incorrect')
        })
        .finally(() => {
          this.loading = false
        })
    },
  },
}
</script>
