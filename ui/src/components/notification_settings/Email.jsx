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
                                  value={data.smtp_server} placeholder='address'
                                  onChange={value => handleDataChange('smtp_server', value)}/>
                <LabeledTextField title='SMTP Port'
                                  value={data.smtp_port} placeholder='587'
                                  onChange={value => handleDataChange('smtp_port', value)}/>
                <LabeledTextField title='SMTP Username'
                                  value={data.smtp_user} placeholder='smtp username'
                                  onChange={value => handleDataChange('smtp_user', value)}/>
                <LabeledTextField title='SMTP Password' placeholder='password'
                                  value={data.smtp_password} is_password={"true"}
                                  onChange={value => handleDataChange('smtp_password', value)}/>
                <LabeledTextField title='From Email'
                                  value={data.from_email} placeholder='from@email.com'
                                  onChange={value => handleDataChange('from_email', value)}/>
                <LabeledTextField title='To Email'
                                  value={data.to_email} placeholder='to@email.com'
                                  onChange={value => handleDataChange('to_email', value)}/>
            </Card>
        </>
    )
}