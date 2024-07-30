import {useEffect, useState} from "react";
import {Button, Card, Flex, message} from "antd";
import LabeledTextField from "../controls/LabeledTextField.jsx";
import KeyValueSettingList from "../controls/KeyValueSettingList.jsx";
import Spinner from "../controls/Spinner.jsx";
import useAuthFetch from "../../hooks/useAuthFetch.js";
import {PX_SETTINGS_URL, PX_VALIDATE_CONNECTION_URL} from "../../config.js";
import useLoadData from "../../hooks/useLoadData.js";

const placeholders = {
    host: 'http://127.0.0.1:8006',
    username: 'user@pve!tokenname',
    token:  'token'
}

export default function ProxmoxSettings() {
    const TITLE = "Proxmox connection settings";

    const [localData, setLocalData] = useState({})
    const [validatingConnection, setValidatingConnection] = useState(false);

    const [apiMessage, contextMessageHolder] = message.useMessage();

    const {authPost} = useAuthFetch();
    const {
        data, isLoading, setIsLoading, isSaving, saveData, notificationHolder
    } = useLoadData(PX_SETTINGS_URL, {extra_settings: {}}, TITLE, (data) => {
        if (data === null) {
            data = {extra_settings: {verify_ssl: false}};
        }
        return data;
    });

    useEffect(() => {
        if (data) {
            setLocalData({...data});
            setIsLoading(false);
        }
    }, [data, setIsLoading]);

    const showMessage = (type, message) => {
        apiMessage.open({
            type: type, content: message,
        });
    };

    const isDataUnchanged = () => {
        return JSON.stringify(data) === JSON.stringify(localData);
    }

    function handleFieldChange(field, value) {
        setLocalData({...localData, [field]: value});
    }

    function convertValue(value) {
        const lValue = value.toLowerCase();
        if (lValue === 'true') {
            return true;
        } else if (lValue === 'false') {
            return false;
        }
        return value;
    }

    function handleExtraSettingsChanged(index, newKey, newValue) {
        const new_extra = Object.entries(localData.extra_settings).map((item, idx) => {
            if (idx === index) {
                return [newKey, convertValue(newValue)];
            }
            return item;
        })

        setLocalData({...localData, ['extra_settings']: Object.fromEntries(new_extra)});
    }

    function handleAddExtraSettingClick() {
        setLocalData({...localData, extra_settings: {...localData.extra_settings, ['']: ''}});
    }

    function handleDeleteExtraSettingClick(index) {
        const new_extra = Object.entries(localData.extra_settings).filter((item, idx) => idx !== index);

        setLocalData({...localData, extra_settings: Object.fromEntries(new_extra)});
    }

    async function handleSaveClick() {
        await saveData(localData);
    }

    async function handleTestClick() {
        setValidatingConnection(true)
        try {
            const res = await authPost(PX_VALIDATE_CONNECTION_URL, {
                host: localData.host,
                token_name: localData.token_name,
                token_value: localData.token_value,
                extra_settings: localData.extra_settings,
            });
            if (res.is_valid) {
                showMessage('success', `Connection successful`);
            } else {
                showMessage('error', `Test connection failed: ${res.message}`);
            }
        } finally {
            setValidatingConnection(false);
        }
    }

    return (<>
        {notificationHolder}
        {contextMessageHolder}
        <Card
            title='Proxmox connection settings'
            style={{
                width: "-moz-fit-content",
            }}>
            {!isLoading ? (<div className="settings">
                <div className="mainBlock">
                    <LabeledTextField title='Host' value={localData.host} placeholder={placeholders.host}
                                      className="p-2"
                                      onChange={value => handleFieldChange('host', value)}/>
                    <LabeledTextField title='Token name' value={localData.token_name} className="p-2"
                                      placeholder={placeholders.username}
                                      onChange={value => handleFieldChange('token_name', value)}/>
                    <LabeledTextField title='Token value' value={localData.token_value} is_password={"true"}
                                      className="p-2"
                                      placeholder={placeholders.token}
                                      onChange={value => handleFieldChange('token_value', value)}/>
                </div>

                <div className="p-2 pt-6">
                    <KeyValueSettingList title='Other settings' settings={localData.extra_settings}
                                         onDataChange={handleExtraSettingsChanged}
                                         onAddClick={handleAddExtraSettingClick}
                                         onDeleteClick={handleDeleteExtraSettingClick}
                    />
                </div>
                <div className="toolbar p-2 pt-6">
                    <Flex justify="space-between">
                        <Button type="primary"
                                disabled={!(localData.host && localData.token_name && localData.token_value)}
                                loading={validatingConnection}
                                onClick={handleTestClick}>Test connection
                        </Button>

                        <Button type="primary" loading={isSaving} disabled={isDataUnchanged()}
                                onClick={handleSaveClick}>Save settings</Button>
                    </Flex>
                </div>
            </div>) : <Spinner/>}
        </Card>
    </>)
}