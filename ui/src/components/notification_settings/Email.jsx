import LabeledTextField from "../controls/LabeledTextField.jsx";
import {Card} from "antd";
import CheckboxField from "../controls/CheckboxField.jsx";

const inputPadding = "p-2";

export default function Email({data, onChange}) {

    const handleDataChange = (field, value) => {
        const newData = {...data, [field]: value};
        onChange(newData);
    };

    return (
        <>
            <Card>
                <CheckboxField className={inputPadding} title='Enabled' value={data.enabled}
                               onChange={e => handleDataChange('enabled', e.target.checked)}/>
                <LabeledTextField className={inputPadding} title='SMTP Server'
                                  value={data.smtp_server} placeholder='address'
                                  onChange={value => handleDataChange('smtp_server', value)}/>
                <LabeledTextField className={inputPadding} title='SMTP Port'
                                  value={data.smtp_port} placeholder='587'
                                  onChange={value => handleDataChange('smtp_port', value)}/>
                <LabeledTextField className={inputPadding} title='SMTP Username'
                                  value={data.smtp_user} placeholder='smtp username'
                                  onChange={value => handleDataChange('smtp_user', value)}/>
                <LabeledTextField className={inputPadding} title='SMTP Password' placeholder='password'
                                  value={data.smtp_password} is_password={"true"}
                                  onChange={value => handleDataChange('smtp_password', value)}/>
                <LabeledTextField className={inputPadding} title='From Email'
                                  value={data.from_email} placeholder='from@email.com'
                                  onChange={value => handleDataChange('from_email', value)}/>
                <LabeledTextField className={inputPadding} title='To Email'
                                  value={data.to_email} placeholder='to@email.com'
                                  onChange={value => handleDataChange('to_email', value)}/>
            </Card>
        </>
    )
}