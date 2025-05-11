import { useState } from "react";
import { startSystem } from "../../../fetchHelpers";


function StartStopSystem () {

    const [systemState, setSystemState] = useState("Apagado");

    const handleStart = () => {
        setSystemState("Encendido")
    }

    const handleStop = () => {
        setSystemState("Apagado")
    }

    return (
        <section className="startStopSystem_main_container">
            <h1>Sistema de Gestión de Energía</h1>
            <section>
                <button onClick= {()=> {handleStart(); startSystem("start")}}>Encender</button>
                <button onClick={()=> {handleStop(); startSystem("stop")}}>Apagar</button>
            </section>
            <section>
                <h2>Estado del sistema</h2>
                <p>El sistema está {systemState}</p>
            </section>
        </section>

    )
}

export default StartStopSystem