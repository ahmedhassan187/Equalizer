import React, { useContext } from 'react'
import { FileContext } from '../contexts/fileContext';


function Modes() {
  const { setModesIndex, } = useContext(FileContext);
  const modesList = [
    {
      id: 0,
      label: "Frequency Bands",
      isChecked: true,
    },
    {
      id: 1,
      label: "Music",
      isChecked: false,
    },
    {
      id: 2,
      label: "Voules",
      isChecked: false,
    }
  ]

  return (
    <div>
      {modesList.map((mode, index) => {
        return (
          <label key={index}>
            <input type="radio" name='radio' defaultChecked={mode.isChecked} onClick={() => {
              setModesIndex(mode.id)
            }} />
            {mode.label}
          </label>
        )
      })}
    </div>
  )
}

export default Modes