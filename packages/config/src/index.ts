export interface ApiConfig {
  baseUrl: string;
  timeout: number;
}

export interface AppConfig {
  api: ApiConfig;
  environment: 'development' | 'staging' | 'production';
}

export const getConfig = (): AppConfig => {
  const environment = (process.env.NODE_ENV || 'development') as AppConfig['environment'];
  
  const config: AppConfig = {
    api: {
      baseUrl: process.env.API_BASE_URL || 'http://localhost:80',
      timeout: Number.parseInt(process.env.API_TIMEOUT || '5000', 10),
    },
    environment,
  };
  
  return config;
};

export const config = getConfig();


