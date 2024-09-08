export const API_URL = import.meta.env.VITE_API_BASE_URL

export const API_VERSION = "/v2"
export const api_prefix = "/api/v2"

export const PX_SETTINGS_URL = api_prefix + "/proxmox/settings"
export const NOTIFICATIONS_SETTINGS_URL = api_prefix + "/config/notifications"
export const STARTUPS_SETTINGS_URL = api_prefix + "/settings/vms1"

export const PX_VALIDATE_CONNECTION_URL = api_prefix + "/proxmox/validate"
export const PX_GET_VMS_URL = api_prefix + "/proxmox/get_vms"

export const RELOAD_CONFIG_URL = api_prefix + "/config/reload"
export const STATUS_URL = api_prefix + "/status/state"

export const LOGIN_URL = api_prefix + "/login"
export const LOGOUT_URL = api_prefix + "/logout"
export const REGISTER_URL = api_prefix + "/register"