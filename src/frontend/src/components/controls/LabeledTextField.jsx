import {Input} from "antd";

function LabeledTextField({ title, value, is_password = false, onChange }) {

    function handleChange(e) {
        if (onChange) {
            onChange(e.target.value);
        }
    }

    return (
        <div >
            <label className="flex">{title}:</label>
            {
                is_password ? (
                    <Input.Password size={"large"} value={value} onChange={handleChange}></Input.Password>
                ) : (
                    <Input size={"large"} value={value} onChange={handleChange}></Input>
                )
            }
        </div>
    )
}

export default LabeledTextField;