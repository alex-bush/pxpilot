import {notification} from "antd";
import {useCallback} from "react";

function useNotifier() {
    const [notificationInstance, notificationHolder] = notification.useNotification();

    const showNotification = useCallback ((type, title) => {
        if (type === "error") {
            notificationInstance[type]({
                message: 'Error',
                description: 'Error while saving ' + title,
            })
            return;
        }

        notificationInstance[type]({
            message: 'Done!',
            description: title + ' saved successfully',
        })
    }, [notificationInstance]);

    return {showNotification, notificationHolder};
}

export default useNotifier;