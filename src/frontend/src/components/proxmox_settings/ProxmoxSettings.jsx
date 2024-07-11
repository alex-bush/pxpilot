import {useCallback, useEffect, useState} from "react";
import {Button, Card, Flex, message, notification} from "antd";
import LabeledTextField from "../controls/LabeledTextField.jsx";
import {fetchProxmoxSettings, reloadConfig, saveProxmoxSettings, testConnection} from "../../services/services.jsx";
import KeyValueSettingList from "../controls/KeyValueSettingList.jsx";
import Spinner from "../controls/Spinner.jsx";

export default function ProxmoxSettings() {
    const TITLE = "Proxmox connection settings";

    const [Data, setData] = useState({isLoaded: false, extra_settings: {}})
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

    const loadData = useCallback(async () => {
        let data = await fetchProxmoxSettings();
        if (data === null) {
            data = {isLoaded: true, extra_settings: { verify_ssl: false }};
        }
        setOriginalData(data);

        data.isLoaded = true;
        setData(data);
    }, [])

    useEffect(() => {
        loadData()
    }, [loadData])

    const isDataUnchanged = () => {
        return JSON.stringify(Data) === JSON.stringify(OriginalData);
    }

    function handleFieldChange(field, value) {
        const newData = {...Data, [field]: value};
        setData(newData);
    }

    function convertValue(value) {
        if (value.toLowerCase() === 'true') {
            return true;
        } else if (value.toLowerCase() === 'false') {
            return false;
        }
        return value;
    }

    function handleExtraSettingsChanged(index, newKey, newValue) {
        const new_extra = Object.entries(Data.extra_settings).map((item, idx) => {
            if (idx === index) {
                return [newKey, convertValue(newValue)];
            }
            return item;
        })

        setData({...Data, ['extra_settings']: Object.fromEntries(new_extra)});
    }

    function handleAddExtraSettingClick() {
        setData({...Data, extra_settings: {...Data.extra_settings, ['']: ''}});
    }

    function handleDeleteExtraSettingClick(index) {
        const new_extra = Object.entries(Data.extra_settings).filter((item, idx) => idx !== index);

        setData({...Data, extra_settings: Object.fromEntries(new_extra)});
    }

    async function handleSaveClick() {
        setLoading(true);

        try {
            await saveProxmoxSettings(Data, true);
            await reloadConfig();
            await loadData();
            showNotification('success', TITLE);
        } catch (err) {
            console.log(err);
            showNotification('error', TITLE);
        } finally {
            setLoading(false);
        }
    }


    async function handleTestClick() {
        setValidatingConnection(true)
        try {
            const res = await testConnection(Data.host, Data.token_name, Data.token_value, Data.extra_settings);
            if (res.is_valid) {
                showMessage('success', `Connection successful`);
            } else {
                showMessage('error', `Test connection failed: ${res.message}`);
            }
        } finally {
            setValidatingConnection(false);
        }
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
                                    <LabeledTextField title='Host' value={Data.host} placeholder='http://127.0.0.1:8006'
                                                      onChange={value => handleFieldChange('host', value)}/>
                                    <LabeledTextField title='Token name' value={Data.token_name}
                                                      placeholder='user@pve!tokenname'
                                                      onChange={value => handleFieldChange('token_name', value)}/>
                                    <LabeledTextField title='Token value' value={Data.token_value} is_password={"true"}
                                                      placeholder='token'
                                                      onChange={value => handleFieldChange('token_value', value)}/>
                                </div>

                                <KeyValueSettingList title='Other settings' settings={Data.extra_settings}
                                                     onDataChange={handleExtraSettingsChanged}
                                                     onAddClick={handleAddExtraSettingClick}
                                                     onDeleteClick={handleDeleteExtraSettingClick}
                                />

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
                        <Spinner/>
                }
            </Card>
        </>
    )
}