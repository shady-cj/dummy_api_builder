import Cookies from "js-cookie"
import { Navigate } from "react-router-dom"
const RedirectPage = (props) => {
    const token = Cookies.get('token', { path: '/' })
    if (token) return <Navigate to="/my_apis" replace={true} />
    return (
        <>
            {props.children}
        </>
    )
}

export default RedirectPage
