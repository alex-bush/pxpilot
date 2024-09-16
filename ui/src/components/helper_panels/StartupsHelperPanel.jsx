import {Card} from "antd";
import {InfoCircleOutlined} from "@ant-design/icons";
import {Link} from "react-router-dom";

export default function StartupsHelperPanel() {
    return <Card className="text-gray-500 pt-5 pb-10">
        <InfoCircleOutlined style={{color: "green", fontSize: "25px"}} className="pb-5"/>
        <h3><strong>Virtual Machines Startup Settings</strong></h3>
        <br/>
        <p>
            Configure the startup settings for virtual machines. Arrange the order in which the virtual machines will be
            started by dragging and dropping the items. This ensures that virtual machines start in the desired
            sequence, providing better control over the infrastructure.
        </p>
        <br/>
        <p>
            New virtual machines can be added to the startup list or existing ones removed. Make sure to save the
            settings after making any changes.
        </p>
        <br/>
        <p>
            Click on a virtual machine entry to edit its startup dependencies and health checks. The icons next to each
            virtual machine provide additional status information.
        </p>
        <br/>
        <p>
            For a better experience, it is recommended to <strong>first configure the <Link to='/startups/proxmox_settings' style={{ color: "#1890ff", fontWeight: "bold", textDecoration: "underline" }}>connection settings</Link> to Proxmox</strong> in order to
            ensure seamless management of your virtual machines.
        </p>
    </Card>;
}