import "./index.scss";
import { useState, useContext } from "react";
import { AppContext } from "../../context";
import { useNavigate } from "react-router-dom";
import Cookies from "js-cookie";

const Index = ({ title, nameValue, descValue, buttonTitle, endpoint, method }) => {
    const { setInvalidate } = useContext(AppContext)
    const token = Cookies.get('token', { path: '/' })
    const [apiData, setApiData] = useState({ name: nameValue, description: descValue })
    const navigate = useNavigate()
    const handleChange = (e) => {
        let value = e.target.value
        if (e.target.name === "name") value = value.trim()
        setApiData(prevData => ({ ...prevData, [e.target.name]: value }))
    }
    const handleSubmit = async e => {
        e.preventDefault()
        if (!apiData.name) return;
        const res = await fetch(`http://192.168.0.105:5900/api/v1/${endpoint}`, {
            method: method,
            headers: {
                "Content-Type": "application/json",
                "x-access-token": token
            },
            body: JSON.stringify(apiData)
        })
        const data = await res.json()
        setInvalidate(true)
        navigate(`/my_apis/${data.id}`)
    }
    return (
        <div className="create-wrapper">
            <section className="create_header">
                <h2>{title}</h2>
            </section>
            <section className="create_form">
                <form action="." onSubmit={handleSubmit}>
                    <div>
                        <label htmlFor="name">Name</label>
                        <input type="text" id="name" name="name" onChange={handleChange} value={apiData.name} />
                    </div>
                    <div>
                        <label htmlFor="desc">Description</label>
                        <textarea name="description" id="desc" onChange={handleChange} value={apiData.description}></textarea>
                    </div>
                    <button>{buttonTitle}</button>
                </form>
            </section>
        </div>
    )
}

export default Index