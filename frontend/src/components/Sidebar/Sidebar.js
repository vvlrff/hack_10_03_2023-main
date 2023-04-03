import './Sidebar.css'

const Sidebar = () => {
  return (
    <div className='sidebar'>

      <div className='column'>

        <form>
          <input type="text" placeholder="Окно поиска" />
          <button type="submit">Поиск</button>
        </form>

      </div>

      <div className='filters'>

        <div className='filter'>
          <input type="checkbox" id="scales" name="scales" />
          <label for="scales">Пропеллеры</label>
        </div>

        <div className='filter'>
          <input type="checkbox" id="horns" name="horns" />
          <label for="horns">Двигатель</label>
        </div>

        <div className='filter'>
          <input type="checkbox" id="horns" name="horns" />
          <label for="horns">Двигатель</label>
        </div>

        <div className='filter'>
          <input type="checkbox" id="horns" name="horns" />
          <label for="horns">Двигатель</label>
        </div>

        <div className='filter'>
          <input type="checkbox" id="horns" name="horns" />
          <label for="horns">Двигатель</label>
        </div>

        <div className='filter'>
          <input type="checkbox" id="horns" name="horns" />
          <label for="horns">Двигатель</label>
        </div>

      </div>


    </div>
  )
}

export default Sidebar