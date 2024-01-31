import "./index.scss"
import Header from "../../components/Header"
import Sidebar from "../../components/Sidebar"
import { Outlet, Navigate, useLocation, useParams } from "react-router-dom"
import Cookies from "js-cookie"
import { useEffect, useContext } from "react"
import { AppContext } from "../../context"

const Index = () => {
    const { fetchApis, user, fetchUser, apis, invalidate, setInvalidate } = useContext(AppContext)
    const token = Cookies.get('token', { path: '/' });
    const location = useLocation();
    const locationPathname = location.pathname.split('/')
    const params = useParams();
    const my_api_page = ["/my_apis/", "/my_apis"].includes(location.pathname)
    if (!token) {
        return <Navigate to="/login" state={{ path: location.pathname }} replace={true} />
    }
    let activeNav = "MY APIS"
    let createApiPage = false
    if (locationPathname[2] === "create") {
        activeNav = "CREATE NEW API";
        createApiPage = true
    }


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

    useEffect(() => {
        if (!user) fetchUser();
        if (invalidate || !apis) {
            fetchApis();
            setInvalidate(false)
        }
    }, [invalidate])
    return (
        <div>
            <Header navs={navs} activeNav={activeNav} type="apis" />
            <section className="my_api_body">
                <Sidebar createApiPage={createApiPage} activeID={params?.apiId} my_api_page={my_api_page} />
                <div className={`api_info_body ${my_api_page && "hide_on_smalldevice"}`}>
                    <Outlet />
                </div>
            </section>
        </div>
    )
}

export default Index
