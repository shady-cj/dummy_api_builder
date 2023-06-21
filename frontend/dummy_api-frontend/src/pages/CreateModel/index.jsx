import ModelForm from "../../components/ModelForm"

const index = () => {
    const mParam = {
        name: "",
        description: "",
        tbl_params: []
    }
    return (
        <ModelForm fList={[]} mParam={mParam} title={"CREATE NEW MODEL"} btnTitle="CREATE" method="POST" endpoint="create_model" />
    )
}

export default index
