<template>
  <tr class="tableRow" @click="collapsed = !collapsed">
    <td>
      <div class="ui progress" :class="{'success': getStatus, 'error': !getStatus}">
        <div class="bar" style="width: 100%"><span> {{ getStatus ? `${getIPStatus.toString()}` : 'Down' }} </span>
        </div>
      </div>
    </td>
    <td>{{ server.name }}</td>
    <td>{{ server.type }}</td>
    <td>{{ server.location }}</td>
    <td>{{ server.uptime || '–' }}</td>
    <td :class="getLoad(server.load_1, server.cpu_cores)">{{ getStatus ? server.load_1 : '-' }}</td>
    <td>{{
        getStatus ? `${tableRowByteConvert(server.network_rx)} | ${tableRowByteConvert(server.network_tx)}` : '–'
      }}
    </td>
    <td>{{
        getStatus ? `${tableRowByteConvert(server.network_in)} | ${tableRowByteConvert(server.network_out)}` : '–'
      }}
    </td>
    <td>
      <div class="ui progress" :class="getProcessBarStatus(getCpuStatus)">
        <div class="bar" :style="{'width': `${getCpuStatus.toString()}%`}">
          {{ getStatus ? `${getCpuStatus.toString()}%` : 'Down' }}
        </div>
      </div>
    </td>
    <td>
      <div class="ui progress" :class="getProcessBarStatus(getRAMStatus)">
        <div class="bar" :style="{'width': `${getRAMStatus.toString()}%`}">
          {{ getStatus ? `${getRAMStatus.toString()}%` : 'Down' }}
        </div>
      </div>
    </td>
    <td>
      <div class="ui progress" :class="getProcessBarStatus(getHDDStatus)">
        <div class="bar" :style="{'width': `${getHDDStatus.toString()}%`}">
          {{ getStatus ? `${getHDDStatus.toString()}%` : 'Down' }}
        </div>
      </div>
    </td>
  </tr>
  <tr class="expandRow">
    <td colspan="12">
      <div :class="{collapsed}" v-if=getStatus>
        <div id="expand_cpu_model">CPU Model : {{ server.cpu_model }}</div>
        <div id="expand_cpu_cores">CPU Cores : {{ server.cpu_cores }} Cores {{ server.cpu_speed }} MHz</div>
        <div id="expand_cpu_kernel">Kernel : {{ server.kernel }}</div>
        <div id="expand_tcp_cc">TCP CC : {{ server.tcp_cc }}</div>
        <div id="expand_mem">Total RAM : {{ expandRowByteConvert(server.memory_used * 1024) }} / {{ expandRowByteConvert(server.memory_total * 1024) }}</div>
        <div id="expand_swap">Total SWAP : {{ expandRowByteConvert(server.swap_used * 1024) }} / {{ expandRowByteConvert(server.swap_total * 1024) }}</div>
        <div id="expand_hdd">Total Space : {{ expandRowByteConvert(server.hdd_used * 1024 * 1024) }} / {{ expandRowByteConvert(server.hdd_total * 1024 * 1024) }}</div>
        <div id="expand_tupd">TCP/UDP/进/线 : {{ server.tcp_count }} / {{ server.udp_count }} / {{ server.process_count }} / {{ server.thread_count }}</div>
        <div id="expand_ssh_sessions">SSH Sessions: {{ server.ssh_sessions }}</div>
        <!--        <div id="expand_custom">{{server.custom}}</div>-->
      </div>
      <div v-else>
      </div>
    </td>
  </tr>
</template>

<script lang="ts">
import {defineComponent, ref, PropType} from 'vue';
import useStatus from './useStatus';

export default defineComponent({
  name: 'ServersTableItem',
  props: {
    server: {
      type: Object as PropType<StatusItem | BoxItem>,
      default: {}
    }
  },
  setup(props) {
    const collapsed = ref(true);
    const utils = useStatus(props);
    return {
      collapsed,
      ...utils
    };
  }
});
</script>

<style scoped>


tr.tableRow {
  background-color: rgba(249, 249, 249, .8);
  vertical-align: middle;
}


tr.expandRow td > div {
  overflow: hidden;
  transition: height .5s ease;
  height: auto;
}

tr.expandRow td > div.collapsed {
  max-height: 0;
}

tr.expandRow > td {
  padding: 0 !important;
  border-top: 0 !important;
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
