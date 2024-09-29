import {Divider, Modal, Typography} from "antd";
import {GithubOutlined, LinkedinOutlined, CoffeeOutlined, MailFilled} from '@ant-design/icons';

const { Text, Title, Paragraph } = Typography;

export default function About({
                                  version, isModalOpen, onClose, settings
                              }) {

    return (
        <>
            <Modal title="About" width='700px' open={isModalOpen} centered onOk={onClose} onCancel={onClose}>
                <Typography>
                    <Paragraph>
                        <center>
                            <img src="/logo.png" alt="Logo" style={{width: '80px', height: '80px'}}/>
                            <Title>PxPilot</Title>
                            <Text>Version: {version}</Text><br/>
                            <Text>Created by Alexander Bush</Text>
                        </center>
                    </Paragraph>
                    <Divider/>
                    <Title level={4}>Contacts</Title>
                    <Paragraph>
                            <a href="mailto:ghostkaa@gmail.com"><MailFilled/> Send Me an Email</a>
                            <br/>
                        <strong></strong> <a href="https://github.com/alex-bush" target="_blank"
                                             rel="noopener noreferrer"><GithubOutlined/> Check it out on GitHub</a><br/>
                        <strong></strong> <a href="https://www.linkedin.com/in/bush-alex/" target="_blank"
                                             rel="noopener noreferrer"><LinkedinOutlined/> LinkedIn</a>
                    </Paragraph>
                    {settings.showVersionHistory && <>
                        <Title level={4}>Version History</Title>
                        <Paragraph>
                            <strong>1.0.0:</strong> Initial release
                        </Paragraph>
                    </>}
                    <Divider/>
                    {/*<center>*/}
                        {(settings.supportPlatforms.buy_me_a_coffee || settings.supportPlatforms.paypal || settings.supportPlatforms.patreon || settings.supportPlatforms.github) && (<>
                            {/*<Title level={4}>Support me</Title>*/}
                            <Paragraph>
                                If you find this project useful, your support would be greatly appreciated to help me
                                maintain and improve it:
                                <br/>
                                {settings.supportPlatforms.buy_me_a_coffee && (<>
                                    <a href="https://www.buymeacoffee.com/alexbush" target="_blank"
                                       rel="noopener noreferrer">
                                        <CoffeeOutlined/> Buy me a coffee
                                    </a>
                                    <br/>
                                </>)}
                                {settings.supportPlatforms.patreon && (<>
                                    <a href="https://www.patreon.com/ghostkaa" target="_blank"
                                       rel="noopener noreferrer">
                                        Support on Patreon
                                    </a>
                                    <br/>
                                </>)}
                                {settings.supportPlatforms.paypal && (<>
                                    <a href="https://www.paypal.me/ghostkaa" target="_blank" rel="noopener noreferrer">
                                        Donate via PayPal
                                    </a>
                                    <br/>
                                </>)}
                                {settings.supportPlatforms.github && (<>
                                    <a href="https://github.com/sponsors/alex-bush" target="_blank"
                                       rel="noopener noreferrer">
                                        <GithubOutlined/> GitHub Sponsors
                                    </a>
                                    <br/>
                                </>)}
                            </Paragraph>
                        </>)}
                    {/*</center>*/}
                    {settings.showUsefulLinks && <>
                        <Title level={4}>Useful Links</Title>
                        <Paragraph>
                            <strong>Documentation:</strong> <a href="https://example.com/docs" target="_blank"
                                                               rel="noopener noreferrer">https://example.com/docs</a><br/>
                            <strong>GitHub Repository:</strong> <a href="https://github.com/ghostkaa/pxpilot"
                                                                   target="_blank"
                                                                   rel="noopener noreferrer">https://github.com/ghostkaa/pxpilot</a><br/>
                            <strong>Support Page:</strong> <a href="https://example.com/support" target="_blank"
                                                              rel="noopener noreferrer">https://example.com/support</a>
                        </Paragraph>
                    </>}
                    {/*<Title level={4}>License</Title>*/}
                    {/*<Paragraph>*/}
                    {/*    <strong>Type:</strong> MIT<br />*/}
                    {/*    <strong>Terms:</strong> Free to use and modify the code while retaining the original copyright.*/}
                    {/*</Paragraph>*/}
                </Typography>
            </Modal>
        </>
    );
}
