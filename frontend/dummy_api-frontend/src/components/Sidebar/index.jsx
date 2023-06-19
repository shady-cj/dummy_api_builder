import "./index.scss"
import caretLogo from "../../assets/caret-blue.svg"
import newIcon from "../../assets/create-new-icon.svg"
import { useNavigate } from "react-router-dom"
const index = () => {
    const navigate = useNavigate();

    return (
        <div className="sidebar_wrapper">
            <section className='my_api_header'>
                <h2>MY APIs</h2> <img src={caretLogo} />
            </section>
            <section className='my_api_list'>
                <article className="active" onClick={() => navigate("/my_apis/1")}>
                    API 1
                </article>
                <article onClick={() => navigate("/my_apis/1")}>
                    API 2
                </article>
                <article onClick={() => navigate("/my_apis/1")}>
                    API 3
                </article>
            </section>
            <section className='my_api_create_btn'>
                <div onClick={() => navigate("/my_apis/create")}>
                    <img src={newIcon} alt="" />
                    CREATE
                </div>
            </section>
        </div>
    )
}

export default index
