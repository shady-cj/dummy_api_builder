import "./index.scss";
import Sidebar from "../../components/Sidebar";
import Header from "../../components/Header";
import FormCreatePage from "../../components/FormCreateApi";

const index = () => {
    const navs = [
        {
            title: "MY APIS",
            path: '/my_apis'
        },
        {
            title: "CREATE NEW API",
            path: '/my_apis/create'
        }
    ]
    return (
        <div>
            <Header navs={navs} activeNav="CREATE NEW API" />
            <section className="my_api_body">
                <Sidebar />
                <FormCreatePage />
            </section>
        </div>
    )
}

export default index
