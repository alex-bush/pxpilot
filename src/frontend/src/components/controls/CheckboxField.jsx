import {Checkbox} from "antd";

export default function CheckboxField({ title, value, onChange }) {
    return (
        <>
            <Checkbox onChange={onChange} checked={value}>{ title }</Checkbox>
        </>
    )
}