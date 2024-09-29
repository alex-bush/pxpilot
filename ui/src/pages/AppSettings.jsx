import {Tabs} from "antd";
import ProxmoxSettings from "../components/proxmox_settings/ProxmoxSettings.jsx";
import {Notifications} from "../components/notification_settings/Notifications.jsx";
import VmsStartupSettings from "../components/start_vm_settings/VmsStartupSettings.jsx";
import {CloudServerOutlined, MailOutlined, PlayCircleOutlined} from "@ant-design/icons";
import {useEffect, useState} from "react";
import { useNavigate, useLocation } from "react-router-dom";

import StartupsHelperPanel from "../components/helper_panels/StartupsHelperPanel.jsx";
import NotificationsHelperPanel from "../components/helper_panels/NotificationsHelperPanel.jsx";
import ProxmoxHelperPanel from "../components/helper_panels/ProxmoxHelperPanel.jsx";


const tabItems = [
    {
        label: "Startup settings",
        key: "startup_settings",
        children: <VmsStartupSettings />,
        icon: <PlayCircleOutlined />,
    },
    {
        label: "Notification settings",
        key: "notification_settings",
        children: <Notifications />,
        icon: <MailOutlined />,
    },
    {
        label: "Proxmox settings",
        key: "proxmox_settings",
        children: <ProxmoxSettings />,
        icon: <CloudServerOutlined />,
    },
];

export default function AppSettings() {
    const navigate = useNavigate();
    const location = useLocation();
    const [selectedTab, setSelectedTab] = useState(null);

    useEffect(() => {
        const path = location.pathname.split('/').pop();
        if (tabItems.some(tab => tab.key === path)) {
            setSelectedTab(path);
        } else {
            navigate('startup_settings');
        }
    }, [location.pathname, navigate]);

    const handleTabChange = (key) => {
        setSelectedTab(key);
        navigate(key);
    };

    return (
        <>
            <div className="flex justify-between gap-4">
                <div className="w-2/3 ">
                    <Tabs
                        activeKey={selectedTab}
                        onChange={handleTabChange}
                        type="card"
                        items={tabItems}
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