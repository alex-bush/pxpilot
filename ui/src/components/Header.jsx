import { Typography } from 'antd';
const { Title } = Typography;

export default function Header({appVersion}) {
    return (
        <>
            <div className="flex pl-4 bg-gray-900">
                <Title style={{ color: 'white' }} level={2}>PxPilot {appVersion}</Title>
            </div>
        </>
    )
}