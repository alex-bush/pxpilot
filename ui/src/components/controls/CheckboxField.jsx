import {Checkbox} from "antd";

export default function CheckboxField({ className, title, value, onChange }) {
    return (
        <>
            <Checkbox className={className} onChange={onChange} checked={value}>{ title }</Checkbox>
        </>
    )
}