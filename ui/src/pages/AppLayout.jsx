import {Suspense, useEffect, useState} from "react";
import {ConfigProvider, Layout, Menu, theme} from 'antd';
import {DesktopOutlined, ToolOutlined} from "@ant-design/icons";
import menuConfig from "../menuConfig.json"
import Spinner from "../components/controls/Spinner.jsx";
import {Link, Outlet} from "react-router-dom";
import AppFooter from "../components/AppFooter.jsx";
import {useAppContext} from "../contexts/AppContext.jsx";

const {Content, Sider} = Layout;

const iconMap = {
    ToolOutlined: <ToolOutlined/>, DesktopOutlined: <DesktopOutlined/>,
}

export default function AppLayout() {
    const {darkThemeEnabled, setDarkThemeEnabled} = useAppContext();
    const [collapsed, setCollapsed] = useState(true);
    const [menuItems, setMenuItems] = useState([]);
    //const [isLoaded, setIsLoaded] = useState(false);
    const selectedMenuItem = location.pathname.split("/")[1] || "settings";

    useEffect(() => {
        const config = menuConfig.map((item) => ({
            key: item.key, icon: iconMap[item.icon], label: <Link to={item.key}>{item.label}</Link>,
        }));
        setMenuItems(config);
        //setIsLoaded(true);
    }, []);

    return (<>
        <ConfigProvider theme={{
            algorithm: darkThemeEnabled ? theme.darkAlgorithm : theme.defaultAlgorithm, token: {
                colorBgBase: darkThemeEnabled ? '#121212' : '#f0f0f0',
            },
        }}>
            <Layout style={{
                minHeight: '100vh',
            }}>
                <Sider width={250} collapsible collapsed={collapsed} onCollapse={(value) => setCollapsed(value)}>
                    <div className="demo-logo-vertical"/>
                    <Menu theme="dark" defaultSelectedKeys={selectedMenuItem} mode="inline" items={menuItems}
                    />
                </Sider>
                <Layout>
                    <Content style={{
                        margin: '0 16px',
                    }}>
                        <Suspense fallback={<Spinner/>}>
                            <Outlet/>
                        </Suspense>
                    </Content>
                    <AppFooter isDarkTheme={darkThemeEnabled} onThemeChange={(value) => setDarkThemeEnabled(value)}/>
                </Layout>
            </Layout>
        </ConfigProvider>
    </>)
}