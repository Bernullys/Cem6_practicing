import SignIn from './Components/SignIn/SignIn';
import Register from './Components/Register/Register';;
import StartStopSystem from './Components/StartStopSystem/StartStopSystem';
import AddUsers from './Components/AddUsers/AddUsers';
import CheckElecParam from './Components/CheckElecParam/CheckElecParam';
import CheckEnergy from './Components/CheckEnergy/CheckEnergy';
import Invoice from './Components/Invoice/Invoice';
import './App.css'

function App() {

  return (
    <>
      <SignIn />
      <Register />
      <StartStopSystem />
      <AddUsers />
      <CheckElecParam />
      <CheckEnergy />
      <Invoice />
    </>
  )
}

export default App
