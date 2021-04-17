<template>
  <tr class="heclthCheckTableRow" @click="collapsed = !collapsed">
    <td>
      <div class="ui progress" :class="check.status">
        <div class="bar" style="width: 100%"><span> {{ check.status }} </span>
        </div>
      </div>
    </td>
    <td>{{ check.name }}</td>
    <td>{{ check.token }}</td>
    <td>{{ check.period }}</td>
    <td>{{ check.grace }} min</td>
    <td>{{ check.next_time }}</td>
    <td>{{ check.last_ping }}</td>
  </tr>
</template>

<script lang="ts">
import {defineComponent, ref, PropType} from 'vue';
import useCheck from './useCheck';

export default defineComponent({
  name: 'HealthCheckTableItem',
  props: {
    check: {
      type: Object as PropType<ChecksStatusItem | ChecksBoxItem>,
      default: {}
    }
  },
  setup(props) {
    const collapsed = ref(true);
    const utils = useCheck(props);
    return {
      collapsed,
      ...utils
    };
  }
});
</script>

<style scoped>

tr.heclthCheckTableRow {
  background-color: rgba(249, 249, 249, .8);
  vertical-align: middle;
}

div.progress {
  display: inline-block;
  overflow: hidden;
  height: 25px;
  width: 50px;
  border-radius: 6px;
  margin-bottom: 0 !important;
}

div.progress div.bar {
  height: 25px;
  border-radius: 6px;
  font-size: .9rem;
  line-height: 25px;
  color: white;
}

tr td {
  color: #616366;
  font-weight: bold;
  border: none !important;
}
</style>
