<template>
  <div class="ui container">
    <table class="ui basic unstackable selectable striped very compact table" id="table">
      <thead>
      <tr>
        <th id="status4">IP</th>
        <th id="name">Name</th>
        <th id="type">Type</th>
        <th id="location">Location</th>
        <th id="uptime">Uptime</th>
        <th id="load_1">Load</th>
        <th id="network">Network(B/s) ↓|↑</th>
        <th id="traffic">Bandwidth(B) ↓|↑</th>
        <th id="cpu">CPU</th>
        <th id="ram">RAM</th>
        <th id="hdd">DISK</th>
      </tr>
      </thead>
      <tbody id="servers">
      <!-- Servers here \o/ -->
      <!--
      use index for the key may cause performance issues when delete a server from array,
      but not a big matter and we cannot find a more suitable data for the unique key.
      -->
      <table-item v-for="(server, index) of servers" :key="index" :server="server"/>
      </tbody>
    </table>
  </div>
</template>
<script lang="ts">
import {defineComponent, PropType} from 'vue';
import TableItem from '@/components/ServersTableItem.vue';

export default defineComponent({
  name: 'ServersTable',
  props: {
    servers: {
      type: Array as PropType<Array<StatusItem | BoxItem>>,
      default: []
    }
  },
  components: {
    TableItem
  }
});
</script>
<style scoped>
#table {
  font-size: 1rem;
  border: none;
  text-align: center;
  vertical-align: middle;
/*
  margin-bottom: 0;
  border-collapse: collapse;
  border-radius: 3px;*/
}

#table thead tr th {
  /*color: #9da2a6;*/
}
</style>
