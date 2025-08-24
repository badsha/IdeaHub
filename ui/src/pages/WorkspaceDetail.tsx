import { useParams } from 'react-router-dom'
import { motion } from 'framer-motion'
import { BuildingOfficeIcon } from '@heroicons/react/24/outline'

export default function WorkspaceDetail() {
  const { id } = useParams()

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.3 }}
      className="text-center py-12"
    >
      <BuildingOfficeIcon className="mx-auto h-12 w-12 text-gray-400" />
      <h3 className="mt-2 text-sm font-medium text-gray-900">Workspace Detail</h3>
      <p className="mt-1 text-sm text-gray-500">
        Workspace ID: {id} - This page is under development.
      </p>
    </motion.div>
  )
}
