import {Button, Card, Empty, Flex, Typography} from "antd";
import {useEffect, useState} from "react";
import AddButton from "../controls/AddButton.jsx";
import VmStartupOptionsModal from "./VmStartupOptionsModal.jsx";
import Spinner from "../controls/Spinner.jsx";
import {closestCenter, DndContext, KeyboardSensor, PointerSensor, useSensor, useSensors,} from '@dnd-kit/core';
import {arrayMove, SortableContext, sortableKeyboardCoordinates, verticalListSortingStrategy,} from '@dnd-kit/sortable';
import {SortableItem} from "./SortableItem.jsx";
import {STARTUPS_SETTINGS_URL} from "../../config.js";
import useLoadData from "../../hooks/useLoadData.js";
import CheckboxField from "../controls/CheckboxField.jsx";
import LabeledTextField from "../controls/LabeledTextField.jsx";
import StartupSettings from "./StartupSettings.jsx";


export default function VmsStartupSettings() {
    const TITLE = "VM startup settings";

    const [localData, setLocalData] = useState(null)

    const [isModalOpen, setIsModalOpen] = useState(false);
    const [currentItem, setCurrentItem] = useState(null);

    const {
        data,
        isLoading,
        setIsLoading,
        isSaving,
        saveData,
        notificationHolder
    } = useLoadData(
        STARTUPS_SETTINGS_URL,
        null,
        TITLE,
        (data) => { return data === null ? [] : data }
    );

    useEffect(() => {
        if (data) {
            setLocalData(data);
            setIsLoading(false);
        }
    }, [data, setIsLoading]);

    const sensors = useSensors(useSensor(PointerSensor, {
        activationConstraint: {
            distance: 5,
        }
    }), useSensor(KeyboardSensor, {
        coordinateGetter: sortableKeyboardCoordinates,
    }));

    function handleDragEnd(event) {
        const {active, over} = event;

        if (active.id !== over.id) {
            setLocalData((items) => {
                const oldIndex = items.findIndex(item => item.vm_id === active.id);
                const newIndex = items.findIndex(item => item.vm_id === over.id);

                return arrayMove(items, oldIndex, newIndex);
            });
        }
    }

    function remove(key) {
        setLocalData([...localData.filter(item => item.vm_id !== key)]);
    }

    function handleItemRowClick(item) {
        setCurrentItem(item);
        setIsModalOpen(true);
    }

    const isDataUnchanged = () => {
        return JSON.stringify(data) === JSON.stringify(localData);
    }

    function handleModalOkClick(key, item) {
        try {
            if (key) {
                setLocalData(localData.map(x => x.vm_id === key ? item : x));
            } else {
                setLocalData([...localData, item])
            }
        } finally {
            setIsModalOpen(false);
        }
    }

    async function handleSaveClick() {
        await saveData(localData);
    }

    return (<>
            {notificationHolder}
            {localData && <VmStartupOptionsModal isModalOpen={isModalOpen}
                                                 inputData={currentItem}
                                                 usedKeys={localData.map(i => i.vm_id)}
                                                 onOk={handleModalOkClick}
                                                 onCancel={() => setIsModalOpen(false)}/>}
        <div className='mb-2'>
            <StartupSettings/>
        </div>
        <div>
        <Card
            title="Virtual machines startup settings">
            {!isLoading ? (<div style={{textAlign: 'left', whiteSpace: 'nowrap'}}>
            <Typography>List of virtual machines in the order they will be started.</Typography>
                        <Typography>The order can be rearranged by dragging and dropping the items.</Typography>

                        {localData && <div className="pt-4">
                            <DndContext
                                sensors={sensors}
                                collisionDetection={closestCenter}
                                onDragEnd={handleDragEnd}
                            >
                                <SortableContext
                                    items={localData.map(item => item.vm_id)}
                                    strategy={verticalListSortingStrategy}
                                >
                                    {localData.map((item) => (<div key={item.vm_id}>
                                        <SortableItem key={item.vm_id}
                                                      id={item.vm_id}
                                                      item={item}
                                                      handleItemRowClick={handleItemRowClick}
                                                      remove={remove}/>
                                    </div>))}
                                </SortableContext>
                            </DndContext>
                            {localData.length === 0 && <div>
                                <Empty image={Empty.PRESENTED_IMAGE_SIMPLE} description={
                                    <div>
                                        <Typography.Text strong>
                                            Your VM List is Empty
                                        </Typography.Text><br/>
                                        <Typography.Text italic>
                                            Start by adding virtual machines to configure their startup order and dependencies.
                                        </Typography.Text>
                                    </div>
                                }
                                ></Empty>
                            </div>}
                            <Flex justify="space-between" className="pt-4">
                                <AddButton onClick={() => {
                                    setCurrentItem(null);
                                    setIsModalOpen(true)
                                }}/>
                                <Button type="primary" loading={isSaving} disabled={isDataUnchanged()}
                                        onClick={handleSaveClick}>Save settings</Button>
                            </Flex>
                        </div>}

                    </div>) : <Spinner/>}
            </Card>
        </div>
        </>)
}