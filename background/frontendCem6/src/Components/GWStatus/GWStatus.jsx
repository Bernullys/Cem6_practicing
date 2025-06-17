import { useState } from "react"

function GWStatus () {

    const [gateWayStatus, setGateWayStatus] = useState({})

    const gwSocket = new WebSocket("http://127.0.0.1:8000/ws/status/")

    gwSocket.onmessage = (event) => {
        const statuses = JSON.parse(event.data)
        console.log("Device statuses: ", statuses)
        setGateWayStatus(statuses)
    }

    gwSocket.onclose = () => {
        console.log("Gateways websocket disconnected")
    }

    return (
        <section>
            <h1>Estado de las pasarelas</h1>
            <ul>
                {Object.entries(gateWayStatus).map(([gtId, gtStatus]) => (
                    <li key={gtId}>
                        Gateway {gtId}: {" "}
                        <span style={{color: gtStatus === "connected" ? "green": "red "}}>
                            {gtStatus}
                        </span>
                    </li>
                ))}
            </ul>
        </section>
    )
}

export default GWStatus