import {BrowserRouter, Navigate, Route, Routes} from "react-router-dom";
import {lazy, Suspense} from "react";
import AppLayer from "./pages/AppLayer.jsx";
import Register from "./pages/Register.jsx";
import {AuthProvider} from "./AuthContext.jsx";
import PrivateRoute from "./PrivateRoute.jsx";
import Login from "./pages/Login.jsx";

const AppSettings = lazy(() => import("./pages/AppSettings"));
const ProxInfo = lazy(() => import("./pages/Proxinfo"));

const AppRouter = () => (
    <AuthProvider>
        <BrowserRouter>
            <Suspense fallback={<div>Loading...</div>}>
                <Routes>
                    <Route path="/login" element={<Login/>}/>
                    <Route path="/register" element={<Register/>}/>
                    <Route path="/" element={<PrivateRoute/>}>
                        <Route path="/*" element={<AppLayer/>}>
                            <Route path="settings" element={<AppSettings/>}/>
                            <Route path="info" element={<ProxInfo/>}/>
                            <Route path="*" element={<Navigate to="settings" replace/>}/>
                        </Route>
                    </Route>
                </Routes>
            </Suspense>
        </BrowserRouter>
    </AuthProvider>
);

export default AppRouter;