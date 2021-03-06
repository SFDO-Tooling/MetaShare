import {
  EPIC_STATUSES,
  REVIEW_STATUSES,
  TASK_STATUSES,
} from '~js/utils/constants';

export const api_urls = {
  account_logout: () => '/accounts/logout/',
  github_login: () => '/accounts/github/login/',
  salesforce_login: () => '/accounts/salesforce/login/',
  user: () => '/api/user/',
  user_refresh: () => '/api/user/refresh/',
  user_disconnect_sf: () => '/api/user/disconnect/',
  agree_to_tos: () => '/api/agree_to_tos/',
  project_list: () => '/api/projects/',
  project_detail: (slug: string) => `/api/projects/${slug}/`,
  project_refresh_github_users: (id: string) =>
    `/api/projects/${id}/refresh_github_users/`,
  epic_list: () => '/api/epics/',
  scratch_org_list: () => '/api/scratch_orgs/',
  scratch_org_detail: (id: string) => `/api/scratch_orgs/${id}/`,
  scratch_org_commit: (id: string) => `/api/scratch_orgs/${id}/commit/`,
  scratch_org_redirect: (id: string) => `/api/scratch_orgs/${id}/redirect/`,
  scratch_org_refresh: (id: string) => `/api/scratch_orgs/${id}/refresh/`,
  task_detail: (id: string) => `/api/tasks/${id}/`,
  task_create_pr: (id: string) => `/api/tasks/${id}/create_pr/`,
  task_review: (id: string) => `/api/tasks/${id}/review/`,
  task_can_reassign: (id: string) => `/api/tasks/${id}/can_reassign/`,
  epic_detail: (id: string) => `/api/epics/${id}/`,
  epic_create_pr: (id: string) => `/api/epics/${id}/create_pr/`,
  epic_refresh_org_config_names: (id: string) =>
    `/api/epics/${id}/refresh_org_config_names/`,
  project_feature_branches: (id: string) =>
    `/api/projects/${id}/feature_branches/`,
};

export const sampleGitHubUser1 = {
  id: '123456',
  login: 'TestGitHubUser',
  avatar_url: 'https://randomuser.me/api/portraits/men/1.jpg',
};

export const sampleGitHubUser2 = {
  id: '234567',
  login: 'OtherUser',
  avatar_url: 'https://randomuser.me/api/portraits/women/1.jpg',
};

export const sampleGitHubUser3 = {
  id: '345678',
  login: 'ThirdUser',
  avatar_url: 'https://randomuser.me/api/portraits/men/2.jpg',
};

export const sampleCommitAuthor = {
  name: 'Jack Brown',
  email: 'developer@web.com',
  username: 'adeveloper',
  avatar_url: 'https://randomuser.me/api/portraits/men/83.jpg',
};

export const sampleCommit1 = {
  id: '8471ad6',
  timestamp: '2019-02-01T19:47:49Z',
  message: 'fix homepage image',
  author: sampleCommitAuthor,
  url: '/',
};

export const sampleCommit2 = {
  id: '8761ad7',
  timestamp: '2020-02-01T19:47:49Z',
  message: 'add color filter to header',
  author: sampleCommitAuthor,
  url: '/',
};

export const sampleEpic1 = {
  id: 'e1',
  project: 'p1',
  name: 'My Epic',
  slug: 'my-epic',
  old_slugs: [],
  description: 'Epic Description',
  description_rendered: '<p>Epic Description</p>',
  branch_name: 'feature/my-epic',
  branch_url: 'https://github.com/test/test-repo/tree/feature/my-epic',
  branch_diff_url:
    'https://github.com/test/test-repo/compare/main...feature/my-epic',
  pr_url: null,
  pr_is_open: false,
  pr_is_merged: false,
  has_unmerged_commits: false,
  currently_creating_pr: false,
  currently_fetching_org_config_names: false,
  github_users: [],
  status: EPIC_STATUSES.PLANNED,
  available_task_org_config_names: [],
};

export const sampleEpic2 = {
  id: 'e2',
  project: 'p1',
  name: 'Mid-Year Project Saturn',
  slug: 'midyear-project-saturn',
  old_slugs: [],
  description:
    'Stabilize existing structures and provide clarity to team members.',
  description_rendered:
    '<p>Stabilize existing structures and provide clarity to team members.</p>',
  branch_name: 'feature/midyear-project-saturn',
  branch_url:
    'https://github.com/test/test-repo/tree/feature/midyear-project-saturn',
  branch_diff_url:
    'https://github.com/test/test-repo/compare/main...feature/midyear-project-saturn',
  pr_url: 'https://github.com/test/test-repo/pull/1234',
  pr_is_open: true,
  pr_is_merged: false,
  has_unmerged_commits: true,
  currently_creating_pr: false,
  currently_fetching_org_config_names: false,
  github_users: [sampleGitHubUser1, sampleGitHubUser2, sampleGitHubUser3],
  status: EPIC_STATUSES.IN_PROGRESS,
  available_task_org_config_names: [],
};

export const sampleEpic3 = {
  id: 'e3',
  project: 'p1',
  name: 'Regular Database Backups',
  slug: 'database-backups',
  old_slugs: [],
  description: '',
  description_rendered: '',
  branch_name: '',
  branch_url: null,
  branch_diff_url: null,
  pr_url: '',
  pr_is_open: false,
  pr_is_merged: false,
  has_unmerged_commits: false,
  currently_creating_pr: false,
  currently_fetching_org_config_names: false,
  github_users: [],
  status: EPIC_STATUSES.PLANNED,
  available_task_org_config_names: [],
};

export const sampleEpic4 = {
  id: 'e4',
  project: 'p1',
  name: 'Data Controls',
  slug: 'data-controls',
  old_slugs: [],
  description: 'Links the controller field to the static items',
  description_rendered: '<p>Links the controller field to the static items</p>',
  branch_name: 'feature/data-controls',
  branch_url: 'https://github.com/test/test-repo/tree/feature/data-controls',
  branch_diff_url:
    'https://github.com/test/test-repo/compare/main...feature/data-controls',
  pr_url: null,
  pr_is_open: false,
  pr_is_merged: false,
  has_unmerged_commits: false,
  currently_creating_pr: false,
  currently_fetching_org_config_names: false,
  github_users: [],
  status: EPIC_STATUSES.MERGED,
  available_task_org_config_names: [],
};

export const sampleEpic5 = {
  id: 'e5',
  project: 'p1',
  name: 'Widgets',
  slug: 'widgets',
  old_slugs: [],
  description: 'These are the widgets.',
  description_rendered: '<p>These are the widgets.</p>',
  branch_name: 'feature/widgets',
  branch_url: 'https://github.com/test/test-repo/tree/feature/widgets',
  branch_diff_url:
    'https://github.com/test/test-repo/compare/main...feature/widgets',
  pr_url: 'https://github.com/test/test-repo/pull/5678',
  pr_is_open: true,
  pr_is_merged: false,
  has_unmerged_commits: true,
  currently_creating_pr: false,
  currently_fetching_org_config_names: false,
  github_users: [sampleGitHubUser1, sampleGitHubUser2],
  status: EPIC_STATUSES.REVIEW,
  available_task_org_config_names: [],
};

export const sampleTask1 = {
  id: 't1',
  name: 'Data Mapping',
  slug: 'data-mapping',
  old_slugs: [],
  epic: 'e1',
  description: 'This is a description',
  description_rendered: '<p>This is <em>safely</em> rendered Markdown.</p>',
  has_unmerged_commits: true,
  currently_creating_pr: false,
  branch_name: 'feature/my-epic__data-mapping',
  branch_url:
    'https://github.com/test/test-repo/tree/feature/my-epic__data-mapping',
  branch_diff_url:
    'https://github.com/test/test-repo/compare/feature/my-epic...feature/my-epic__data-mapping',
  pr_url: 'https://github.com/test/test-repo/pull/1357',
  pr_is_open: true,
  commits: [sampleCommit1],
  origin_sha: '723b342',
  assigned_dev: sampleGitHubUser1,
  assigned_qa: null,
  status: TASK_STATUSES.IN_PROGRESS,
  currently_submitting_review: false,
  review_submitted_at: '2019-03-01T19:47:49Z',
  review_valid: true,
  review_status: REVIEW_STATUSES.APPROVED,
  review_sha: '617a512',
  org_config_name: 'dev',
};

export const sampleTask2 = {
  id: 't2',
  name: 'Control Toggles for Accessible Actions',
  slug: 'control-toggles',
  old_slugs: [],
  epic: 'e1',
  description:
    'Add panel for controls toggles allowing for accessible interaction',
  description_rendered:
    '<p>Add panel for controls toggles allowing for accessible interaction.</p>',
  has_unmerged_commits: false,
  currently_creating_pr: false,
  branch_name: '',
  branch_url: null,
  branch_diff_url: null,
  pr_url: null,
  pr_is_open: false,
  commits: [],
  origin_sha: '',
  assigned_dev: null,
  assigned_qa: null,
  status: TASK_STATUSES.PLANNED,
  currently_submitting_review: false,
  review_submitted_at: null,
  review_valid: false,
  review_status: '' as const,
  review_sha: '',
  org_config_name: 'dev',
};

export const sampleTask3 = {
  id: 't3',
  name: 'Dark Mode and High Contrast Options',
  slug: 'dark-mode',
  old_slugs: [],
  epic: 'e1',
  description: 'Include options set by operating system preferences',
  description_rendered:
    '<p>Include options set by **operating system preferences**</p>',
  has_unmerged_commits: false,
  currently_creating_pr: false,
  branch_name: 'feature/my-epic__dark-mode',
  branch_url:
    'https://github.com/test/test-repo/tree/feature/my-epic__dark-mode',
  branch_diff_url:
    'https://github.com/test/test-repo/compare/feature/my-epic...feature/my-epic__dark-mode',
  pr_url: 'https://github.com/test/test-repo/pull/1357',
  pr_is_open: false,
  commits: [sampleCommit1],
  origin_sha: '723b342',
  assigned_dev: sampleGitHubUser3,
  assigned_qa: sampleGitHubUser1,
  status: TASK_STATUSES.COMPLETED,
  currently_submitting_review: false,
  review_submitted_at: '2019-03-01T19:47:49Z',
  review_valid: true,
  review_status: REVIEW_STATUSES.APPROVED,
  review_sha: '617a512',
  org_config_name: 'dev',
};

export const sampleTask4 = {
  id: 't4',
  name: 'Universal Language Selectors',
  slug: 'universal-language',
  old_slugs: [],
  epic: 'e1',
  description: 'Internationalization and Localization built in options',
  description_rendered:
    '<p>Internationalization and Localization built in options</p>',
  has_unmerged_commits: false,
  currently_creating_pr: false,
  branch_name: 'feature/my-epic__universal-language',
  branch_url:
    'https://github.com/test/test-repo/tree/feature/my-epic__universal-language',
  branch_diff_url:
    'https://github.com/test/test-repo/compare/feature/my-epic...feature/my-epic__universal-language',
  pr_url: 'https://github.com/test/test-repo/pull/9999',
  pr_is_open: true,
  commits: [sampleCommit1],
  origin_sha: '723b342',
  assigned_dev: sampleGitHubUser2,
  assigned_qa: sampleGitHubUser3,
  status: TASK_STATUSES.IN_PROGRESS,
  currently_submitting_review: false,
  review_submitted_at: '2019-03-01T19:47:49Z',
  review_valid: true,
  review_status: REVIEW_STATUSES.CHANGES_REQUESTED,
  review_sha: '617a512',
  org_config_name: 'dev',
};

export const sampleTask5 = {
  id: 't5',
  name: 'Additional User Role Permissions',
  slug: 'user-roles',
  old_slugs: [],
  epic: 'e1',
  description: '',
  description_rendered: '',
  has_unmerged_commits: false,
  currently_creating_pr: false,
  branch_name: 'feature/my-epic__user-roles',
  branch_url:
    'https://github.com/test/test-repo/tree/feature/my-epic__user-roles',
  branch_diff_url:
    'https://github.com/test/test-repo/compare/feature/my-epic...feature/my-epic__user-roles',
  pr_url: '',
  pr_is_open: false,
  commits: [sampleCommit2],
  origin_sha: '723b342',
  assigned_dev: sampleGitHubUser1,
  assigned_qa: null,
  status: TASK_STATUSES.IN_PROGRESS,
  currently_submitting_review: false,
  review_submitted_at: null,
  review_valid: false,
  review_status: '' as const,
  review_sha: '',
  org_config_name: 'dev',
};

export const sampleUser1 = {
  id: 'U1',
  username: 'someuser1',
  email: 'developer@web.com',
  avatar_url: 'https://randomuser.me/api/portraits/men/1.jpg',
  valid_token_for: '00Dxxxxxxxxxxxxxxx',
  sf_username: 'developer@web.com',
  org_name: 'OddBird',
  org_type: 'Developer Edition',
  is_devhub_enabled: true,
  is_staff: false,
  currently_fetching_repos: false,
  devhub_username: '',
  uses_global_devhub: false,
  agreed_to_tos_at: '2019-02-01T19:47:49Z',
};

export const sampleProject1 = {
  id: 'p1',
  name: 'Sample Project',
  slug: 'my-project',
  old_slugs: [],
  repo_url: 'https://github.com/test/test-repo',
  repo_owner: 'test',
  repo_name: 'test-repo',
  description: 'This is *safely* rendered Markdown.',
  description_rendered: '<p>This is <em>safely</em> rendered Markdown.</p>',
  is_managed: false,
  branch_prefix: '',
  github_users: [sampleGitHubUser1],
  currently_refreshing_gh_users: false,
  repo_image_url:
    'https://repository-images.githubusercontent.com/123456/123-456',
};
