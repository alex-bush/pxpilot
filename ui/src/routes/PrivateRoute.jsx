import {Navigate, Outlet} from "react-router-dom";
import {useAuth} from "../contexts/AuthContext.jsx";
import {useEffect, useState} from "react";
import {get_api_status} from "../services/auth.js";
import Spinner from "../components/controls/Spinner.jsx";
import {useAppContext} from "../contexts/AppContext.jsx";
import useAuthFetch from "../hooks/useAuthFetch.js";
import {USER_SETTINGS_URL} from "../config.js";
import {Constants} from "../constants.js";

const PrivateRoute = () => {
    const { isAuthenticated } = useAuth();
    const { authGet } = useAuthFetch();
    const { setVersion, setDarkThemeEnabled } = useAppContext();
    const [isFirstRun, setIsFirstRun] = useState(true);
    const [isLoading, setIsLoading] = useState(true);

    useEffect(() => {
        async function fetchStatus() {
            const state = await get_api_status();
            setVersion(state.version);
            //setDarkThemeEnabled(state.dark_theme);
            setIsFirstRun(state.is_first_run);
            setIsLoading(false);

            if (isAuthenticated) {
                let settings = await authGet(USER_SETTINGS_URL);
                if (settings) {
                    let theme = settings.filter(x => x.name === Constants.UserSettings.THEME_NAME)[0];
                    if (theme) {
                        setDarkThemeEnabled(theme.value === Constants.UserSettings.DARK_THEME);
                    }
                }
            }
        }

        fetchStatus();
    }, [authGet, isAuthenticated, setDarkThemeEnabled, setVersion]);

    if (isLoading) {
        return <div className="flex justify-center items-center min-h-screen">
            <Spinner/>
        </div>;
    }

    if (isAuthenticated) {
        return <Outlet/>;
    } else {
        return isFirstRun ? <Navigate to="/register" /> : <Navigate to="/login" />;
    }
};

export default PrivateRoute;
