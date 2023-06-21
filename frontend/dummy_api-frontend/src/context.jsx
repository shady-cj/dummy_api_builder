import React from "react"
import Cookies from "js-cookie";

export const AppContext = React.createContext();

const AppProvider = ({ children }) => {
    const [user, setUser] = React.useState(null)
    const [apis, setApis] = React.useState(null)
    const [model, setModel] = React.useState(null)
    const [loading, setLoading] = React.useState(false)
    const [apiLoading, setApiLoading] = React.useState(false)
    const [userLoading, setUserLoading] = React.useState(false)
    const [invalidate, setInvalidate] = React.useState(false)
    const [apiDetail, setApiDetail] = React.useState(null)


    const fetchApiDetail = async (apiId) => {
        const token = Cookies.get('token', { path: '/' })
        setLoading(true)
        const response = await fetch(`http://192.168.0.105:5900/api/v1/my_api/${apiId}`, {
            headers: {
                'x-access-token': token
            }
        });
        const data = await response.json();
        if (response.status === 200) {

            setApiDetail(data)
        }
        setLoading(false)

    }
    const fetchApis = async () => {
        const token = Cookies.get('token', { path: '/' })
        setApiLoading(true)
        const response = await fetch("http://192.168.0.105:5900/api/v1/my_apis", {
            headers: {
                'x-access-token': token
            }
        });
        const data = await response.json();
        if (response.status === 200) setApis(data)
        setApiLoading(false)
    }
    const fetchUser = async () => {
        const token = Cookies.get('token', { path: '/' })
        setUserLoading(true)
        const response = await fetch("http://192.168.0.105:5900/api/v1/me", {
            headers: {
                'x-access-token': token
            }
        });
        const data = await response.json();
        if (response.status === 200) setUser(data)
        setUserLoading(false)
    }
    const fetchModel = async (apiId, modelName) => {
        const token = Cookies.get('token', { path: '/' })
        setLoading(true)
        const response = await fetch(`http://192.168.0.105:5900/api/v1/my_api/${apiId}/show_model/${modelName}`, {
            headers: {
                'x-access-token': token
            }
        });
        const data = await response.json();
        if (response.status === 200) setModel(data)
        setLoading(false)
    }
    return (<AppContext.Provider value={{
        user, fetchUser, apis, fetchApis, model, fetchModel,
        loading, userLoading, invalidate, setInvalidate,
        apiDetail, fetchApiDetail, apiLoading
    }}> {children} </AppContext.Provider>)
}
export default AppProvider;