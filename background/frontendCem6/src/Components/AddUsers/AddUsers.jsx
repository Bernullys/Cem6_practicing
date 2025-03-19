import { useState } from "react"

// AddUsers takes from a form an object with the properties of Users
function AddUsers () {
    // formData set the object empty at first and then get the data using setFormData
    const [formData, setFormData] = useState({
        first_name: "",
        last_name: "",
        rut: "",
        phone: "",
        email: "",
        address: "",
        sensor_id: ""
    });
    // handleChange spread the formData and set the value of the input in the key of the object.
    const handleChange = (e) => {
        setFormData({ ...formData, [e.target.name]: e.target.value});
    }
    // handleSubmit makes a post request to the server with the data of the form.
    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            const response = await fetch("http://127.0.0.1:8000/add_user/", {
                method: "POST",
                headers: { "Content-Type": "application/json"},
                body: JSON.stringify(formData)
            });
            const data = await response.json();

            if (response.ok) {
                alert("User added successfully");
                setFormData({ first_name: "", last_name: "", rut: "", phone: "", email: "", address: "", sensor_id: ""});
            } else {
                alert("Response error adding user: " + data.detail);
            }
        } catch (error) {
            alert("Catched error adding user: " + error);
        }
    }

return (
    <section className="addUsers_main_container">
        <section>
            <h2>Agregar usuario</h2>
            <form onSubmit={handleSubmit} className="addUsers_form">
                <section>
                    <label htmlFor="">Nombre(s)</label>
                    <input onChange={handleChange} value={formData.first_name} required placeholder="Nombre"  type="text" name="first_name" id="" />
                </section>
                <section>
                    <label htmlFor="">Apellido(s)</label>
                    <input onChange={handleChange} value={formData.last_name} required placeholder="Apellido"  type="text" name="last_name" id="" />
                </section>
                <section>
                    <label htmlFor="">RUN/RUT</label>
                    <input onChange={handleChange} value={formData.rut} required placeholder="RUT"  type="text" name="rut" id="" />
                </section>
                <section>
                    <label htmlFor="">Telefono</label>
                    <input onChange={handleChange} value={formData.phone} required placeholder="Telefono"  type="text" name="phone" id="" />
                </section>
                <section>
                    <label htmlFor="">Correo</label>
                    <input onChange={handleChange} value={formData.email} required placeholder="Correo"  type="text" name="email" id="" />
                </section>
                <section>
                    <label htmlFor="">Dirección</label>
                    <input onChange={handleChange} value={formData.address} required placeholder="Dirección"  type="text" name="address" id="" />
                </section>
                <section>
                    <label htmlFor="">ID del medidor</label>
                    <input onChange={handleChange} value={formData.sensor_id} required placeholder="ID del medidor"  type="numeric" name="sensor_id" id="" />
                </section>
                <section>
                    <button type="submit">Agregar</button>
                </section>
            </form>
        </section>
    </section>
)
};

export default AddUsers