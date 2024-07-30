import {Button, Checkbox, ConfigProvider, Form, Input, theme} from "antd";
import {ExclamationCircleOutlined, LockOutlined, UserOutlined} from "@ant-design/icons";
import {useAuth} from "../contexts/AuthContext.jsx";
import {useNavigate} from "react-router-dom";
import {get_api_status, login} from "../services/auth.js"
import {useEffect, useState} from "react";

export default function Login() {
    const { set_login } = useAuth()
    const [form] = Form.useForm();
    const navigate = useNavigate();
    const [invalidCredentials, setInvalidCredentials] = useState(false);
    const [isLoading, setIsLoading] = useState(false);

    useEffect(() => {
        async function fetch() {
            const state = await get_api_status();
            if (state.is_first_run) {
                navigate("/register");
            }
        }

        fetch();
    }, [navigate]);

    async function handleLogin(values) {
        setIsLoading(true);
        const response = await login(values.username, values.password);
        if (response && response.access_token) {
            set_login(response.access_token);
            navigate('/settings');
        } else {
            setInvalidCredentials(true);
            setIsLoading(false);
        }
    }

    return (
        <>
            <ConfigProvider theme={{algorithm: theme.darkAlgorithm}}>
                <div className="flex justify-center items-center min-h-screen">
                    <div
                        className="shadow-md shadow-gray-950 flex flex-col w-full max-w-xl rounded-2xl items-center bg-gray-900 p-8">
                        <h2 className="text-2xl font-bold mb-8 text-white">Login to PxPilot</h2>
                        {invalidCredentials && (
                            <div className='text-white flex gap-2 pb-4'>
                                <ExclamationCircleOutlined className='text-red-500'
                                                           style={{color: 'red', fontSize: '1.5rem'}}/>
                                <span>Invalid username or password</span>
                            </div>
                        )}
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
                                <Button type="primary" htmlType="submit" loading={isLoading} className="w-full">
                                    Log in
                                </Button>
                            </Form.Item>
                        </Form>

                    </div>
                </div>
            </ConfigProvider>
        </>
    )
}