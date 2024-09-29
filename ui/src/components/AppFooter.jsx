import {Layout} from "antd";
import ThemeSwitcher from "./ThemeSwitcher.jsx";

const {Footer} = Layout;

export default function AppFooter({isDarkTheme, onThemeChange}) {
    return (<>
            <Footer className='flex justify-end gap-5 p-10'>
                {/*<ThemeSwitcher isDarkTheme={isDarkTheme} onThemeChange={onThemeChange} />*/}
            </Footer>
    </>)
}