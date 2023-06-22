import "./index.scss"
import { useState } from "react"
import { useParams, useNavigate } from "react-router-dom"
import Cookies from "js-cookie"
const Index = ({ fList, mParam, endpoint, title, btnTitle, method }) => {
    const params = useParams();
    const navigate = useNavigate()
    const token = Cookies.get('token', { path: '/' })
    const [fieldList, setFieldList] = useState(fList || [])
    const [modelParam, setModelParam] = useState(mParam)

    const handleChange = e => {
        const splitText = e.target.name.split("-")
        if (splitText.length === 1) {
            let value = e.target.value;
            if (splitText[0] === "name") value = value.trim()
            setModelParam(prevParam => {
                return { ...prevParam, [e.target.name]: value }
            })
        }
        else {
            const targetName = splitText[0]
            const index = parseInt(splitText[1])
            let targetValues = null
            const getTbl_param = modelParam.tbl_params.find((entry) => {
                if (entry.index == index) return entry
            })
            if (targetName === "constraints") {
                targetValues = []
                for (const v of e.target.selectedOptions) targetValues.push(v.value)
            } else {
                targetValues = e.target.value;
            }
            let mapValues;
            if (getTbl_param) {
                mapValues = modelParam.tbl_params.map(entry => {
                    if (entry.index === index) {
                        return { ...entry, [targetName]: targetValues }
                    }
                    return entry
                })
            } else {
                mapValues = [...modelParam.tbl_params, { index: index, [targetName]: targetValues, datatype: "string" }]
            }
            setModelParam((prev) => {
                return { ...prev, tbl_params: mapValues }
            })

        }
    }
    const handleSubmit = async e => {
        e.preventDefault()
        if (!modelParam.name) return;
        const res = await fetch(`http://192.168.0.105:5900/api/v1/my_api/${params.apiId}/${endpoint}`, {
            method: method,
            headers: {
                "Content-Type": "application/json",
                "x-access-token": token
            },
            body: JSON.stringify(modelParam)
        })
        const data = await res.json()
        // console.log(data)
        if (res.status == 200) {
            navigate(`/my_apis/${params.apiId}/model/${data.name}`)
        } else navigate(`/my_apis/${params.apiId}`)

    }
    return (
        <div className="model-create__wrapper">
            <h2>{title}</h2>
            <section className="model-create__form">
                <form action="" onSubmit={handleSubmit}>
                    <section className="model-form_main">
                        <div>
                            <label htmlFor="name" >Model Name</label>
                            <input type="text" name="name" value={modelParam.name} id="name" onChange={handleChange} />
                            <small>Name must be a valid identifier &nbsp;
                                <a href="https://www.askpython.com/python/python-identifiers-rules-best-practices" target="_blank" rel="noreferrer">more</a>
                            </small>
                        </div>
                        <div>
                            <label htmlFor="desc">Description</label>
                            <textarea name="description" id="desc" value={modelParam.description} onChange={handleChange}></textarea>
                        </div>
                    </section>
                    <section className="model-form_fields">
                        <div className="model-form_fields_wrapper">
                            {fieldList.map((field, index) => {
                                const currentTbl_params = modelParam.tbl_params.find((tblP) => tblP.index === field)
                                return (
                                    <section key={field}>
                                        <h5>Field {index}</h5>
                                        <div>
                                            <label htmlFor={`field-name-${field}`}>Field Name</label>
                                            <input type="text" name={`name-${field}`} value={currentTbl_params?.name || ""} id={`field-name-${field}`} onChange={handleChange} required />
                                        </div>
                                        <div>
                                            <label htmlFor={`field-length-${field}`}>Max Length</label>
                                            <input type="number" id={`field-length-${field}`} name={`dt_length-${field}`} value={currentTbl_params?.dt_length || ""} onChange={handleChange} />

                                        </div>
                                        <div>
                                            <label htmlFor={`field-datatype-${field}`}>Field Data Type</label>
                                            <select name={`datatype-${field}`} id={`field-datatype-${field}`} value={currentTbl_params?.datatype || "string"} onChange={handleChange}>
                                                <option value="string">String</option>
                                                <option value="text">Text</option>
                                                <option value="integer">Integer</option>
                                                <option value="boolean">Boolean</option>
                                                <option value="date">Date</option>
                                                <option value="datetime">Datetime</option>
                                            </select>
                                        </div>
                                        <div>
                                            <label htmlFor={`field-constraints-${field}`}>Field Constraints</label>
                                            <select name={`constraints-${field}`} id={`field-constraints-${field}`} onChange={handleChange} multiple>
                                                <option value="primary_key" selected={currentTbl_params?.constraints?.includes("primary_key") ? true : false}>Primary Key</option>
                                                <option value="foreign_key" selected={currentTbl_params?.constraints?.includes("foreign_key") ? true : false}>Foreign Key</option>
                                                <option value="unique" selected={currentTbl_params?.constraints?.includes("unique") ? true : false}>Unique</option>
                                                <option value="nullable" selected={currentTbl_params?.constraints?.includes("nullable") ? true : false}>Nullable</option>
                                            </select>
                                        </div>
                                        <div>
                                            {/*  */}
                                            <label htmlFor={`field-fk-ref-${field}`}>Foreign Key Reference Table</label>
                                            <input type="text" id={`field-fk-ref-${field}`} name={`foreign_key_rf-${field}`} placeholder="api.table" value={currentTbl_params?.foreign_key_rf || ""} onChange={handleChange} />

                                        </div>
                                        <button type="button" style={{ float: "right" }} onClick={() => {
                                            setFieldList((prev) => prev.filter(v => v != field));
                                            setModelParam(prevModelP => ({ ...prevModelP, tbl_params: prevModelP.tbl_params.filter((entry) => entry.index != field) }))
                                        }}>Remove</button>
                                    </section>
                                )
                            })}
                        </div>
                        <button type="button" onClick={() => {
                            let nextIndex = null
                            if (fieldList.length == 0)
                                nextIndex = 1
                            else {
                                const lastIndex = fieldList[fieldList.length - 1]
                                nextIndex = lastIndex + 1
                            }
                            setFieldList((prev) => ([...prev, nextIndex]))

                        }}>Add Field</button>
                    </section>
                    <button className="model-submit_btn">{btnTitle}</button>
                </form>
            </section>

        </div>
    )
}

export default Index
