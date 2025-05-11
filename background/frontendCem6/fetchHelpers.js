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

// Function to start the system:
export async function startSystem (onOff) {
    try {
        const response = await fetch(`${baseEndPoint}/${onOff}/`)
        if (response.ok) {
            alert("El sistema se encendió/apagó correctamente")
        } else {
            const errorData = await response.json()
            throw new Error(extractErrorMessage(errorData))
        }
    } catch (error) {
        console.log("Error al encender/apagar el systema: ", error.message)
        alert("Error al encender/apagar el systema: " + error.message)
    }
}

// Funtion to add users and app users:
export async function fetchUsers (formData, endPoint) {
    try {
        const response = await fetch(`${baseEndPoint}/${endPoint}/`, {
            method: "POST",
            headers: { "Content-Type": "application/json"},
            body: JSON.stringify(formData)
        })
        const data = await response.json()
        if (!response.ok) {
            throw new Error(extractErrorMessage(data))
        }
        console.log("User added successfully: ", data)
        alert(`${endPoint} added successfully`)
    } catch (error) {
        console.error(`Error adding ${endPoint}: `, error.message)
        alert(`Error adding ${endPoint}: ` + error.message)
    }
}

// Function to fetch the device electric parameters:
export async function fetchElecParam (device_id) {
    try {
        const response = await fetch(`${baseEndPoint}/read/${device_id}/`, {
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
        const response = await fetch(`${baseEndPoint}/energy_consumption/${device_id}/?start_time=${start_time}&end_time=${end_time}/`, {
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
        alert("Error fetching energy--: " + error.message)
        return []
    }
}

// Function to print invoice by device Id:
export async function fetchInvoice (device_id) {
    try {
        const response = await fetch(`${baseEndPoint}/invoice/${device_id}/`, {
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