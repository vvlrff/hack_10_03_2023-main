import { useState, useEffect } from "react"
import axios from 'axios'
import { Link, useLocation, useNavigate } from "react-router-dom"
import ClipLoader from 'react-spinners/ClipLoader'
import { filterCards } from '../functions/filterCards'
import { Pagination, PaginationItem } from '@mui/material'

import '../assets/css/CardsPage.css'

const CardsPage = () => {
  const location = useLocation()

  // Получение данных с API get_data
  const [cards, setCards] = useState([])
  const size = 40
  const [page, setPage] = useState(parseInt(location.search?.split('=')[1] || 1))
  const [pageQty, setPageQty] = useState(0)

  useEffect(() => {
    axios
      .get(`http://195.161.68.132:8000/api/get_data?page=${page}&size=${size}`)
      .then(res => {
        setCards(res.data.items)
        setPageQty(res.data.pages)
      })
      .catch(err => {
        console.log(err);
      })
  }, [page, size])


  // Для фильтра по странам
  const [countries, setCountries] = useState([])

  useEffect(() => {
    axios
      .get(`http://195.161.68.132:8000/api/get_data/countrus`)
      .then(res => {
        console.log(res.data)
        setCountries(res.data)
      })
      .catch(err => {
        console.log(err);
      })
  }, [])


  // Для фильтра по категориям
  const [categories, setCategories] = useState([])

  useEffect(() => {
    axios
      .get(`http://195.161.68.132:8000/api/get_data/category`)
      .then(res => {
        console.log(res.data)
        setCategories(res.data)
      })
      .catch(err => {
        console.log(err);
      })
  }, [])


  // Для поиска
  const [cardsList, setCardList] = useState(cards)
  const [searchTerm, setSearchTerm] = useState('')

  useEffect(() => {
    const Debounce = setTimeout(() => {
      const filteredCards = filterCards(searchTerm, cards)
      setCardList(filteredCards)
    }, 300)

    return () => clearTimeout(Debounce)
  }, [cards, searchTerm])

  // Для добавления состояния прогрузки на странице
  const [loading, setLoading] = useState(false)

  // Для кнопок sidebar
  const parsingTurkey = () => {
    setLoading(true)
    axios
      .get('http://195.161.68.132:8000/pars/pars_Turkey_drone')
      .then(res => {
        console.log(res)
        if (res.status === 200) {
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
          setLoading(false)
        }
      })
      .catch(err => {
        console.log(err);
        setLoading(false)
      })
  }
  

  const getExcel = () => {
    setLoading(true)
    axios
      .get('http://195.161.68.132:8000/output/get_XlSX')
      .then(res => {
        if (res.status === 200) {
          alert('Успешно')
          setLoading(false)
        }
      })
      .catch(err => {
        alert(err)
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
          <>
            <div className='sidebar'>

              <div className='column'>
                <form>
                  <input
                    type="text"
                    placeholder="Окно поиска по странице"
                    autoComplete="off"
                    value={searchTerm}
                    onChange={(e => setSearchTerm(e.target.value))} />
                  <button type="submit">Поиск</button>
                </form>
              </div>


              <div className='filters'>
                <button className='sidebar-btn2' onClick={parsingTurkey}>
                  Парсинг www.drone.net.tr
                </button>
                <button className='sidebar-btn2' onClick={parsingGermany}>
                  Парсинг www.banggood.com
                </button>
                <button className='sidebar-btn2' onClick={parsingDJI}>
                  Парсинг www.dji.com
                </button>
                <button className='sidebar-btn2' onClick={parsingAeromotus}>
                  Парсинг aeromotus.ru
                </button>
                <button className='sidebar-btn2' onClick={parsingNelk}>
                  Парсинг nelk.ru
                </button>
              </div>
            </div>

            <div className="anotation">Для отображения данных перезагрузите страницу</div>


            <div className='sidebar2'>
              <div className='filters'>
                {
                  countries.map(country => (
                    <Link key={country.country} className='sidebar-btn2' to={`/cards/country/${country.country}`}>
                      Страна: {country.country}
                    </Link>
                  ))
                }
              </div>
            </div>

            <div className='sidebar4'>
              <div className='filters'>

                {
                  categories.map(category => (
                    <Link key={category.category} className='sidebar-btn3' to={`/cards/category/${category.category}`}>
                      Категория: {category.category}
                    </Link>
                  ))
                }

              </div>
            </div>

            <div className='sidebar3'>
              <div className='filters2'>
                <button className='sidebar-btn' onClick={getExcel}>
                  Получить Excel
                </button>
              </div>
            </div>

            <div className='grid'>
              {
                cardsList.map(card => (
                  <div className="card">
                    <Link key={card.id_data} to={`/card/${card.id_data}`} >
                      <div className='name element'>
                        {card.name}
                      </div>
                      <div className="flex-center">
                        <img src={card.img_href} alt={card.name} className='cards-img' />
                      </div>
                      <Link to={`/cards/${card.id_data}`} className='false-btn element-btn flex-center'>
                        Перейти к описанию
                      </Link>
                    </Link>
                  </div>
                ))
              }
            </div>

            <div className="flex">
              <Pagination
                count={pageQty}
                page={page}
                onChange={(_, num) => setPage(num)}
                sx={{ marginY: 3, marginX: 'auto' }}
                renderItem={
                  (item) => (
                    <PaginationItem
                      component={Link}
                      to={`/cards/?page=${item.page}`}
                      {...item}
                    />
                  )
                }
              />
            </div>
          </>
      }
    </>
  )
}

export default CardsPage