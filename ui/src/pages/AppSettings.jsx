import {Card, Tabs, Typography} from "antd";
import ProxmoxSettings from "../components/proxmox_settings/ProxmoxSettings.jsx";
import {Notifications} from "../components/notification_settings/Notifications.jsx";
import StartupSettings from "../components/start_vm_settings/StartupSettings.jsx";
import {CloudServerOutlined, InfoCircleOutlined, MailOutlined, PlayCircleOutlined} from "@ant-design/icons";

export default function AppSettings() {
    return (
        <>
            <div className="flex justify-between gap-4">
                <div className="w-2/3 ">
                    <Tabs
                        onChange={() => {
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
                <div className="flex-grow mt-14 ml-1 w-1/3">
                    <Card className="text-gray-500 pt-5 pb-10">
                        <InfoCircleOutlined style={{ color: "green", fontSize: '25px' }} className="pb-5" />
                        <h3>Virtual Machines Startup Settings</h3>
                        <br/>
                        <p>
                            In this section, you can configure the startup settings for your virtual machines.
                            You can arrange the order in which the virtual machines will be started by dragging and
                            dropping the items.
                            This ensures that the virtual machines are started in the desired sequence, providing better
                            control over your infrastructure.
                        </p>
                        <br/>
                        <p>
                            Additionally, you can add new virtual machines to the startup list or remove existing ones.
                            Make sure to save your settings after making any changes.
                        </p>
                        <p>
                            Use the icons next to each virtual machine to further configure their startup dependencies
                            and parameters.
                        </p>
                    </Card>
                </div>
            </div>
        </>
    )
}