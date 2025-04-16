const baseEndPoint = "http://127.0.0.1:8000";

// Utility function to handle errors:
function extractErrorMessage(errorData) {
    if (Array.isArray(errorData.detail)) {
        return errorData.detail.map(error => error.input).join(" | ")
    } else if (typeof errorData.detail === "string") {
        return errorData.detail
    } else {
        return "Unknown error occurred"
    }
}

// Funtion to add users:
export async function fetchUsers (formData) {
    try {
        const response = await fetch(`${baseEndPoint}/add_user/`, {
            method: "POST",
            headers: { "Content-Type": "application/json"},
            body: JSON.stringify(formData)
        })
        if (!response.ok) {
            const errorData = await response.json()
            throw new Error(extractErrorMessage(errorData))
        }
        const data = await response.json()
        console.log("User added successfully: ", data)
        alert("User added successfully")
    } catch (error) {
        console.error("Error adding user: ", error.message)
        alert("Error adding user: " + error.message)
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

// Function to fetch energy by device Id and optional time range:
export async function fetchEnergy (device_id, start_time, end_time) {
    try {
        const response = await fetch(`${baseEndPoint}/energy_consumption/${device_id}/?start_time=${start_time}&end_time=${end_time}`, {
            method: "GET",
            mode: "cors",
            headers: {"Content-Type": "application/json"}
        });
        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(extractErrorMessage(errorData))
        }
        const result = await response.json();
        console.log("Fetch Energy: ", result);
        return result;
    } catch (error) {
        console.log("Error fetching energy: ", error.message);
        alert("Error fetching energy: " + error.message)
        return []
    }
}

// Function to print invoice by device Id:
export async function fetchInvoice (device_id) {
    try {
        const response = await fetch(`${baseEndPoint}/invoice/${device_id}`, {
            method: "GET",
            mode: "cors",
            headers: {"Content-Type": "application/json"}
        });
        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(extractErrorMessage(errorData))
        }
        const result = await response.json()
        console.log("Fetch Invoice: ", result);
        return result;
    } catch (error) {
        console.log("Error fetching invoice: ", error.message);
        alert("Error fetching invoice: " + error.message)
        return []
    }
}