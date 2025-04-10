import { useState } from "react";
import { fetchEnergy } from "../../../fetchHelpers";

function CheckEnergy () {

    // I have to create a function which comsume my end point which brings me the value of the energy diference.

    // I have to create an async function which execute the values of the form.
    const [data, setData] = useState("")

    async function handleEnergy (e) {
        e.preventDefault()
        const response = await fetchEnergy(deviceId, startDate, endDate)
        setData(response)
    }
    console.log(data["energy"])

    // I have to create a function that get the value of the deviceID and alse the dates.
    const [deviceId, setDeviceId] = useState("");
    const [startDate, setStartDate] = useState("");
    const [endDate, setEndDate] = useState("");

    //console.log(`start date: ${startDate}`, `end date: ${endDate}`)

    const handleDeviceId = (e) => {
        e.preventDefault()
        setDeviceId(e.target.value)
    }

    const handleStartDate = (e) => {
        e.preventDefault()
        setStartDate(e.target.value)
    }

    const handleEndDate = (e) => {
        e.preventDefault()
        setEndDate(e.target.value)
    }

    return (
        <section className="checkEnergy_main_container">
            <h2>Consultar consumo de energía eléctrica del mes anterior o entre fechas seleccionadas</h2>
            <section>
                <form onSubmit={handleEnergy}>
                    <section>
                        <label htmlFor="deviceId">ID del medidor</label>
                        <input type="number" name="deviceId" required value={deviceId} onChange={handleDeviceId} placeholder="Número del medidor"/>
                    </section>
                    <section>
                        <label htmlFor="startDate">Fecha y Hora inicial</label>
                        <input type="text" name="startDate" value={startDate} onChange={handleStartDate} placeholder="AAAA-MM-DD hh:mm:ss"/>
                    </section>
                    <section>
                        <label htmlFor="endDate">Fecha y Hora final</label>
                        <input type="text" name="endDate" value={endDate} onChange={handleEndDate} placeholder="AAAA-MM-DD hh:mm:ss"/>
                    </section>
                    <button type="submit">Buscar</button>
                </form>
                <p>Energía: {data["energy"]}</p>
                <p>Fecha inicial: {data["from"]}</p>
                <p>Fecha final: {data["to"]}</p>
            </section>
        </section>
    )
}

export default CheckEnergy