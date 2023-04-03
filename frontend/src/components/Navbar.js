import Logo from '../assets/image/dron_navbar.svg'
import '../assets/css/Navbar.css'

const Navbar = () => {
  return (
    <header className='navbar'>
      <img src={Logo} alt="icon" />
      <div className='title'>Комплектующие для БПЛА</div>
    </header>
  )
}

export default Navbar