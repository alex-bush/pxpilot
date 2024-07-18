import {
    API_URL, CONFIG_URL,
    NOTIFICATIONS_SETTINGS_URL, PX_GET_VMS_URL,
    PX_SETTINGS_URL,
    PX_VALIDATE_CONNECTION_URL,
    STARTUPS_SETTINGS_URL
} from "../config.js"

const apiBaseUrl = API_URL;

async function fetchProxmoxSettings() {
    return internal_get(apiBaseUrl + PX_SETTINGS_URL);
}

async function fetchNotificationSettings() {
    return internal_get(apiBaseUrl + NOTIFICATIONS_SETTINGS_URL);
}

async function fetchStartupSettings() {
    return internal_get(apiBaseUrl + STARTUPS_SETTINGS_URL);
}

async function saveProxmoxSettings(data) {
    return internal_post(apiBaseUrl + PX_SETTINGS_URL, data);
}

async function saveNotificationSettings(data) {
    return internal_post(apiBaseUrl + NOTIFICATIONS_SETTINGS_URL, data);
}

async function saveStartupSettings(data) {
    return internal_post(apiBaseUrl + STARTUPS_SETTINGS_URL, data);
}

async function testConnection(host, token, token_value, extra_settings) {
    try {
        let response = await fetch(apiBaseUrl + PX_VALIDATE_CONNECTION_URL, {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({
                host: host,
                token_name: token,
                token_value: token_value,
                extra_settings: extra_settings,
            })
        });
        if (response.ok) {
            return await response.json();
        }
    } catch (err) {
        console.log(err);
    }

}

async function reloadConfig() {
    try {
        let response = await fetch(apiBaseUrl + CONFIG_URL);
        if (response.ok) {
            return true;
        }
        return false;
    } catch (err) {
        console.log(err);
    }
}

async function fetchAllVirtualMachines() {
    try {
        let response = await fetch(apiBaseUrl + PX_GET_VMS_URL);
        if (response.ok) {
            return await response.json();
        }
    } catch (err) {
        console.log(err);
    }
}

async function internal_get(url, log_to_console = false) {

    let response = await fetch(url);
    if (response.status === 204) {
        return null;
    }
    if (response.ok && response.status === 200) {
        let dt = await response.json();

        if (log_to_console) {
            console.log(dt);
        }

        return dt;
    }
}

async function internal_post(url, data) {
    let response = await fetch(url, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify(data),
    });
    if (!response.ok) {
        throw new Error(`HTTP error! Status: ${response.status}`);
    }
    return response.status;
}

export {
    fetchProxmoxSettings,
    fetchNotificationSettings,
    fetchStartupSettings,
    saveProxmoxSettings,
    saveNotificationSettings,
    saveStartupSettings,
    testConnection,
    reloadConfig,
    fetchAllVirtualMachines
}