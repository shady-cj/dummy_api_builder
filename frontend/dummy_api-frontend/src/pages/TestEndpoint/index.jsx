import "./index.scss"
import { useState } from "react"
// import { hostUrl } from "../../variables";

const Index = () => {
    const [endpointParam, setEndpointParam] = useState({ "url": "", "method": "GET", "data": "" });
    const [response, setResponse] = useState(null)

    const handleChange = (e) => {
        setEndpointParam(prev => ({ ...prev, [e.target.name]: e.target.value.trim() }))
    }

    const handleSubmit = async (e) => {
        e.preventDefault()
        setResponse(null)
        if (!endpointParam.url) {
            return;
        }
        if (["POST", "PUT"].includes(endpointParam.method)) {
            if (!endpointParam.data) return;
            try {
                const data = eval(endpointParam.data)
                const resp = await fetch(endpointParam.url, {
                    method: endpointParam.method,
                    headers: {
                        "Content-Type": "application/json"
                    },
                    body: JSON.stringify({
                        "entries": data
                    })
                })
                const resp_data = await resp.json()
                setResponse(resp_data)
            } catch (err) {
                return;
            }


        }
        else {
            const resp = await fetch(endpointParam.url, {
                method: endpointParam.method
            })
            if (resp.status == 204) {
                setResponse({ "message": "Deleted Successfully" })
                return;
            }
            const resp_data = await resp.json()

            setResponse(resp_data)
        }


    }
    return (
        <div className="test_endpoint-wrapper">
            <h2>Test Your API</h2>
            <section className="endpoint_info">
                <p>
                    Copy your api id from you user profile at the top right corner. (in the dropdown click on the &lsquo;copy&rsquo;  button next to &lsquo;Api id&rsquo;)
                </p>
                <small>Note: Do not share this id. refer to the <a href="https://github.com/shady-cj/dummy_api_builder/blob/main/README.md" target="_blank" rel="noreferrer">docs</a> for more info</small>
            </section>
            <section className="endpoint_form">
                <form action="" onSubmit={handleSubmit}>
                    <div>
                        <label htmlFor="url">Endpoint</label>
                        <input type="text" onChange={handleChange} id="url" name="url" value={endpointParam.url} placeholder="dummyapibuilder.com/api/v1/<yourapiId>/my_api/<Api_name>/model/<Model_name>/{model_id}" />
                    </div>
                    <div>
                        <label htmlFor="method">Method</label>
                        <select name="method" id="method" onChange={handleChange} value={endpointParam.method}>
                            <option value="GET">GET</option>
                            <option value="POST">POST</option>
                            <option value="PUT">PUT</option>
                            <option value="DELETE">DELETE</option>
                        </select>
                    </div>
                    <div>
                        <label htmlFor="data">Data</label>
                        <textarea name="data" id="data" onChange={handleChange} value={endpointParam.data}></textarea>
                    </div>
                    <button>Send</button>
                </form>
            </section>
            {
                response && <section className="response_section">
                    <h2>Response</h2>
                    <div className="response_data">
                        {JSON.stringify(response, undefined, 2)}
                    </div>
                </section>
            }

        </div>
    )
}

export default Index
