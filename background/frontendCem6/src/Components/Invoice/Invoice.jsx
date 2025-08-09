import { useState } from "react"
import { fetchInvoice } from "../../../fetchHelpers"

function Invoice () {

    const [deviceId, setDeviceId] = useState("")

    function handleDeviceId (event) {
        event.preventDefault()
        setDeviceId(event.target.value)
    }

    async function handleInvoicePrint (event) {
        event.preventDefault()
        const invoice = await fetchInvoice(deviceId)
        console.log("Invoice: ", invoice)
        invoice.message == "Not data from last month" ? alert("Not lectures from last month") : alert("Invoice created")
    }

    return (
        <section className="checkEnergy_main_container">
            <h2>Imprimir factura eléctrica de mes anterior</h2>
            <section>
                <form onSubmit={handleInvoicePrint}>
                    <section>
                        <label htmlFor="deviceId">ID del medidor</label>
                        <input value={deviceId} type="number" name="deviceId" required   placeholder="Número del medidor" onChange={handleDeviceId}/>
                    </section>
                    {/* <section>
                        <label htmlFor="startDate">Fecha inicial</label>
                        <input type="text" name="startDate"   placeholder="AAAA-MM-DD"/>
                    </section>
                    <section>
                        <label htmlFor="endDate">Fecha final</label>
                        <input type="text" name="endDate"  placeholder="AAAA-MM-DD"/>
                    </section> */}
                    <button type="submit">Imprimir</button>
                </form>
            </section>
        </section>
    )
}

export default Invoice;