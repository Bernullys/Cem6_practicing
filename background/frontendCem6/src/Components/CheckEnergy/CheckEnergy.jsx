import { useState } from "react";
import { fetchEnergy } from "../../../fetchHelpers";

function CheckEnergy () {


    // I have to create a function which comsume my end point which brings me the value of the energy diference.

    // I have to create an async function which execute the values of the form.
    const [data, setData] = useState("")

    async function handleEnergy (e) {
        e.preventDefault()
        const response = await fetchEnergy(deviceId)
        setData(response)
    }
    console.log(data["Energy consumed last month"])

    // I have to create a function that get the value of the deviceID and alse the dates.
    const [deviceId, setDeviceId] = useState("");
    const [startDate, setStartDate] = useState("");
    const [endDate, setEndDate] = useState("");

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
        <section>
            <h2>Consultar consumo de energía eléctrica del mes anterior</h2>
            <section>
                <form onSubmit={handleEnergy}>
                    <section>
                        <label htmlFor="deviceId">ID del medidor</label>
                        <input type="number" name="deviceId" required value={deviceId} onChange={handleDeviceId}/>
                    </section>
                    <button type="submit">Buscar</button>
                    <section>
                        <p>Energía {data["Energy consumed last month"]} [kWh]</p>
                    </section>
                </form>
            </section>
            <h2>Consultar consumo de energía eléctrica entre fechas</h2>
            <section>
                <form onSubmit={handleEnergy}>
                    <section>
                        <label htmlFor="deviceId">ID del medidor</label>
                        <input type="number" name="deviceId" required value={deviceId} onChange={handleDeviceId}/>
                    </section>
                    <section>
                        <label htmlFor="startDate">Fecha inicial</label>
                        <input type="text" name="startDate" value={startDate} onChange={handleStartDate}/>
                    </section>
                    <section>
                        <label htmlFor="endDate">Fecha final</label>
                        <input type="text" name="endDate" value={endDate} onChange={handleEndDate}/>
                    </section>
                    <button type="submit">Buscar</button>
                </form>
            </section>
        </section>
    )
}

export default CheckEnergy