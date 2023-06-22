import Header from "./components/Header"
import Footer from "./components/Footer"
import ErrorElement from "./components/ErrorElement"

const ErrorPage = () => {
    return (
        <div>
            <Header />
            <section className="error-wrapper">
                <ErrorElement />
            </section>
            <Footer />
        </div>
    )
}

export default ErrorPage
