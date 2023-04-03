import './Navbar.css'
import Logo from './../../assets/image/dron_navbar.svg'

const Navbar = () => {
  return (
    <div className='navbar'>
      <img src={Logo} alt="icon" />
      <div className='title'>Комплектующие для БПЛА</div>
      <div className='nav'>
        <div className='nav-link'>Главная</div>
        <div className='nav-link'>Элемент</div>
        <div className='nav-link'>Еще что-нибудь</div>
      </div>
    </div>
  )
}

export default Navbar