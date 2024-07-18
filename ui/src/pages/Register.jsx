import {Button, ConfigProvider, Form, Input, theme} from "antd";
import {register} from "../services/auth.js"
import {useNavigate} from 'react-router-dom';
import {useAuth} from "../contexts/AuthContext.jsx";
import {LockOutlined, UserOutlined} from "@ant-design/icons";

const formItemLayout = {
    labelCol: {
        xs: {
            span: 24,
        }, sm: {
            span: 8,
        },
    }, wrapperCol: {
        xs: {
            span: 24,
        }, sm: {
            span: 16,
        },
    },
};
const tailFormItemLayout = {
    wrapperCol: {
        xs: {
            span: 24, offset: 0,
        }, sm: {
            span: 16, offset: 8,
        },
    },
};

export default function Register() {
    const {set_login} = useAuth();
    const [form] = Form.useForm();
    const navigate = useNavigate();

    const onFinish = async (values) => {
        console.log('Received values of form: ', values);
        if (await register(values.username, values.password)) {
            set_login();
            navigate('/settings');
        }
    };

    return (<>
        <div className="flex justify-center items-center min-h-screen py-10">
            <div className="shadow-md flex flex-row w-full max-w-4xl min-h-max rounded-3xl bg-gray-900">
                <div className="w-1/2 p-8 text-gray-400 bg-black rounded-l-3xl pb-10 pt-10">
                    <h2 className="text-2xl font-bold mb-8 text-white">PxPilot</h2>
                    <p className="mb-4">
                        To use the application, registration is required. Although this may seem like a formality, it is
                        essential for protecting the app from accidental use and ensuring access to all its features.
                    </p>
                    <p className="">
                        So go ahead, create an account and join in! The process takes less time than making a cup of
                        coffee.
                    </p>
                </div>
                <div className="w-1/2 p-8 text-gray-100 pb-10 pt-10">
                    <h2 className="text-2xl font-bold mb-8">Create your account</h2>
                    <ConfigProvider theme={{ algorithm: theme.darkAlgorithm, }}>
                        <Form
                            form={form}
                            name="register"
                            onFinish={onFinish}
                            scrollToFirstError
                            className="w-full space-y-6"
                        >
                            <Form.Item
                                name="username"
                                rules={[{required: true, message: 'Please input your username'},]}
                            >
                                <Input size={"large"} prefix={<UserOutlined className="site-form-item-icon"/>}
                                       placeholder="Username"/>
                            </Form.Item>

                            <Form.Item
                                name="password"
                                rules={[{required: true, message: 'Please input your password'},]}
                                hasFeedback
                            >
                                <Input.Password size={"large"} prefix={<LockOutlined className="site-form-item-icon"/>}
                                                placeholder="Password"/>
                            </Form.Item>

                            <Form.Item
                                name="confirm"
                                dependencies={['password']}
                                hasFeedback
                                rules={[{
                                    required: true, message: 'Please confirm your password'
                                }, ({getFieldValue}) => ({
                                    validator(_, value) {
                                        if (!value || getFieldValue('password') === value) {
                                            return Promise.resolve();
                                        }
                                        return Promise.reject(new Error('The passwords do not match!'));
                                    },
                                }),]}
                            >
                                <Input.Password size={"large"} prefix={<LockOutlined className="site-form-item-icon"/>}
                                                placeholder="Confirm password"/>
                            </Form.Item>

                            <Form.Item>
                                <Button type="primary" htmlType="submit" className="w-full mt-6">
                                    Register
                                </Button>
                            </Form.Item>
                        </Form>
                    </ConfigProvider>
                </div>
            </div>
        </div>
    </>)
}