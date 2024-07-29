import {Button, Card, Empty, Flex, notification, Typography} from "antd";
import {useCallback, useEffect, useState} from "react";
import AddButton from "../controls/AddButton.jsx";
import VmStartupOptionsModal from "./VmStartupOptionsModal.jsx";
import Spinner from "../controls/Spinner.jsx";
import {closestCenter, DndContext, KeyboardSensor, PointerSensor, useSensor, useSensors,} from '@dnd-kit/core';
import {arrayMove, SortableContext, sortableKeyboardCoordinates, verticalListSortingStrategy,} from '@dnd-kit/sortable';
import {SortableItem} from "./SortableItem.jsx";
import useAuthFetch from "../../hooks/useAuthFetch.js";
import {STARTUPS_SETTINGS_URL} from "../../config.js";
import {data} from "autoprefixer";


export default function StartupSettings() {
    const TITLE = "VM startup settings";

    const [Data, setData] = useState([{}])
    const [OriginalData, setOriginalData] = useState({})
    const [isLoaded, setIsLoaded] = useState(false);

    const [isModalOpen, setIsModalOpen] = useState(false);
    const [currentItem, setCurrentItem] = useState(null);
    const [loading, setLoading] = useState(false);
    const [notificationInstance, notificationHolder] = notification.useNotification();

    const {authGet, authPost} = useAuthFetch();

    const loadData = useCallback(async () => {
        let data = await authGet(STARTUPS_SETTINGS_URL);
        if (data === null) {
            data = [];
        }
        setOriginalData(data);

        setIsLoaded(true);
        setData(data);
    }, [authGet])

    useEffect(() => {
        loadData();
    }, [loadData])

    const sensors = useSensors(
        useSensor(PointerSensor, {
        activationConstraint: {
            distance: 5,
        }}),
        useSensor(KeyboardSensor, {
            coordinateGetter: sortableKeyboardCoordinates,
        })
    );

    function handleDragEnd(event) {
        const {active, over} = event;

        if (active.id !== over.id) {
            setData((items) => {
                const oldIndex = items.findIndex(item => item.vm_id === active.id);
                const newIndex = items.findIndex(item => item.vm_id === over.id);

                return arrayMove(items, oldIndex, newIndex);
            });
        }
    }

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
                setData(Data.map(x => x.vm_id === key ? item : x));
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
            await authPost(STARTUPS_SETTINGS_URL, data);
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
                                   inputData={currentItem}
                                   usedKeys={Data.map(i => i.vm_id)}
                                   onOk={handleModalOkClick}
                                   onCancel={() => setIsModalOpen(false)}/>

            <Card
                title="Virtual machines startup settings">
                {isLoaded ? (
                    <div style={{textAlign: 'left', whiteSpace: 'nowrap'}}>
                        <Typography>List of virtual machines in the order they will be started.</Typography>
                        <Typography>The order can be rearranged by dragging and dropping the items.</Typography>

                        <div className="pt-4">
                            <DndContext
                                sensors={sensors}
                                collisionDetection={closestCenter}
                                onDragEnd={handleDragEnd}
                            >
                                <SortableContext
                                    items={Data.map(item => item.vm_id)}
                                    strategy={verticalListSortingStrategy}
                                >
                                    {Data.map((item) => (
                                        <div key={item.vm_id}>
                                            <SortableItem key={item.vm_id}
                                                          id={item.vm_id}
                                                          item={item}
                                                          handleItemRowClick={handleItemRowClick}
                                                          remove={remove} />
                                        </div>))}
                                </SortableContext>
                            </DndContext>
                            {Data.length === 0 &&
                                <div>
                                    <Empty image={Empty.PRESENTED_IMAGE_SIMPLE}/>
                                </div>
                            }
                            <Flex justify="space-between" className="pt-4">
                                <AddButton onClick={() => {
                                    setCurrentItem(null);
                                    setIsModalOpen(true)
                                }}/>
                                <Button type="primary" loading={loading} disabled={isDataUnchanged()}
                                        onClick={handleSaveClick}>Save settings</Button>
                            </Flex>
                        </div>

                    </div>
                ) : <Spinner/>
                }
            </Card>
        </>
    )
}