import KeyValueTextField from "./KeyValueTextField.jsx";
import DeleteButton from "./DeleteButton.jsx";
import AddButton from "./AddButton.jsx";
import {Collapse} from "antd";

export default function KeyValueSettingList({title, settings, onDataChange, onAddClick, onDeleteClick}) {
    return (<>
        <Collapse
            items={[{
                key: 'other', label: title, children: <div className="keyValueList">
                    {settings &&
                        settings.map((setting, index) => (
                            <div key={index} className={"flex flex-row gap-2 items-center  p-2"}>
                                <KeyValueTextField
                                    field_name={setting.name}
                                    field_value={setting.value}
                                    onNameChange={(newName) => onDataChange(index, newName, setting.value)}
                                    onValueChange={(newValue) => onDataChange(index, setting.name, newValue)}
                                />
                                <DeleteButton popoverContext={<p>Delete setting</p>}
                                              onDelete={() => onDeleteClick(index)}/>
                            </div>))
                    }
                    <div className="pl-2 pt-2"><AddButton onClick={onAddClick}/></div>
                </div>
            }]}
        />
    </>)
}