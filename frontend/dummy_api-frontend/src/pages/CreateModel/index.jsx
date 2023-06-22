import ModelForm from "../../components/ModelForm"
import { useContext, useEffect } from "react"
import { AppContext } from "../../context"
import { useParams } from "react-router-dom"
import ErrorElement from "../../components/ErrorElement"

const Index = () => {
    const params = useParams()
    const { loading, fetchApiDetail, apiDetail } = useContext(AppContext)
    useEffect(() => {
        if (!apiDetail) fetchApiDetail(params.apiId)
    }, [params.apiId])
    const mParam = {
        name: "",
        description: "",
        tbl_params: []
    }
    return (
        <>
            {
                loading ? "" : !loading && !apiDetail ? <ErrorElement /> : <ModelForm fList={[]} mParam={mParam} title={"CREATE NEW MODEL"} btnTitle="CREATE" method="POST" endpoint="create_model" />

            }
        </>
    )
}

export default Index
