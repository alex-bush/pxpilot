import {Badge, Table, Tag} from "antd";

export default function DependenciesSelector({dataTable, selectedRowKeys, onSelectChange}) {
    const columns = [
        {
            title: 'VM Id',
            dataIndex: 'vmid',
        },
        {
            title: 'Name',
            dataIndex: 'name',
        },
        {
            title: 'Status',
            dataIndex: 'status',
            //render: () => <Tag color="success">{}</Tag>
        }
    ];

    const rowSelection = {
        selectedRowKeys,
        onChange: onSelectChange,
    };

    return (
        <>
            <Table
                rowSelection={rowSelection}
                columns={columns}
                dataSource={dataTable}/>
        </>
    )
}