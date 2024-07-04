import {Button, Card, Collapse, Flex, notification, Spin} from "antd";
import {useEffect, useState} from "react";
import Telegram from "./Telegram.jsx";
import Email from "./Email.jsx";
import {fetchNotificationSettings, saveNotificationSettings} from "../services/services.jsx";

export const Notifications = () => {
    const TITLE = "Notification settings";

    const [Data, setData] = useState({isLoaded: false, dataChanged: false});
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

    useEffect(() => {
        loadData();
    }, [])

    function loadData() {
        fetchNotificationSettings().then(data => {
            setOriginalData(data);
            data.isLoaded = true;
            data.dataChanged = false;
            setData(data);
        });
    }

    const handleDataChange = (key, newData) => {
        setData({...Data, [key]: newData, dataChanged: true});
    }

    function handleSaveClick() {
        setSaving(true);

        saveNotificationSettings(Data, true).then(() => {
            loadData();
            setSaving(false);
            showNotification('success', TITLE);
        }).catch(err => {
            console.log(err);
            setSaving(false);
            showNotification('error', TITLE);
        });
    }

    const isDataUnchanged = () => {
        return Data.telegram.token === OriginalData.telegram.token
            && Data.telegram.chat_id === OriginalData.telegram.chat_id
            && Data.telegram.enabled === OriginalData.telegram.enabled
            && Data.email.enabled === OriginalData.email.enabled
            && Data.email.smtp_server === OriginalData.email.smtp_server
            && Data.email.smtp_port === OriginalData.email.smtp_port
            && Data.email.smtp_user === OriginalData.email.smtp_user
            && Data.email.smtp_password === OriginalData.email.smtp_password
            && Data.email.from_email === OriginalData.email.from_email
            && Data.email.to_email === OriginalData.email.to_email;
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
                            <div className="toolbar">
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
                    <Spin size={"large"}/>
                }

            </Card>
        </>
    )
}