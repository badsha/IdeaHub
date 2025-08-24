import { Routes, Route } from 'react-router-dom'
import { Suspense, lazy } from 'react'
import Layout from './components/Layout'
import LoadingSpinner from './components/LoadingSpinner'

// Lazy load pages for better performance
const Home = lazy(() => import('./pages/Home'))
const Workspaces = lazy(() => import('./pages/Workspaces'))
const WorkspaceDetail = lazy(() => import('./pages/WorkspaceDetail'))
const Communities = lazy(() => import('./pages/Communities'))
const CommunityDetail = lazy(() => import('./pages/CommunityDetail'))
const Ideas = lazy(() => import('./pages/Ideas'))
const IdeaDetail = lazy(() => import('./pages/IdeaDetail'))
const Search = lazy(() => import('./pages/Search'))
const Analytics = lazy(() => import('./pages/Analytics'))
const NotFound = lazy(() => import('./pages/NotFound'))

function App() {
  return (
    <Layout>
      <Suspense fallback={<LoadingSpinner />}>
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/workspaces" element={<Workspaces />} />
          <Route path="/workspaces/:id" element={<WorkspaceDetail />} />
          <Route path="/communities" element={<Communities />} />
          <Route path="/communities/:id" element={<CommunityDetail />} />
          <Route path="/ideas" element={<Ideas />} />
          <Route path="/ideas/:id" element={<IdeaDetail />} />
          <Route path="/search" element={<Search />} />
          <Route path="/analytics" element={<Analytics />} />
          <Route path="*" element={<NotFound />} />
        </Routes>
      </Suspense>
    </Layout>
  )
}

export default App
