import {Button, Card, Form, Input} from "antd";

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
    const [form] = Form.useForm();

    const onFinish = (values) => {
        console.log('Received values of form: ', values);
    };

    return (
        <div className="flex justify-center items-center min-h-screen">
            <div className="shadow-md rounded-2xl flex flex-row w-full max-w-4xl">
                <div className="w-1/2 p-8">
                    <h2 className="text-xl font-bold mb-4">Proxmox Pilot</h2>
                    <p className="text-sm m-2">
                        To use the application, registration is required. Although this may seem like a formality, it is essential for protecting the app from accidental use and ensuring access to all its features.
                    </p>
                    <p className="text-sm m-2">
                        So go ahead, create an account and join in! The process takes less time than making a cup of coffee.
                    </p>
                    {/*<p className="text-sm m-2">*/}
                    {/*    For security reasons, the password will not be saved in a recoverable form. Therefore, it will not be possible to restore the password if it is forgotten. Please ensure that the password is kept securely.*/}
                    {/*</p>*/}
                </div>
                <div className="w-1/2 p-8 mt-4">
                    <Form
                        {...formItemLayout}
                        form={form}
                        name="register"
                        onFinish={onFinish}
                        scrollToFirstError
                    >
                        <Form.Item
                            label="Username"
                            name="username"
                            rules={[
                                {required: true, message: 'Please input your username!'},
                            ]}
                        >
                            <Input size={"large"} />
                        </Form.Item>

                        <Form.Item
                            name="password"
                            label="Password"
                            rules={[
                                {required: true, message: 'Please input your password!'},
                            ]}
                            hasFeedback
                        >
                            <Input.Password size={"large"} />
                        </Form.Item>

                        <Form.Item
                            name="confirm"
                            label="Confirm Password"
                            dependencies={['password']}
                            hasFeedback
                            rules={[
                                {required: true, message: 'Please confirm your password!'},
                                ({getFieldValue}) => ({
                                    validator(_, value) {
                                        if (!value || getFieldValue('password') === value) {
                                            return Promise.resolve();
                                        }
                                        return Promise.reject(new Error('The passwords do not match!'));
                                    },
                                }),
                            ]}
                        >
                            <Input.Password size={"large"} />
                        </Form.Item>

                        <Form.Item {...tailFormItemLayout}>
                            <Button type="primary" htmlType="submit">
                                Register
                            </Button>
                        </Form.Item>
                    </Form>
                </div>
            </div>
        </div>)
}