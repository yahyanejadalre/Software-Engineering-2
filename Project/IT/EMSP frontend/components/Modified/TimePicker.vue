<template>
  <v-dialog ref="dialog" v-model="modal" width="290px">
    <template #activator="{ on, attrs }">
      <v-text-field
        :value="value"
        class="custom-date-picker"
        :label="label"
        :disabled="disabled"
        prepend-icon="mdi-clock"
        readonly
        v-bind="attrs"
        outlined
        dense
        background-color="var(--clr-main-400)"
        light
        v-on="on"
      ></v-text-field>
    </template>
    <v-time-picker
      :value="value"
      scrollable
      color="var(--clr-main-400)"
      :min="min"
      dark
      @change="onSelectDate"
    />
  </v-dialog>
</template>

<script>
export default {
  name: 'DatePicker',

  props: {
    value: {
      type: String,
      default: null,
    },

    label: {
      type: String,
      default: 'Select Time',
    },

    min: {
      type: String,
      default: undefined,
    },

    disabled: {
      type: Boolean,
      default: false,
    },
  },

  data() {
    return {
      modal: false,
    }
  },

  methods: {
    onSelectDate(e) {
      this.$emit('input', e)
      this.modal = false
    },
  },
}
</script>

<style scoped>
.custom-date-picker::v-deep(i.v-icon) {
  color: var(--clr-main-400);
}

.custom-date-picker::v-deep(.v-label) {
  background-color: var(--clr-main-400);
  border-radius: 100vmax;
  padding-inline: 0.2rem;
}
</style>
