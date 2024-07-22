import {Layout, Popover, Typography} from "antd";
import {MoonOutlined, SunOutlined} from "@ant-design/icons";
import {useAppContext} from "../contexts/AppContext.jsx";
import About from "./About.jsx";
import {useState} from "react";

const {Footer} = Layout;


export default function AppFooter({isDarkTheme, onThemeChange}) {
    const { version } = useAppContext();
    const [isModalOpen, setIsModalOpen] = useState(false);

    return (
        <>
            <About isModalOpen={isModalOpen} onClose={() => setIsModalOpen(false)} />
            <Footer className='flex justify-end gap-5 p-5'>

                <div>
                    <Typography
                        style={{color: isDarkTheme ? 'darkslategrey' : 'gray'}}
                        onClick={() => setIsModalOpen(true)}>
                        Version: {version}
                    </Typography>
                </div>
                <div className='theme-switcher'>
                    {isDarkTheme ?
                        <Popover content={<p>Switch to light theme</p>} placement="topLeft">
                            <SunOutlined className='theme-icon'
                                         onClick={() => onThemeChange(false)}/>
                        </Popover>
                        :
                        <Popover content={<p>Switch to dark theme</p>} placement="topLeft">
                            <MoonOutlined className='theme-icon'
                                          onClick={() => onThemeChange(true)}/>
                        </Popover>
                    }
                </div>

            </Footer>
        </>
    )
}