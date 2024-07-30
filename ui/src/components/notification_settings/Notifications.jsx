import {Button, Card, Collapse, Flex} from "antd";
import {useEffect, useState} from "react";
import Telegram from "./Telegram.jsx";
import Email from "./Email.jsx";
import Spinner from "../controls/Spinner.jsx";
import {NOTIFICATIONS_SETTINGS_URL} from "../../config.js";
import useLoadData from "../../hooks/useLoadData.js";

export const Notifications = () => {
    const TITLE = "Notification settings";

    const [localData, setLocalData] = useState(null)

    const {
        data, isLoading, setIsLoading, isSaving, saveData, notificationHolder
    } = useLoadData(NOTIFICATIONS_SETTINGS_URL, null, TITLE, (dt) => {
        if (dt === null) {
            dt = {telegram: {}, email: {}};
        }
        return dt;
    });

    useEffect(() => {
        if (data) {
            setLocalData(data);
            setIsLoading(false);
        }
    }, [data, setIsLoading]);

    const handleDataChange = (key, newData) => {
        setLocalData({...localData, [key]: newData});
    }

    async function handleSaveClick() {
        await saveData(localData);
    }

    const isDataUnchanged = () => {
        return JSON.stringify(data) === JSON.stringify(localData);
    }

    return (
        <>
            {notificationHolder}
            <Card
                title="Notification settings"
                style={{
                    //width: "-moz-fit-content",
                }}>
                {!isLoading ?
                    (
                        <div>
                            <Collapse items={[
                                {
                                    key: 'tg',
                                    label: 'Telegram',
                                    children: <Telegram data={localData.telegram}
                                                        onChange={data => handleDataChange('telegram', data)}/>
                                },
                                {
                                    key: 'email',
                                    label: 'Email',
                                    children: <Email data={localData.email}
                                                     onChange={data => handleDataChange('email', data)}/>
                                }
                            ]}/>
                            <div className="toolbar pt-7">
                                <Flex justify="flex-end">
                                    <Button
                                        type="primary"
                                        loading={isSaving}
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