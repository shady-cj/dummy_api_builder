import "./index.scss"
import caretLogo from "../../assets/caret-blue.svg"
import newIcon from "../../assets/create-new-icon.svg"
import newIconWhite from "../../assets/create-new-icon-white.svg"
import { useNavigate } from "react-router-dom"
import { useContext } from "react"
import { AppContext } from "../../context"
import { Bars } from "react-loader-spinner"

const Index = ({ activeID, createApiPage, my_api_page }) => {
    const navigate = useNavigate();
    const { apis, apiLoading } = useContext(AppContext)


    return (
        <div className={`sidebar_wrapper ${!my_api_page && "hide_on_smalldevice"}`}>
            <section className='my_api_header'>
                <h2>MY APIs</h2> <img src={caretLogo} />
            </section>
            {
                apiLoading ? <section className="loading-sidebar-wrapper">

                    <Bars
                        height="40"
                        width="40"
                        color="#44859F"
                        ariaLabel="bars-loading"
                        wrapperStyle={{}}
                        wrapperClass="loading_element"
                        visible={true}
                    />
                </section> : <section className='my_api_list'>
                    {

                        apis && apis.map((api) => {
                            return <article key={api.id} className={`${api.id === +activeID ? 'sidebar_active' : undefined}`} onClick={() => navigate(`/my_apis/${api.id}`)}>
                                {api.name}
                            </article>
                        })
                    }
                </section>
            }


            <section className={"my_api_create_btn"}>
                <div className={`${createApiPage ? 'sidebar_active' : undefined}`} onClick={() => navigate("/my_apis/create")}>
                    <img src={createApiPage ? newIconWhite : newIcon} alt="" />
                    CREATE
                </div>
            </section>
        </div>
    )
}

export default Index
