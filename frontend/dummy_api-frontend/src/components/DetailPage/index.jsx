import "./index.scss";
import { Link, useNavigate } from "react-router-dom";

const index = () => {
    const navigate = useNavigate();
    return (
        <div className="detail-wrapper">
            <section className="detail_header">
                <h2>API 1</h2>
                <p>
                    Lorem ipsum dolor sit amet consectetur adipisicing elit. Sit possimus eius nulla nesciunt. Dolorem, voluptate nihil. Dicta dolores maxime ad facere corrupti esse animi, eaque ea, suscipit sequi, aspernatur quis?

                </p>
            </section>
            <section className="detail-list_models">
                <article>
                    <Link to="model/1">
                        Model 1
                    </Link>
                </article>
                <article>
                    <Link to="model/2">
                        Model 2
                    </Link>
                </article>
                <article>
                    <Link to="model/3">
                        Model 3
                    </Link>
                </article>
                <article>
                    <Link to="model/4">
                        Model 4
                    </Link>
                </article>
                <article>
                    <Link to="model/5">
                        Model 5
                    </Link>
                </article>
                <article>
                    <Link to="model/6">
                        Model 6
                    </Link>
                </article>
                <article>
                    <Link to="model/7">
                        Model 7
                    </Link>
                </article>
                <article>
                    <Link to="model/8">
                        Model 8
                    </Link>
                </article>
                <article>
                    <Link to="model/9">
                        Model 9
                    </Link>
                </article>
                <article>
                    <Link to="model/10">
                        Model 10
                    </Link>
                </article>
            </section>
            <section className="detail_footer">
                <button onClick={() => navigate('model/create')}>
                    Add Model
                </button>
                <button>
                    Test Endpoint
                </button>

            </section>
        </div>
    )
}

export default index
