import LabeledTextField from "../controls/LabeledTextField.jsx";
import {Card, Divider, Modal, Select} from "antd";
import CheckboxField from "../controls/CheckboxField.jsx";
import {useEffect, useMemo, useState} from "react";
import {fetchAllVirtualMachines} from "../../services/services.jsx";
import DependenciesSelector from "./DependenciesSelector.jsx";
import InfoMark from "../controls/InfoMark.jsx";

export default function VmStartupOptionsModal({isModalOpen, inputData, usedKeys, onOk, onCancel}) {
    const defaultCheck = 'none';
    const healthCheckTypes = [
        {value: 'none', label: 'None'},
        {value: 'ping', label: 'PING'},
        {value: 'http', label: 'HTTP request'}
        ,];

    const emptyItem = useMemo(() => ({
            startup_parameters: {await_running: true, startup_timeout: 120, enable_dependencies: false},
            healthcheck: {check_method: defaultCheck},
            dependencies: [],
        }), [])
    ;

    const [healthcheckEnabled, setHealthcheckEnabled] = useState(false);
    const [data, setData] = useState(emptyItem);
    const [key, setKey] = useState(null);
    const [isOkDisabled, setIsOkDisabled] = useState(false);
    const [availableVms, setAvailableVms] = useState([]);
    const [selectVm, setSelectVm] = useState(null);

    const [dataTable, setDataTable] = useState([]);

    useEffect(() => {
        if (!isModalOpen) {
            // Reset state when the modal is closed
            setHealthcheckEnabled(false);
            setKey(null);
            setData(emptyItem);
            setSelectVm(null);
        } else {
            if (inputData) {
                if (inputData.vm_id) {
                    setKey(inputData.vm_id);
                    setSelectVm(inputData.vm_id);
                }
                setHealthcheckEnabled(!!inputData.healthcheck);
                setData(inputData);
            }
            fetchAllVirtualMachines().then(vms => {
                let vmList = vms.map(vm => {
                    return {
                        value: vm.id,
                        label: vm.id + ': ' + vm.name,
                        disabled: usedKeys && usedKeys.findIndex(i => i === vm.id) > -1,
                        name: vm.name,
                    }
                })
                setAvailableVms(vmList);
            })
        }
    }, [isModalOpen, inputData, emptyItem, usedKeys]);

    useEffect(() => {
        let isValid = data.vm_id && (
            !healthcheckEnabled
            || healthcheckEnabled
            && data.healthcheck.check_method
            && data.healthcheck.check_method !== defaultCheck
            && data.healthcheck.target_url
        );
        setIsOkDisabled(!isValid);

    }, [data, healthcheckEnabled]);

    useEffect(() => {
        const table = availableVms
            .sort((a, b) => (a.value < b.value ? -1 : 1))
            .filter(vm => vm.value !== data.vm_id)
            .map(vm => {
                return {
                    key: vm.value,
                    vmid: vm.value,
                    name: vm.name,
                }
            })
        setDataTable(table);
    }, [availableVms, data]);

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

    const handleDependencySelectChange = (newSelectedRowKeys) => {
        setData({...data, dependencies: [...newSelectedRowKeys]});
    };

    return (<>
        <Modal
            title="Add VM to startup list"
            centered
            width={900}
            open={isModalOpen}
            onOk={handleOkClick}
            onCancel={handleCancelClick}
            okButtonProps={{disabled: isOkDisabled}}>
            <div className='flex w-full gap-1'>
                <Card className='w-7/12'>
                    <div className='flex gap-4 w-full items-end'>
                        <LabeledTextField
                            title='* VM Id'
                            type='number'
                            value={data.vm_id}
                            onChange={(value) => setData({...data, vm_id: value})}/>
                        <Select
                            value={selectVm}
                            className='w-2/3'
                            size='large'
                            placeholder="Select existing VM"
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
                        placeholder='Enter VM description (e.g., Backup server)'
                        value={data.description}
                        onChange={(value) => setData({...data, description: value})}/>
                    <Divider/>
                    <div className='flex gap-0 items-end'>
                        <CheckboxField
                            className='mt-3'
                            title='Wait for the virtual machine to finish starting'
                            value={data.startup_parameters?.await_running}
                            onChange={(e) => setData({
                                ...data,
                                startup_parameters: {...data.startup_parameters, await_running: e.target.checked}
                            })}/>
                        <InfoMark placement='top' content={(
                            <>
                                <p>PxPilot will wait for the VM to fully start within this timeout period after
                                    initiating the startup.</p>
                                <p>The startup duration will be included in the notification message.</p>
                                <p>or an error message will be displayed if the VM does not fully start within this
                                    timeout.</p>
                                <p>Proxmox status or the health check option (if enabled) will be used to verify the
                                    VM's startup.</p>
                            </>
                        )}/>
                    </div>
                    <LabeledTextField
                        className='mt-3'
                        title='Timeout'
                        type='number'
                        value={data.startup_parameters.startup_timeout}
                        disabled={!data.startup_parameters?.await_running}
                        onChange={(value) => setData({
                            ...data,
                            startup_parameters: {...data.startup_parameters, startup_timeout: value}
                        })}/>

                    <Divider/>
                    <div className='health-check'>

                        <div className='flex w-full'>
                            <label className='content-center'>Healthcheck:</label>
                            <InfoMark className='content-center pl-1 pr-3' placement='top' content={(
                                <>
                                    <p>Checking the host availability:</p>
                                    <ul>
                                        <li><strong>Ping:</strong> Checks network reachability</li>
                                        <li><strong>HTTP Request:</strong> Verifies that the web service is functional.</li>
                                    </ul>
                                </>
                            )}/>
                            <Select
                                size={"large"}
                                defaultValue={defaultCheck}
                                value={data.healthcheck?.check_method}
                                className='w-full'
                                options={healthCheckTypes}
                                onChange={handleHealthcheckSelectChange}
                            />
                        </div>

                        <div className='pt-4'>
                            <LabeledTextField
                                title='Healthcheck address'
                                value={data.healthcheck?.target_url}
                                disabled={!healthcheckEnabled}
                                placeholder={data.healthcheck?.check_method === 'http' ? 'http://target_url/some_api' : '127.0.0.1'}
                                onChange={(value) => setData({
                                    ...data, healthcheck: {...data.healthcheck, target_url: value}
                                })}
                            />
                        </div>
                    </div>


                </Card>
                <Card className='w-3/6'>
                    <div>
                        <div className='flex gap-0 items-end'>
                            <CheckboxField
                                className='mt-3'
                                title='This VM depends on the following VM(s):'
                                value={data.startup_parameters.enable_dependencies}
                                onChange={(e) => setData({
                                    ...data,
                                    startup_parameters: {
                                        ...data.startup_parameters,
                                        enable_dependencies: e.target.checked
                                    }
                                })}
                            />
                            <InfoMark placement='top' content={(
                                <>
                                    <p>Specify VMs that this VM depends on. </p>
                                    <p>It won&apos;t start unless the dependent VMs are running.</p>
                                    <p>Ensure proper startup order and timeouts.</p>
                                </>
                            )}/>
                        </div>
                        <span>{data.dependencies.join(', ')}</span>
                        <div className={data.startup_parameters.enable_dependencies ? '' : 'disabled'}>
                            {(
                                <DependenciesSelector
                                    dataTable={dataTable}
                                    onSelectChange={handleDependencySelectChange}
                                    selectedRowKeys={data.dependencies}
                                />
                            )}
                        </div>
                    </div>
                </Card>
            </div>
        </Modal>
    </>)
}