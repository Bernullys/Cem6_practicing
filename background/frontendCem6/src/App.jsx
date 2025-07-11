import { useRoutes, HashRouter, useLocation } from 'react-router-dom';
import ProtectedRoute from './Components/ProtectedRoute.jsx/ProtectedRoute';
import Home from './Components/Home/Home';
import SignIn from './Components/SignIn/SignIn';
import Register from './Components/Register/Register';;
import StartStopSystem from './Components/StartStopSystem/StartStopSystem';
import AddUsers from './Components/AddUsers/AddUsers';
import CheckElecParam from './Components/CheckElecParam/CheckElecParam';
import CheckEnergy from './Components/CheckEnergy/CheckEnergy';
import Invoice from './Components/Invoice/Invoice';
import LogoutButton from './Components/LogoutButton/LogoutButton';
import AuthWatcher from './Components/AuthWatcher/AuthWatcher';
import GWStatus from './Components/GWStatus/GWStatus';
import './App.css'

export const AppRoutes = () => {
  let routes = useRoutes([
    { path: "/", element: <Home />},
    { path: "/login", element: <SignIn/>},
    { path: "/register", element: <Register />},
    { path: "/allApp", element: 
    <ProtectedRoute>
      <StartStopSystem />
      <AddUsers />
      <CheckElecParam />
      <CheckEnergy />
      <Invoice />
      <GWStatus />
      <LogoutButton />
    </ProtectedRoute>}
  ])
  return (
    <>
      <AuthWatcher />
      { routes }
    </>
  )
}

function App() {

  return (
    <HashRouter>
      <AppRoutes />
    </HashRouter>
  )
}

export default App
