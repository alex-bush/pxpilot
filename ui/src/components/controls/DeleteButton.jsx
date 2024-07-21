import {Popover} from "antd";
import {CloseCircleOutlined} from "@ant-design/icons";

export default function DeleteButton({size = 'middle', popoverContext, onDelete}) {
    return (
        <>
            <div className="delete-icon-container" onClick={onDelete}>
                <Popover content={popoverContext} placement='top'>
                    <CloseCircleOutlined className='delete-icon' />
                </Popover>
            </div>
        </>
    )
}