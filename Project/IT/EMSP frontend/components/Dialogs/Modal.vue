<template>
  <v-dialog
    :value="value"
    max-width="290"
    dark
    @click:outside="$emit('input', false)"
  >
    <div class="v-card-box-shadow dialog-content centered">
      <slot />
    </div>
  </v-dialog>
</template>

<script>
export default {
  name: 'Modal',

  props: {
    value: {
      type: Boolean,
      default: false,
    },
  },
}
</script>

<style scoped>
.dialog-content {
  padding: 1rem;
  min-height: 100px;
  min-width: 100px;
  border: 2px solid var(--clr-main-700);
  border-radius: 8px;
  overflow: hidden;
  background-color: var(--clr-background);
}
</style>
