import { useEffect, useContext } from 'react'
import FormCreatePage from "../../components/FormCreatePage"
import { useParams } from 'react-router-dom'
import { AppContext } from '../../context'
import { Bars } from 'react-loader-spinner'
const Index = () => {
    const { fetchApiDetail, apiDetail, loading } = useContext(AppContext)
    const params = useParams()
    useEffect(() => {
        fetchApiDetail(params.apiId)
    }, [])
    return (
        <>
            {
                loading ? <div className="loading-wrapper">

                    <Bars
                        height="80"
                        width="80"
                        color="#44859F"
                        ariaLabel="bars-loading"
                        wrapperStyle={{}}
                        wrapperClass="loading_element"
                        visible={true}
                    />
                </div> :
                    <FormCreatePage title="EDIT API" nameValue={apiDetail.name} descValue={apiDetail.description} buttonTitle="EDIT" endpoint={`update_api/${params.apiId}`} method="PUT" />

            }
        </>
    )
}

export default Index
