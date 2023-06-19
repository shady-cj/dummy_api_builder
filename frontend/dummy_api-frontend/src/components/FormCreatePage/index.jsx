import "./index.scss";

const index = () => {
    return (
        <div className="create-wrapper">
            <section className="create_header">
                <h2>CREATE NEW API</h2>
            </section>
            <section className="create_form">
                <form action=".">
                    <div>
                        <label htmlFor="name">Name</label>
                        <input type="text" id="name" name="name" />
                    </div>
                    <div>
                        <label htmlFor="desc">Description</label>
                        <textarea name="description" id="desc"></textarea>
                    </div>
                    <button>CREATE</button>
                </form>
            </section>
        </div>
    )
}

export default index