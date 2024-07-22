import {BrowserRouter, Navigate, Route, Routes} from "react-router-dom";
import {lazy, Suspense} from "react";
import AppLayout from "../pages/AppLayout.jsx";
import Register from "../pages/Register.jsx";
import {AuthProvider} from "../contexts/AuthContext.jsx";
import PrivateRoute from "./PrivateRoute.jsx";
import Login from "../pages/Login.jsx";
import {AppProvider} from "../contexts/AppContext.jsx";

const AppSettings = lazy(() => import("../pages/AppSettings.jsx"));
const ProxmoxManagement = lazy(() => import("../pages/ProxmoxManagement.jsx"));

const AppRouter = () => (
    <AuthProvider>
        <AppProvider>
            <BrowserRouter>
                <Suspense fallback={<div>Loading...</div>}>
                    <Routes>
                        <Route path="/login" element={<Login/>}/>
                        <Route path="/register" element={<Register/>}/>
                        <Route path="/" element={<PrivateRoute/>}>
                            <Route path="/*" element={<AppLayout/>}>
                                <Route path="settings" element={<AppSettings/>}/>
                                <Route path="info" element={<ProxmoxManagement/>}/>
                                <Route path="*" element={<Navigate to="settings" replace/>}/>
                            </Route>
                        </Route>
                    </Routes>
                </Suspense>
            </BrowserRouter>
        </AppProvider>
    </AuthProvider>
);

export default AppRouter;