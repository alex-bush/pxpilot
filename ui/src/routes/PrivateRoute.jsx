import {Navigate, Outlet} from "react-router-dom";
import {useAuth} from "../contexts/AuthContext.jsx";
import {useEffect, useState} from "react";
import {get_api_status} from "../services/auth.js";

const PrivateRoute = () => {
    const {isAuthenticated} = useAuth();
    const [isFirstRun, setIsFirstRun] = useState(true);

    useEffect(() => {
        async function fetch() {
            const state = await get_api_status();
            setIsFirstRun(state.is_first_run);
        }

        fetch();
    }, []);

    return isAuthenticated ? <Outlet/> : isFirstRun ? <Navigate to="/register"/> : <Navigate to="/login"/>;
};

export default PrivateRoute;
