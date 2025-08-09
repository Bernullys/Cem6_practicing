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
    const token = localStorage.getItem("access_token")
    console.log("Token: ", token)
    if (!token) {
        alert("Por favor inicia sesión.")
        return
    }
    try {
        const response = await fetch(`${baseEndPoint}/${onOff}/`, {
            method: "GET",
            headers: { 
                Authorization: `Bearer ${token}`,
                "Content-Type": "application/json"}
        })
        if (response.ok) {
            alert(`El sistema ${onOff}  correctamente`)
            return {ok: true}
        } else {
            const errorData = await response.json()
            throw new Error(extractErrorMessage(errorData))
        }
    } catch (error) {
        console.log(`Error al ${onOff} el systema: `, error.message)
        alert(`Error al ${onOff} el systema: ` + error.message)
        return {ok: false, error: error.message }
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

// Funtion login users:
export async function logUsers (formData) {
    try {
        const urlEncoded = new URLSearchParams()
        urlEncoded.append("username", formData.username)
        urlEncoded.append("password", formData.password)

        const response = await fetch(`${baseEndPoint}/token/`, {
            method: "POST",
            headers: { "Content-Type": "application/x-www-form-urlencoded"},
            body: urlEncoded.toString()
        })
        const data = await response.json()
        if (!response.ok) {
            throw new Error(extractErrorMessage(data))
        }
        const token = data.access_token
        console.log("User loged successfully: ", data, token)
        // Store the token in local storage
        localStorage.setItem("access_token", token)
    } catch (error) {
        console.error(`Error loging`, error.message)
        alert(`Error loging: ` + error.message)
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