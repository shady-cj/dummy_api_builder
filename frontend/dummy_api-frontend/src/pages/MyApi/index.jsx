import "./index.scss"
import Header from "../../components/Header"
import Footer from "../../components/Footer"

const index = () => {
    const navs = [
        {
            title: "MY APIS",
            path: '/my_apis'
        },
        {
            title: "CREATE NEW API",
            path: '/create_new_api'
        }
    ]
    return (
        <div>
            <Header navs={navs} activeNav="MY APIS" />
            <section className="my_api_body">

            </section>
            <Footer />
        </div>
    )
}

export default index
