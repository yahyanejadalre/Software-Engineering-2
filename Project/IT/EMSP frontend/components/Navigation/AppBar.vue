<template>
  <div class="appbar">
    <v-btn
      class="appbar__avatar"
      icon
      outlined
      color="var(--clr-main-400)"
      to="/panel"
      exact
    >
      <v-icon>mdi-account-tie</v-icon>
    </v-btn>

    <span class="appbar__text">
      {{ appbarText }}
    </span>

    <v-btn
      class="appbar__menu"
      icon
      color="var(--clr-main-400)"
      @click.prevent="navigationDrawer = true"
    >
      <v-icon>mdi-menu</v-icon>
    </v-btn>

    <NavigationDrawer v-model="navigationDrawer" />
  </div>
</template>

<script>
import NavigationDrawer from '~/components/Navigation/NavigationDrawer'

export default {
  name: 'AppBar',

  components: { NavigationDrawer },

  data() {
    return {
      navigationDrawer: false,
    }
  },

  computed: {
    appbarText() {
      const defaultText = 'Hello ' + this.$auth.user?.first_name || ''

      if (this.$route?.name === 'panel') return 'PROFILE'

      return defaultText
    },
  },
}
</script>

<style lang="scss" scoped>
.appbar {
  color: var(--clr-main-400);
  background-color: var(--clr-main-900);
  display: flex;
  align-items: center;
  padding: 0.5rem;

  &__avatar {
    margin-right: 1rem;
  }

  &__text {
    font-weight: bold;
  }

  &__menu {
    margin-left: auto;
  }
}
</style>
