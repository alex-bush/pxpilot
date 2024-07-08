import KeyValueTextField from "./KeyValueTextField.jsx";
import DeleteButton from "./DeleteButton.jsx";
import AddButton from "./AddButton.jsx";
import {Collapse} from "antd";
import {useEffect, useState} from "react";

export default function KeyValueSettingList({title, settings}) {
    const [data, setSettings] = useState({});

    useEffect(() => {
        setSettings(settings);
    }, [settings]);

    function handleAddClick() {
        const key = '';
        const value = '';
        const newExtra = {...data, [key]: value};

        setSettings(newExtra);
    }

    function handleDeleteClick(key) {
        console.log(key)
        const {[key]: _, ...extra} = data;
        setSettings(extra);
    }

    function handleDataChange(oldKey, newKey, newValue) {
        const {[oldKey]: _, ...rest} = data;
        const updatedExtra = {...rest, [newKey]: newValue};

        setSettings(updatedExtra);
    }

    return (
        <>
            <Collapse
                items={[{
                    key: 'other', label: title, children:
                        <div className="keyValueList">
                            {Object.entries(data).map(([key, value]) => (
                                <div key={key} className={"flex flex-row gap-2 items-center"}>
                                    <KeyValueTextField
                                        field_name={key}
                                        field_value={value}
                                        onNameChange={(newName) => handleDataChange(key, newName, value)}
                                        onValueChange={(newValue) => handleDataChange(key, key, newValue)}
                                    />
                                    <DeleteButton onDelete={() => handleDeleteClick(key)}/>
                                </div>
                            ))}
                            <AddButton onClick={handleAddClick}/>
                        </div>
                }]}
            />
        </>
    )
}