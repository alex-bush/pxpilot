import {Button, Card, Flex, List, Modal, Spin, Typography} from "antd";
import {useEffect, useState} from "react";
import DeleteButton from "./buttons/DeleteButton.jsx";
import AddButton from "./buttons/AddButton.jsx";
import {fetchStartupSettings} from "../services/services.jsx";
import VmStartupOptions from "./VmStartupOptions.jsx";

export default function StartupSettings() {
    const [Data, setData] = useState({isLoading: true})
    const [modal2Open, setModal2Open] = useState(false);

    useEffect(() => {
        fetchStartupSettings().then(res => {
                res.isLoading = false;
                setData(res)
            }
        )
    }, [])

    function add() {
        if (Data.findIndex(x => x.vm_id === 0) > 0) {
            console.log('already exists')
            return
        }
        setData([
                ...Data, {
                    vm_id: 0,
                    name: '',
                    healthcheck: null
                }
            ]
        )
    }

    function remove(key) {
        setData(prevData => prevData.filter(item => item.vm_id !== key));
    }

    return (
        <>
            <Card
                title="Virtual machines startup settings"
                style={{
                    width: "-moz-fit-content",
                }}>
                {Data.isLoading ? <Spin size={"large"}/> : (
                    <div style={{textAlign: 'left', whiteSpace: 'nowrap'}}>
                        <Typography>List of virtual machines in the order in which they will be started</Typography>
                        <List
                            itemLayout="horizontal"
                            dataSource={Data}
                            renderItem={(item, index) => (
                                <List.Item key={index}>
                                    <div style={{display: 'flex', justifyContent: 'space-between', width: '100%'}}>
                                        <div>
                                            <List.Item.Meta
                                                title={item.vm_id + ': ' + item.name}
                                                description={item.description}
                                            />
                                        </div>
                                        <DeleteButton size={'small'} onDelete={() => remove(item.vm_id)}/>
                                    </div>
                                </List.Item>
                            )}>

                        </List>
                        <p/>
                        <Flex justify="space-between">
                            <AddButton onclick={() => setModal2Open(true) }/>
                            <Button type="primary">Save settings</Button>
                        </Flex>

                        <Modal
                            title="Add VM to startup list"
                            centered
                            open={modal2Open}
                            onOk={() => setModal2Open(false)}
                            onCancel={() => setModal2Open(false)}
                        >
                            <VmStartupOptions item={{}}/>
                        </Modal>

                        {/*<Space direction="vertical" size="middle" style={{display: 'flex', gap: '1em'}}>*/}
                        {/*    {Data.map(item =>*/}
                        {/*        <div style={{display: 'flex'}} key={item.vm_id}>*/}
                        {/*            <div style={{*/}
                        {/*                flex: "1 1 100%",*/}
                        {/*            }}>*/}
                        {/*                <VmStartupOptions item={item}/>*/}
                        {/*            </div>*/}
                        {/*            <DeleteButton onDelete={() => remove(item.vm_id)}/>*/}
                        {/*        </div>*/}
                        {/*    )}*/}

                        {/*    <AddButton onclick={add}/>*/}
                        {/*    <Button type="primary">Save</Button>*/}
                        {/*</Space>*/}
                    </div>)
                }
            </Card>
        </>
    )
}