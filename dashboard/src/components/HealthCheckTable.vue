<template>
  <div class="ui container">
    <table class="ui basic unstackable selectable striped very compact table" id="health_check_table">
      <thead>
      <tr>
        <th id="status">Status</th>
        <th id="name">Name</th>
        <th id="token">Token</th>
        <th id="period">Period</th>
        <th id="grace">Grace</th>
        <th id="nexttime">Next Time</th>
        <th id="lastping">Last Ping</th>
      </tr>
      </thead>
      <tbody id="checks">
      <!-- Checks here \o/ -->
      <!--
      use index for the key may cause performance issues when delete a server from array,
      but not a big matter and we cannot find a more suitable data for the unique key.
      -->
      <table-item v-for="(check, index) of checks" :key="index" :check="check"/>
      </tbody>
    </table>
  </div>
</template>

<script lang="ts">
import {defineComponent, PropType} from 'vue';
import TableItem from '@/components/HealthCheckTableItem.vue';

export default defineComponent({
  name: 'HealthCheckTable',
  props: {
    checks: {
      type: Array as PropType<Array<ChecksStatusItem | ChecksBoxItem>>,
      default: []
    }
  },
  components: {
    TableItem
  }
});
</script>

<style scoped>
#health_check_table {
  font-size: 1rem;
  border: none;
  text-align: center;
  vertical-align: middle;
}
</style>
