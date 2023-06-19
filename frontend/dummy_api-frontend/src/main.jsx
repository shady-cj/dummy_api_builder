import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App.jsx'
import Login from './pages/Login'
import Register from './pages/Register'
import MyApi from './pages/MyApi'
import CreateAPI from "./pages/CreateAPI"
import MyApiDetail from "./pages/MyApiDetail"
import ModelPage from "./pages/ModelPage"
import CreateModel from "./pages/CreateModel"
import './index.scss'
import {
  createBrowserRouter,
  RouterProvider,
} from "react-router-dom";

const router = createBrowserRouter([
  {
    path: "/",
    element: <App />,
  },
  {
    path: '/login',
    element: <Login />,
  },
  {

    path: '/register',
    element: <Register />
  },
  {
    path: '/my_apis',
    element: <MyApi />,
    children: [
      {
        path: ":apiId",
        element: <MyApiDetail />
      },
      {
        path: "create",
        element: <CreateAPI />
      },
      {
        path: ":apiId/model/create",
        element: <CreateModel />
      },
      {
        path: ":apiId/model/:modelsId",
        element: <ModelPage />
      },

    ]
  },
]);


ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <RouterProvider router={router} />
  </React.StrictMode>,
)
