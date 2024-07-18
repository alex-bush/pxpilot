import {Input} from "antd";
import {useEffect, useState} from "react";

export default function KeyValueTextField({ field_name, field_value, onNameChange, onValueChange }) {
    const [value, setValue] = useState(field_value);
    const [title, setTitle] = useState(field_name);

    useEffect(() => {
        setValue(field_value);
    }, [field_value]);

    useEffect(() => {
        setTitle(field_name);
    }, [field_name]);

    function _onNameChange(e) {
        const value = e.target.value;
        setTitle(value)
        if (onNameChange) {
            onNameChange(value);
        }
    }

    function _onValueChange(e) {
        const value = e.target.value;
        setValue(value)
        if (onValueChange) {
            onValueChange(value);
        }
    }

    return (
        <>
            <Input size={"large"} value={ title } placeholder='name' onChange={_onNameChange}></Input>
            <Input size={"large"} value={ value } placeholder='value' onChange={_onValueChange}></Input>
        </>
    )
}