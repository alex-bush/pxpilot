import {Card} from "antd";
import {InfoCircleOutlined} from "@ant-design/icons";

export default function ProxmoxHelperPanel() {
    return <Card className="text-gray-500 pt-5 pb-10">
        <InfoCircleOutlined style={{color: "green", fontSize: "25px"}} className="pb-5"/>
        <h3><strong>Proxmox Connection Settings</strong></h3>
        <br/>
        <p>
            Configure the connection settings for Proxmox to manage virtual machines. These settings allow the application to connect to the Proxmox server and perform necessary operations.
        </p>
        <br/>
        <p>
            <strong>Host:</strong> Enter the Proxmox server address, including the protocol and port number.
        </p>
        <br/>
        <p>
            <strong>Token name:</strong> Provide the API token name that will be used to authenticate the connection to Proxmox.
        </p>
        <br/>
        <p>
            <strong>Token value:</strong> Enter the API token value corresponding to the provided token name for authentication.
        </p>
        <br/>
        <p>
            <strong>Other settings:</strong> Additional settings such as SSL verification can be configured here. Ensure the necessary parameters are set correctly to establish a secure connection.
        </p>
        <br/>
        <p>
            After configuring the connection settings, use the "Test connection" button to verify that the application can successfully connect to the Proxmox server. Save the settings to apply the changes.
        </p>
    </Card>;
}