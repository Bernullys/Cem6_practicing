import { useNavigate } from "react-router-dom"

function LogoutButton () {
    const navigate = useNavigate()
    const handleLogout = () => {
        localStorage.removeItem("access_token")
        navigate("/")
    }
    return (
        <button onClick={handleLogout}>Salir</button>
    )
}

export default LogoutButton