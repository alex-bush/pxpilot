import {Card} from "antd";
import {InfoCircleOutlined} from "@ant-design/icons";

export default function NotificationsHelperPanel() {
    return <Card className="text-gray-500 pt-5 pb-10">
        <InfoCircleOutlined style={{color: "green", fontSize: "25px"}} className="pb-5"/>
        <h3><strong>Notification Settings</strong></h3>
        <br/>
        <p>
            Configure the notification settings for the startup of virtual machines using Telegram and Email. These
            settings enable the system to send status updates about the virtual machines.
        </p>
        <br/>
        <p>
            <strong>Telegram:</strong> To enable Telegram notifications, provide the bot token and chat ID. This allows
            the system to send messages directly through Telegram when there are updates on the virtual machines.
        </p>
        <br/>
        <p>
            <strong>Email:</strong> To enable Email notifications, configure the SMTP server details, such as server
            address, port, username, and password. This allows the system to send emails regarding the status and
            updates of the virtual machines.
        </p>
        <br/>
        <p>
            Save the settings after configuring the notification options to ensure timely updates and the ability to
            take necessary actions based on the received information.
        </p>
    </Card>
}