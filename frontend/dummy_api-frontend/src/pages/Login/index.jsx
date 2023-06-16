import Header from '../../components/Header';
import Footer from '../../components/Footer';
import "./index.scss"
import desktop_logo from "../../assets/logo_desktop.svg"
import { Link } from 'react-router-dom';
import { useState } from 'react';


function index() {
    const [credentials, setCredentials] = useState({ email: "", password: "" })


    const handleChange = (e) => {
        setCredentials(prevCred => ({ ...prevCred, [e.target.name]: e.target.value }));
    }
    const handleSubmit = e => {
        e.preventDefault()
        console.log(credentials)
    }
    const navs = [
        {
            title: "LOGIN",
            path: '/login'
        },
        {
            title: "SIGN UP",
            path: '/register'
        }
    ]

    return (
        <div>
            <Header navs={navs} activeNav="LOGIN" />

            <section className='login-section'>
                <div className='auth-section-wrapper'>
                    <img src={desktop_logo} alt="" />
                    <section>
                        <form onSubmit={handleSubmit}>
                            <div>
                                <label htmlFor="email">Email</label>
                                <input name="email" type="email" onChange={handleChange} placeholder='email@email.com' id="email" />
                            </div>
                            <div>
                                <label htmlFor="password">Password</label>
                                <input name="password" type="password" onChange={handleChange} placeholder='*************' id="password" />
                            </div>
                            <button type="submit">Login</button>
                        </form>
                        <Link to="/register">Create a new account</Link>
                    </section>
                </div>
            </section>
            <Footer />
        </div>
    )
}

export default index
