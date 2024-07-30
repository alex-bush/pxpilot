import {useCallback, useEffect, useRef, useState} from "react";
import useAuthFetch from "./useAuthFetch.js";
import {RELOAD_CONFIG_URL} from "../config.js";
import useNotifier from "./useNotifier.js";

function useLoadData(url, initialState, title, processData = null) {
    const [data, setData] = useState(initialState);
    const [isLoading, setIsLoading] = useState(false);
    const [isSaving, setIsSaving] = useState(false);

    const {authGet, authPost} = useAuthFetch();
    const {showNotification, notificationHolder} = useNotifier();

    const processDataRef = useRef(processData);

    const fetchData = useCallback(async () => {
        setIsLoading(true);

        let data = await authGet(url);

        if (processDataRef.current) {
            data = processDataRef.current(data);
        }

        setData(data);
        setIsLoading(false);
    }, [authGet, url]);

    const saveData = useCallback(async (body) => {
        setIsSaving(true);

        try {
            await authPost(url, body);
            await authPost(RELOAD_CONFIG_URL);
            await fetchData();
            showNotification('success', title);
        } catch (err) {
                console.log(err);
                showNotification('error', title);
        } finally {
            setIsSaving(false);
        }
    }, [authPost, url, fetchData, showNotification, title]);

    useEffect(() => {
        fetchData();
    }, [fetchData]);

    return {data, isLoading, isSaving, fetchData, saveData, showNotification, notificationHolder};
}

export default useLoadData;