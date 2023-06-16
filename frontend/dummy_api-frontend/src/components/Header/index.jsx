import './index.scss'
import desktop_logo from "../../assets/icon_lite_desktop.svg"
import { Link, useNavigate } from "react-router-dom"
const index = ({ navs, activeNav, type }) => {
    const navigate = useNavigate();
    return (
        <header>
            <div>
                <img src={desktop_logo} alt="" onClick={() => navigate('/')} />
                <ul>
                    {navs.map((nav, index) => {

                        return (<li key={index} className={nav.title === activeNav && "nav-active"}>
                            <Link to={nav.path}>{nav.title}</Link>
                        </li>)
                    })}

                    {
                        type === "landing" && <li> <a href='https://github.com/shady-cj/dummy_api_builder/tree/main' target="_blank" rel="noreferrer"> DOCS </a></li>
                    }
                </ul>
            </div>


        </header>
    )
}

export default index
