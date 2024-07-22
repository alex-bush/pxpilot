import {Modal} from "antd";

export default function About({isModalOpen, onClose}) {
    return (
        <>
            <Modal title="About" open={isModalOpen} centered onOk={onClose}  onCancel={onClose}>
                <span>About PxPilot</span>
            </Modal>
        </>
    )
}