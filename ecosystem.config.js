module.exports = {
  apps: [
    {
      name: 'task-manager-backend',
      script: 'backend.main:app',
      interpreter: 'python3',
      exec_mode: 'cluster',
      env: {
        NODE_ENV: 'production',
        DATABASE_URL: process.env.DATABASE_URL || 'sqlite:///./tasks.db',
      },
      env_file: '.env',
      instances: 1,
      autorestart: true,
      watch: false,
      max_memory_restart: '1G',
    },
    {
      name: 'task-manager-bot',
      script: 'bot_logic/bot.py',
      interpreter: 'python3',
      env: {
        NODE_ENV: 'production',
      },
      env_file: '.env',
      autorestart: true,
      max_memory_restart: '512M',
    },
    {
      name: 'task-manager-worker',
      script: 'backend/worker.py',
      interpreter: 'python3',
      env: {
        NODE_ENV: 'production',
      },
      env_file: '.env',
      autorestart: true,
      max_memory_restart: '512M',
    }
  ]
};
