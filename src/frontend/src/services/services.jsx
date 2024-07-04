const apiBaseUrl = "http://127.0.0.1:8000/api";

async function fetchProxmoxSettings() {
    return internal_get(apiBaseUrl + "/config/px");
}

async function fetchNotificationSettings() {
    return internal_get(apiBaseUrl + "/config/notifications");
}

async function fetchStartupSettings() {
    return internal_get(apiBaseUrl + "/config/startups");
}

async function saveProxmoxSettings(data) {
    return internal_post(apiBaseUrl + "/config/px", data);
}

async function saveNotificationSettings(data) {
    return internal_post(apiBaseUrl + "/config/notifications", data);
}

async function testConnection(host, token, token_value){
    try {
        let response = await fetch(apiBaseUrl + '/status/px-validate', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({
                host: host,
                token_name: token,
                token_value: token_value,
            })
        });
        if (response.ok) {
            return await response.json();
        }
    }
    catch(err) {
        console.log(err);
    }

}

async function internal_get(url, log_to_console = false) {

    let response = await fetch(url);
    let dt = await response.json();

    if (log_to_console) {
        console.log(dt);
    }

    return dt;
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
    testConnection
}