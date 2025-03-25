function Invoice () {
    return (
        <section className="checkEnergy_main_container">
            <h2>Imprimir factura eléctrica</h2>
            <section>
                <form>
                    <section>
                        <label htmlFor="deviceId">ID del medidor</label>
                        <input type="number" name="deviceId" required   placeholder="Número del medidor"/>
                    </section>
                    <section>
                        <label htmlFor="startDate">Fecha inicial</label>
                        <input type="text" name="startDate"   placeholder="AAAA-MM-DD"/>
                    </section>
                    <section>
                        <label htmlFor="endDate">Fecha final</label>
                        <input type="text" name="endDate"  placeholder="AAAA-MM-DD"/>
                    </section>
                    <button type="submit">Imprimir</button>
                </form>
            </section>
        </section>
    )
}

export default Invoice;