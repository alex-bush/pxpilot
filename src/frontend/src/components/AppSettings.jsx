import {Space} from "antd";
import ProxmoxSettings from "./ProxmoxSettings.jsx";
import {Notifications} from "./Notifications.jsx";
import StartupSettings from "./StartupSettings.jsx";

export default function AppSettings() {
    return (
        <>
            <div style={{display: 'flex '}}>
                <Space direction="vertical" size="middle" style={{flex: 1, margin: 20}}>
                    <ProxmoxSettings/>
                    <Notifications/>
                </Space>
                <div style={{flex: 1, flexDirection: "column", margin: 20}}>
                    <StartupSettings/>
                </div>
            </div>
        </>
    )
}