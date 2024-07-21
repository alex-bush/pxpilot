import { useSortable } from '@dnd-kit/sortable';
import { CSS } from '@dnd-kit/utilities';
import StartItemRow from "./StartItemRow.jsx";

export function SortableItem({ id, item, handleItemRowClick, remove }) {
    const {
        attributes,
        listeners,
        setNodeRef,
        transform,
        transition,
        isDragging,
    } = useSortable({ id });

    const style = {
        transform: CSS.Transform.toString(transform),
        transition,
        zIndex: isDragging ? 1000 : 'auto',
        position: isDragging ? 'relative' : 'static',
    };

    return (
        <div ref={setNodeRef} style={style} {...attributes} {...listeners}>
            <StartItemRow
                key={item.vm_id}
                item={item}
                onClick={() => handleItemRowClick(item)}
                onRemove={remove}
            />
        </div>
    );
}
