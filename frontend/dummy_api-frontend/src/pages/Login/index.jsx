import Header from '../../components/Header';
import Footer from '../../components/Footer';
import "./index.scss"
import desktop_logo from "../../assets/logo_desktop.svg"
import { Link } from 'react-router-dom';


function index() {
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
                <div className='login-section-wrapper'>
                    <img src={desktop_logo} alt="" />
                    <section>
                        <form action="">
                            <div>
                                <label htmlFor="email">Email</label>
                                <input type="email" placeholder='email@email.com' id="email" />
                            </div>
                            <div>
                                <label htmlFor="password">Password</label>
                                <input type="password" placeholder='*************' id="password" />
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
