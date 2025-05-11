function SignIn () {
    return (
        <section>
            <h1>Entrar</h1>
            <form action="" className="signin_form">
                <section>
                    <label htmlFor="">Usuario</label>
                    <input type="text" />
                </section>
                <section>
                    <label htmlFor="">Contraseña</label>
                    <input type="text" />
                </section>
                <button>Entrar</button>
            </form>
        </section>       
    )
}

export default SignIn