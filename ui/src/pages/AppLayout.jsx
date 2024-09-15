import {Suspense, useCallback, useEffect, useState} from "react";
import {ConfigProvider, Layout, Menu, theme} from 'antd';
import {DesktopOutlined, LogoutOutlined, SettingOutlined, ToolOutlined} from "@ant-design/icons";
import menuConfig from "../menuConfig.json"
import sysMenuConfig from "../sysMenuConfig.json"
import Spinner from "../components/controls/Spinner.jsx";
import {Link, Outlet} from "react-router-dom";
import AppFooter from "../components/AppFooter.jsx";
import {useAppContext} from "../contexts/AppContext.jsx";
import Header from "../components/Header.jsx";
import {useAuth} from "../contexts/AuthContext.jsx";

const {Content, Sider} = Layout;

const iconMap = {
    ToolOutlined: <ToolOutlined/>, DesktopOutlined: <DesktopOutlined/>, SettingOutlined: <SettingOutlined />, LogoutOutlined: <LogoutOutlined />
}

export default function AppLayout() {
    const { set_logout } = useAuth()

    const {darkThemeEnabled, setDarkThemeEnabled} = useAppContext();
    const [collapsed, setCollapsed] = useState(true);
    const [menuItems, setMenuItems] = useState([]);
    const [sysMenuItems, setSysMenuItems] = useState([]);

    //const [isLoaded, setIsLoaded] = useState(false);
    // const selectedMenuItem = location.pathname.split("/")[1] || "startups";

    const handleSysClickMenu = useCallback((item) => {
        if (item.key === 'logout') {
            set_logout();
        }
    }, [set_logout]);

    useEffect(() => {
        const config = menuConfig.map((item) => ({
            key: item.key,
            icon: iconMap[item.icon],
            label: !item.disabled && <Link to={item.key}>{item.label}</Link>,
            disabled: item.disabled
        }));
        setMenuItems(config);

        const sys_config = sysMenuConfig.map((item) => ({
            key: item.key,
            icon: iconMap[item.icon],
            label: !item.disabled && <Link to={item.key}>{item.label}</Link>,
            disabled: item.disabled,
            onClick: () => { handleSysClickMenu(item); },
        }));
        setSysMenuItems(sys_config);
        //setIsLoaded(true);
    }, [handleSysClickMenu]);

    return (<>
        <ConfigProvider theme={{
            algorithm: darkThemeEnabled ? theme.darkAlgorithm : theme.defaultAlgorithm, token: {
                colorBgBase: darkThemeEnabled ? '#121212' : '#f0f0f0',
            },
        }}>
            <Layout style={{
                minHeight: '100vh',
            }}>
                <Sider width={250}
                       style={{
                           position: 'fixed',
                            display: 'flex',
                            flexDirection: 'column',
                            height: '100vh'
                        }}
                       collapsible
                       collapsed={collapsed}
                       onCollapse={(value) => setCollapsed(value)}
                >
                    <div className="sider-container" style={{display: 'flex', flexDirection: 'column', height: '100%'}}>
                        <div>
                            <div className="demo-logo-vertical"/>
                            <Menu theme="dark" defaultSelectedKeys={['1']} mode="inline" items={menuItems}/>
                        </div>
                        <div style={{marginTop: 'auto'}}>
                            <Menu theme="dark" defaultSelectedKeys={['1']} mode="inline" items={sysMenuItems} selectedKeys={[]}/>
                        </div>
                    </div>
                </Sider>
                <Layout style={{
                    marginLeft: collapsed ? 80 : 250,
                    transition: 'margin-left 0.2s'
                }}>
                    <Header/>
                    <Content style={{
                        margin: '10px 16px',
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