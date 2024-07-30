import {Card, Tabs, Typography} from "antd";
import ProxmoxSettings from "../components/proxmox_settings/ProxmoxSettings.jsx";
import {Notifications} from "../components/notification_settings/Notifications.jsx";
import StartupSettings from "../components/start_vm_settings/StartupSettings.jsx";
import {CloudServerOutlined, InfoCircleOutlined, MailOutlined, PlayCircleOutlined} from "@ant-design/icons";
import {useState} from "react";
import StartupsHelperPanel from "../components/helper_panels/StartupsHelperPanel.jsx";
import NotificationsHelperPanel from "../components/helper_panels/NotificationsHelperPanel.jsx";
import ProxmoxHelperPanel from "../components/helper_panels/ProxmoxHelperPanel.jsx";



export default function AppSettings() {
    const [selectedTab, setSelectedTab] = useState(null);
    return (
        <>
            <div className="flex justify-between gap-4">
                <div className="w-2/3 ">
                    <Tabs
                        onChange={(e) => {
                            setSelectedTab(e)
                        }}
                        type="card"
                        items={[{
                            label: "Startup settings",
                            key: "startup_settings",
                            children: <StartupSettings/>,
                            icon: <PlayCircleOutlined/>
                        }, {
                            label: "Notification settings",
                            key: "notification_settings",
                            children: <Notifications/>,
                            icon: <MailOutlined/>
                        }, {
                            label: "Proxmox settings",
                            key: "proxmox_settings",
                            children: <ProxmoxSettings/>,
                            icon: <CloudServerOutlined/>,
                        },

                        ]}

                    />
                </div>
                <div className="flex-grow mt-14 ml-10 mr-10 w-1/3">
                    {selectedTab === 'startup_settings' && <StartupsHelperPanel/> }
                    {selectedTab === 'notification_settings' && <NotificationsHelperPanel/> }
                    {selectedTab === 'proxmox_settings' && <ProxmoxHelperPanel/> }
                </div>
            </div>
        </>
    )
}