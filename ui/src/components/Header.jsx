import { Typography } from 'antd';
const { Title } = Typography;

export default function Header({appVersion}) {
    return (
        <>
            <div className="flex pl-4 pt-0">
                <Title level={3}>PxPilot {appVersion}</Title>
            </div>
        </>
    )
}