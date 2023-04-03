import axios from 'axios'
import { useNavigate } from 'react-router-dom'
import { useState } from 'react'
import ClipLoader from 'react-spinners/ClipLoader'

import '../assets/css/HomePage.css'

const Homepage = () => {
  const navigate = useNavigate();
  const [loading, setLoading] = useState(false)
  const path = `cards/`

  const parsingTurkey = () => {
    setLoading(true)
    axios
      .get('http://195.161.68.132:8000/pars/pars_Turkey_drone')
      .then(res => {
        console.log(res)
        if (res.status === 200) {
          navigate(path)
          setLoading(false)
          
        }
      })
      .catch(err => {
        console.log(err);
        setLoading(false)
      })
  }

  const parsingNelk = () => {
    setLoading(true)
    axios
      .get('http://195.161.68.132:8000/pars/pars_Russian_nelik')
      .then(res => {
        console.log(res)
        if (res.status === 200) {
          navigate(path)
          setLoading(false)

        }
      })
      .catch(err => {
        console.log(err);
        setLoading(false)
      })
  }
  

  const parsingGermany = () => {
    setLoading(true)
    axios
      .get('http://195.161.68.132:8000/pars/pars_Germany_banggood')
      .then(res => {
        console.log(res)
        if (res.status === 200) {
          navigate(path)
          setLoading(false)
        }
      })
      .catch(err => {
        console.log(err);
        setLoading(false)
      })
  }

  const parsingDJI = () => {
    setLoading(true)
    axios
      .get('http://195.161.68.132:8000/pars/pars_Russian_dji')
      .then(res => {
        console.log(res)
        if (res.status === 200) {
          navigate(path)
          setLoading(false)
        }
      })
      .catch(err => {
        console.log(err);
        setLoading(false)
      })
  }

  const parsingAeromotus = () => {
    setLoading(true)
    axios
      .get('http://195.161.68.132:8000/pars/pars_Russian_aeromotus')
      .then(res => {
        console.log(res)
        if (res.status === 200) {
          navigate(path)
          setLoading(false)
        }
      })
      .catch(err => {
        console.log(err);
        setLoading(false)
      })
  }

  return (
    <>
      {
        loading ?
          <div className='center'>
            <ClipLoader
              color={'#242121'}
              loading={loading}
              size={'70px'}
            />
          </div>
          :
          <div className='flex'>
            <div className='block'>
              <button onClick={parsingTurkey} className='homepage-btn'>
                  Парсинг www.drone.net.tr
              </button>
              <button onClick={parsingGermany} className='homepage-btn'>
                  Парсинг www.banggood.com
              </button>
              <button onClick={parsingDJI} className='homepage-btn'>
                  Парсинг www.dji.com
              </button>
              <button onClick={parsingAeromotus} className='homepage-btn'>
                  Парсинг aeromotus.ru
              </button>
              <button onClick={parsingNelk} className='homepage-btn'>
                  Парсинг nelk.ru
              </button>
            </div>

          </div>
      }
    </>
  )
}

export default Homepage