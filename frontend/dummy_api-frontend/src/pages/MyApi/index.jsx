import "./index.scss"
import Header from "../../components/Header"
import Sidebar from "../../components/Sidebar"
import { Outlet, useLocation } from "react-router-dom"

const index = () => {
    const navs = [
        {
            title: "MY APIS",
            path: '/my_apis'
        },
        {
            title: "CREATE NEW API",
            path: '/my_apis/create'
        }
    ]
    let activeNav = "MY APIS"
    const location = useLocation();
    const locationPathname = location.pathname.split('/')
    if (locationPathname[2] === "create")
        activeNav = "CREATE NEW API";

    return (
        <div>
            <Header navs={navs} activeNav={activeNav} />
            <section className="my_api_body">
                <Sidebar />
                <Outlet />
            </section>
        </div>
    )
}

export default index
