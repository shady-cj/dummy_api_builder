import "./index.scss"

const index = () => {
    return (
        <div className="modelPage-wrapper">
            <section className="modelPage_header">
                <h2>Model 1</h2>
                <p>Lorem ipsum dolor sit amet consectetur adipisicing elit. Libero magni rem numquam dolor minima soluta, cupiditate, excepturi molestias reiciendis corporis laborum quibusdam alias hic accusantium obcaecati non consequatur sapiente vero!</p>
            </section>

            <section className="modelPage_body">
                <table>
                    <thead>
                        <tr>
                            <th>
                                Fields
                            </th>
                            <th>
                                Field Type
                            </th>
                            <th>
                                Field Length
                            </th>
                            <th>
                                Field Constraints
                            </th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td>_id</td>
                            <td>Integer</td>
                            <td>Null</td>
                            <td>
                                primary_key
                            </td>
                        </tr>
                        <tr>
                            <td>email</td>
                            <td>Integer</td>
                            <td>30</td>
                            <td>
                                unique, nullable,
                            </td>
                        </tr>
                        <tr>
                            <td>First Name</td>
                            <td>String</td>
                            <td>
                                60
                            </td>
                            <td>Null</td>
                        </tr>
                        <tr>
                            <td>Last Name</td>
                            <td>String</td>
                            <td>
                                60
                            </td>
                            <td>Null</td>
                        </tr>
                        <tr>
                            <td>Last Name</td>
                            <td>String</td>
                            <td>
                                60
                            </td>
                            <td>Null</td>
                        </tr>
                        <tr>
                            <td>Last Name</td>
                            <td>String</td>
                            <td>
                                60
                            </td>
                            <td>Null</td>
                        </tr>
                    </tbody>
                </table>
            </section>
            <section className="modelPage_btns">
                <button>Add Field</button>
                <button>Edit Field</button>
            </section>
        </div>
    )
}

export default index
