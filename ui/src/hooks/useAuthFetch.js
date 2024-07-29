import {useNavigate} from "react-router-dom";
import {API_URL} from "../config.js";
import {useAuth} from "../contexts/AuthContext.jsx";
import {useCallback} from "react";

export default function useAuthFetch() {
    const navigate = useNavigate();
    const {access_token, set_logout} = useAuth();

    const authGet = useCallback(async (url, options = {}, navigate_to = '/login') => {
        const accessToken = access_token();
        options.headers = {
            ...options.headers,
            'Authorization': `Bearer ${accessToken}`,
            'Content-Type': 'application/json',
        }

        const response = await fetch(API_URL + url, options);
        if (response.status === 401) {
            set_logout();
            navigate(navigate_to);
        }
        if (response.status === 204) {
            return null;
        }
        if (response.ok && response.headers.get('content-type')?.includes('application/json')) {
            return await response.json();
        }
    }, [access_token, navigate, set_logout]);

    const authPost = useCallback(async (url, body = null, options = {}, navigate_to = '/login') => {
        const accessToken = access_token();
        options.headers = {
            ...options.headers,
            'Authorization': `Bearer ${accessToken}`,
            'Content-Type': 'application/json',
        }
        options.method = 'POST';
        if (body) {
            options.body = JSON.stringify(body);
        }

        const response = await fetch(API_URL + url, options);
        if (response.status === 401) {
            set_logout();
            navigate(navigate_to);
        }
        if (response.ok && response.headers.get('content-type')?.includes('application/json')){
            return await response.json();
        }
        if (!response.ok) {
            throw response;
        }
    }, [access_token, navigate, set_logout]);

    return { authGet, authPost };
}