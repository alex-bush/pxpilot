import LabeledTextField from "./controls/LabeledTextField.jsx";
import {Card, Modal, Select} from "antd";
import CheckboxField from "./controls/CheckboxField.jsx";
import {useEffect, useState} from "react";

export default function VmStartupOptionsModal({isModalOpen, item, onOk, onCancel}) {
    const defaultCheck = 'none';

    const [healthcheckEnabled, setHealthcheckEnabled] = useState(false);
    const [data, setData] = useState({healthcheck: {check_method: defaultCheck}});
    const [key, setKey] = useState(null);
    const [isOkDisabled, setIsOkDisabled] = useState(false);

    useEffect(() => {
        if (!isModalOpen) {
            // Reset state when the modal is closed
            setHealthcheckEnabled(false);
            setKey(null);
            setData({healthcheck: {check_method: defaultCheck}});
        } else if (item) {
            if (item.vm_id){
                setKey(item.vm_id);
            }
            setHealthcheckEnabled(!!item.healthcheck);
            setData(item);
        }
    }, [isModalOpen, item]);

    useEffect(() => {
        let isValid = data.vm_id && (
            !healthcheckEnabled
            || healthcheckEnabled
                && data.healthcheck.check_method
                && data.healthcheck.check_method !== 'none'
                && data.healthcheck.target_url
        );
        setIsOkDisabled(!isValid);
    }, [data, healthcheckEnabled]);

    const handleOk = () => {
        if (!data.healthcheck || data.healthcheck.check_method === defaultCheck) {
            onOk(key, {...data, healthcheck: null});
        } else {
            onOk(key, data);
        }

        setData({healthcheck: {check_method: defaultCheck}});
    };

    const handleCancel = () => {
        onCancel();
        setData({healthcheck: {check_method: defaultCheck}});
    };

    function handleHealthCheckChange(value) {
        if (value === 'none') {
            setHealthcheckEnabled(false);
            setData({
                ...data, healthcheck: {check_method: defaultCheck}
            })
        } else {
            setHealthcheckEnabled(true);
            setData({
                ...data, healthcheck: {...data.healthcheck, check_method: value}
            })
        }
    }

    return (<>
        <Modal
            title="Add VM to startup list"
            centered
            open={isModalOpen}
            onOk={handleOk}
            onCancel={handleCancel}
            okButtonProps={{disabled: isOkDisabled}}>
            <Card>
                <LabeledTextField
                    title='VM Id'
                    type='number'
                    value={data.vm_id}
                    onChange={(value) => setData({...data, vm_id: value})}/>
                <LabeledTextField
                    className='mt-3'
                    title='VM Name'
                    value={data.name}
                    onChange={(value) => setData({...data, name: value})}/>
                <LabeledTextField
                    className='mt-3'
                    title='Description'
                    value={data.description}
                    onChange={(value) => setData({...data, description: value})}/>
                <CheckboxField
                    className='mt-3'
                    title='Wait for the virtual machine to finish starting'
                    value={data.await_running}
                    onChange={(e) => setData({...data, await_running: e.target.checked})}/>
                <LabeledTextField
                    className='mt-3'
                    title='Timeout'
                    type='number'
                    value={data.startup_timeout} disabled={!data.await_running}
                    onChange={(value) => setData({...data, startup_timeout: value})}/>

                <div title='Healthcheck'>

                    <div className='flex gap-4 w-full mt-3'>
                        <label className='flex-col content-center'>Healthcheck:</label>
                        <Select
                            defaultValue={defaultCheck}
                            className='w-full'
                            options={[{value: 'none', label: 'None'}, {value: 'ping', label: 'PING'}, {
                                value: 'http',
                                label: 'HTTP request'
                            },]}
                            onChange={handleHealthCheckChange}
                        />
                    </div>

                    <div className='mt-3'>
                        <LabeledTextField

                            title='Healthcheck url'
                            value={data.healthcheck?.target_url}
                            disabled={!healthcheckEnabled}
                            onChange={(value) => setData({
                                ...data, healthcheck: {...data.healthcheck, target_url: value}
                            })}
                        />
                    </div>


                </div>
            </Card>
        </Modal>
    </>)
}