<template>
  <transition name="snack">
    <div
      v-if="show"
      class="snackbar"
      :style="{ backgroundColor: color }"
      @click="show = false"
    >
      <div class="snackbar-box">
        {{ message }}
      </div>
      <div
        class="snackbar-line"
        :style="{ animationDuration: activeTime + 'ms' }"
      />
    </div>
  </transition>
</template>

<script>
export default {
  data() {
    return {
      show: false,
      message: '',
      color: '',
      activeTime: 0,
    }
  },

  created() {
    this.$store.subscribe((mutation, state) => {
      if (mutation.type !== 'snackbar/showMessage') return

      this.message = state.snackbar.message
      this.color = state.snackbar.color
      this.activeTime = state.snackbar.activeTime
      this.show = true

      setTimeout(() => {
        this.show = false
      }, this.activeTime)
    })
  },
}
</script>

<style lang="scss" scoped>
.snackbar {
  position: fixed;
  z-index: 9999;
  bottom: 20px;
  left: 50%;
  transform: translateX(-50%);
  border-radius: 5px;
  min-width: 310px;
  margin-inline: 0.5rem;

  &-box {
    padding: 0.5rem 1.5rem;
    font-size: 0.95rem;
    font-weight: 500;
    color: white;
    text-align: center;
  }

  &-line {
    height: 4px;
    background-color: white;
    animation-name: line;
    animation-timing-function: linear;
    border-radius: 2px;
  }
}

@keyframes line {
  from {
    width: 0;
  }
  to {
    width: 100%;
  }
}

.snack-enter-active,
.snack-leave-active {
  transition: all 200ms ease-out;
}

.snack-enter {
  transform: translateX(-100%);
  opacity: 0;
}

.snack-leave-active {
  transform: translateX(0);
  opacity: 0;
}
</style>
