const baseEndPoint = "http://127.0.0.1:8000";

// Utility function to handle errors:
function extractErrorMessage(errorData) {
    if (Array.isArray(errorData.detail)) {
        return errorData.detail.map(error => error.msg).join(" | ")
    } else if (typeof errorData.detail === "string") {
        return errorData.detail
    } else {
        return "Unknown error occurred"
    }
}

// Function to fetch the device electric parameters:
export async function fetchElecParam (device_id) {
    try {
        const response = await fetch(`${baseEndPoint}/read/${device_id}`, {
            method: "GET",
            mode: "cors",
            headers: { "Content-Type": "application/json"},
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(extractErrorMessage(errorData));
        }
        const result = await response.json();
        console.log("Fetched electric parameters: ", result);
        return result;

    } catch (error) {
        console.error("Error fetching electric parameters:", error.message);
        alert("Error fetching electric parameters: " + error.message)
        return []
    }
}

export async function fetchEnergy (device_id, start_time, end_time) {
    try {
        const response = await fetch(`${baseEndPoint}/energy_consumption/${device_id}/?start_time=${start_time}&end_time=${end_time}`, {
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

export async function fetchInvoice (device_id) {
    try {
        const response = await fetch(`${baseEndPoint}/invoice/${device_id}`, {
            method: "GET",
            mode: "cors",
            headers: {"Content-Type": "application/json"}
        });
        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.detail || "Failed to fetch invoice")
        }
        const result = await response.json()
        console.log("Fetch Invoice: ", result);
        return result;
    } catch (error) {
        console.log("Error fetching invoice: ", error);
        return []
    }
}