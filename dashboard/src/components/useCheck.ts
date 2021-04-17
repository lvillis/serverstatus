import {computed} from 'vue';

interface Props {
    check: ChecksStatusItem | ChecksBoxItem;
}

export default (props: Props) => {
    const getProcessBarStatus = computed(
        () => (data: number) => {
            if (data > 90)
                return 'error';
            else if (data > 70)
                return 'warning';
            else
                return 'success';
        });
    const tableRowByteConvert = computed(
        () => (data: number): string => {
            if (data < 1024)
                return data.toFixed(0) + 'B';
            else if (data < 1024 * 1024)
                return (data / 1024).toFixed(0) + 'K';
            else if (data < 1024 * 1024 * 1024)
                return (data / 1024 / 1024).toFixed(1) + 'M';
            else if (data < 1024 * 1024 * 1024 * 1024)
                return (data / 1024 / 1024 / 1024).toFixed(2) + 'G';
            else
                return (data / 1024 / 1024 / 1024 / 1024).toFixed(2) + 'T';
        });
    const expandRowByteConvert = computed(
        () => (data: number): string => {
            if (data < 1024)
                return data.toFixed(0) + ' B';
            else if (data < 1024 * 1024)
                return (data / 1024).toFixed(2) + ' KiB';
            else if (data < 1024 * 1024 * 1024)
                return (data / 1024 / 1024).toFixed(2) + ' MiB';
            else if (data < 1024 * 1024 * 1024 * 1024)
                return (data / 1024 / 1024 / 1024).toFixed(2) + ' GiB';
            else
                return (data / 1024 / 1024 / 1024 / 1024).toFixed(2) + ' TiB';
        });
    const getLoad = computed(
        () => (load: number, cores: number) => {
            const value = load / cores;
            if (value < 1)
                return "";
            else if (value >= 1 && value < 2)
                return "warning";
            else if (value >= 2)
                return "error";
        });
    return {
        getProcessBarStatus,
        tableRowByteConvert,
        expandRowByteConvert,
        getLoad
    };
};