import {Button} from "antd";

export default function AddButton({onClick}) {
    return (
        <>
            <Button type="primary" shape="circle" onClick={onClick}>+</Button>
        </>
    )
}