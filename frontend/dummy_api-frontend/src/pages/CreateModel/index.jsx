import "./index.scss"
import { useState } from "react"
const index = () => {
    const [fieldList, setFieldList] = useState([])
    const [modelParam, setModelParam] = useState({
        name: "",
        description: "",
        tbl_params: []
    })

    const handleChange = e => {
        const splitText = e.target.name.split("-")
        if (splitText.length === 1) {
            setModelParam(prevParam => {
                return { ...prevParam, [e.target.name]: e.target.value }
            })
        }
        else {
            const targetName = splitText[0]
            const index = splitText[1]
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
    const handleSubmit = e => {
        e.preventDefault()
        console.log(modelParam)
    }
    return (
        <div className="model-create__wrapper">
            <h2>Create New Model</h2>
            <section className="model-create__form">
                <form action="" onSubmit={handleSubmit}>
                    <section className="model-form_main">
                        <div>
                            <label htmlFor="name">Model Name</label>
                            <input type="text" name="name" id="name" onChange={handleChange} />
                            <small>Name must be a valid identifier &nbsp;
                                <a href="https://www.askpython.com/python/python-identifiers-rules-best-practices" target="_blank" rel="noreferrer">more</a>
                            </small>
                        </div>
                        <div>
                            <label htmlFor="desc">Description</label>
                            <textarea name="description" id="desc" onChange={handleChange}></textarea>
                        </div>
                    </section>
                    <section className="model-form_fields">
                        <div className="model-form_fields_wrapper">
                            {fieldList.map((field, index) => {
                                return (
                                    <section key={field}>
                                        <h5>Field {index}</h5>
                                        <div>
                                            <label htmlFor={`field-name-${field}`}>Field Name</label>
                                            <input type="text" name={`name-${field}`} id={`field-name-${field}`} onChange={handleChange} required />
                                        </div>
                                        <div>
                                            <label htmlFor={`field-length-${field}`}>Max Length</label>
                                            <input type="number" id={`field-length-${field}`} name={`length-${field}`} onChange={handleChange} />

                                        </div>
                                        <div>
                                            <label htmlFor={`field-datatype-${field}`}>Field Data Type</label>
                                            <select name={`datatype-${field}`} id={`field-datatype-${field}`} defaultValue={"string"} onChange={handleChange}>
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
                                                <option value="primary_key">Primary Key</option>
                                                <option value="foreign_key">Foreign Key</option>
                                                <option value="unique">Unique</option>
                                                <option value="nullable">Nullable</option>
                                            </select>
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
                            console.log(fieldList)
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
                    <button className="model-submit_btn">CREATE</button>
                </form>
            </section>

        </div>
    )
}

export default index
