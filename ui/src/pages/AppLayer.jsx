import {lazy, Suspense, useEffect, useState} from "react";
import {Layout, Menu, Spin} from 'antd';
import {DesktopOutlined, ToolOutlined} from "@ant-design/icons";
import menuConfig from "../menuConfig.json"
import Spinner from "../components/controls/Spinner.jsx";

const {Content, Sider} = Layout;

const iconMap = {
    ToolOutlined: <ToolOutlined/>, DesktopOutlined: <DesktopOutlined/>,
}

const componentMap = {
    AppSettings: lazy(() => import("./AppSettings")), ProxInfo: lazy(() => import("./Proxinfo")),
}

export default function AppLayer() {
    const [collapsed, setCollapsed] = useState(true);
    const [menuItems, setMenuItems] = useState([]);
    const [selectedMenuItem, setSelectedMenuItem] = useState('1');
    const [SelectedComponent, setSelectedComponent] = useState(componentMap['AppSettings']);
    const [isLoaded, setIsLoaded] = useState(false);

    useEffect(() => {
        const config = menuConfig.map((item) => ({
            key: item.key, icon: iconMap[item.icon], label: item.label, component: item.component,
        }));
        setMenuItems(config);
        setSelectedComponent(componentMap[config[0].component]);
        setIsLoaded(true);
    }, []);

    function hundleMenuClick(e) {
        setSelectedMenuItem(e.key);
        const selectedItem = menuItems.find(item => item.key === e.key);
        setSelectedComponent(componentMap[selectedItem.component]);
    }

    return (<>
        <Layout style={{
            minHeight: '100vh',
        }}>
            <Sider width={250} collapsible collapsed={collapsed} onCollapse={(value) => setCollapsed(value)}>
                <div className="demo-logo-vertical"/>
                <Menu theme="dark" defaultSelectedKeys={selectedMenuItem} mode="inline" items={menuItems}
                      onClick={hundleMenuClick}/>
            </Sider>
            <Content style={{
                margin: '0 16px',
            }}>
                <Suspense fallback={<Spinner/>}>
                    {isLoaded ? <SelectedComponent /> : <Spinner/>}
                </Suspense>
            </Content>
        </Layout>
    </>)
}