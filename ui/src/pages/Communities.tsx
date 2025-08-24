import { motion } from 'framer-motion'
import { UserGroupIcon } from '@heroicons/react/24/outline'

export default function Communities() {
  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.3 }}
      className="text-center py-12"
    >
      <UserGroupIcon className="mx-auto h-12 w-12 text-gray-400" />
      <h3 className="mt-2 text-sm font-medium text-gray-900">Communities</h3>
      <p className="mt-1 text-sm text-gray-500">
        This page is under development.
      </p>
    </motion.div>
  )
}
