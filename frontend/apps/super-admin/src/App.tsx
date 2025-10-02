import { Routes, Route } from 'react-router-dom'
import { SuperAdminLayout } from './components/SuperAdminLayout'
import { DashboardPage } from './pages/DashboardPage'
import { SystemPage } from './pages/SystemPage'
import { LogsPage } from './pages/LogsPage'
import { DatabasePage } from './pages/DatabasePage'
import { UsersPage } from './pages/UsersPage'
import { SettingsPage } from './pages/SettingsPage'
import { LoginPage } from './pages/LoginPage'

function App() {
  return (
    <div className="min-h-screen bg-gray-900 text-white">
      <Routes>
        <Route path="/login" element={<LoginPage />} />
        <Route path="/" element={<SuperAdminLayout />}>
          <Route index element={<DashboardPage />} />
          <Route path="dashboard" element={<DashboardPage />} />
          <Route path="system" element={<SystemPage />} />
          <Route path="logs" element={<LogsPage />} />
          <Route path="database" element={<DatabasePage />} />
          <Route path="users" element={<UsersPage />} />
          <Route path="settings" element={<SettingsPage />} />
        </Route>
      </Routes>
    </div>
  )
}

export default App