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
                                <div key={index} className={"flex flex-row gap-2 items-center  p-2"}>
                                    <KeyValueTextField
                                        field_name={key}
                                        field_value={value}
                                        onNameChange={(newName) => onDataChange(index, newName, value)}
                                        onValueChange={(newValue) => onDataChange(index, key, newValue)}
                                    />
                                    <DeleteButton popoverContext={<p>Delete setting</p>} onDelete={() => onDeleteClick(index)}/>
                                </div>
                            ))

                            }
                            <div className="pl-2 pt-2"><AddButton onClick={onAddClick}/></div>
                        </div>
                }]}
            />
        </>
    )
}