import Header from '../../components/Header';
import Footer from '../../components/Footer';
import "./index.scss"
import desktop_logo from "../../assets/logo_desktop.svg"
import { Link, useNavigate, useLocation } from 'react-router-dom';
import { useState } from 'react';
import Cookies from 'js-cookie'


function Index() {
    const location = useLocation()
    const navigate = useNavigate()
    const [credentials, setCredentials] = useState({ email: "", password: "" })
    const [status, setStatus] = useState({ type: "", message: "" })

    const handleChange = (e) => {
        if (status.type.length)
            setStatus({ type: "", message: "" });
        setCredentials(prevCred => ({ ...prevCred, [e.target.name]: e.target.value.trim() }));
    }
    const handleSubmit = async e => {
        e.preventDefault()
        setStatus({ type: "", message: "" });
        if (!credentials.password && !credentials.email)
            return;
        const req = await fetch('http://192.168.0.105:5900/api/v1/login', {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                "email": credentials.email,
                "password": credentials.password,
            })
        })
        // console.log(req, req.statusText)
        const data = await req.json();
        if (req.status === 401)
            setStatus({ type: "error", message: data.error })
        else if (req.status === 200) {
            setStatus({ type: "success", message: "Login Succesful" })
            Cookies.set('token', data.token, { path: '/', expires: (1 / 24) })
            setTimeout(() => {
                if (location.state?.path)
                    navigate(location.state.path)
                else
                    navigate('/my_apis')
            }, 2000)
        }
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
                            {
                                status.type && (<div className={`
                                    form-card
                                    ${status.type === "error" ?
                                        "form-error-card" :
                                        status.type === "redirect" ?
                                            "form-redirect-card" :
                                            "form-success-card"}
                                    `
                                }>
                                    {status.message}
                                </div>)
                            }

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

export default Index
