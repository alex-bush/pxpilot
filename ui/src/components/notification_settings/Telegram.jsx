import LabeledTextField from "../controls/LabeledTextField.jsx";
import {Card} from "antd";
import CheckboxField from "../controls/CheckboxField.jsx";

const inputPadding = "p-2";
export default function Telegram({ data, onChange }) {

    const handleDataChange = (field, value) => {
        const newData = { ...data, [field]: value };
        onChange(newData);
    };

    return (
        <>
            <Card>
                <CheckboxField className={inputPadding} title='Enabled' value={data.enabled} onChange={e => handleDataChange('enabled', e.target.checked)}/>
                <LabeledTextField className={inputPadding} title='Token' value={ data.token } placeholder='telegram bot id' onChange={value => handleDataChange('token', value) }/>
                <LabeledTextField className={inputPadding} title='Chat Id' value={ data.chat_id } placeholder='chat id' onChange={value => handleDataChange('chat_id', value) }/>
            </Card>
        </>
    )
}