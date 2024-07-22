import {createContext, useContext, useState} from "react";

const AppContext = createContext();

export const AppProvider = ({children}) => {
    const [version, setVersion] = useState(0);
    const [darkThemeEnabled, setDarkThemeEnabled] = useState(true);

    return (<AppContext.Provider value={{darkThemeEnabled, setDarkThemeEnabled, version, setVersion}}>
        {children}
    </AppContext.Provider>);
}

export const useAppContext = () => useContext(AppContext);