import Header from '../../components/Header';
import Footer from '../../components/Footer';
import "./index.scss"
import desktop_logo from "../../assets/logo_desktop.svg"
import { Link, useNavigate } from 'react-router-dom';
import { useState } from 'react';

const index = () => {
    const navigate = useNavigate();
    const [credentials, setCredentials] = useState({ email: "", password: "", confirm_password: "" })
    const [status, setStatus] = useState({ type: "", message: "" })
    const handleChange = (e) => {
        if (status.type.length)
            setStatus({ type: "", message: "" });
        setCredentials(prevCred => ({ ...prevCred, [e.target.name]: e.target.value.trims() }));
    }
    const handleSubmit = async (e) => {
        e.preventDefault()
        setStatus({ type: "", message: "" });
        if (!credentials.password && !credentials.email)
            return;
        if (credentials.password !== credentials.confirm_password) {
            setStatus({ type: "error", message: "Passwords must match" });
            return;
        }

        const req = await fetch('http://192.168.0.105:5900/api/v1/signup', {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                "email": credentials.email,
                "password": credentials.password,
                "confirm_password": credentials.confirm_password
            })
        })
        // console.log(req, req.statusText)
        const data = await req.json();
        console.log(data, req.status)
        if (req.status === 401)
            setStatus({ type: "error", message: data.error })
        else if (req.status === 202)
            setStatus({ type: "redirect", message: data.message })
        else if (req.status === 201) {
            setStatus({ type: "success", message: data.message })
            setTimeout(() => {
                navigate('/login')
            }, 3000)
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
            <Header navs={navs} activeNav="SIGN UP" />

            <section className='register-section'>
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
                            <div>
                                <label htmlFor="confirmpassword">Confirm Password</label>
                                <input name="confirm_password" type="password" onChange={handleChange} placeholder='*************' id="confirmpassword" />
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


                            <button type="submit">REGISTER</button>
                        </form>
                        <Link to="/login">Already have an account?</Link>
                    </section>
                </div>
            </section>
            <Footer />
        </div>
    )
}

export default index
