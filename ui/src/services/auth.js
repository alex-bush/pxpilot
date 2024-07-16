import {API_URL, LOGIN_URL, REGISTER_URL} from "../config.js";

async function login(username, password){
    return await inner_fetch(API_URL + LOGIN_URL, JSON.stringify({
        username: username,
        password: password,
    }));
}

async function register(username, password) {
    return await inner_fetch(API_URL + REGISTER_URL, JSON.stringify({
        username: username,
        password: password,
    }));
}

async function inner_fetch(url, data) {
    try {
        let response = await fetch(url, {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: data
        });
        if (response.ok) {
            console.log(response);
            return await response.json();
        }
    } catch (err) {
        console.log(err);
    }
}
export {login, register}