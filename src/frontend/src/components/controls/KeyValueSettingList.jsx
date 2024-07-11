import KeyValueTextField from "./KeyValueTextField.jsx";
import DeleteButton from "./DeleteButton.jsx";
import AddButton from "./AddButton.jsx";
import {Collapse} from "antd";

export default function KeyValueSettingList({title, settings, onDataChange, onAddClick, onDeleteClick}) {
    return (
        <>
            <Collapse
                items={[{
                    key: 'other', label: title, children:
                        <div className="keyValueList">
                            {Object.entries(settings).map(([key, value], index) => (
                                <div key={index} className={"flex flex-row gap-2 items-center"}>
                                    <KeyValueTextField
                                        field_name={key}
                                        field_value={value}
                                        onNameChange={(newName) => onDataChange(index, newName, value)}
                                        onValueChange={(newValue) => onDataChange(index, key, newValue)}
                                    />
                                    <DeleteButton onDelete={() => onDeleteClick(index)}/>
                                </div>
                            ))

                            }
                            <AddButton onClick={onAddClick}/>
                        </div>
                }]}
            />
        </>
    )
}