<template>
  <div class="login">
    <div class="card" :class="{ flipped }">
      <!-- login form -->
      <div class="login-dialog front">
        <v-icon size="100" color="var(--clr-main-400)">
          mdi-lock-pattern
        </v-icon>

        <div class="login-dialog__title">Customer Login</div>

        <v-text-field
          v-model="info.username"
          type="username"
          placeholder="Username"
          background-color="var(--clr-main-400)"
          outlined
          rounded
          dense
          append-icon="mdi-information-variant"
        />
        <v-text-field
          v-model="info.password"
          type="password"
          placeholder="Password"
          background-color="var(--clr-main-400)"
          outlined
          rounded
          dense
          append-icon="mdi-key-variant"
          @keypress.enter="onLogin"
        />
        <v-btn
          :loading="loading"
          class="white--text"
          color="var(--clr-main-700)"
          @click="onLogin"
        >
          Login
        </v-btn>

        <div class="login-dialog__footer">
          Don't have an account?
          <span @click.self="flipped = !flipped"> Sign Up! </span>
        </div>
      </div>

      <!-- register form -->
      <div class="login-dialog back">
        <v-icon size="100" color="var(--clr-main-400)">
          mdi-account-multiple-plus-outline
        </v-icon>

        <div class="login-dialog__title">Customer Register</div>

        <v-text-field
          v-model="info.first_name"
          placeholder="First Name"
          background-color="var(--clr-main-400)"
          outlined
          rounded
          dense
        />
        <v-text-field
          v-model="info.last_name"
          placeholder="Last Name"
          background-color="var(--clr-main-400)"
          outlined
          rounded
          dense
        />
        <v-text-field
          v-model="info.email"
          placeholder="Email"
          type="email"
          background-color="var(--clr-main-400)"
          outlined
          rounded
          dense
        />
        <v-text-field
          v-model="info.password"
          placeholder="Password"
          background-color="var(--clr-main-400)"
          outlined
          rounded
          dense
        />
        <v-btn
          class="white--text"
          color="var(--clr-main-700)"
          :loading="loading"
          @click="onRegister"
        >
          Sign Up
        </v-btn>

        <div class="login-dialog__footer">
          Already have an account?
          <span @click.self="flipped = !flipped"> Log In! </span>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Login',

  layout: 'empty',

  middleware: 'auth',

  auth: 'guest',

  data() {
    return {
      flipped: false,
      loading: false,

      info: {
        username: null,
        email: null,
        password: null,
        first_name: null,
        last_name: null,
      },
    }
  },

  methods: {
    onRegister() {
      this.loading = true

      this.info.username = this.info.email
      this.$services.auth
        .register(this.info)
        .then(() => {
          this.$notifier.success('Registration Successful')
          this.flipped = false
        })
        .catch((err) => this.$notifier.error(err))
        .finally(() => (this.loading = false))
    },

    onLogin() {
      this.loading = true

      const data = {
        username: this.info.username,
        password: this.info.password,
      }

      this.$auth
        .loginWith('local', { data })
        .then(() => this.$notifier.success('Logged In Successfully!'))
        .catch((err) => this.$notifier.error(err))
        .finally(() => (this.loading = false))
    },
  },
}
</script>

<style lang="scss" scoped>
.login {
  padding: 1.5rem;
  height: 100%;

  .card {
    perspective: 150rem;
    position: relative;
    max-width: 400px;
    box-shadow: none;
    background: none;
    width: 100%;
    margin-inline: auto;

    &.flipped {
      .front {
        transform: rotateY(180deg);
      }
      .back {
        transform: rotateY(0deg);
      }
    }
  }

  .login-dialog {
    transition: all 0.8s ease;
    backface-visibility: hidden;
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    padding: 1.5rem;

    display: flex;
    align-items: center;
    flex-direction: column;

    background: rgba(255, 255, 255, 0.16);
    border-radius: 16px;
    box-shadow: 0 4px 30px rgba(0, 0, 0, 0.1);
    backdrop-filter: blur(5px);
    -webkit-backdrop-filter: blur(5px);
    border: 1px solid rgba(255, 255, 255, 0.3);

    & > * {
      width: 100%;
    }

    &__title {
      margin-bottom: 1rem;
      font-size: 2rem;
      font-weight: bolder;
      text-align: center;
      color: var(--clr-main-400);
      user-select: none;
    }

    &__footer {
      font-size: 0.85rem;
      text-align: center;
      color: white;
      margin-top: 0.5rem;

      span {
        text-decoration: underline;
        color: var(--clr-main-400);
        cursor: pointer;
      }
    }

    &.back {
      transform: rotateY(-180deg);
    }

    &.front {
      transform: rotateY(0deg);
    }
  }
}
</style>
