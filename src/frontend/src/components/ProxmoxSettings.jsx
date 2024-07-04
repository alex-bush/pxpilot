import {useEffect, useState} from "react";
import {Button, Card, Flex, message, notification, Spin} from "antd";
import LabeledTextField from "./controls/LabeledTextField.jsx";
import {fetchProxmoxSettings, saveProxmoxSettings, testConnection} from "../services/services.jsx";
import KeyValueSettingList from "./controls/KeyValueSettingList.jsx";

export default function ProxmoxSettings() {
    const TITLE = "Proxmox connection settings";

    const [Data, setData] = useState({isLoaded: false, extra_settings: []})
    const [OriginalData, setOriginalData] = useState({})

    const [loading, setLoading] = useState(false);
    const [validatingConnection, setValidatingConnection] = useState(false);
    const [notificationInstance, notificationHolder] = notification.useNotification();
    const [apiMessage, contextMessageHolder] = message.useMessage();

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

    const showMessage = (type, message) => {
        apiMessage.open({
            type: type,
            content: message,
        });
    };

    useEffect(() => {
        loadData();
    }, [])

    function loadData() {
        fetchProxmoxSettings().then(data => {
            data.isLoaded = true;

            setData(data);
            setOriginalData(data);
        });
    }

    const isDataUnchanged = () => {
        return Data.host === OriginalData.host
            && Data.token_name === OriginalData.token_name
            && Data.token_value === OriginalData.token_value;
    }

    function handleFieldChange(field, value) {
        const newData = {...Data, [field]: value};
        setData(newData);
    }

    function handleSaveClick() {
        setLoading(true);

        saveProxmoxSettings(Data, true).then(() => {
            loadData();
            setLoading(false);
            showNotification('success', TITLE);
        }).catch(err => {
            console.log(err);
            setLoading(false);
            showNotification('error', TITLE);
        });
    }

    function handleTestClick() {
        setValidatingConnection(true)
        testConnection(Data.host, Data.token_name, Data.token_value).then(res => {
            if (res.is_valid) {
                showMessage('success', `Connection successful`);
            } else {
                showMessage('error', `Test connection failed: ${res.message}`);
            }
            setValidatingConnection(false);
        });
    }

    return (
        <>
            {notificationHolder}
            {contextMessageHolder}
            <Card
                title='Proxmox connection settings'
                style={{
                    width: "-moz-fit-content",
                }}>
                {
                    Data.isLoaded
                        ? (
                            <div className="settings">
                                <div className="mainBlock">
                                    <LabeledTextField title='Host' value={Data.host}
                                                      onChange={value => handleFieldChange('host', value)}/>
                                    <LabeledTextField title='Token name' value={Data.token_name}
                                                      onChange={value => handleFieldChange('token_name', value)}/>
                                    <LabeledTextField title='Token value' value={Data.token_value} is_password={"true"}
                                                      onChange={value => handleFieldChange('token_value', value)}/>
                                </div>

                                <KeyValueSettingList title='Other settings' settings={Data.extra_settings}/>

                                <div className="toolbar">
                                    <Flex justify="space-between">
                                        <Button type="primary"
                                                disabled={!(Data.host && Data.token_name && Data.token_value)}
                                                loading={validatingConnection}
                                                onClick={handleTestClick}>Test connection
                                        </Button>

                                        <Button type="primary" loading={loading} disabled={isDataUnchanged()}
                                                onClick={handleSaveClick}>Save settings</Button>
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