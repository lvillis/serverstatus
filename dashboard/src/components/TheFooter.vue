<template>
  <p><a href="https://github.com/lvillis/serverstatus">ServerStatus</a></p>
</template>

<script lang="ts">
import {defineComponent} from 'vue';

export default defineComponent({
  name: 'TheFooter'
});
</script>

<style scoped>
p {
  text-align: center;
  padding-bottom: 15px;
}

p a {
  vertical-align: middle;
}

p a:hover {
  color: #ff779a;
}
</style>
