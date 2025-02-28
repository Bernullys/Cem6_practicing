import { useState } from "react";
import CardElecParam from "../CardElecParam/CardElecParam";
import fetchElecParam from "./fetchElectricParam";


function CheckElecParam () {
    
    const [device_id, setDeviceId] = useState("");
    const [data, setData] = useState([]);

    const handleData = async(e) => {
        e.preventDefault();

        
        const fetchedData = await fetchElecParam(device_id);
        console.log(fetchedData);
        setData(fetchedData);

    }

    return (
        <section>
            <h1>Consultar parametros electricos</h1>
            <section>
                <h2>Parametros electricos</h2>
            </section>
            <section>
                <form onSubmit={handleData}>
                    <section>
                        <label htmlFor="device_id">ID del medidor</label>
                        <input onChange={(e) => setDeviceId(e.target.value)} value={device_id} type="number" name="device_id" id="device_id" />
                    </section>
                    <section>
                        <button type="submit" >Buscar</button>
                    </section>
                </form>
            </section>
            <section>
                <h3>Parametros</h3>
                {
                    data.map((electricParameters, index) => (
                        <CardElecParam 
                            key={index}
                            sensor_id={electricParameters.sensor_id}
                            date_time={electricParameters.date_time}
                            voltage={electricParameters.voltage}
                            current={electricParameters.current}
                            frecuency={electricParameters.frecuency}
                            active_power={electricParameters.active_power}
                            reactive_power={electricParameters.reactive_power}
                            apparent_power={electricParameters.apparent_power}
                            power_factor={electricParameters.power_factor}
                            energy_active={electricParameters.energy_active}
                        />
                    ))
                }
            </section>
        </section>
    )
}

export default CheckElecParam