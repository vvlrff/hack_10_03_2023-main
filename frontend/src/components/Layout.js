import { Outlet } from "react-router-dom"
import Navbar from "./Navbar"

import '../assets/css/Layout.css'

const Layout = () => {
  return (
    <>
      <Navbar />
      <main>
        <Outlet />
      </main>
    </>
  )
}

export default Layout