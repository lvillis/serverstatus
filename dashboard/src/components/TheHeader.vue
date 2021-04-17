<template>
  <div class="ui vertical masthead center aligned segment" id="header">
    <div id="header-content">
      <h2 class="ui inverted header">
        ServerStatus & HealthChecks
      </h2>
    </div>
  </div>
</template>
<script lang="ts">
import {defineComponent} from 'vue';

export default defineComponent({
  name: 'TheHeader'
});
</script>
<style scoped>
#header {
  height: 5rem;
  position: relative;
  /*Replace your header image at this place!*/
}

#header::before {
  content: '';
  position: absolute;
  width: 100%;
  top: 0;
  left: 0;
  bottom: 0;
  right: 0;
  z-index: 1;
  background: rgba(66, 64, 64, .15);
}

/*#header::after {
    content: '';
    display: inline-block;
    vertical-align: middle;
    height: 100%;
}*/
#header-content {
  text-shadow: 2px 2px 2px #666;
  position: absolute;
  z-index: 3;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
}

#header h1 {
  font-size: 3.57rem;
  white-space: nowrap;
}

#header p {
  font-size: 1.5rem;
  color: aliceblue;
  /*white-space: nowrap;*/
}
</style>
