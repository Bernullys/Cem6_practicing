function CardElecParam ( { sensor_id, date_time, voltage, current, frecuency, active_power, reactive_power, apparent_power, power_factor, energy_active } ) {
    return (
        <section>
            <section>
                <h1>Parámetros eléctricos</h1>
                <section>
                    <section>
                        <h2>ID del medidor</h2>
                        <p>{sensor_id}</p>
                    </section>
                    <section>
                        <h2>Fecha y hora</h2>
                        <p>{date_time}</p>
                    </section>
                    <section>
                        <h2>Voltaje</h2>
                        <p>{voltage}</p>
                    </section>
                    <section>
                        <h2>Corriente</h2>
                        <p>{current}</p>
                    </section>
                    <section>
                        <h2>Frecuencia</h2>
                        <p>{frecuency}</p>
                    </section>
                    <section>
                        <h2>Potencia activa</h2>
                        <p>{active_power}</p>
                    </section>
                    <section>
                        <h2>Potencia reactiva</h2>
                        <p>{reactive_power}</p>
                    </section>
                    <section>
                        <h2>Potencia aparente</h2>
                        <p>{apparent_power}</p>
                    </section>
                    <section>
                        <h2>Factor de potencia</h2>
                        <p>{power_factor}</p>
                    </section>
                    <section>
                        <h2>Energía activa</h2>
                        <p>{energy_active}</p>
                    </section>
                </section>
            </section>
        </section>
    )
}

export default CardElecParam;