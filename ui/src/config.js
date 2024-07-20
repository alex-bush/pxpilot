export const API_URL = import.meta.env.VITE_API_BASE_URL

export const api_prefix = "/api"

export const PX_SETTINGS_URL = api_prefix + "/config/px"
export const NOTIFICATIONS_SETTINGS_URL = api_prefix + "/config/notifications"
export const STARTUPS_SETTINGS_URL = api_prefix + "/config/startups"

export const PX_VALIDATE_CONNECTION_URL = api_prefix + "/proxmox/px-validate"
export const PX_GET_VMS_URL = api_prefix + "/proxmox/get_vms"

export const CONFIG_URL = api_prefix + "/config"
export const STATUS_URL = api_prefix + "/status/state"

export const LOGIN_URL = api_prefix + "/login"
export const LOGOUT_URL = api_prefix + "/logout"
export const REGISTER_URL = api_prefix + "/register"