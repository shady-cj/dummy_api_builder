import "./index.scss"
import desktop_logo from "../../assets/logo_desktop.svg"

const index = () => {
    return (
        <section className="hero_section">
            <div>
                <img src={desktop_logo} alt="dummy api Builder" />
                <a>Get Started</a>
            </div>
        </section>
    )
}

export default index