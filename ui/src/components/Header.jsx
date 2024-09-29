import { Typography } from 'antd';
import ThemeSwitcher from "./ThemeSwitcher.jsx";
const { Title } = Typography;

export default function Header({isDarkTheme, onThemeChange}) {
    return (
        <>
            <div className="flex bg-gray-900 justify-between">
                <Title style={{ color: 'white' }} className="pt-1 pl-4 v" level={2}>PxPilot</Title>
                <ThemeSwitcher isDarkTheme={isDarkTheme} onThemeChange={onThemeChange} />
            </div>

        </>
    )
}