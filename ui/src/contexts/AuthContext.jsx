import {createContext, useContext, useEffect, useState} from "react";

const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
    const [isAuthenticated, setIsAuthenticated] = useState(false);

    useEffect(() => {
        const token = localStorage.getItem("access_token");
        if (token) {
            setIsAuthenticated(true);
        }
    }, [])

    const set_login = (token) => {
        localStorage.setItem("access_token", token);
        setIsAuthenticated(true);
    };
    const set_logout = () => {
        localStorage.removeItem("access_token");
        setIsAuthenticated(false)
    };
    const access_token = () =>  localStorage.getItem("access_token");

    return (
        <AuthContext.Provider value={{ isAuthenticated, set_login, set_logout, access_token }}>
            {children}
        </AuthContext.Provider>
    );
};

export const useAuth = () => useContext(AuthContext);
