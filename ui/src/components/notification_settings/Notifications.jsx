import {Button, Card, Collapse, Flex, notification} from "antd";
import {useCallback, useEffect, useState} from "react";
import Telegram from "./Telegram.jsx";
import Email from "./Email.jsx";
import Spinner from "../controls/Spinner.jsx";
import useAuthFetch from "../../hooks/useAuthFetch.js";
import {NOTIFICATIONS_SETTINGS_URL} from "../../config.js";

export const Notifications = () => {
    const TITLE = "Notification settings";

    const {authGet, authPost} = useAuthFetch();
    const [Data, setData] = useState({isLoaded: false});
    const [OriginalData, setOriginalData] = useState({})

    const [saving, setSaving] = useState(false);
    const [notificationInstance, notificationHolder] = notification.useNotification();

    const showNotification = (type, title) => {
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
    }

    const loadData = useCallback(async () => {
        let data = await authGet(NOTIFICATIONS_SETTINGS_URL);
        if (data === null){
            data = {isLoaded: true, telegram: {}, email: {}};
        }
        setOriginalData(data);

        data.isLoaded = true;
        setData(data);
    }, [authGet])

    useEffect(() => {
        loadData();
    }, [authGet, loadData])

    const handleDataChange = (key, newData) => {
        setData({...Data, [key]: newData});
    }

    async function handleSaveClick() {
        setSaving(true);

        try {
            await authPost(NOTIFICATIONS_SETTINGS_URL, Data);
            await loadData();
            showNotification('success', TITLE);
        }
        catch(err) {
            console.log(err);
            showNotification('error', TITLE);
        }
        finally {
            setSaving(false);
        }
    }

    const isDataUnchanged = () => {
        if (Data && OriginalData) {
            return Data.telegram?.token === OriginalData.telegram?.token
                && Data.telegram?.chat_id === OriginalData.telegram?.chat_id
                && Data.telegram?.enabled === OriginalData.telegram?.enabled
                && Data.email?.enabled === OriginalData.email?.enabled
                && Data.email?.smtp_server === OriginalData.email?.smtp_server
                && Data.email?.smtp_port === OriginalData.email?.smtp_port
                && Data.email?.smtp_user === OriginalData.email?.smtp_user
                && Data.email?.smtp_password === OriginalData.email?.smtp_password
                && Data.email?.from_email === OriginalData.email?.from_email
                && Data.email?.to_email === OriginalData.email?.to_email;
        }
        return false;
    }

    return (
        <>
            {notificationHolder}
            <Card
                title="Notification settings"
                style={{
                    //width: "-moz-fit-content",
                }}>
                {Data.isLoaded ?
                    (
                        <div>
                            <Collapse items={[
                                {
                                    key: 'tg',
                                    label: 'Telegram',
                                    children: <Telegram data={Data.telegram}
                                                        onChange={data => handleDataChange('telegram', data)}/>
                                },
                                {
                                    key: 'email',
                                    label: 'Email',
                                    children: <Email data={Data.email}
                                                     onChange={data => handleDataChange('email', data)}/>
                                }
                            ]}/>
                            <div className="toolbar pt-7">
                                <Flex justify="flex-end">
                                    <Button
                                        type="primary"
                                        loading={saving}
                                        disabled={isDataUnchanged()}
                                        onClick={handleSaveClick}>
                                        Save settings
                                    </Button>
                                </Flex>
                            </div>
                        </div>

                    )
                    :
                    <Spinner/>
                }

            </Card>
        </>
    )
}