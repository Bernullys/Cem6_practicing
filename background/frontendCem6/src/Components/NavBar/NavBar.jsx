import { NavLink } from "react-router-dom"


function NavBar () {
    return (
        <header>
            <nav>
                <ul>
                    <li>
                        <NavLink to="/login">Entrar</NavLink>
                    </li>
                    <li>
                        <NavLink to="/register">Registrarse</NavLink>
                    </li>
                </ul>
            </nav>

        </header>
    )
}

export default NavBar