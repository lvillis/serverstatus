declare global {
    interface BoxItem {
        "name": string;
        "host": string;
        "type": string;
        "online4": boolean;
        "online6": boolean;
        "location": string;
    }

    interface StatusItem extends BoxItem {
        "uptime": string;
        "load_1": number;
        "load_5": number;
        "load_15": number;
        "cpu": number;
        "network_rx": number;
        "network_tx": number;
        "network_in": number;
        "network_out": number;
        "memory_total": number;
        "memory_used": number;
        "swap_total": number;
        "swap_used": number;
        "hdd_total": number;
        "hdd_used": number;
        "custom": string;
        "tcp_count": number;
        "udp_count": number
        "process_count": number
        "thread_count": number
        "ssh_sessions": number;
        "kernel": string;
        "tcp_cc":string;
        "cpu_model": string;
        "cpu_cores": number;
        "cpu_speed": number;
    }
}
export {}