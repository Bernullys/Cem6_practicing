import { useState } from "react"
import { fetchUsers } from "../../../fetchHelpers"



function Register () {

    const [appUserData, setAppUserData] = useState ({
        full_name: "",
        username: "",
        password: "",
        email: "",
        role: ""
    })

    const handleInputsChange = (e) => {
        setAppUserData({ ...appUserData, [e.target.name]: e.target.value})
    }

    const handleSubmit = async (e) => {
        e.preventDefault()
        try {
            const response = await fetchUsers(appUserData, "register")
            setAppUserData({
                full_name: "",
                username: "",
                password: "",
                email: "",
                role: ""
            })

        } catch (error) {
            console.log("Catched error registering app user")
        }
    }

    return (
        <section>
            <h1>Registro de usuario</h1>
            <form onSubmit={handleSubmit} className="login_form">
                <section>
                    <label htmlFor="full_name">Nombre completo</label>
                    <input required value={appUserData.full_name} name="full_name"  type="text" onChange={handleInputsChange}/>
                </section>
                <section>
                    <label htmlFor="email">Correo</label>
                    <input required value={appUserData.email} name="email"  type="email"onChange={handleInputsChange} />
                </section>
                <section>
                    <label htmlFor="username">Usuario</label>
                    <input required value={appUserData.username} name="username"  type="text" onChange={handleInputsChange}/>
                </section>
                <section>
                    <label htmlFor="password">Contraseña</label>
                    <input required value={appUserData.password} name="password"  type="password" onChange={handleInputsChange} />
                </section>
                <section>
                    <label htmlFor="role">Rol</label>
                    <input required value={appUserData.role} name="role"  type="text" onChange={handleInputsChange}/>
                </section>
                <button type="submit">Registrar</button>
            </form>

        </section>
    )
}

export default Register