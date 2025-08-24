import { Link } from 'react-router-dom'
import { motion } from 'framer-motion'
import { useTranslation } from 'react-i18next'
import {
  LightBulbIcon,
  UserGroupIcon,
  BuildingOfficeIcon,
  MagnifyingGlassIcon,
  ArrowRightIcon,
  ChartBarIcon,
  ShieldCheckIcon,
  SparklesIcon,
} from '@heroicons/react/24/outline'

const features = [
  {
    name: 'Collaborative Workspaces',
    description: 'Create and manage workspaces for your organization with team collaboration features.',
    icon: BuildingOfficeIcon,
    href: '/workspaces',
  },
  {
    name: 'Community Engagement',
    description: 'Build communities around shared interests and foster meaningful discussions.',
    icon: UserGroupIcon,
    href: '/communities',
  },
  {
    name: 'Idea Management',
    description: 'Capture, organize, and track ideas from concept to implementation.',
    icon: LightBulbIcon,
    href: '/ideas',
  },
  {
    name: 'Advanced Search',
    description: 'Find ideas, communities, and content with powerful search capabilities.',
    icon: MagnifyingGlassIcon,
    href: '/search',
  },
]

const stats = [
  { name: 'Active Workspaces', value: '2,847' },
  { name: 'Communities', value: '12,000+' },
  { name: 'Ideas Shared', value: '45,000+' },
  { name: 'Active Users', value: '8,500+' },
]

export default function Home() {
  const { t } = useTranslation()

  return (
    <div className="space-y-16">
      {/* Hero Section */}
      <section className="text-center">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6 }}
        >
          <h1 className="text-4xl font-bold tracking-tight text-gray-900 sm:text-6xl">
            {t('home.hero.title')}
            <span className="text-primary-600"> {t('home.hero.title_highlight')}</span>
          </h1>
          <p className="mt-6 text-lg leading-8 text-gray-600 max-w-2xl mx-auto">
            {t('home.hero.subtitle')}
          </p>
          <div className="mt-10 flex items-center justify-center gap-x-6">
            <Link
              to="/workspaces"
              className="btn-primary btn-lg"
            >
              {t('home.hero.get_started')}
              <ArrowRightIcon className="ml-2 h-5 w-5" />
            </Link>
            <Link
              to="/search"
              className="btn-outline btn-lg"
            >
              {t('home.hero.explore_ideas')}
            </Link>
          </div>
        </motion.div>
      </section>

      {/* Stats Section */}
      <section className="bg-white rounded-lg shadow-sm border">
        <div className="px-6 py-12">
          <dl className="grid grid-cols-1 gap-5 sm:grid-cols-2 lg:grid-cols-4">
            {stats.map((stat, index) => (
              <motion.div
                key={stat.name}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.6, delay: index * 0.1 }}
                className="relative overflow-hidden rounded-lg bg-gray-50 px-4 pb-12 pt-5 sm:px-6 sm:pt-6"
              >
                <dt>
                  <div className="absolute rounded-md bg-primary-500 p-3">
                    <ChartBarIcon className="h-6 w-6 text-white" aria-hidden="true" />
                  </div>
                  <p className="ml-16 truncate text-sm font-medium text-gray-500">{stat.name}</p>
                </dt>
                <dd className="ml-16 flex items-baseline pb-6 sm:pb-7">
                  <p className="text-2xl font-semibold text-gray-900">{stat.value}</p>
                </dd>
              </motion.div>
            ))}
          </dl>
        </div>
      </section>

      {/* Features Section */}
      <section>
        <div className="text-center mb-12">
          <h2 className="text-3xl font-bold tracking-tight text-gray-900 sm:text-4xl">
            Everything you need to manage ideas
          </h2>
          <p className="mt-4 text-lg text-gray-600">
            Powerful features designed to streamline your idea management workflow
          </p>
        </div>
        <div className="grid grid-cols-1 gap-8 sm:grid-cols-2 lg:grid-cols-4">
          {features.map((feature, index) => (
            <motion.div
              key={feature.name}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6, delay: index * 0.1 }}
              className="relative group"
            >
              <Link
                to={feature.href}
                className="block p-6 bg-white rounded-lg border border-gray-200 hover:border-primary-300 hover:shadow-md transition-all duration-200"
              >
                <div className="flex items-center justify-center w-12 h-12 rounded-lg bg-primary-100 group-hover:bg-primary-200 transition-colors">
                  <feature.icon className="h-6 w-6 text-primary-600" aria-hidden="true" />
                </div>
                <h3 className="mt-4 text-lg font-semibold text-gray-900 group-hover:text-primary-600 transition-colors">
                  {feature.name}
                </h3>
                <p className="mt-2 text-sm text-gray-600">
                  {feature.description}
                </p>
              </Link>
            </motion.div>
          ))}
        </div>
      </section>

      {/* CTA Section */}
      <section className="bg-primary-600 rounded-lg">
        <div className="px-6 py-12 text-center">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6 }}
          >
            <h2 className="text-3xl font-bold tracking-tight text-white sm:text-4xl">
              Ready to get started?
            </h2>
            <p className="mt-4 text-lg text-primary-100">
              Join thousands of teams already using IdeaHub to manage their ideas
            </p>
            <div className="mt-8 flex items-center justify-center gap-x-6">
              <Link
                to="/workspaces"
                className="bg-white text-primary-600 hover:bg-gray-100 btn btn-lg"
              >
                Create Workspace
                <ArrowRightIcon className="ml-2 h-5 w-5" />
              </Link>
              <Link
                to="/communities"
                className="text-white border border-white hover:bg-white hover:text-primary-600 btn btn-lg"
              >
                Join Community
              </Link>
            </div>
          </motion.div>
        </div>
      </section>
    </div>
  )
}
