import "./index.scss"
import desktop_logo from "../../assets/logo_desktop.svg"
import { Link } from "react-router-dom"

const index = () => {
    return (
        <section className="hero_section">
            <div>
                <img src={desktop_logo} alt="dummy api Builder" />
                <Link to='/register'>Get Started</Link>
            </div>
        </section>
    )
}

export default index