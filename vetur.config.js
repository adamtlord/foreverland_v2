module.exports = {
  settings: {
    "vetur.useWorkspaceDependencies": true,
    "vetur.experimental.templateInterpolationService": true
  },
  projects: [
    './web/vue',
    {
      root: './web/vue',
      package: './package.json',
      tsconfig: './jsconfig.json',
    }
  ]
}