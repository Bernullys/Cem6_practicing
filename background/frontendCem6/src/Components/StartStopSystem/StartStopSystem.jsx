import { useState } from "react";
import { startSystem } from "../../../fetchHelpers";


function StartStopSystem () {

    const [systemState, setSystemState] = useState("Apagado");

    const handleStartSystem = async (action) => {
        const response = await startSystem(action)
        console.log("handle StartSystem response", response)
        if (response.ok) {
            setSystemState(action === "start" ? "Encendido" : "Apagado")
        } else {
            console.log("System start or stop action failed: ", response.error)
        }
    }

    return (
        <section className="startStopSystem_main_container">
            <h1>Sistema de Gestión de Energía</h1>
            <section>
                <button onClick= {() => handleStartSystem("start")}>Encender</button>
                <button onClick={() => handleStartSystem("stop")}>Apagar</button>
            </section>
            <section>
                <h2>Estado del sistema</h2>
                <p>El sistema está {systemState}</p>
            </section>
        </section>

    )
}

export default StartStopSystem