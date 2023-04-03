const filterCards = (searchText, listOfCards) => {
  if (!searchText) {
    return listOfCards
  }
  return listOfCards.filter(({ name }) =>
  name.toLowerCase().includes(searchText.toLowerCase())
  )
}

export { filterCards }