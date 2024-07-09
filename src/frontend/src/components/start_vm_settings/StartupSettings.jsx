import {Button, Card, Flex, notification, Spin, Typography} from "antd";
import {useCallback, useEffect, useState} from "react";
import AddButton from "../controls/AddButton.jsx";
import {fetchStartupSettings, saveStartupSettings} from "../../services/services.jsx";
import VmStartupOptionsModal from "./VmStartupOptionsModal.jsx";
import StartItemRow from "./StartItemRow.jsx";
import Spinner from "../controls/Spinner.jsx";

export default function StartupSettings() {
    const TITLE = "VM startup settings";

    const [Data, setData] = useState([{}])
    const [OriginalData, setOriginalData] = useState({})
    const [isLoaded, setIsLoaded] = useState(false);

    const [isModalOpen, setIsModalOpen] = useState(false);
    const [currentItem, setCurrentItem] = useState(null);
    const [loading, setLoading] = useState(false);
    const [notificationInstance, notificationHolder] = notification.useNotification();

    const showNotification = (type, title) => {
        if (type === "error") {
            notificationInstance[type]({
                message: 'Error',
                description: 'Error while saving ' + title,
            })
            return;
        }

        notificationInstance[type]({
            message: 'Done!',
            description: title + ' saved successfully',
        })
    }

    const loadData = useCallback(async () => {
        let data = await fetchStartupSettings();
        setOriginalData(data);

        setIsLoaded(true);
        setData(data);
    }, [])

    useEffect(() => {
        loadData();
    }, [loadData])

    function remove(key) {
        let data = Data.filter(item => item.vm_id !== key);
        setData([...data]);
    }

    function handleItemRowClick(item) {
        setCurrentItem(item);
        setIsModalOpen(true);
    }

    const isDataUnchanged = () => {
        return JSON.stringify(Data) === JSON.stringify(OriginalData);
    }

    function handleModalOkClick(key, item) {
        try {
            if (key) {
                setData(Data.map(x => x.vm_id === key? item : x));
            } else {
                setData([...Data, item])
            }
        } finally {
            setIsModalOpen(false);
        }
    }

    async function handleSaveClick() {
        setLoading(true);

        try {
            await saveStartupSettings(Data);
            await loadData();
            showNotification('success', TITLE);
        } catch (err) {
            console.log(err);
            showNotification('error', TITLE);
        } finally {
            setLoading(false);
        }
    }

    return (
        <>
            {notificationHolder}
            <VmStartupOptionsModal isModalOpen={isModalOpen}
                                   item={currentItem}
                                   usedKeys={Data.map(i => i.vm_id)}
                                   onOk={handleModalOkClick}
                                   onCancel={() => setIsModalOpen(false)}/>

            <Card
                title="Virtual machines startup settings">
                {isLoaded ? (
                    <div style={{textAlign: 'left', whiteSpace: 'nowrap'}}>
                        <Typography>List of virtual machines in the order in which they will be started</Typography>
                        {Data.map((item) => (
                            <div key={item.vm_id}>
                                <StartItemRow key={item.vm_id} item={item}
                                              onClick={() => handleItemRowClick(item)}
                                              onRemove={remove}/>
                            </div>))}
                        <p/>
                        <Flex justify="space-between">
                            <AddButton onClick={() => {
                                setCurrentItem(null);
                                setIsModalOpen(true)
                            }}/>
                            <Button type="primary" loading={loading} disabled={isDataUnchanged()} onClick={handleSaveClick}>Save settings</Button>
                        </Flex>
                    </div>) : <Spinner/>
                }
            </Card>
        </>
    )
}