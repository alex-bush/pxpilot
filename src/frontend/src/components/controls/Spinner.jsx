import {Spin} from "antd";

export default function Spinner() {
    return (
        <>
            <div className="flex justify-center items-center w-full h-full">
                <Spin size={"large"}/>
            </div>
        </>
    )
}