import LabeledTextField from "../controls/LabeledTextField.jsx";
import {Card} from "antd";
import CheckboxField from "../controls/CheckboxField.jsx";

export default function Email({data, onChange}) {

    const handleDataChange = (field, value) => {
        const newData = {...data, [field]: value};
        onChange(newData);
    };

    return (
        <>
            <Card>
                <CheckboxField title='Enabled' value={data.enabled}
                               onChange={e => handleDataChange('enabled', e.target.checked)}/>
                <LabeledTextField title='SMTP Server'
                                  value={data.smtp_server}
                                  onChange={value => handleDataChange('smtp_server', value)}/>
                <LabeledTextField title='SMTP Port'
                                  value={data.smtp_port}
                                  onChange={value => handleDataChange('smtp_port', value)}/>
                <LabeledTextField title='SMTP Username'
                                  value={data.smtp_user}
                                  onChange={value => handleDataChange('smtp_user', value)}/>
                <LabeledTextField title='SMTP Password'
                                  value={data.smtp_password} is_password={"true"}
                                  onChange={value => handleDataChange('smtp_password', value)}/>
                <LabeledTextField title='From Email'
                                  value={data.from_email}
                                  onChange={value => handleDataChange('from_email', value)}/>
                <LabeledTextField title='To Email'
                                  value={data.to_email}
                                  onChange={value => handleDataChange('to_email', value)}/>
            </Card>
        </>
    )
}