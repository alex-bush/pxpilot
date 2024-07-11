import {Table} from "antd";

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