import './App.scss'
import Header from "./components/Header"
import Footer from "./components/Footer"
import Hero from "./components/Hero"
import About from "./components/About"

function App() {
  const navs = [
    {
      title: "LOGIN",
      path: '/login'
    },
    {
      title: "SIGN UP",
      path: '/register'
    }
  ]
  return (
    <>
      <div className='main-container'>
        <Header navs={navs} type="landing" />
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
