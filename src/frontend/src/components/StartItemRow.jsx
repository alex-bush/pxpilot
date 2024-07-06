import DeleteButton from "./buttons/DeleteButton.jsx";

export default function StartItemRow({item, onClick, onRemove}) {
    return (<>
            <div id={item.vm_id} className="w-full mb-3 cursor-pointer" onClick={onClick}>
                <div
                    className="flex justify-between items-center w-full p-4 border border-gray-300 shadow-md sm:rounded-2xl">
                    <div className="flex flex-col w-full">
                        <div className="flex items-center">
                            <span className="mr-0.5">id: </span>
                            <span className="font-bold">{item.vm_id}</span>
                            {item.name &&  <span className="font-bold">: {item.name}</span>}
                        </div>
                        <div className="flex justify-between items-center w-full mt-1">
                            <span className="flex-1">{item.description}</span>
                            {item.healthcheck && (
                                <span className="flex-0 ml-auto text-gray-400 text-center w-7/12">
                                Healthcheck: {item.healthcheck?.check_method || 'none'}: {item.healthcheck?.target_url || 'N/A'}
                            </span>
                            )}
                        </div>
                    </div>
                    <div className="ml-4">
                        <DeleteButton size={'small'} onDelete={(e) => {
                            e.stopPropagation(); onRemove(item.vm_id)
                        }}/>
                    </div>
                </div>
            </div>

        </>)
}