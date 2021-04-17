declare global {
    interface ChecksBoxItem {
        "name": string;
        "token": string;
        "period": string;
        "grace": string;
    }

    interface ChecksStatusItem extends ChecksBoxItem {
        "status": string;
        "next_time": string;
        "last_ping": string;
    }
}
export {}