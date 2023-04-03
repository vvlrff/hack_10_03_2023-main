import { useParams, useNavigate } from 'react-router-dom'
import { useState, useEffect } from 'react'
import axios from 'axios'

import '../assets/css/CardPage.css'

const CardPage = () => {
  const { id_data } = useParams()
  const [cards, setCards] = useState([])
  const navigate = useNavigate();

  const goBack = () => {
    navigate(-1)
  }

  useEffect(() => {
    axios
      .get(`http://195.161.68.132:8000/api/get_data/id?id=${id_data}`)
      .then(res => {
        console.log(res.data)
        setCards(res.data)
      })
      .catch(err => {
        console.log(err);
      })
  }, [id_data])

  return (
    <>
      <button onClick={goBack} className='go-back-btn'>Вернуться назад</button>
      <div className='flex'>
        {
          cards.map(card => (
            <div key={card.id_data} className='card-block'>
              <div className='margin'>
                <div className='card-category'>
                  Категория: {card.category}
                </div>
                <div className='card-country'>
                  Сайт: {card.net_href}
                </div>
                <div className='card-name'>
                  {card.name}
                </div>

                <div className='card-flex'>
                  <img src={card.img_href} alt={card.name} className='card-img' />
                  <div className='card-flex-column'>
                    <div>
                      {
                        Object.entries(card.specifications)
                          .map(([key, value]) => (
                            <div key={key}>
                              <div className='card-spec'>
                                {key}: {value}
                              </div >
                            </div>
                          ))
                      }
                    </div>
                  </div>
                </div>
                <div className='card-url-center'>

                  <a href={card.url}>
                    <div className='card-url'>
                      Перейти к источнику
                    </div>
                  </a>

                </div>
              </div>
            </div>
          )
          )}
      </div>
    </>
  )
}

export default CardPage
