import LabeledTextField from "./controls/LabeledTextField.jsx";
import {Card} from "antd";
import CheckboxField from "./controls/CheckboxField.jsx";

export default function Telegram({ data, onChange }) {

    const handleDataChange = (field, value) => {
        const newData = { ...data, [field]: value };
        onChange(newData);
    };

    return (
        <>
            <Card>
                <CheckboxField title='Enabled' value={data.enabled} onChange={e => handleDataChange('enabled', e.target.checked)}/>
                <LabeledTextField title='Token' value={ data.token } onChange={value => handleDataChange('token', value) }/>
                <LabeledTextField title='Chat Id' value={ data.chat_id } onChange={value => handleDataChange('chat_id', value) }/>
            </Card>
        </>
    )
}