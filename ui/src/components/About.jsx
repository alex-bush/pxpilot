import { Modal, Typography } from "antd";
import { GithubOutlined, LinkedinOutlined, CoffeeOutlined } from '@ant-design/icons';

const { Title, Paragraph } = Typography;

export default function About({
                                  version, isModalOpen, onClose, settings
                              }) {

    return (
        <>
            <Modal title="About" width='700px' open={isModalOpen} centered onOk={onClose} onCancel={onClose}>
                <Typography>
                    <Title level={4}>General Information</Title>
                    <Paragraph>
                        <strong>Name:</strong> PxPilot<br />
                        <strong>Version:</strong> {version}<br />
                        <strong>Description:</strong> An application for managing Proxmox virtual machines, considering their dependencies and sending notifications via Telegram.
                    </Paragraph>
                    <Title level={4}>Author</Title>
                    <Paragraph>
                        <strong>Author:</strong> Alexander Bush<br />
                        <strong>Contact:</strong> ghostkaa@gmail.com<br />
                        <strong></strong> <a href="https://github.com/alex-bush" target="_blank" rel="noopener noreferrer"><GithubOutlined /> https://github.com/alex-bush</a><br />
                        <strong></strong> <a href="https://www.linkedin.com/in/bush-alex/" target="_blank" rel="noopener noreferrer"><LinkedinOutlined /> Alexander Bush</a>
                    </Paragraph>
                    {settings.showVersionHistory && <>
                        <Title level={4}>Version History</Title>
                        <Paragraph>
                            <strong>1.0.0:</strong> Initial release
                        </Paragraph>
                    </>}
                    <Title level={4}>Acknowledgements</Title>
                    <Paragraph>
                        Thanks to everyone who supported the project development.
                    </Paragraph>
                    {(settings.supportPlatforms.buymeacoffee || settings.supportPlatforms.paypal || settings.supportPlatforms.patreon || settings.supportPlatforms.github) && (<>
                        <Title level={4}>Support</Title>
                        <Paragraph>
                            If you find this project useful, please consider supporting its development:
                            <br />
                            {settings.supportPlatforms.buymeacoffee && (<>
                                <a href="https://www.buymeacoffee.com/alexbush" target="_blank" rel="noopener noreferrer">
                                    <CoffeeOutlined  /> Buy me a coffee
                                </a>
                                <br />
                            </>)}
                            {settings.supportPlatforms.patreon && (<>
                                <a href="https://www.patreon.com/ghostkaa" target="_blank" rel="noopener noreferrer">
                                     Support on Patreon
                                </a>
                                <br />
                            </>)}
                            {settings.supportPlatforms.paypal && (<>
                                <a href="https://www.paypal.me/ghostkaa" target="_blank" rel="noopener noreferrer">
                                     Donate via PayPal
                                </a>
                                <br />
                            </>)}
                            {settings.supportPlatforms.github && (<>
                                <a href="https://github.com/sponsors/alex-bush" target="_blank" rel="noopener noreferrer">
                                    <GithubOutlined /> GitHub Sponsors
                                </a>
                                <br />
                            </>)}
                        </Paragraph>
                    </>)}
                    {settings.showUsefulLinks && <>
                        <Title level={4}>Useful Links</Title>
                        <Paragraph>
                            <strong>Documentation:</strong> <a href="https://example.com/docs" target="_blank" rel="noopener noreferrer">https://example.com/docs</a><br />
                            <strong>GitHub Repository:</strong> <a href="https://github.com/ghostkaa/pxpilot" target="_blank" rel="noopener noreferrer">https://github.com/ghostkaa/pxpilot</a><br />
                            <strong>Support Page:</strong> <a href="https://example.com/support" target="_blank" rel="noopener noreferrer">https://example.com/support</a>
                        </Paragraph>
                    </>}
                    <Title level={4}>License</Title>
                    <Paragraph>
                        <strong>Type:</strong> MIT<br />
                        <strong>Terms:</strong> Free to use and modify the code while retaining the original copyright.
                    </Paragraph>
                </Typography>
            </Modal>
        </>
    );
}
