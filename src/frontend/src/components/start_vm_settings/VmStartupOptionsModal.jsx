import LabeledTextField from "../controls/LabeledTextField.jsx";
import {Card, Divider, Modal, Select} from "antd";
import CheckboxField from "../controls/CheckboxField.jsx";
import {useEffect, useMemo, useState} from "react";
import {fetchAllVirtualMachines} from "../../services/services.jsx";

export default function VmStartupOptionsModal({isModalOpen, item, usedKeys, onOk, onCancel}) {
    const defaultCheck = 'none';
    const healthCheckTypes = [
        {value: 'none', label: 'None'},
        {value: 'ping', label: 'PING'},
        {value: 'http', label: 'HTTP request'}
        ,];

    const emptyItem = useMemo(() => ({
            startup_parameters: {await_running: true, startup_timeout: 120},
            healthcheck: {check_method: defaultCheck}
        }), [])
    ;

    const [healthcheckEnabled, setHealthcheckEnabled] = useState(false);
    const [data, setData] = useState(emptyItem);
    const [key, setKey] = useState(null);
    const [isOkDisabled, setIsOkDisabled] = useState(false);
    const [availableVms, setAvailableVms] = useState([]);
    const [selectVm, setSelectVm] = useState(null);

    useEffect(() => {
        if (!isModalOpen) {
            // Reset state when the modal is closed
            setHealthcheckEnabled(false);
            setKey(null);
            setData(emptyItem);
            setSelectVm(null);
        } else {
            if (item) {
                if (item.vm_id) {
                    setKey(item.vm_id);
                    setSelectVm(item.vm_id);
                }
                setHealthcheckEnabled(!!item.healthcheck);
                setData(item);
            }
            fetchAllVirtualMachines().then(vms => {
                let d = vms.map(vm => {
                    return {
                        value: vm.id,
                        label: vm.id + ': ' + vm.name,
                        disabled: usedKeys && usedKeys.findIndex(i => i === vm.id) > -1,
                        name: vm.name,
                    }
                })
                setAvailableVms(d);
            })
        }
    }, [isModalOpen, item, emptyItem, usedKeys]);

    useEffect(() => {
        let isValid = data.vm_id && (
            !healthcheckEnabled
            || healthcheckEnabled
            && data.healthcheck.check_method
            && data.healthcheck.check_method !== defaultCheck
            && data.healthcheck.target_url
        );
        setIsOkDisabled(!isValid);
    }, [data, healthcheckEnabled, usedKeys]);

    const handleOkClick = () => {
        if (!data.healthcheck || data.healthcheck.check_method === defaultCheck) {
            onOk(key, {...data, healthcheck: null});
        } else {
            onOk(key, data);
        }

        setData(emptyItem);
    };

    const handleCancelClick = () => {
        onCancel();
        setData(emptyItem);
    };

    function handleHealthcheckSelectChange(value) {
        if (value === defaultCheck) {
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

    function handleVmSelectChange(value) {
        setSelectVm(value);
        let name = availableVms.find(i => i.value === value)?.name;
        setData({...data, vm_id: value, name: name});
    }

    return (<>
        <Modal
            title="Add VM to startup list"
            centered
            open={isModalOpen}
            onOk={handleOkClick}
            onCancel={handleCancelClick}
            okButtonProps={{disabled: isOkDisabled}}>
            <Card>
                <div className='flex gap-4 w-full items-end'>
                    <LabeledTextField
                        title='VM Id'
                        type='number'
                        value={data.vm_id}
                        onChange={(value) => setData({...data, vm_id: value})}/>
                    <Select
                        value={selectVm}
                        className='w-2/5'
                        size='large'
                        placeholder="Select a VM"
                        options={availableVms}
                        allowClear
                        onChange={handleVmSelectChange}
                    />
                </div>
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
                <Divider/>
                <CheckboxField
                    className='mt-3'
                    title='Wait for the virtual machine to finish starting'
                    value={data.startup_parameters?.await_running}
                    onChange={(e) => setData({
                        ...data,
                        startup_parameters: {...data.startup_parameters, await_running: e.target.checked}
                    })}/>
                <LabeledTextField
                    className='mt-3'
                    title='Timeout'
                    type='number'
                    value={data.startup_parameters.startup_timeout} disabled={!data.startup_parameters?.await_running}
                    onChange={(value) => setData({
                        ...data,
                        startup_parameters: {...data.startup_parameters, startup_timeout: value}
                    })}/>

                <Divider/>
                <div className='health-check'>

                    <div className='flex gap-4 w-full mt-3'>
                        <label className='flex-col content-center'>Healthcheck:</label>
                        <Select
                            defaultValue={defaultCheck}
                            value={data.healthcheck?.check_method}
                            className='w-full'
                            options={healthCheckTypes}
                            allowClear
                            onChange={handleHealthcheckSelectChange}
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

                {data?.dependencies?.length > 0 && (
                    <div>
                        <Divider/>
                        <span>Depends on: </span>
                        {data.dependencies?.map(d => (
                            <span key={d}>{d}</span>
                        ))}
                    </div>)}
            </Card>
        </Modal>
    </>)
}