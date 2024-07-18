import {Input} from "antd";

function LabeledTextField({ className, title, value, type = 'default', placeholder,
                              is_password = false, disabled = false,
                              onChange }) {

    function handleChange(e) {
        if (onChange) {
            onChange(e.target.value);
        }
    }

    return (
        <div className={className}>
            <label>{title}:</label>
            {
                is_password ? (
                    <Input.Password size={"large"} value={value} placeholder={placeholder} onChange={handleChange} disabled={disabled}></Input.Password>
                ) : (
                    <Input type={type} size={"large"} value={value} placeholder={placeholder} onChange={handleChange} disabled={disabled}></Input>
                )
            }
        </div>
    )
}

export default LabeledTextField;