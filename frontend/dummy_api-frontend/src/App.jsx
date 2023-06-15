import './App.scss'
import Header from "./components/Header"
import Footer from "./components/Footer"
import Hero from "./components/Hero"
import About from "./components/About"

function App() {

  return (
    <>
      <div>
        <Header />
        <main className='landing-main-block'>
          <Hero />
          <About />
        </main>
        <Footer />
      </div>
    </>
  )
}

export default App
