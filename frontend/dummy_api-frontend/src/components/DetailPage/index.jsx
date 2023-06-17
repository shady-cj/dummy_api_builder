import "./index.scss";
import { Link } from "react-router-dom";

const index = () => {
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
                    <Link to="model">
                        Model 1
                    </Link>
                </article>
                <article>
                    <Link to="model">
                        Model 2
                    </Link>
                </article>
                <article>
                    <Link to="model">
                        Model 3
                    </Link>
                </article>
                <article>
                    <Link to="model">
                        Model 4
                    </Link>
                </article>
                <article>
                    <Link to="model">
                        Model 5
                    </Link>
                </article>
                <article>
                    <Link to="model">
                        Model 6
                    </Link>
                </article>
                <article>
                    <Link to="model">
                        Model 5
                    </Link>
                </article>
                <article>
                    <Link to="model">
                        Model 6
                    </Link>
                </article>
                <article>
                    <Link to="model">
                        Model 5
                    </Link>
                </article>
                <article>
                    <Link to="model">
                        Model 6
                    </Link>
                </article>
            </section>
            <section className="detail_footer">
                <button>
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
