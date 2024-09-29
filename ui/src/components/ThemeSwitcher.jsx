import {Popover} from "antd";
import {MoonOutlined, QuestionCircleFilled, SunOutlined} from "@ant-design/icons";
import {useAppContext} from "../contexts/AppContext.jsx";
import {useState} from "react";
import About from "./About.jsx";

export default function ThemeSwitcher({isDarkTheme, onThemeChange}) {
    const {version} = useAppContext();
    const [isModalOpen, setIsModalOpen] = useState(false);

    return (<>
        <About
            version={version}
            isModalOpen={isModalOpen}
            settings={{
                supportPlatforms: {buy_me_a_coffee: true, github: true},
                showUsefulLinks: false,
                showVersionHistory: false
            }}
            onClose={() => setIsModalOpen(false)}/>
        <div className="flex flex-row pt-1">
            <div className="theme-icon-wrapper">
                <Popover content={<p>About</p>} placement="topLeft">
                    <a style={{color: isDarkTheme ? '#08c' : '#08c'}}
                       onClick={() => setIsModalOpen(true)}>
                        <div className='flex gap-2'>
                            <QuestionCircleFilled style={{fontSize: '16px', color: '#08c'}}/>
                            Version: {version}
                        </div>
                    </a>
                </Popover>
            </div>
            <div className='theme-switcher'>
                {isDarkTheme ? (
                    <Popover content={<p>Switch to light theme</p>} placement="topLeft">
                        <div className="theme-icon-wrapper">
                            <SunOutlined className='theme-icon' onClick={() => onThemeChange(false)}/>
                        </div>
                    </Popover>
                ) : (
                    <Popover content={<p>Switch to dark theme</p>} placement="topLeft">
                        <div className="theme-icon-wrapper">
                            <MoonOutlined className='theme-icon' onClick={() => onThemeChange(true)}/>
                        </div>
                    </Popover>
                )}
            </div>
        </div>
    </>)
}