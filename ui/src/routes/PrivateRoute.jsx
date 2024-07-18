import {Navigate, Outlet} from "react-router-dom";
import {useAuth} from "../contexts/AuthContext.jsx";
import {useEffect, useState} from "react";
import {get_api_status} from "../services/auth.js";
import Spinner from "../components/controls/Spinner.jsx";

const PrivateRoute = () => {
    const { isAuthenticated } = useAuth();
    const [isFirstRun, setIsFirstRun] = useState(true);
    const [isLoading, setIsLoading] = useState(true);

    useEffect(() => {
        async function fetchStatus() {
            const state = await get_api_status();
            setIsFirstRun(state.is_first_run);
            setIsLoading(false);
        }

        fetchStatus();
    }, []);

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
