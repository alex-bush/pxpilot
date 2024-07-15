import {useState} from "react";
import {Layout, Menu} from 'antd';
import AppSettings from "./AppSettings.jsx";
import {DesktopOutlined, ToolOutlined} from "@ant-design/icons";
import ProxInfo from "./Proxinfo.jsx";

const {Content,  Sider} = Layout;

function getItem(label, key, icon, children) {
    return {
        key,
        icon,
        children,
        label,
    };
}

const items = [
    getItem('VM startup management', '1', <ToolOutlined/>),
    getItem('Proxmox information', '2', <DesktopOutlined/>),
];

export default function AppLayer() {
    const [collapsed, setCollapsed] = useState(true);
    const [selectedMenuItem, setSelectedMenuItem] = useState(null);

    return (
        <>
            <Layout style={{
                minHeight: '100vh',
            }}>
                <Sider width={250} collapsible collapsed={collapsed} onCollapse={(value) => setCollapsed(value)}>
                    <div className="demo-logo-vertical"/>
                    <Menu theme="dark" defaultSelectedKeys={['1']} mode="inline" items={items}
                          onClick={(e) => setSelectedMenuItem(e.key)}/>
                </Sider>
                <Content style={{
                    margin: '0 16px',
                }}>
                    {selectedMenuItem === '1' && <AppSettings/>}
                    {selectedMenuItem === '2' && <ProxInfo/>}
                </Content>
            </Layout>
        </>
    )
}