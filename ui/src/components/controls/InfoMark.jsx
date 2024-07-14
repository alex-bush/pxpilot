import {FontAwesomeIcon} from "@fortawesome/react-fontawesome";
import {Popover} from "antd";
import {faCircleQuestion} from "@fortawesome/free-regular-svg-icons";

export default function InfoMark({content, placement}) {
    const popoverContext = (
        <div>
            {content}
        </div>
    );

    return (
        <>
            <div className="info">
                <Popover content={popoverContext} placement={placement}>
                    <FontAwesomeIcon  icon={faCircleQuestion}/>
                </Popover>
            </div>
        </>
    )
}