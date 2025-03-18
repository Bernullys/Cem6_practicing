function CardElecParam ( { sensor_id, datetime, voltage, current, frecuency, active_power, reactive_power, apparent_power, power_factor, energy_active } ) {
    return (
        <section>
            <section>
                <section>
                    <section>
                        <h3>ID del medidor:</h3>
                        <p>{sensor_id}</p>
                    </section>
                    <section>
                        <h3>Fecha y hora:</h3>
                        <p>{datetime}</p>
                    </section>
                    <section>
                        <h3>Voltaje:</h3>
                        <p>{voltage}</p>
                    </section>
                    <section>
                        <h3>Corriente:</h3>
                        <p>{current}</p>
                    </section>
                    <section>
                        <h3>Frecuencia:</h3>
                        <p>{frecuency}</p>
                    </section>
                    <section>
                        <h3>Potencia activa:</h3>
                        <p>{active_power}</p>
                    </section>
                    <section>
                        <h3>Potencia reactiva:</h3>
                        <p>{reactive_power}</p>
                    </section>
                    <section>
                        <h3>Potencia aparente:</h3>
                        <p>{apparent_power}</p>
                    </section>
                    <section>
                        <h3>Factor de potencia:</h3>
                        <p>{power_factor}</p>
                    </section>
                    <section>
                        <h3>Energía activa:</h3>
                        <p>{energy_active}</p>
                    </section>
                </section>
            </section>
        </section>
    )
}

export default CardElecParam;