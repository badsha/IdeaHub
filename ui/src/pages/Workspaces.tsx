import { useQuery } from '@tanstack/react-query'
import { Link } from 'react-router-dom'
import { motion } from 'framer-motion'
import {
  BuildingOfficeIcon,
  PlusIcon,
  UserGroupIcon,
  CalendarIcon,
  EyeIcon,
} from '@heroicons/react/24/outline'
import LoadingSpinner from '@/components/LoadingSpinner'

// Mock data for demonstration
const mockWorkspaces = [
  {
    id: 1,
    name: 'Acme Corporation',
    description: 'Main workspace for Acme Corporation employees',
    member_count: 150,
    created_at: '2024-01-15T10:00:00Z',
    public_default: true,
  },
  {
    id: 2,
    name: 'Innovation Lab',
    description: 'Research and development workspace for innovative projects',
    member_count: 25,
    created_at: '2024-02-01T14:30:00Z',
    public_default: false,
  },
  {
    id: 3,
    name: 'Product Team',
    description: 'Workspace for the product development team',
    member_count: 45,
    created_at: '2024-01-20T09:15:00Z',
    public_default: true,
  },
]

export default function Workspaces() {
  // In a real app, you would use the actual API
  // const { data: workspaces, isLoading, error } = useQuery({
  //   queryKey: ['workspaces'],
  //   queryFn: apiService.getWorkspaces,
  // })

  // For now, using mock data
  const { data: workspaces, isLoading } = useQuery({
    queryKey: ['workspaces'],
    queryFn: () => Promise.resolve(mockWorkspaces),
  })

  if (isLoading) {
    return <LoadingSpinner />
  }

  return (
    <div className="space-y-8">
      {/* Header */}
      <div className="sm:flex sm:items-center sm:justify-between">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Workspaces</h1>
          <p className="mt-2 text-sm text-gray-700">
            Manage your organization's workspaces and collaborate with teams
          </p>
        </div>
        <div className="mt-4 sm:mt-0">
          <Link
            to="/workspaces/new"
            className="btn-primary btn-md"
          >
            <PlusIcon className="h-5 w-5 mr-2" />
            Create Workspace
          </Link>
        </div>
      </div>

      {/* Workspaces Grid */}
      <div className="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-3">
        {workspaces?.map((workspace, index) => (
          <motion.div
            key={workspace.id}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.3, delay: index * 0.1 }}
            className="bg-white rounded-lg border border-gray-200 hover:border-primary-300 hover:shadow-md transition-all duration-200"
          >
            <Link to={`/workspaces/${workspace.id}`} className="block p-6">
              <div className="flex items-center justify-between mb-4">
                <div className="flex items-center space-x-3">
                  <div className="h-10 w-10 rounded-lg bg-primary-100 flex items-center justify-center">
                    <BuildingOfficeIcon className="h-6 w-6 text-primary-600" />
                  </div>
                  <div>
                    <h3 className="text-lg font-semibold text-gray-900 group-hover:text-primary-600">
                      {workspace.name}
                    </h3>
                    <div className="flex items-center space-x-2 text-sm text-gray-500">
                      <UserGroupIcon className="h-4 w-4" />
                      <span>{workspace.member_count} members</span>
                    </div>
                  </div>
                </div>
                {workspace.public_default && (
                  <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-green-100 text-green-800">
                    Public
                  </span>
                )}
              </div>
              
              <p className="text-sm text-gray-600 mb-4 line-clamp-2">
                {workspace.description}
              </p>
              
              <div className="flex items-center justify-between text-sm text-gray-500">
                <div className="flex items-center space-x-1">
                  <CalendarIcon className="h-4 w-4" />
                  <span>Created {new Date(workspace.created_at).toLocaleDateString()}</span>
                </div>
                <div className="flex items-center space-x-1 text-primary-600">
                  <EyeIcon className="h-4 w-4" />
                  <span>View</span>
                </div>
              </div>
            </Link>
          </motion.div>
        ))}
      </div>

      {/* Empty State */}
      {workspaces?.length === 0 && (
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          className="text-center py-12"
        >
          <BuildingOfficeIcon className="mx-auto h-12 w-12 text-gray-400" />
          <h3 className="mt-2 text-sm font-medium text-gray-900">No workspaces</h3>
          <p className="mt-1 text-sm text-gray-500">
            Get started by creating your first workspace.
          </p>
          <div className="mt-6">
            <Link
              to="/workspaces/new"
              className="btn-primary btn-md"
            >
              <PlusIcon className="h-5 w-5 mr-2" />
              Create Workspace
            </Link>
          </div>
        </motion.div>
      )}
    </div>
  )
}
