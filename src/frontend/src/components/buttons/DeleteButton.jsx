import {Button} from "antd";

export default function DeleteButton({size = 'middle', onDelete}) {
    return (
        <>
            <Button className={"deleteButton"} type="default" danger shape="default" size={size}
                    onClick={onDelete}> X </Button>
        </>
    )
}