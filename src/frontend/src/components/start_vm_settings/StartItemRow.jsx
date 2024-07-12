import DeleteButton from "../controls/DeleteButton.jsx";
import {FontAwesomeIcon} from "@fortawesome/react-fontawesome";
import {faClockRotateLeft, faHeartbeat, faLink} from '@fortawesome/free-solid-svg-icons';
import {Popover} from "antd";

export default function StartItemRow({item, onClick, onRemove}) {
    const waitContent = (
        <div>
            {item.startup_parameters.await_running && <p>Wait {item.startup_parameters.startup_timeout} seconds until VM started successfully</p>}
            {!item.startup_parameters.await_running && <p>No waiting for the VM to be fully started</p>}
        </div>
    );

    const get = (h) => {
        if (h === 'ping') {
            return 'Ping';
        }
        if (h === 'http') {
            return 'HTTP request to';
        }
    }

    const healthcheckContent = (
        <div>
            {item.healthcheck && item.healthcheck.check_method !== 'none' && (
                <>
                    <p>Healthcheck:</p>
                    <p>{get(item.healthcheck.check_method)}: {item.healthcheck.target_url}</p>
                </>
            )}
            {!(item.healthcheck && item.healthcheck.check_method !== 'none') && <p>Healthcheck is not defined</p>}
        </div>
    );

    const dependenciesContent = (
        <div>
            {item.dependencies && item.dependencies.length > 0 && (
                <>
                    <p>Depends on: {item.dependencies.join(', ')}</p>
                    <p>{item.startup_parameters.enable_dependencies ? 'Enabled' : 'Disabled'}</p>
                </>
                )}
            {!(item.dependencies && item.dependencies.length > 0) && <p>There are no dependencies to run</p>}
        </div>
    );

    return (<>
        <div id={item.vm_id} className="w-full mb-3 cursor-pointer" onClick={onClick}>
            <div
                className="flex justify-between items-center w-full p-4 border border-gray-300 shadow-md sm:rounded-2xl">
                <div className="flex flex-col w-full">
                    <div className="flex items-center">
                        <span className="mr-0.5">id: </span>
                        <span className="font-bold">{item.vm_id}</span>
                        {item.name && <span className="font-bold">: {item.name}</span>}
                    </div>
                    <div className="flex justify-between items-center w-full mt-1">
                        <span className="flex-1">{item.description}</span>
                        <div className="flex gap-3 w-1/6 text-center mr-3">
                            <div>
                                <Popover content={waitContent}>
                                    <FontAwesomeIcon icon={faClockRotateLeft} flip="horizontal"
                                                     className={!item.startup_parameters.await_running ? 'disabled-icon' : ''}
                                    />
                                </Popover>
                            </div>
                            <div>
                                <Popover content={healthcheckContent}>
                                    <FontAwesomeIcon icon={faHeartbeat}
                                                     className={!(item.healthcheck && item.healthcheck.check_method !== 'none') ? 'disabled-icon' : ''}
                                                     title='Healthcheck enabled'/>
                                </Popover>
                            </div>
                            <div>
                                <Popover content={dependenciesContent}>
                                    <FontAwesomeIcon icon={faLink} color={item.startup_parameters.enable_dependencies ? 'blue' : 'black'}
                                                     className={!(item.dependencies && item.dependencies.length > 0) ? 'disabled-icon' : ''}
                                                     title='Healthcheck enabled'/>
                                </Popover>
                            </div>
                        </div>
                    </div>
                </div>
                <div className="ml-4">
                <DeleteButton size={'small'} onDelete={(e) => {
                        e.stopPropagation();
                        onRemove(item.vm_id)
                    }}/>
                </div>
            </div>
        </div>

    </>)
}