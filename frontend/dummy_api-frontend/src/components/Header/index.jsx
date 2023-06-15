import './index.scss'
import desktop_logo from "../../assets/icon_lite_desktop.svg"
import { Link } from "react-router-dom"
const index = () => {
    return (
        <header>
            <div>
                <img src={desktop_logo} alt="" />
                <ul>
                    <li>
                        <Link to='/login'>LOGIN</Link>
                    </li>
                    <li>
                        <Link to='/register'>SIGN UP</Link>
                    </li>
                    <li>
                        <a href="https://github.com/shady-cj/dummy_api_builder/tree/main" target="_blank" rel="noreferrer">DOCS</a>
                    </li>
                </ul>
            </div>
        </header>
    )
}

export default index
