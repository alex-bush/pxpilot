import {Button, Checkbox, ConfigProvider, Form, Input, theme} from "antd";
import {LockOutlined, UserOutlined} from "@ant-design/icons";
import {useAuth} from "../contexts/AuthContext.jsx";
import {useNavigate} from "react-router-dom";
import {login} from "../services/auth.js"

export default function Login() {
    const {set_login} = useAuth()
    const [form] = Form.useForm();
    const navigate = useNavigate();

    async function handleLogin(values) {
        if (await login(values.username, values.password)) {
            set_login();
            navigate('/settings');
        }
    }

    return (
        <>
            <div className="flex justify-center items-center min-h-screen">
                <div
                    className="shadow-md shadow-gray-950 flex flex-col w-full max-w-xl rounded-3xl min-h-96 items-center bg-gray-900 p-8">
                    <h2 className="text-2xl font-bold mb-4 text-gray-400">PxPilot</h2>
                    <ConfigProvider theme={{algorithm: theme.darkAlgorithm}}>
                        <Form
                            form={form}
                            name="login"
                            onFinish={handleLogin}
                            className="w-full px-8"
                        >
                            <Form.Item
                                name="username"
                                rules={[{required: true, message: 'Please input your Username!'}]}
                            >
                                <Input
                                    size="large"
                                    prefix={<UserOutlined className="site-form-item-icon"/>}
                                    placeholder="Username"
                                />
                            </Form.Item>
                            <Form.Item
                                name="password"
                                rules={[{required: true, message: 'Please input your Password!'}]}
                            >
                                <Input
                                    size="large"
                                    prefix={<LockOutlined className="site-form-item-icon"/>}
                                    type="password"
                                    placeholder="Password"
                                />
                            </Form.Item>
                            <Form.Item>
                                <Form.Item name="remember" valuePropName="checked" noStyle>
                                    <Checkbox>Remember me</Checkbox>
                                </Form.Item>
                            </Form.Item>
                            <Form.Item>
                                <Button type="primary" htmlType="submit" className="w-full">
                                    Log in
                                </Button>
                            </Form.Item>
                        </Form>
                    </ConfigProvider>
                </div>
            </div>
        </>
    )
}