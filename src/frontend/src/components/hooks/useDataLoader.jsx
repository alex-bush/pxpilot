import {useEffect, useState} from "react";

export default function useDataLoader(fetchDataFunc) {
    const [data, setData] = useState(null);
    const [isLoading, setIsLoading] = useState(true);

    useEffect(() => {
        const loadData = async () => {
            setData(fetchDataFunc());
        }

        loadData();
    })
}