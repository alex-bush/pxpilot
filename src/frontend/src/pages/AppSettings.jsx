import {Space} from "antd";
import ProxmoxSettings from "../components/proxmox_settings/ProxmoxSettings.jsx";
import {Notifications} from "../components/notification_settings/Notifications.jsx";
import StartupSettings from "../components/start_vm_settings/StartupSettings.jsx";

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