const baseEndPoint = "http://127.0.0.1:8000";

export async function fetchElecParam (device_id) {
    try {
        const response = await fetch(`${baseEndPoint}/read/${device_id}`, {
            method: "GET",
            mode: "cors",
            headers: { "Content-Type": "application/json"},
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.detail || "Failed to fetch electric parameters");
        }
        const result = await response.json();
        console.log("Fetched electric parameters: ", result);
        return result;

    } catch (error) {
        console.error("Error fetching electric parameters: ", error);
        return []
    }
}

export async function fetchEnergy (device_id) {
    try {
        const response = await fetch(`${baseEndPoint}/energy_consumption/${device_id}`, {
            method: "GET",
            mode: "cors",
            headers: {"Content-Type": "application/json"}
        });
        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.detail || "Fail to fetch energy")
        }
        const result = await response.json();
        console.log("Fetch Energy: ", result);
        return result;
    } catch (error) {
        console.log("Error fetching energy: ", error);
        return []
    }
}
