async function fetchElecParam (device_id) {
    try {
        const response = await fetch(`http://127.0.0.1:8000/read/${device_id}?start_add=0&end_add=9`, {
            method: "GET",
            mode: "cors",
            headers: { "Content-Type": "application/json"},
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.detail || "Failed to fetch data");
        }
        const result = await response.json();
        console.log("Fetched data: ", result);
        return result.data || [];

    } catch (error) {
        console.error("Error fetching electric parameters: ", error);
        return []
    }
}

export default fetchElecParam;