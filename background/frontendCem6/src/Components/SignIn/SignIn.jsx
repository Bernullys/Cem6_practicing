import { useState } from "react"
import { logUsers } from "../../../fetchHelpers"

function SignIn () {

    const [formData, setFormData] = useState({
        username: "",
        password: ""
    })

    const handleInputChange = (e) => {
        setFormData({
            ...formData,
            [e.target.name]: e.target.value
        })
    }

    const handleSubmit = async (e) => {
        e.preventDefault()
        try {
            const response = await logUsers(formData)
        
            setFormData({
                username: "",
                password: ""
            })
        } catch (error) {
            console.log("Catched error loging user")
        }
    }

    return (
        <section>
            <h1>Entrar</h1>
            <form onSubmit={handleSubmit} className="signin_form">
                <section>
                    <label htmlFor="username">Usuario</label>
                    <input required value={formData.username} onChange={handleInputChange} name="username" type="text" />
                </section>
                <section>
                    <label htmlFor="password">Contraseña</label>
                    <input required value={formData.password} onChange={handleInputChange} name="password" type="password" />
                </section>
                <button type="submit">Entrar</button>
            </form>
        </section>       
    )
}

export default SignIn