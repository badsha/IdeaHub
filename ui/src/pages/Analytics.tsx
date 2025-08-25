import React, { useState, useEffect } from 'react';
import { useTranslation } from 'react-i18next';
import { motion } from 'framer-motion';
import { 
  ChartBarIcon, 
  UsersIcon, 
  LightBulbIcon,
  ArrowTrendingUpIcon,
  ClockIcon
} from '@heroicons/react/24/outline';
import api from '../services/api';

interface AnalyticsData {
  workspace: {
    id: number;
    name: string;
    url: string;
  };
  statistics: {
    workspace: {
      total_members: number;
      total_communities: number;
      total_ideas: number;
      implementation_rate: number;
      avg_ideas_per_community: number;
    };
    activity_summary: {
      total_activities: number;
      unique_participants: number;
      activity_breakdown: Record<string, number>;
    };
  };
  recent_activities: Array<{
    id: number;
    activity_type: string;
    entity_type: string;
    entity_id: number;
    timestamp: string;
    member_id: number;
  }>;
  last_updated: string;
}

const Analytics: React.FC = () => {
  const { t } = useTranslation();
  const [data, setData] = useState<AnalyticsData | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetchAnalyticsData();
  }, []);

  const fetchAnalyticsData = async () => {
    try {
      setLoading(true);
      const response = await api.get('/reporting/analytics/dashboard');
      setData(response.data.data);
      setError(null);
    } catch (err) {
      setError('Failed to load analytics data');
      console.error('Analytics error:', err);
    } finally {
      setLoading(false);
    }
  };

  const StatCard: React.FC<{
    title: string;
    value: string | number;
    icon: React.ReactNode;
    color: string;
  }> = ({ title, value, icon, color }) => (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      className={`bg-white rounded-lg shadow-md p-6 border-l-4 ${color}`}
    >
      <div className="flex items-center justify-between">
        <div>
          <p className="text-sm font-medium text-gray-600">{title}</p>
          <p className="text-2xl font-bold text-gray-900">{value}</p>
        </div>
        <div className="text-gray-400">
          {icon}
        </div>
      </div>
    </motion.div>
  );

  const ActivityItem: React.FC<{
    activity: {
      activity_type: string;
      entity_type: string;
      entity_id: number;
      timestamp: string;
      member_id: number;
    };
  }> = ({ activity }) => {
    const getActivityIcon = () => {
      switch (activity.activity_type) {
        case 'idea_created':
          return <LightBulbIcon className="w-5 h-5 text-blue-500" />;
        case 'idea_voted':
          return <ArrowTrendingUpIcon className="w-5 h-5 text-green-500" />;
        case 'member_joined':
          return <UsersIcon className="w-5 h-5 text-purple-500" />;
        default:
          return <ClockIcon className="w-5 h-5 text-gray-500" />;
      }
    };

    const formatTimestamp = (timestamp: string) => {
      return new Date(timestamp).toLocaleString();
    };

    return (
      <div className="flex items-center space-x-3 p-3 hover:bg-gray-50 rounded-lg">
        {getActivityIcon()}
        <div className="flex-1">
          <p className="text-sm font-medium text-gray-900">
            {activity.activity_type.replace('_', ' ').toUpperCase()}
          </p>
          <p className="text-xs text-gray-500">
            {activity.entity_type} #{activity.entity_id} • {formatTimestamp(activity.timestamp)}
          </p>
        </div>
      </div>
    );
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-blue-500"></div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="text-center">
          <p className="text-red-500 text-lg">{error}</p>
          <button
            onClick={fetchAnalyticsData}
            className="mt-4 px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600"
          >
            {t('common.retry')}
          </button>
        </div>
      </div>
    );
  }

  if (!data) {
    return null;
  }

  return (
    <div className="min-h-screen bg-gray-50 p-6">
      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        className="max-w-7xl mx-auto"
      >
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900 mb-2">
            {t('analytics.dashboard')}
          </h1>
          <p className="text-gray-600">
            {t('analytics.workspace')}: {data.workspace.name}
          </p>
          <p className="text-sm text-gray-500">
            {t('analytics.lastUpdated')}: {new Date(data.last_updated).toLocaleString()}
          </p>
        </div>

        {/* Stats Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          <StatCard
            title={t('analytics.totalMembers')}
            value={data.statistics.workspace.total_members}
            icon={<UsersIcon className="w-8 h-8" />}
            color="border-blue-500"
          />
          <StatCard
            title={t('analytics.totalCommunities')}
            value={data.statistics.workspace.total_communities}
            icon={<ChartBarIcon className="w-8 h-8" />}
            color="border-green-500"
          />
          <StatCard
            title={t('analytics.totalIdeas')}
            value={data.statistics.workspace.total_ideas}
            icon={<LightBulbIcon className="w-8 h-8" />}
            color="border-yellow-500"
          />
          <StatCard
            title={t('analytics.implementationRate')}
            value={`${data.statistics.workspace.implementation_rate.toFixed(1)}%`}
            icon={<ArrowTrendingUpIcon className="w-8 h-8" />}
            color="border-purple-500"
          />
        </div>

        {/* Activity Section */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          {/* Recent Activity */}
          <motion.div
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            className="bg-white rounded-lg shadow-md p-6"
          >
            <h2 className="text-xl font-semibold text-gray-900 mb-4">
              {t('analytics.recentActivity')}
            </h2>
            <div className="space-y-2 max-h-96 overflow-y-auto">
              {data.recent_activities.map((activity, index) => (
                <ActivityItem key={activity.id || index} activity={activity} />
              ))}
            </div>
          </motion.div>

          {/* Activity Summary */}
          <motion.div
            initial={{ opacity: 0, x: 20 }}
            animate={{ opacity: 1, x: 0 }}
            className="bg-white rounded-lg shadow-md p-6"
          >
            <h2 className="text-xl font-semibold text-gray-900 mb-4">
              {t('analytics.activitySummary')}
            </h2>
            <div className="space-y-4">
              <div className="flex justify-between items-center">
                <span className="text-gray-600">{t('analytics.totalActivities')}</span>
                <span className="font-semibold">{data.statistics.activity_summary.total_activities}</span>
              </div>
              <div className="flex justify-between items-center">
                <span className="text-gray-600">{t('analytics.uniqueParticipants')}</span>
                <span className="font-semibold">{data.statistics.activity_summary.unique_participants}</span>
              </div>
              <div className="flex justify-between items-center">
                <span className="text-gray-600">{t('analytics.avgIdeasPerCommunity')}</span>
                <span className="font-semibold">{data.statistics.workspace.avg_ideas_per_community.toFixed(1)}</span>
              </div>
            </div>

            {/* Activity Breakdown */}
            <div className="mt-6">
              <h3 className="text-lg font-medium text-gray-900 mb-3">
                {t('analytics.activityBreakdown')}
              </h3>
              <div className="space-y-2">
                {Object.entries(data.statistics.activity_summary.activity_breakdown).map(([type, count]) => (
                  <div key={type} className="flex justify-between items-center">
                    <span className="text-sm text-gray-600">
                      {type.replace('_', ' ').toUpperCase()}
                    </span>
                    <span className="text-sm font-medium">{count}</span>
                  </div>
                ))}
              </div>
            </div>
          </motion.div>
        </div>

        {/* Refresh Button */}
        <div className="mt-8 text-center">
          <button
            onClick={fetchAnalyticsData}
            className="px-6 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600 transition-colors"
          >
            {t('analytics.refresh')}
          </button>
        </div>
      </motion.div>
    </div>
  );
};

export default Analytics;
