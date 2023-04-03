import axios from 'axios'
import { useNavigate } from 'react-router-dom'

import '../assets/css/Search.css'

const Search = () => {
  const navigate = useNavigate(); 

  const parsingTurkey = () => {
    axios
      .get('http://195.161.68.132:8000/pars/pars_turkey')
      .then(res => {
        console.log(res)
      })
      .catch(err => {
        console.log(err);
      })
    const path = `cards`; 
    navigate(path)
  }

  return (
    <div className='flex'>
      <div className='block'>
        <button onClick={parsingTurkey}>
          Парсинг Турков
        </button>
        <button>
          Парсинг 2
        </button>
        <button>
          Парсинг 3
        </button>
        <button>
          Парсинг 4
        </button>
        <button>
          Парсинг 5
        </button>
        <button>
          Парсинг 6
        </button>
      </div>
    </div>
  )
}

export default Search