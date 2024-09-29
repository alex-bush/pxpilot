import CheckboxField from "../controls/CheckboxField.jsx";
import LabeledTextField from "../controls/LabeledTextField.jsx";
import {Button, Card, Flex} from "antd";
import {useEffect, useState} from "react";
import useLoadData from "../../hooks/useLoadData.js";
import Spinner from "../controls/Spinner.jsx";
import {STARTUP_SETTINGS_URL} from "../../config.js";

export default function StartupSettings() {
    const [localData, setLocalData] = useState(null)
    const {
        data,
        isLoading,
        setIsLoading,
        isSaving,
        saveData,
        notificationHolder} = useLoadData(STARTUP_SETTINGS_URL, null, '')

    useEffect(() => {
        if (data) {
            setLocalData(data);
            setIsLoading(false);
        }
    }, [data, setIsLoading]);

    const isDataUnchanged = () => {
        return JSON.stringify(data) === JSON.stringify(localData);
    }

    async function handleSaveClick() {
        await saveData(localData);
    }

    return (<>
        {notificationHolder}
        <Card title='Startup Settings'>
            {!isLoading ? (
                <div >
                    <div className="space-y-4">
                        <CheckboxField
                            title='Enable starting'
                            value={localData.enable}
                            onChange={(e) => setLocalData({...localData, enable: e.target.checked})}>
                        </CheckboxField>
                        <LabeledTextField
                            title='Timeout threshold'
                            placeholder='0'
                            className='w-1/4'
                            value={localData.uptime_threshold}
                            onChange={(e) => setLocalData({...localData, uptime_threshold: e})}>
                        </LabeledTextField>
                    </div>
                    <div className="toolbar p-2 pt-6">
                        <Flex justify="flex-end">
                            <Button type="primary" loading={isSaving} disabled={isDataUnchanged()}
                                    onClick={handleSaveClick}>Save settings</Button>
                        </Flex>
                    </div>
                </div>

            ) : <Spinner/>}
        </Card>
    </>)
}