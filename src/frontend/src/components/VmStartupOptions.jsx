import LabeledTextField from "./controls/LabeledTextField.jsx";
import {Button, Card, Select} from "antd";

export default function VmStartupOptions(props) {
    return (
        <>
            <Card
                style={{
                    width: "-moz-fit-content",
                }}
            >
                <LabeledTextField title='Vm Id' value={props.item.vm_id}/>
                <LabeledTextField title='Vm Name' value={props.item.name}/>

                {props.item.healthcheck ?
                    (
                        <div>
                        <LabeledTextField title='Healthcheck url' value={props.item.healthcheck.target_url}/>

                    <Select
                        defaultValue="PING"
                        style={{ width: 120 }}
                        allowClear
                        options={[{ value: 'PING', label: 'PING' }, { value: 'HTTP', label: 'HTTP request' }]}
                    />
                        </div>
                    )
                    :
                    <p/>
                }

            </Card>
        </>
    )
}