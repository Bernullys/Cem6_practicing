import { useState } from "react";
import CardElecParam from "../CardElecParam/CardElecParam";
import { fetchElecParam } from "../../../fetchHelpers";


function CheckElecParam () {
    
    const [device_id, setDeviceId] = useState("");
    const [data, setData] = useState({});

    const handleData = async(e) => {
        e.preventDefault();
        const fetchedData = await fetchElecParam(device_id);
        console.log(fetchedData, "electric parameters");
        setData(fetchedData);
    }

    return (
        <section className="checkElecParam_main_container">
            <h2>Consultar parámetros eléctricos actuales (instantaneos)</h2>
            <section>
                <form onSubmit={handleData}>
                    <section>
                        <label htmlFor="device_id">ID del medidor</label>
                        <input onChange={(e) => setDeviceId(e.target.value)} value={device_id} type="number" name="device_id" id="device_id" required />
                    </section>
                    <section>
                        <button type="submit" >Buscar</button>
                    </section>
                </form>
            </section>
            <section>
                {
                    <CardElecParam 
                        sensor_id={data.sensor_id}
                        datetime={data.datetime}
                        voltage={data.voltage}
                        current={data.current}
                        frecuency={data.frequency}
                        active_power={data.active_power}
                        reactive_power={data.reactive_power}
                        apparent_power={data.aparent_power}
                        power_factor={data.power_factor}
                        energy_active={data.active_energy}
                    />
                }
            </section>
        </section>
    )
}

export default CheckElecParam