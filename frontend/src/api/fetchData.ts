const VERCEL_ENV = import.meta.env.VERCEL_ENV;
const VERCEL_RELATED_PROJECTS = import.meta.env.VERCEL_RELATED_PROJECTS;

const DEFAULT_HOST = 'http://localhost:8000';

const getApiHost = (): string => {
  // Local
  if (VERCEL_ENV === undefined || VERCEL_RELATED_PROJECTS === undefined) {
    return DEFAULT_HOST;
  }

  const relatedProjects = JSON.parse(VERCEL_RELATED_PROJECTS);
  const project = relatedProjects[0];

  // Preview
  if (VERCEL_ENV === 'preview' && project.preview.branch) {
    return `https://${project.preview.branch}`;
  }

  // Production
  if (VERCEL_ENV === 'production') {
    if (project.production.alias) {
      return `https://${project.production.alias}`;
    }

    if (project.production.url) {
      return `https://${project.production.url}`;
    }
  }

  return DEFAULT_HOST;
};

export const fetchData = async (): Promise<string> => {
  const apiHost = getApiHost();
  const response = await fetch(apiHost);
  return response.json();
};
